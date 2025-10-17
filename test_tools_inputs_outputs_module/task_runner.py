import os
import json
import glob
import shutil
import traceback
from datetime import datetime
from running_tasks import env_interface, execute_api, clear_session


def get_available_interfaces(base_path="tools_regression_tests"):
    """Get list of interface folders (subdirectories containing JSON files)"""
    if not os.path.exists(base_path):
        return []
    
    interfaces = []
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            # Check if this folder contains any JSON files
            json_files = glob.glob(os.path.join(item_path, "*.json"))
            if json_files:
                interfaces.append(item)
    
    return sorted(interfaces)


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
                "status_code": None
            }
            
            try:
                api_response, status_code = execute_api(
                    api_name=action.get("name"),
                    arguments=action.get("arguments", {})
                )
                
                action_result["status_code"] = status_code
                action_result["output"] = api_response
                
                if status_code == 200:
                    action_result["success"] = True
                    # Check if API returned an error in the response
                    if isinstance(api_response, list) and len(api_response) > 0:
                        if isinstance(api_response[0], dict) and "error" in api_response[0]:
                            action_result["success"] = False
                            action_result["error"] = api_response[0]["error"]
                    elif isinstance(api_response, dict) and "error" in api_response:
                        action_result["success"] = False
                        action_result["error"] = api_response["error"]
                else:
                    action_result["error"] = api_response.get("message", "API execution failed")
                
            except Exception as e:
                action_result["error"] = str(e)
                action_result["traceback"] = traceback.format_exc()
            
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
            json.dump(result, f, indent=2)
        
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
        json.dump(summary, f, indent=2)
    
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