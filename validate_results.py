import os
import json
import glob
import sys
import io
import re
from contextlib import redirect_stdout, redirect_stderr
# Ensure running_tasks is accessible
from running_tasks import *

def find_all_result_files(base_path="batch_Batch_version_control_system_20260108_195536_adjusted"):
    """Find all result.json files recursively."""
    pattern = os.path.join(base_path, "**", "result.json")
    files = glob.glob(pattern, recursive=True)
    return files

def strict_equal(obj1, obj2):
    """Check equality allowing for JSON string parsing."""
    if isinstance(obj1, str) and not isinstance(obj2, str):
        try: obj1 = json.loads(obj1)
        except: pass
    if isinstance(obj2, str) and not isinstance(obj1, str):
        try: obj2 = json.loads(obj2)
        except: pass

    if type(obj1) != type(obj2): return False
    
    if isinstance(obj1, dict):
        if obj1.keys() != obj2.keys(): return False
        return all(strict_equal(obj1[key], obj2[key]) for key in obj1.keys())
    elif isinstance(obj1, (list, tuple)):
        if len(obj1) != len(obj2): return False
        return all(strict_equal(a, b) for a, b in zip(obj1, obj2))
    return obj1 == obj2

def normalize_error_response(actual_data):
    """
    Normalizes a dictionary error response into the expected string format.
    Transforms: 
      {'status': 'error', 'message': 'Failed to execute API: Tools.resolve_user_identity_invoke() ...'}
    Into:
      'Error: ResolveUserIdentity.invoke() ...'
    """
    msg = ""
    # 1. Extract message from dict if applicable
    if isinstance(actual_data, dict) and actual_data.get("status") == "error":
        msg = actual_data.get("message", "")
    elif isinstance(actual_data, str):
        msg = actual_data
    else:
        return str(actual_data) 

    # 2. Remove "Failed to execute API: Tools." prefix
    prefix_pattern = r"Failed to execute API:\s*Tools\."
    msg = re.sub(prefix_pattern, "", msg)

    # 3. Convert snake_case_invoke to PascalCase.invoke
    def to_pascal(match):
        snake_str = match.group(1)
        pascal_str = "".join(x.capitalize() for x in snake_str.split("_"))
        return f"{pascal_str}.invoke"

    msg = re.sub(r'([a-z0-9_]+)_invoke', to_pascal, msg)

    # 4. Ensure it starts with "Error: "
    if not msg.startswith("Error: "):
        msg = f"Error: {msg}"

    return msg

def is_error_match(actual_normalized, expected_str):
    """
    Compares two error strings leniently.
    It ignores the specific argument name at the end of the error.
    
    Example Match:
      Actual:   "Error: Func() got an unexpected keyword argument 'repo_name'"
      Expected: "Error: Func() got an unexpected keyword argument 'repository_id'"
      Result:   True
    """
    # If they match exactly, great
    if actual_normalized == expected_str:
        return True

    # Common Python error patterns to fuzzy match
    # We strip the specific variable name typically found in single quotes at the end
    patterns = [
        r"(got an unexpected keyword argument) '.*?'",
        r"(missing \d+ required positional argument): '.*?'",
        r"(missing \d+ required positional arguments): .*"
    ]

    for pattern in patterns:
        # Check if BOTH strings match the same core error pattern
        # AND imply the same function/method name (start of string)
        
        # 1. Extract function name prefix (e.g., "Error: GetRepoBranch.invoke()")
        func_name_pattern = r"^(Error: [a-zA-Z0-9_.]+\(\))"
        
        act_func = re.match(func_name_pattern, actual_normalized)
        exp_func = re.match(func_name_pattern, expected_str)
        
        if act_func and exp_func and act_func.group(1) == exp_func.group(1):
            # Same function, now check the error message body
            act_body = re.search(pattern, actual_normalized)
            exp_body = re.search(pattern, expected_str)
            
            # If both contain the same type of error (e.g. "unexpected keyword argument")
            if act_body and exp_body and act_body.group(1) == exp_body.group(1):
                return True

    return False

def load_environment_config(result_file_path, result_data):
    # 1. Check result.json
    sample = result_data[0] if isinstance(result_data, list) and result_data else result_data
    if isinstance(sample, dict):
        env = sample.get("env") or sample.get("info", {}).get("env")
        interface = sample.get("interface_num") or sample.get("info", {}).get("interface_num")
        if env: return env, interface

    # 2. Check sibling task.json
    task_path = os.path.join(os.path.dirname(result_file_path), "task.json")
    if os.path.exists(task_path):
        try:
            with open(task_path, 'r') as f:
                cfg = json.load(f)
                return cfg.get("env"), cfg.get("interface_num")
        except: pass
        
    return None, None

def run_trial_replay(trial_data, env_name, interface_num):
    if not env_name:
        return False, "Configuration Error: Missing 'env'"

    # 1. Init Environment
    try:
        f = io.StringIO()
        with redirect_stdout(f), redirect_stderr(f):
            env_interface(environment=env_name, interface=interface_num)
    except Exception as e:
        return False, f"Environment Init Failed: {str(e)}"

    # 2. Get Tool Calls
    traj = trial_data.get("traj", [])
    tool_calls = [step for step in traj if step.get("role") == "tool"]

    if not tool_calls:
        return True, None

    # 3. Replay Steps
    for i, step in enumerate(tool_calls):
        api_name = step.get("name")
        args = step.get("args") or step.get("kwargs") or {}
        
        # Expected Output
        expected_raw = step.get("content")
        expected = expected_raw
        if isinstance(expected_raw, str):
            try: expected = json.loads(expected_raw)
            except: pass

        # Execution
        actual = None
        f = io.StringIO()
        try:
            with redirect_stdout(f), redirect_stderr(f):
                res = execute_api(api_name=api_name, arguments=args)
                actual = res[0] if isinstance(res, (list, tuple)) and len(res) > 0 else res
        except Exception as e:
            logs = f.getvalue()
            actual = {"status": "error", "message": str(e)}
        
        if actual is None:
            logs = f.getvalue().strip()
            if logs:
                actual = {"status": "error", "message": logs}

        # --- VALIDATION ---
        
        # 1. Strict Match
        if strict_equal(actual, expected):
            continue

        # 2. Error Normalization Match (Exact string match after cleanup)
        normalized_actual = normalize_error_response(actual)
        if strict_equal(normalized_actual, expected):
            continue

        # 3. Fuzzy Error Match (Ignoring variable names)
        # Check if expected is a string error message
        if isinstance(expected, str) and expected.startswith("Error:"):
            if is_error_match(normalized_actual, expected):
                continue

        return False, (
            f"Mismatch at step {i} ({api_name}):\n"
            f"   Expected: {str(expected)}\n"
            f"   Got:      {str(actual)}\n"
            f"   (Norm):   {normalized_actual}"
        )

    return True, None

def process_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        return [{"file": file_path, "status": "Load Error", "error": str(e)}]

    if not data: return []

    env_name, interface_num = load_environment_config(file_path, data)
    trials = data if isinstance(data, list) else [data]
    results = []
    consecutive_failures = 0

    for idx, trial in enumerate(trials):
        task_id = trial.get("task_id", f"unknown_{idx}")
        
        success, error_msg = run_trial_replay(trial, env_name, interface_num)
        
        status = "Success" if success else "Failed"
        results.append({
            "file": file_path,
            "task_id": task_id,
            "trial_index": idx,
            "status": status,
            "error": error_msg
        })

        if not success:
            consecutive_failures += 1
        else:
            consecutive_failures = 0
            
        if consecutive_failures >= 5:
            results.append({
                "file": file_path,
                "task_id": "SKIPPED",
                "trial_index": idx + 1,
                "status": "Skipped",
                "error": "Aborted file after 5 consecutive failures."
            })
            break

    return results

def main(base_path):
    print("=" * 60)
    print(f"REPLAYING TOOL CALLS FROM: {base_path}")
    print("=" * 60)

    files = find_all_result_files(base_path)
    if not files:
        print("No result.json files found.")
        return

    print(f"Found {len(files)} files.\n")

    all_results = []
    
    for i, file_path in enumerate(files[3:5]):
        print(f"[{i+1}/{len(files)}] {file_path} ...", end="", flush=True)
        file_results = process_file(file_path)
        all_results.extend(file_results)
        
        failures = [r for r in file_results if r['status'] == 'Failed']
        skipped = [r for r in file_results if r['status'] == 'Skipped']
        
        if skipped:
            print(f" Aborted ({len(failures)} fails)")
        elif failures:
            print(f" Failed ({len(failures)} trials)")
        else:
            print(" OK")

    successful = [r for r in all_results if r['status'] == 'Success']
    failed = [r for r in all_results if r['status'] == 'Failed']

    print("\n" + "=" * 60)
    print("REPLAY SUMMARY")
    print("=" * 60)
    print(f"Total Files:   {len(files)}")
    print(f"Total Trials:  {len(all_results)}")
    print(f"Successful:    {len(successful)}")
    print(f"Failed:        {len(failed)}")

    if failed:
        log_file = "replay_errors.log"
        with open(log_file, 'w') as f:
            f.write("Replay Error Log\n================\n\n")
            for item in failed:
                f.write(f"File:  {item['file']}\n")
                f.write(f"Trial: {item.get('trial_index')}\n")
                f.write(f"Error: {item.get('error')}\n")
                f.write("-" * 60 + "\n")
        print(f"\nDetailed errors written to {log_file}")

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "batch_Batch_version_control_system_20260108_195536_adjusted"
    main(folder)