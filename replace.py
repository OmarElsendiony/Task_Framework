import os
import json
import glob
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from running_tasks import *

def find_all_task_files(base_path="week_10"):
    """Find all task.json files."""
    pattern = os.path.join(base_path, "**", "task.json")
    task_files = glob.glob(pattern, recursive=True)
    return task_files

def strict_equal(obj1, obj2):
    """Check if two objects are equal."""
    if type(obj1) != type(obj2): return False
    if isinstance(obj1, dict):
        if obj1.keys() != obj2.keys(): return False
        return all(strict_equal(obj1[key], obj2[key]) for key in obj1.keys())
    elif isinstance(obj1, (list, tuple)):
        if len(obj1) != len(obj2): return False
        return all(strict_equal(a, b) for a, b in zip(obj1, obj2))
    return obj1 == obj2

def is_error_response(data):
    """Checks if the data looks like an API error response."""
    if isinstance(data, dict):
        # Common error patterns in your system
        if "error" in data or data.get("status") == "error": return True
    return False

def run_single_task_and_update(task_file_path):
    """
    Run a task.json. If actual output differs from expected (and is not an error),
    UPDATE the file in-place.
    
    Includes logic to propagate 'commit_sha' from outputs to subsequent arguments.
    """
    try:
        with open(task_file_path, 'r', encoding='utf-8') as f:
            task_data = json.load(f)
        
        environment = task_data.get("env")
        interface = task_data.get("interface_num")
        
        # Initialize environment (Silently)
        f_io = io.StringIO()
        try:
            with redirect_stdout(f_io), redirect_stderr(f_io):
                env_interface(environment=environment, interface=interface)
        except Exception as e:
            return "Failed", f"Env Init Error: {str(e)}"
        
        actions = task_data.get("task", {}).get("actions", [])
        file_modified = False
        
        # --- STATE VARIABLE FOR SHA PROPAGATION ---
        last_observed_commit_sha = None

        for i, action in enumerate(actions):
            action_name = action.get("name")
            arguments = action.get("arguments", {})
            expected_output = action.get("output", None)
            
            # --- 1. DYNAMIC ARGUMENT REPLACEMENT ---
            # If we have seen a commit_sha, replace any argument containing "sha" with it
            if last_observed_commit_sha:
                for arg_key in list(arguments.keys()):
                    if "sha" in arg_key.lower():
                        # Update the argument in the dictionary passed to the API
                        arguments[arg_key] = last_observed_commit_sha
                        
                        # OPTIONAL: Also update the 'task.json' argument permanently?
                        # Usually better to only update the Output, but if you want the 
                        # input file to be self-consistent, uncomment the next line:
                        # action["arguments"][arg_key] = last_observed_commit_sha
                        # file_modified = True

            # Execute API (Silently)
            actual_res_container = None
            try:
                with redirect_stdout(f_io), redirect_stderr(f_io):
                    actual_res_container = execute_api(api_name=action_name, arguments=arguments)
            except Exception as e:
                return "Failed", f"Action '{action_name}' raised exception: {str(e)}"

            # Extract actual result
            actual_output = actual_res_container[0] if actual_res_container and isinstance(actual_res_container, (list, tuple)) else actual_res_container

            # --- 2. CAPTURE COMMIT_SHA FROM OUTPUT ---
            # Helper to recursively find 'commit_sha' in a nested dict
            def find_sha_recursive(data):
                if isinstance(data, dict):
                    if "commit_sha" in data and isinstance(data["commit_sha"], str):
                        return data["commit_sha"]
                    for value in data.values():
                        found = find_sha_recursive(value)
                        if found: return found
                return None

            found_sha = find_sha_recursive(actual_output)
            if found_sha:
                last_observed_commit_sha = found_sha

            # --- Validation & Update Logic ---
            if not strict_equal(actual_output, expected_output):
                
                # Check if the actual result is an Error
                if is_error_response(actual_output):
                    if not is_error_response(expected_output):
                        return "Failed", f"Action '{action_name}' failed unexpectedly: {actual_output}"
                    action["output"] = actual_output 
                    file_modified = True

                # If it is NOT an error, but different -> Update File
                elif actual_output is not None:
                    action["output"] = actual_output
                    file_modified = True
                
                else:
                    if expected_output is not None:
                         return "Failed", f"Action '{action_name}' returned None, expected {expected_output}"

        # Save changes if any modifications happened
        if file_modified:
            with open(task_file_path, 'w', encoding='utf-8') as f:
                json.dump(task_data, f, indent=2)
            return "Updated", "File updated with new outputs"
            
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
        
        status, msg = run_single_task_and_update(task_file)
        
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