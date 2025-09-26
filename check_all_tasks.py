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


def run_single_task(task_file_path):
    """
    Run a single task from a task.json file.
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
            # print(action_name)
            # break
            # if (action_name == "manage_instrument" or action_name == "handle_instrument" or 
            #     action_name == "manipulate_instrument" or action_name == "address_instrument"):
            #     print("create_instrument, handle_instrument, manipulate_instrument, address_instrument functions are disabled in this script.")
            arguments = action.get("arguments", {})
            
            # print(f"  Running action {i+1}/{len(actions)}: {action_name}")
            
            res = execute_api(api_name=action_name, arguments=arguments)
            
            # Check for errors
            if res and len(res) > 0 and isinstance(res[0], dict) and "error" in res[0].keys():
                error_msg = f"Error in action '{action_name}': {res[0].get('error', 'Unknown error')}"
                # print(f"  ERROR: {error_msg}")
                return False, error_msg
        
        # print(f"  Successfully completed all actions for {task_file_path}")
        return True, None
        
    except FileNotFoundError:
        error_msg = f"Task file not found: {task_file_path}"
        # print(f"  ERROR: {error_msg}")
        return False, error_msg
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in task file {task_file_path}: {str(e)}"
        # print(f"  ERROR: {error_msg}")
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error processing {task_file_path}: {str(e)}"
        # print(f"  ERROR: {error_msg}")
        return False, error_msg


def run_all_tasks(base_path="week_11"):  
    """
    Find and run all task.json files, logging errors to a file.
    """
    # Find all task files
    task_files = find_all_task_files(base_path)
    
    if not task_files:
        print("No task.json files found in the directory structure.")
        return
    
    # print(f"Found {len(task_files)} task files to process:")
    # for task_file in task_files:
    #     print(f"  - {task_file}")
    # print()
    
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
        # print()  # Add spacing between tasks
    
    # Write error log
    if failed_tasks:
        error_log_file = "task_errors.log"
        with open(error_log_file, 'w') as f:
            f.write(f"Task Execution Error Log\n")
            # f.write(f"Generated: {json.dumps(task_data.get('timestamp', 'unknown'))}\n")
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
        print(f"\nSuccessful tasks:")
        for successful_task in successful_tasks:
            print(f"  - {successful_task}")


if __name__ == "__main__":
    run_all_tasks("week_10")