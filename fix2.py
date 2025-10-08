import os
import json
import glob
import typing
from pathlib import Path
from running_tasks import env_interface, create_tools_class


def find_all_task_files(base_path="week_11_new"):
    """Find all task.json files in the directory structure."""
    pattern = os.path.join(base_path, "**", "task.json")
    task_files = glob.glob(pattern, recursive=True)
    return task_files


def convert_int_to_float(value):
    """Recursively convert integers to floats."""
    if isinstance(value, int):
        return float(value)
    elif isinstance(value, dict):
        return {k: convert_int_to_float(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_int_to_float(item) for item in value]
    return value


def get_expected_types(tools_instance, api_name, arguments):
    """Get expected types for function arguments."""
    method_name = api_name + "_invoke"
    if not hasattr(tools_instance, method_name):
        return None
    
    try:
        annotations = getattr(tools_instance, method_name).__annotations__
        type_mismatches = {}
        
        for arg_name, arg_value in arguments.items():
            if arg_name not in annotations:
                continue
            
            expected_type = annotations[arg_name]
            origin = typing.get_origin(expected_type)
            
            # Handle Union/Optional types
            if origin is typing.Union:
                allowed_types = typing.get_args(expected_type)
                allowed_types = tuple(t for t in allowed_types if t is not type(None))
                
                if arg_value is None and type(None) in typing.get_args(expected_type):
                    continue
                
                # Check if conversion needed (int to float)
                if allowed_types and not isinstance(arg_value, allowed_types):
                    if float in allowed_types and isinstance(arg_value, int):
                        type_mismatches[arg_name] = 'int_to_float'
            
            # Handle generic types (Dict, List, etc.)
            elif origin is not None:
                if not isinstance(arg_value, origin):
                    if origin == float and isinstance(arg_value, int):
                        type_mismatches[arg_name] = 'int_to_float'
            
            # Handle regular types
            else:
                if not isinstance(arg_value, expected_type):
                    if expected_type == float and isinstance(arg_value, int):
                        type_mismatches[arg_name] = 'int_to_float'
        
        return type_mismatches
    except Exception as e:
        print(f"Error checking types for {api_name}: {e}")
        return None


def fix_task_file(task_file_path, output_base_path="week_11_fixed", session_data=None):
    """
    Process a single task file and fix type mismatches.
    Only converts integers to floats where needed based on function signatures.
    """
    try:
        # Read the task file
        with open(task_file_path, 'r') as f:
            task_data = json.load(f)
        
        modified = False
        environment = task_data.get("env")
        interface = task_data.get("interface_num")
        
        # Initialize environment if not already done for this env/interface
        env_key = f"{environment}_{interface}"
        if session_data.get('current_env') != env_key:
            env_result = env_interface(environment=environment, interface=interface)
            session_data['current_env'] = env_key
            session_data['imports_set'] = env_result[0].get('imports_set', [])
            session_data['invoke_methods'] = env_result[0].get('invoke_methods', [])
        
        # Create tools instance
        tools_instance = create_tools_class(
            session_data.get('imports_set', []), 
            session_data.get('invoke_methods', [])
        )
        
        # Process each action
        actions = task_data.get("task", {}).get("actions", [])
        for action in actions:
            action_name = action.get("name")
            arguments = action.get("arguments", {})
            
            # Check for type mismatches
            type_mismatches = get_expected_types(tools_instance, action_name, arguments)
            
            if type_mismatches:
                # Fix arguments
                for arg_name, fix_type in type_mismatches.items():
                    if fix_type == 'int_to_float':
                        action["arguments"][arg_name] = float(arguments[arg_name])
                        modified = True
            
            # Also check and fix output if it contains integers that should be floats
            # We do a blanket conversion for outputs to be safe
            output = action.get("output")
            if output is not None:
                converted_output = convert_int_to_float(output)
                if converted_output != output:
                    action["output"] = converted_output
                    modified = True
        
        # Create output path preserving directory structure
        relative_path = os.path.relpath(task_file_path, "week_11_new")
        output_path = os.path.join(output_base_path, relative_path)
        output_dir = os.path.dirname(output_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Write the modified task file (preserves order in Python 3.7+)
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
    
    # Shared session data to avoid reinitializing environments
    session_data = {}
    
    # Track results
    successful = 0
    modified_count = 0
    failed = []
    
    # Process each task file
    for i, task_file in enumerate(task_files, 1):
        success, modified, error = fix_task_file(task_file, output_base_path, session_data)
        
        if success:
            successful += 1
            if modified:
                modified_count += 1
                print(f"[{i}/{len(task_files)}] Fixed: {task_file}")
            else:
                print(f"[{i}/{len(task_files)}] No changes: {task_file}")
        else:
            failed.append({'file': task_file, 'error': error})
            print(f"[{i}/{len(task_files)}] FAILED: {task_file} - {error}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Total files: {len(task_files)}")
    print(f"Successfully processed: {successful}")
    print(f"Files modified: {modified_count}")
    print(f"Files failed: {len(failed)}")
    
    if failed:
        print("\nFailed files:")
        for fail in failed:
            print(f"  - {fail['file']}: {fail['error']}")
    
    print(f"\nFixed files saved to: {output_base_path}/")


if __name__ == "__main__":
    process_all_tasks("week_11_new", "week_11_omar")