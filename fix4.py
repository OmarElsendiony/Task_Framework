import os
import json
import glob
from running_tasks import *


def find_all_task_files(base_path="week_10"):
    """
    Find all task.json files in the directory structure.
    Pattern: week_11/*/philip-*-*/task.json
    """
    pattern = os.path.join(base_path, "**", "task.json")
    task_files = glob.glob(pattern, recursive=True)
    return task_files

def strict_equal(obj1, obj2):
    """Check if two objects are equal in both value and type."""
    if type(obj1) != type(obj2):
        return False
    
    if isinstance(obj1, dict):
        if obj1.keys() != obj2.keys():
            return False
        return all(strict_equal(obj1[key], obj2[key]) for key in obj1.keys())
    
    elif isinstance(obj1, (list, tuple)):
        if len(obj1) != len(obj2):
            return False
        return all(strict_equal(a, b) for a, b in zip(obj1, obj2))
    
    else:
        return obj1 == obj2


def loose_equal(obj1, obj2):
    """Check if two objects are equal in value, ignoring key order in dicts."""
    if type(obj1) != type(obj2):
        return False
    
    if isinstance(obj1, dict):
        if set(obj1.keys()) != set(obj2.keys()):
            return False
        return all(loose_equal(obj1[key], obj2[key]) for key in obj1.keys())
    
    elif isinstance(obj1, (list, tuple)):
        if len(obj1) != len(obj2):
            return False
        return all(loose_equal(a, b) for a, b in zip(obj1, obj2))
    
    else:
        return obj1 == obj2


def convert_to_float(value):
    """Convert integer to float recursively in data structures, but preserve booleans."""
    if isinstance(value, bool):
        # Check bool first because bool is a subclass of int in Python
        return value
    elif isinstance(value, int):
        return float(value)
    elif isinstance(value, dict):
        return {k: convert_to_float(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_to_float(item) for item in value]
    return value


def fix_and_save_task(task_file_path, task_data, action_index, fix_type, new_arguments=None, new_output=None):
    """
    Fix the task file by updating arguments or output and save it back.
    
    Args:
        task_file_path: Path to the task file
        task_data: The loaded task data
        action_index: Index of the action to fix
        fix_type: 'arguments' or 'output'
        new_arguments: New arguments (if fixing arguments)
        new_output: New output (if fixing output)
    """
    if fix_type == 'arguments' and new_arguments is not None:
        task_data["task"]["actions"][action_index]["arguments"] = new_arguments
    elif fix_type == 'output' and new_output is not None:
        task_data["task"]["actions"][action_index]["output"] = new_output
    
    # Write back to file (preserves order in Python 3.7+)
    with open(task_file_path, 'w') as f:
        json.dump(task_data, f, indent=2)


def run_single_task(task_file_path):
    """
    Run a single task from a task.json file.
    Automatically fixes type mismatches and output mismatches by converting ints to floats.
    Returns (success: bool, error_message: str or None)
    """
    try:
        with open(task_file_path, 'r') as f:
            task_data = json.load(f)
        
        environment = task_data.get("env")
        interface = task_data.get("interface_num")
        
        # Initialize environment
        env_interface(environment=environment, interface=interface)
        
        # Execute each action in the task
        actions = task_data.get("task", {}).get("actions", [])
        for i, action in enumerate(actions):
            action_name = action.get("name")
            arguments = action.get("arguments", {})
            expected_output = action.get("output")
            
            # Try to execute with current arguments
            try:
                res = execute_api(api_name=action_name, arguments=arguments)
                actual_output = res[0] if res else None
                
                # Check for type mismatch error in response
                if (res and len(res) > 0 and isinstance(res[0], dict) and 
                    res[0].get("status") == "error" and "Type mismatch" in res[0].get("message", "")):
                    
                    # Fix: Convert all integers to floats in arguments
                    converted_arguments = convert_to_float(arguments)
                    fix_and_save_task(task_file_path, task_data, i, 'arguments', new_arguments=converted_arguments)
                    
                    # Retry with converted arguments
                    res = execute_api(api_name=action_name, arguments=converted_arguments)
                    actual_output = res[0] if res else None
                
                # Check for output mismatch
                if not strict_equal(actual_output, expected_output):
                    # Try converting expected output to floats
                    converted_output = convert_to_float(expected_output)
                    
                    if loose_equal(actual_output, converted_output):
                        # Values match after conversion (ignoring key order), so just update with converted
                        fix_and_save_task(task_file_path, task_data, i, 'output', new_output=converted_output)
                    else:
                        # Output mismatch that can't be fixed by float conversion
                        error_msg = f"Output mismatch in action '{action_name}': expected {expected_output}, got {actual_output}"
                        return False, error_msg
                
                # Check for other errors in response
                if (res and len(res) > 0 and isinstance(res[0], dict) and 
                    ("error" in res[0].keys() or (res[0].get("status") == "error" and "Type mismatch" not in res[0].get("message", "")))):
                    error_msg = f"Error in action '{action_name}': {res[0].get('error', res[0].get('message'))}"
                    return False, error_msg
                    
            except TypeError as e:
                if "Type mismatch" in str(e):
                    # Fix: Convert all integers to floats in arguments
                    converted_arguments = convert_to_float(arguments)
                    fix_and_save_task(task_file_path, task_data, i, 'arguments', new_arguments=converted_arguments)
                    
                    # Retry with converted arguments
                    res = execute_api(api_name=action_name, arguments=converted_arguments)
                    actual_output = res[0] if res else None
                    
                    # Check output after retry
                    if not strict_equal(actual_output, expected_output):
                        converted_output = convert_to_float(expected_output)
                        if loose_equal(actual_output, converted_output):
                            fix_and_save_task(task_file_path, task_data, i, 'output', new_output=converted_output)
                        else:
                            error_msg = f"Output mismatch in action '{action_name}': expected {expected_output}, got {actual_output}"
                            return False, error_msg
                else:
                    raise
        
        return True, None
        
    except FileNotFoundError:
        error_msg = f"Task file not found: {task_file_path}"
        return False, error_msg
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in task file {task_file_path}: {str(e)}"
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error processing {task_file_path}: {str(e)}"
        print(f"ERROR in file {task_file_path}: {e}")
        return False, error_msg


def run_all_tasks(base_path="week_11_new"):  
    """
    Find and run all task.json files, logging errors to a file.
    Automatically fixes type mismatches and output mismatches.
    """
    # Find all task files
    task_files = find_all_task_files(base_path)
    
    if not task_files:
        print("No task.json files found in the directory structure.")
        return
    
    # Track results
    successful_tasks = []
    failed_tasks = []
    
    # Process each task file
    for task_number, task_file in enumerate(task_files):
        try:
            success, error_message = run_single_task(task_file)
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            success = False
            
        
        if success:
            successful_tasks.append(task_file)
        else:
            failed_tasks.append({
                'file': task_file,
                'error': error_message
            })
        if (task_number + 1) % 10 == 0:
            print(f"Processed {task_number + 1}/{len(task_files)} tasks...")
    
    # Write error log
    if failed_tasks:
        error_log_file = "task_errors.log"
        with open(error_log_file, 'w') as f:
            f.write(f"Task Execution Error Log\n")
            f.write(f"Total tasks processed: {len(task_files)}\n")
            f.write(f"Failed tasks: {len(failed_tasks)}\n")
            f.write(f"Successful tasks: {len(successful_tasks)}\n\n")
            
            f.write("FAILED TASKS:\n")
            f.write("=" * 50 + "\n")
            for failed_task in failed_tasks:
                f.write(f"File: {failed_task['file']}\n")
                f.write(f"Error: {failed_task['error']}\n")
                f.write("-" * 30 + "\n")
            
            f.write("\nSUCCESSFUL TASKS:\n")
            f.write("=" * 50 + "\n")
            for successful_task in successful_tasks:
                f.write(f"{successful_task}\n")
    
    # Print summary
    print("=" * 60)
    print("EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Total tasks processed: {len(task_files)}")
    print(f"Successful: {len(successful_tasks)}")
    print(f"Failed: {len(failed_tasks)}")
    
    if failed_tasks:
        print(f"\nError log written to: task_errors.log")
        print("\nFailed tasks:")
        for failed_task in failed_tasks:
            print(f"  - {failed_task['file']}")
    
    if successful_tasks:
        print(f"\nSuccessful tasks: {len(successful_tasks)}")


if __name__ == "__main__":
    run_all_tasks("week_11_new")