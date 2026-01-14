import os
import json
import glob
import sys
import io
import re
from contextlib import redirect_stdout, redirect_stderr
from running_tasks import *

def find_all_task_files(base_path="week_10"):
    """Find all task.json files in the directory structure."""
    pattern = os.path.join(base_path, "**", "task.json")
    task_files = glob.glob(pattern, recursive=True)
    return task_files

def strict_equal(obj1, obj2):
    """Check if two objects are equal in both value and type."""
    if type(obj1) != type(obj2): return False
    if isinstance(obj1, dict):
        if obj1.keys() != obj2.keys(): return False
        return all(strict_equal(obj1[key], obj2[key]) for key in obj1.keys())
    elif isinstance(obj1, (list, tuple)):
        if len(obj1) != len(obj2): return False
        return all(strict_equal(a, b) for a, b in zip(obj1, obj2))
    return obj1 == obj2

def normalize_error_response(data):
    """Normalizes errors to a standard string format 'Error: ...'."""
    msg = ""
    if isinstance(data, dict):
        if data.get("status") == "error": msg = data.get("message", "")
        elif "error" in data: msg = data["error"]
        else: return str(data)
    else:
        msg = str(data)

    # Cleanup prefixes
    msg = re.sub(r"Failed to execute API:\s*Tools\.", "", msg)
    msg = re.sub(r"Error executing API .*?:\s*", "", msg)

    # Normalize function names
    def to_pascal(match):
        parts = match.group(1).split("_")
        return "".join(p.capitalize() for p in parts) + ".invoke"
    
    msg = re.sub(r'([a-z0-9_]+)_invoke', to_pascal, msg)

    if not msg.strip().lower().startswith("error"):
        msg = f"Error: {msg}"
    return msg

def is_error_response(data):
    """Checks if the data is an API error."""
    if isinstance(data, dict):
        return "error" in data or (data.get("status") == "error")
    if isinstance(data, str) and data.strip().lower().startswith("error"):
        return True
    return False

def process_single_task(task_file_path):
    """
    Runs a task.json file.
    Updates the file IN-PLACE if output differs AND 'got' is NOT an error (unless expected was also error).
    """
    try:
        with open(task_file_path, 'r', encoding='utf-8') as f:
            task_data = json.load(f)
        
        environment = task_data.get("env")
        interface = task_data.get("interface_num")
        
        if not environment:
            return "Failed", "Missing 'env' configuration"

        # Initialize environment (Silent)
        f_io = io.StringIO()
        try:
            with redirect_stdout(f_io), redirect_stderr(f_io):
                env_interface(environment=environment, interface=interface)
        except Exception as e:
            return "Failed", f"Env Init Error: {str(e)}"
        
        actions = task_data.get("task", {}).get("actions", [])
        file_modified = False
        
        for i, action in enumerate(actions):
            action_name = action.get("name")
            arguments = action.get("arguments", {})
            expected_output = action.get("output", None)
            
            # Execute API (Silent)
            actual_res_container = None
            try:
                with redirect_stdout(f_io), redirect_stderr(f_io):
                    actual_res_container = execute_api(api_name=action_name, arguments=arguments)
            except Exception as e:
                return "Failed", f"Action '{action_name}' raised exception: {str(e)}"

            # Extract actual output
            actual_output = actual_res_container[0] if actual_res_container and isinstance(actual_res_container, (list, tuple)) else actual_res_container

            # --- Validation Logic ---
            
            # 1. Strict Match check
            if strict_equal(actual_output, expected_output):
                continue # Exact match, move to next action

            # 2. Check if Actual is an Error
            if is_error_response(actual_output):
                # Is Expected ALSO an error?
                if is_error_response(expected_output):
                    # Compare Normalized Errors
                    norm_actual = normalize_error_response(actual_output)
                    norm_expected = normalize_error_response(expected_output)
                    
                    if norm_expected in norm_actual: # Fuzzy match allowed
                        continue # Success (Error matched expected error)
                    else:
                        return "Failed", f"Error Mismatch.\n   Exp: {norm_expected}\n   Got: {norm_actual}"
                else:
                    # CRITICAL: Got Error, but Expected NOT Error -> FAIL
                    return "Failed", f"Action '{action_name}' failed unexpectedly.\n   Exp: {expected_output}\n   Got Error: {actual_output}"

            # 3. Valid Output Mismatch -> Update File
            # We are here because:
            #  - Not strict equal
            #  - Actual is NOT an error (it's valid data)
            #  - So it must be a data mismatch we want to update
            
            if actual_output is not None:
                action["output"] = actual_output
                file_modified = True
            else:
                if expected_output is not None:
                     return "Failed", f"Action '{action_name}' returned None, expected data."

        # Save changes
        if file_modified:
            with open(task_file_path, 'w', encoding='utf-8') as f:
                json.dump(task_data, f, indent=2)
            return "Updated", "Output corrected in file"
            
        return "Success", None
        
    except FileNotFoundError:
        return "Failed", "File not found"
    except json.JSONDecodeError:
        return "Failed", "Invalid JSON"
    except Exception as e:
        return "Failed", f"Unexpected error: {str(e)}"

def run_all_tasks(base_path="week_11_new"): 
    print("=" * 60)
    print(f"VALIDATING AND UPDATING TASKS IN: {base_path}")
    print("=" * 60)

    task_files = find_all_task_files(base_path)
    
    if not task_files:
        print("No task.json files found.")
        return
    
    print(f"Found {len(task_files)} files.\n")
    
    stats = {"Success": 0, "Updated": 0, "Failed": 0}
    failures = []
    
    for i, task_file in enumerate(task_files):
        print(f"[{i+1}/{len(task_files)}] {task_file} ...", end="", flush=True)
        
        status, msg = process_single_task(task_file)
        
        stats[status] += 1
        
        if status == "Updated":
            print(f" -> UPDATED")
        elif status == "Success":
            print(f" -> OK")
        else:
            print(f" -> FAILED")
            failures.append({"file": task_file, "error": msg})
    
    # Summary
    print("\n" + "=" * 60)
    print("EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Total:     {len(task_files)}")
    print(f"Success:   {stats['Success']}")
    print(f"Updated:   {stats['Updated']}")
    print(f"Failed:    {stats['Failed']}")
    
    if failures:
        print("\n" + "=" * 60)
        print("FAILURE DETAILS")
        print("=" * 60)
        for fail in failures:
            print(f"File:  {fail['file']}")
            print(f"Error: {fail['error']}")
            print("-" * 40)
            
        with open("task_update_errors.log", "w") as f:
            for fail in failures:
                f.write(f"File: {fail['file']}\nError: {fail['error']}\n\n")
        print("\nDetailed errors written to task_update_errors.log")

if __name__ == "__main__":
    folder = "batch_Batch_version_control_system_20260108_195536_adjusted"
    if len(sys.argv) > 1:
        folder = sys.argv[1]
        
    run_all_tasks(folder)