import os
import json
import glob
from collections import OrderedDict
from running_tasks import *


def find_all_task_files(base_path="week_10"):
    """
    Find all task.json files in the directory structure.
    """
    pattern = os.path.join(base_path, "**", "task.json")
    task_files = glob.glob(pattern, recursive=True)
    return task_files


def ordered_json_load(fp):
    """Load JSON while preserving key order"""
    return json.load(fp, object_pairs_hook=OrderedDict)


def ordered_json_loads(s):
    """Load JSON string while preserving key order"""
    return json.loads(s, object_pairs_hook=OrderedDict)


def ordered_json_dump(obj, fp, **kwargs):
    """Dump JSON while preserving key order"""
    json.dump(obj, fp, **kwargs)


def run_single_task(task_file_path):
    """
    Run a single task from a task.json file.
    Returns (success: bool, error_message: str or None, outputs_updated: bool)
    """
    try:
        with open(task_file_path, 'r', encoding='utf-8') as f:
            task_data = ordered_json_load(f)
        
        environment = task_data.get("env")
        interface = task_data.get("interface_num")
        
        # Initialize environment
        env_interface(environment=environment, interface=interface)
        
        # Track if any outputs were updated
        outputs_updated = False
        
        # Execute each action in the task
        actions = task_data.get("task", OrderedDict()).get("actions", [])
        for i, action in enumerate(actions):
            action_name = action.get("name")
            arguments = action.get("arguments", OrderedDict())
            
            res = execute_api(api_name=action_name, arguments=arguments)
            
            # Check for errors first
            if res and len(res) > 0 and isinstance(res[0], dict) and ("error" in res[0].keys() or "status" in res[0].keys() and res[0]["status"] == "error"):
                error_msg = f"Error in action '{action_name}': {res[0].get('error', res[0].get('message'))}"
                return False, error_msg, False
            
            # Check if output matches
            expected_output = action.get("output", "No output specified")
            actual_output = res[0] if res else 'No result'
            
            if actual_output != expected_output:
                # Convert actual_output to OrderedDict if it's a dict to maintain consistency
                if isinstance(actual_output, dict) and not isinstance(actual_output, OrderedDict):
                    actual_output = ordered_json_loads(json.dumps(actual_output))
                
                # Update the output value while preserving the OrderedDict structure
                action["output"] = actual_output
                outputs_updated = True
        
        # Write back to file if any outputs were updated
        if outputs_updated:
            with open(task_file_path, 'w', encoding='utf-8') as f:
                ordered_json_dump(task_data, f, indent=2, ensure_ascii=False)
        
        return True, None, outputs_updated
        
    except FileNotFoundError:
        error_msg = f"Task file not found: {task_file_path}"
        return False, error_msg, False
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in task file {task_file_path}: {str(e)}"
        return False, error_msg, False
    except Exception as e:
        error_msg = f"Unexpected error processing {task_file_path}: {str(e)}"
        print(f"ERROR in file {task_file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False, error_msg, False


def run_all_tasks(base_path="week_11_new"):  
    """
    Find and run all task.json files, logging errors to a file.
    """
    # Find all task files
    task_files = find_all_task_files(base_path)
    
    if not task_files:
        print("No task.json files found in the directory structure.")
        return
    
    # Track results
    successful_tasks = []
    failed_tasks = []
    updated_tasks = []
    
    # Process each task file
    for task_number, task_file in enumerate(task_files):
        try:
            success, error_message, outputs_updated = run_single_task(task_file)
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            success = False
            outputs_updated = False
            
        
        if success:
            successful_tasks.append(task_file)
            if outputs_updated:
                updated_tasks.append(task_file)
        else:
            failed_tasks.append({
                'file': task_file,
                'error': error_message
            })
        if (task_number + 1) % 10 == 0:
            print(f"Processed {task_number + 1}/{len(task_files)} tasks...")
    
    # Write error log
    if failed_tasks or updated_tasks:
        error_log_file = "task_errors.log"
        with open(error_log_file, 'w') as f:
            f.write(f"Task Execution Error Log\n")
            f.write(f"Total tasks processed: {len(task_files)}\n")
            f.write(f"Failed tasks: {len(failed_tasks)}\n")
            f.write(f"Successful tasks: {len(successful_tasks)}\n")
            f.write(f"Tasks with updated outputs: {len(updated_tasks)}\n\n")
            
            if failed_tasks:
                f.write("FAILED TASKS:\n")
                f.write("=" * 50 + "\n")
                for failed_task in failed_tasks:
                    f.write(f"File: {failed_task['file']}\n")
                    f.write(f"Error: {failed_task['error']}\n")
                    f.write("-" * 30 + "\n")
            
            if updated_tasks:
                f.write("\nTASKS WITH UPDATED OUTPUTS:\n")
                f.write("=" * 50 + "\n")
                for updated_task in updated_tasks:
                    f.write(f"{updated_task}\n")
            
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
    print(f"Tasks with updated outputs: {len(updated_tasks)}")
    
    if failed_tasks:
        print(f"\nError log written to: task_errors.log")
        print("\nFailed tasks:")
        for failed_task in failed_tasks:
            print(f"  - {failed_task['file']}")
    
    if updated_tasks:
        print(f"\nTasks with updated outputs:")
        for updated_task in updated_tasks:
            print(f"  - {updated_task}")
    
    if successful_tasks:
        print(f"\nSuccessful tasks:")
        for successful_task in successful_tasks:
            print(f"  - {successful_task}")


if __name__ == "__main__":
    run_all_tasks("week_11")