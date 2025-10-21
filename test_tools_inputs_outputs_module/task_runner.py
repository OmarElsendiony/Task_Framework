import os
import json
import glob
import shutil
import traceback
from datetime import datetime
from running_tasks import env_interface, execute_api, clear_session


def get_available_interfaces(base_path="tools_regression_tests"):
    """Get list of interface folders (subdirectories containing JSON files).
    Supports both:
      - tools_regression_tests/interface_1
      - tools_regression_tests/domain_name/interface_1
    Returns relative paths (relative to base_path) pointing to the interface directories,
    e.g. ['interface_1', 'domain_name/interface_1'].
    """
    if not os.path.exists(base_path):
        return []
    
    interfaces = set()
    # Walk the directory tree and find dirs that contain JSON files.
    for root, dirs, files in os.walk(base_path):
        json_files = [f for f in files if f.endswith(".json")]
        if not json_files:
            continue
        # Determine interface folder: prefer path segments that start with 'interface_'
        rel = os.path.relpath(root, base_path)
        parts = rel.split(os.sep) if rel != "." else []
        iface_index = None
        for i, p in enumerate(parts):
            if p.startswith("interface_"):
                iface_index = i
        if iface_index is not None:
            # include everything up to and including the interface_ segment
            iface_path = os.path.join(*parts[: iface_index + 1])
            interfaces.add(iface_path)
        else:
            # No explicit interface_ folder found; use the directory relative path
            # (useful if tests live directly in domain folder or root)
            interfaces.add(rel if rel != "." else "")

    # Normalize and sort; filter out empty string entries (representing root) for clarity
    result = sorted([i for i in interfaces if i])
    return result


def find_all_task_files(base_path="tools_regression_tests"):
    """Recursively find all .json test files"""
    pattern = os.path.join(base_path, "**", "*.json")
    return sorted(glob.glob(pattern, recursive=True))


def run_single_task(task_file_path, envs_path="envs"):
    """
    Run a single JSON task file and return detailed results
    Returns: (success: bool, result: dict)
    """
    result = {
        "task_file": task_file_path,
        "timestamp": datetime.now().isoformat(),
        "actions": [],
        "error": None,
        "envs_path": envs_path
    }
    
    try:
        # Load task file
        with open(task_file_path, "r") as f:
            task_data = json.load(f)
        
        environment = task_data.get("env")
        interface = task_data.get("interface_num")
        
        if not environment or not interface:
            result["error"] = "Missing environment or interface_num in task file"
            return False, result
        
        # Initialize environment with custom path
        env_response, status_code = env_interface(
            environment=environment, 
            interface=interface, 
            envs_path=envs_path
        )
        
        if status_code != 200:
            result["error"] = f"Environment setup failed: {env_response.get('message', 'Unknown error')}"
            return False, result
        
        result["environment"] = environment
        result["interface"] = interface
        result["functions_loaded"] = len(env_response.get("functions_info", []))
        
        # Execute each action
        actions = task_data.get("task", {}).get("actions", [])
        
        if not actions:
            result["error"] = "No actions found in task file"
            return False, result
        
        for idx, action in enumerate(actions):
            action_result = {
                "index": idx,
                "name": action.get("name"),
                "arguments": action.get("arguments", {}),
                "success": False,
                "output": None,
                "error": None,
                "status_code": None,
                # expectation fields populated below if present
                "expected": action.get("expected"),
                "expected_match": None,
                "actual_text": None,
                "mismatch_reasons": None
            }
            
            try:
                api_response, status_code = execute_api(
                    api_name=action.get("name"),
                    arguments=action.get("arguments", {})
                )
                
                action_result["status_code"] = status_code
                action_result["output"] = api_response
                
                # Detect if API returned an 'error' field (but do NOT immediately mark failure;
                # we'll consider expectations before deciding)
                api_has_error = False
                api_error_msg = None
                if isinstance(api_response, list) and len(api_response) > 0:
                    if isinstance(api_response[0], dict) and "error" in api_response[0]:
                        api_has_error = True
                        api_error_msg = api_response[0]["error"]
                elif isinstance(api_response, dict) and "error" in api_response:
                    api_has_error = True
                    api_error_msg = api_response["error"]

                # Normalize a textual representation of the API output for expectation checks
                api_text = None
                try:
                    if isinstance(api_response, str):
                        api_text = api_response
                    elif isinstance(api_response, dict):
                        # prefer a 'text' field if present
                        if "text" in api_response and isinstance(api_response["text"], str):
                            api_text = api_response["text"]
                        else:
                            api_text = json.dumps(api_response, ensure_ascii=False)
                    elif isinstance(api_response, list):
                        # try first element's text or dump entire list
                        if len(api_response) > 0 and isinstance(api_response[0], dict) and "text" in api_response[0]:
                            api_text = api_response[0]["text"]
                        else:
                            api_text = json.dumps(api_response, ensure_ascii=False)
                    else:
                        api_text = str(api_response)
                except Exception:
                    api_text = str(api_response)

                action_result["actual_text"] = api_text

                # Start by treating status_code==200 as optimistic success
                if status_code == 200:
                    action_result["success"] = True
                else:
                    # Non-200 -> treat as failure regardless of expectations
                    action_result["error"] = api_response.get("message", "API execution failed") if isinstance(api_response, dict) else str(api_response)
                    action_result["success"] = False

                # If an expectation is provided, validate it against the API output
                expected = action.get("expected")
                expected_ok = True
                mismatch_reasons = []
                if expected:
                    # exact text match
                    expected_text = expected.get("expected_text")
                    if expected_text is not None:
                        if (api_text or "").strip() != expected_text.strip():
                            expected_ok = False
                            mismatch_reasons.append("expected_text_mismatch")

                    # substring checks
                    expected_contains = expected.get("expected_contains", [])
                    for substr in expected_contains:
                        if substr.lower() not in (api_text or "").lower():
                            expected_ok = False
                            mismatch_reasons.append(f"missing_substring:{substr}")

                    # severity semantic check (if API returns dict with severity)
                    expected_severity = expected.get("severity")
                    if expected_severity is not None:
                        found_sev = None
                        if isinstance(api_response, dict) and "severity" in api_response:
                            found_sev = api_response.get("severity")
                        else:
                            # try to parse severity from text
                            txt = (api_text or "").lower()
                            if expected_severity.lower() in txt:
                                found_sev = expected_severity
                        if found_sev is None or str(found_sev).lower() != str(expected_severity).lower():
                            expected_ok = False
                            mismatch_reasons.append(f"severity_mismatch(expected={expected_severity}, found={found_sev})")

                    # (Optional) boolean 'authorized' check if present in expected
                    expected_authorized = expected.get("authorized")
                    if expected_authorized is not None:
                        actual_authorized = None
                        if isinstance(api_response, dict) and "authorized" in api_response:
                            actual_authorized = api_response.get("authorized")
                        else:
                            try:
                                parsed = json.loads(api_text) if api_text else None
                                if isinstance(parsed, dict) and "authorized" in parsed:
                                    actual_authorized = parsed.get("authorized")
                            except Exception:
                                actual_authorized = None

                        if actual_authorized is None:
                            expected_ok = False
                            mismatch_reasons.append(f"authorized_missing_in_response(expected={expected_authorized})")
                        else:
                            try:
                                if bool(actual_authorized) != bool(expected_authorized):
                                    expected_ok = False
                                    mismatch_reasons.append(f"authorized_mismatch(expected={expected_authorized}, found={actual_authorized})")
                            except Exception:
                                expected_ok = False
                                mismatch_reasons.append(f"authorized_mismatch(expected={expected_authorized}, found={actual_authorized})")

                    action_result["expected_match"] = expected_ok
                    action_result["mismatch_reasons"] = mismatch_reasons or None

                else:
                    # no expectation provided
                    action_result["expected_match"] = None

                # Decide final success:
                # - Non-200 status already failed above.
                # - If API included an 'error' field:
                #     * If there's an expectation and it matched -> consider passed (clear error)
                #     * Otherwise -> fail and surface API error message
                # - If expectations exist and did not match -> fail
                if status_code == 200:
                    if api_has_error:
                        if expected is not None and action_result.get("expected_match"):
                            # expectation matched the error response -> treat as success
                            action_result["success"] = True
                            action_result["error"] = None
                        else:
                            action_result["success"] = False
                            action_result["error"] = api_error_msg
                    # If expectations were provided but did not match, mark failure
                    if expected is not None and action_result.get("expected_match") is False:
                        action_result["success"] = False
                        action_result["error"] = f"Expectation mismatch: {', '.join(mismatch_reasons)}"
                    # If expectation matched, ensure success True and clear any previously set error
                    if expected is not None and action_result.get("expected_match"):
                        action_result["success"] = True
                        action_result["error"] = None

            except Exception as e:
                action_result["error"] = str(e)
                action_result["traceback"] = traceback.format_exc()
                action_result["success"] = False

            result["actions"].append(action_result)
        
        # Determine overall success
        all_actions_succeeded = all(a["success"] for a in result["actions"])
        
        if not all_actions_succeeded:
            failed_actions = [a["name"] for a in result["actions"] if not a["success"]]
            result["error"] = f"Some actions failed: {', '.join(failed_actions)}"
        
        return all_actions_succeeded, result
        
    except FileNotFoundError as e:
        result["error"] = f"Task file not found: {task_file_path}"
        result["error_type"] = "FileNotFoundError"
        return False, result
        
    except json.JSONDecodeError as e:
        result["error"] = f"Invalid JSON in task file: {str(e)}"
        result["error_type"] = "JSONDecodeError"
        result["error_details"] = {"line": e.lineno, "column": e.colno}
        return False, result
        
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
        result["error_type"] = type(e).__name__
        result["traceback"] = traceback.format_exc()
        return False, result
    
    finally:
        # Clear session after each task
        clear_session()


def run_all_tasks(base_path="tools_regression_tests", output_dir="tools_test_output", envs_path="envs"):
    """
    Run all test files and generate comprehensive reports
    """
    # Clean and create output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all task files
    task_files = find_all_task_files(base_path)
    
    if not task_files:
        return {
            "total_tasks": 0,
            "passed": 0,
            "failed": 0,
            "pass_rate": "0%",
            "test_results": []
        }
    
    # Summary statistics
    summary = {
        "total_tasks": len(task_files),
        "passed": 0,
        "failed": 0,
        "start_time": datetime.now().isoformat(),
        "envs_path": envs_path,
        "test_results": []
    }
    
    print(f"\n🧪 Running {len(task_files)} test tasks...\n")
    
    # Run each task
    for idx, task_file in enumerate(task_files, 1):
        task_name = os.path.basename(task_file).replace(".json", "")
        print(f"[{idx}/{len(task_files)}] Testing: {task_name}...", end=" ")
        
        success, result = run_single_task(task_file, envs_path=envs_path)
        
        # Update summary
        if success:
            summary["passed"] += 1
            print("✅ PASSED")
        else:
            summary["failed"] += 1
            print(f"❌ FAILED - {result.get('error', 'Unknown error')}")
        
        # Save individual test result
        output_file = os.path.join(output_dir, f"{task_name}_result.json")
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        # Print per-action comparison (Actual vs Expected) so you can compare quickly
        print("  Actions:")
        for a in result.get("actions", []):
            idx_a = a.get("index")
            name = a.get("name")
            status_icon = "��" if a.get("success") else "❌"
            print(f"    - Action[{idx_a}] {name}: {status_icon}")
            print(f"        Actual: {a.get('actual_text')}")
            if a.get("expected") is not None:
                print(f"        Expected: {json.dumps(a.get('expected'), ensure_ascii=False)}")
                print(f"        Expected match: {a.get('expected_match')}")
                if a.get("mismatch_reasons"):
                    print(f"        Mismatches: {', '.join(a.get('mismatch_reasons'))}")
            else:
                # show raw output if no structured expectation provided
                if a.get("output") is not None:
                    try:
                        raw = json.dumps(a.get("output"), ensure_ascii=False)
                    except Exception:
                        raw = str(a.get("output"))
                    print(f"        Output (raw): {raw}")

        # Add to summary
        summary["test_results"].append({
            "file": task_file,
            "name": task_name,
            "success": success,
            "error": result.get("error"),
            "actions_count": len(result.get("actions", []))
        })
    
    # Finalize summary
    summary["end_time"] = datetime.now().isoformat()
    summary["pass_rate"] = f"{(summary['passed'] / summary['total_tasks'] * 100):.1f}%"
    
    # Save summary report
    summary_file = os.path.join(output_dir, "summary.json")
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"Total Tasks:  {summary['total_tasks']}")
    print(f"✅ Passed:    {summary['passed']}")
    print(f"❌ Failed:    {summary['failed']}")
    print(f"Pass Rate:    {summary['pass_rate']}")
    print("="*60)
    print(f"\n📁 Results saved to: {output_dir}/")
    
    return summary
