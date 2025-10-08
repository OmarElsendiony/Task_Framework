import os
import json
import glob


def find_all_task_files(base_path="week_11_new"):
    """Find all task.json files in the directory structure."""
    pattern = os.path.join(base_path, "**", "task.json")
    task_files = glob.glob(pattern, recursive=True)
    return task_files


def fix_size_in_output(output):
    """
    Recursively find and convert 'size' field from int to float.
    Returns (modified_output, was_modified)
    """
    modified = False
    
    if isinstance(output, dict):
        new_output = {}
        for key, value in output.items():
            if key == 'size' and isinstance(value, int):
                new_output[key] = float(value)
                modified = True
            elif isinstance(value, (dict, list)):
                fixed_value, value_modified = fix_size_in_output(value)
                new_output[key] = fixed_value
                if value_modified:
                    modified = True
            else:
                new_output[key] = value
        return new_output, modified
    elif isinstance(output, list):
        new_list = []
        for item in output:
            fixed_item, item_modified = fix_size_in_output(item)
            new_list.append(fixed_item)
            if item_modified:
                modified = True
        return new_list, modified
    else:
        return output, False


def fix_task_file(task_file_path):
    """
    Fix task file by converting 'size' field to float in fund_entities APIs.
    """
    try:
        # Read the task file
        with open(task_file_path, 'r') as f:
            task_data = json.load(f)
        
        modified = False
        
        # Process each action
        actions = task_data.get("task", {}).get("actions", [])
        for action in actions:
            action_name = action.get("name", "")
            
            # Check if this is a fund_entities or trading_entities API
            if 'entities' in action_name:
                output = action.get("output")
                if output:
                    fixed_output, was_modified = fix_size_in_output(output)
                    if was_modified:
                        action["output"] = fixed_output
                        modified = True
        
        # Write back if modified
        if modified:
            with open(task_file_path, 'w') as f:
                json.dump(task_data, f, indent=2)
        
        return True, modified, None
        
    except Exception as e:
        return False, False, str(e)


def process_all_tasks(base_path="week_11_new"):
    """Process all task files and fix size fields."""
    
    # Find all task files
    task_files = find_all_task_files(base_path)
    
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
        success, modified, error = fix_task_file(task_file)
        
        if success:
            successful += 1
            if modified:
                modified_count += 1
                print(f"[{i}/{len(task_files)}] Fixed: {task_file}")
        else:
            failed.append({'file': task_file, 'error': error})
            print(f"[{i}/{len(task_files)}] FAILED: {task_file} - {error}")
    
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
    
    print(f"\nFixed files in place in: {base_path}/")


if __name__ == "__main__":
    process_all_tasks("week_11_new")