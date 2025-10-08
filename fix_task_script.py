import os
import json
import glob
import shutil
from pathlib import Path
from running_tasks import *


def find_all_task_files(base_path="week_11_new"):
    """Find all task.json files in the directory structure."""
    pattern = os.path.join(base_path, "**", "task.json")
    task_files = glob.glob(pattern, recursive=True)
    return task_files


def convert_to_float_if_needed(value):
    """Convert integer to float by adding .0 if it's a number."""
    if isinstance(value, int):
        return float(value)
    elif isinstance(value, dict):
        return {k: convert_to_float_if_needed(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_to_float_if_needed(item) for item in value]
    return value


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


def fix_task_file(task_file_path, output_base_path="week_11_fixed"):
    """
    Process a single task file, fix type mismatches and output differences,
    and save to the new location preserving directory structure.
    """
    try:
        # Read the task file
        with open(task_file_path, 'r') as f:
            task_data = json.load(f)
        
        modified = False
        environment = task_data.get("env")
        interface = task_data.get("interface_num")
        
        # Initialize environment
        env_interface(environment=environment, interface=interface)
        
        # Process each action
        actions = task_data.get("task", {}).get("actions", [])
        for action in actions:
            action_name = action.get("name")
            arguments = action.get("arguments", {})
            
            # Convert arguments if needed (int to float)
            original_arguments = arguments.copy()
            converted_arguments = convert_to_float_if_needed(arguments)
            
            if converted_arguments != original_arguments:
                action["arguments"] = converted_arguments
                modified = True
            
            # Execute and check output
            try:
                res = execute_api(api_name=action_name, arguments=converted_arguments)
                actual_output = res[0] if res else None
                expected_output = action.get("output")
                
                # Check if outputs match
                if not strict_equal(actual_output, expected_output):
                    # Try converting expected output
                    converted_output = convert_to_float_if_needed(expected_output)
                    if strict_equal(actual_output, converted_output):
                        action["output"] = converted_output
                        modified = True
                    else:
                        # If still doesn't match, use actual output
                        action["output"] = actual_output
                        modified = True
            except Exception as e:
                print(f"Error executing {action_name} in {task_file_path}: {e}")
                # Keep original values on error
                pass
        
        # Create output path preserving directory structure
        relative_path = os.path.relpath(task_file_path, "week_11_new")
        output_path = os.path.join(output_base_path, relative_path)
        output_dir = os.path.dirname(output_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Write the modified task file
        with open(output_path, 'w') as f:
            json.dump(task_data, f, indent=2)
        
        return True, modified, None
        
    except Exception as e:
        return False, False, str(e)


def process_all_tasks(input_base_path="week_11_new", output_base_path="week_11_fixed"):
    """Process all task files and save fixed versions."""
    
    # Find all task files
    task_files = find_all_task_files(input_base_path)
    
    if not task_files:
        print("No task.json files found.")
        return
    
    print(f"Found {len(task_files)} task files to process.\n")
    
    # Track results
    successful = 0
    modified_count = 0
    failed = []
    
    # Process each task file
    for i, task_file in enumerate(task_files, 1):
        success, modified, error = fix_task_file(task_file, output_base_path)
        
        if success:
            successful += 1
            if modified:
                modified_count += 1
                print(f"[{i}/{len(task_files)}] Fixed and saved: {task_file}")
            else:
                print(f"[{i}/{len(task_files)}] No changes needed: {task_file}")
        else:
            failed.append({'file': task_file, 'error': error})
            print(f"[{i}/{len(task_files)}] FAILED: {task_file} - {error}")
            return
    
    # Print summary
    print("\n" + "=" * 60)
    print("PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {len(task_files)}")
    print(f"Successfully processed: {successful}")
    print(f"Files modified: {modified_count}")
    print(f"Files failed: {len(failed)}")
    
    if failed:
        print("\nFailed files:")
        for fail in failed:
            print(f"  - {fail['file']}: {fail['error']}")
    
    print(f"\nFixed files saved to: {output_base_path}/")


if __name__ == "__main__":
    process_all_tasks("week_11_new", "week_11_fixed")