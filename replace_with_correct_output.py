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

def extract_all_values(data, seen=None):
    """
    Recursively extract all scalar values from a nested structure.
    Returns a set of string representations of all values.
    """
    if seen is None:
        seen = set()
    
    if isinstance(data, dict):
        for value in data.values():
            extract_all_values(value, seen)
    elif isinstance(data, list):
        for item in data:
            extract_all_values(item, seen)
    elif data is not None:
        # Convert to string for comparison
        seen.add(str(data))
    
    return seen

def find_value_changes(old_data, new_data):
    """
    Compare two data structures and return a mapping of old values to new values.
    Only tracks values that appear in old_data but with different values in new_data.
    Returns dict: {old_value_str: new_value_str}
    """
    old_values = extract_all_values(old_data)
    new_values = extract_all_values(new_data)
    
    value_mapping = {}
    
    # Find values that changed
    for old_val in old_values:
        if old_val not in new_values:
            # This value disappeared, it might have been replaced
            # We'll track it for potential replacement
            value_mapping[old_val] = None
    
    return value_mapping

def deep_compare_and_track(old_data, new_data, path="", changes=None):
    """
    Deep comparison that tracks exactly which field values changed.
    Returns dict mapping old_value -> new_value for changed fields.
    Handles both exact type preservation and string conversion for flexibility.
    """
    if changes is None:
        changes = {}
    
    # If types differ, the whole value changed
    if type(old_data) != type(new_data):
        if old_data is not None and new_data is not None:
            # Store both string and original type mappings
            changes[str(old_data)] = str(new_data)
            # Also store original types if different
            if not isinstance(old_data, str):
                changes[old_data] = new_data
        return changes
    
    if isinstance(old_data, dict) and isinstance(new_data, dict):
        all_keys = set(old_data.keys()) | set(new_data.keys())
        for key in all_keys:
            old_val = old_data.get(key)
            new_val = new_data.get(key)
            new_path = f"{path}.{key}" if path else key
            deep_compare_and_track(old_val, new_val, new_path, changes)
    
    elif isinstance(old_data, list) and isinstance(new_data, list):
        for i, (old_item, new_item) in enumerate(zip(old_data, new_data)):
            new_path = f"{path}[{i}]"
            deep_compare_and_track(old_item, new_item, new_path, changes)
    
    else:
        # Scalar values - track if changed
        if old_data != new_data and old_data is not None and new_data is not None:
            # Store string version
            changes[str(old_data)] = str(new_data)
            # Also store typed version if not already string
            if not isinstance(old_data, str):
                changes[old_data] = new_data
    
    return changes

def update_outputs_array(outputs, value_mapping):
    """
    Update the outputs array based on value_mapping.
    Handles both string and typed values in the outputs array.
    Returns (updated_outputs, modifications_made)
    """
    if not outputs or not value_mapping:
        return outputs, []
    
    updated_outputs = []
    modifications = []
    
    for idx, output_val in enumerate(outputs):
        # Check both the original value and its string representation
        str_val = str(output_val)
        found_replacement = False
        
        # First try exact match (preserves types like int vs string)
        if output_val in value_mapping and value_mapping[output_val] is not None:
            new_val = value_mapping[output_val]
            updated_outputs.append(new_val)
            modifications.append(f"  Updated outputs[{idx}]: {output_val} -> {new_val} (exact match)")
            found_replacement = True
        # Then try string match
        elif str_val in value_mapping and value_mapping[str_val] is not None:
            new_val = value_mapping[str_val]
            # Try to preserve the original type
            if isinstance(output_val, int):
                try:
                    new_val = int(new_val)
                except (ValueError, TypeError):
                    pass
            elif isinstance(output_val, float):
                try:
                    new_val = float(new_val)
                except (ValueError, TypeError):
                    pass
            updated_outputs.append(new_val)
            modifications.append(f"  Updated outputs[{idx}]: {output_val} -> {new_val} (string match)")
            found_replacement = True
        
        if not found_replacement:
            updated_outputs.append(output_val)
    
    return updated_outputs, modifications

def run_single_task_and_update(task_file_path):
    """
    Run a task.json. If actual output differs from expected (and is not an error),
    UPDATE the file in-place.
    
    Includes logic to:
    1. Propagate 'commit_sha' from outputs to subsequent arguments
    2. Track value changes in outputs and update the outputs array accordingly
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
        
        # --- STATE VARIABLES ---
        last_observed_commit_sha = None
        # Track all value changes across all actions
        global_value_mapping = {}

        for i, action in enumerate(actions):
            action_name = action.get("name")
            arguments = action.get("arguments", {})
            expected_output = action.get("output", None)
            
            # --- 1. DYNAMIC ARGUMENT REPLACEMENT (commit_sha) ---
            if last_observed_commit_sha:
                for arg_key in list(arguments.keys()):
                    if "sha" in arg_key.lower():
                        arguments[arg_key] = last_observed_commit_sha

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

            # --- 3. VALIDATION & UPDATE LOGIC ---
            if not strict_equal(actual_output, expected_output):
                
                # Check if the actual result is an Error
                if is_error_response(actual_output):
                    if not is_error_response(expected_output):
                        return "Failed", f"Action '{action_name}' failed unexpectedly: {actual_output}"
                    action["output"] = actual_output 
                    file_modified = True

                # If it is NOT an error, but different -> Update File
                elif actual_output is not None:
                    # Track what changed between expected and actual
                    changes = deep_compare_and_track(expected_output, actual_output)
                    global_value_mapping.update(changes)
                    
                    action["output"] = actual_output
                    file_modified = True
                
                else:
                    if expected_output is not None:
                         return "Failed", f"Action '{action_name}' returned None, expected {expected_output}"

        # --- 4. UPDATE OUTPUTS ARRAY BASED ON VALUE CHANGES ---
        if file_modified and global_value_mapping:
            outputs = task_data.get("task", {}).get("outputs", [])
            if outputs:
                updated_outputs, output_modifications = update_outputs_array(outputs, global_value_mapping)
                if output_modifications:
                    task_data["task"]["outputs"] = updated_outputs
                    # Note: file_modified is already True, so we'll save anyway

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
    folder = "hr_admin_2"
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    run_all_tasks(folder)