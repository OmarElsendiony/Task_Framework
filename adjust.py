import os
import json
import glob
import shutil
import copy
from pathlib import Path
from typing import Dict, Any, List, Set

# Define ID field mappings based on schema
# Format: 'field_name': 'source_table.json' (the table this ID references)
# Includes both full names and common API parameter aliases
ID_FIELD_TO_TABLE_MAPPING = {
    # User references
    'user_id': 'users.json',
    'parent_id': 'users.json',
    'author_id': 'users.json',
    'committer_id': 'users.json',
    'reviewer_id': 'users.json',
    'assignee_id': 'users.json',
    'merged_by': 'users.json',
    'owner_id': None,  # Polymorphic: user OR organization (context-dependent)
    
    # Access tokens
    'token_id': 'access_tokens.json',
    
    # Organizations
    'organization_id': 'organizations.json',
    'org_id': 'organizations.json',  # Common alias
    
    # Organization members
    'membership_id': 'organization_members.json',
    
    # Workspaces
    'workspace_id': 'workspaces.json',
    'ws_id': 'workspaces.json',  # Common alias
    
    # Workspace members
    'workspace_member_id': 'workspace_members.json',
    
    # Projects
    'project_id': 'projects.json',
    'proj_id': 'projects.json',  # Common alias
    
    # Project members
    'project_member_id': 'project_members.json',
    
    # Repositories (CRITICAL: includes repo_id alias)
    'repository_id': 'repositories.json',
    'repo_id': 'repositories.json',  # API parameter alias
    'parent_repository_id': 'repositories.json',
    
    # Repository collaborators
    'collaborator_id': 'repository_collaborators.json',
    
    # Branches
    'branch_id': 'branches.json',
    'source_branch': 'branches.json',
    'target_branch': 'branches.json',
    
    # Commits
    'commit_id': 'commits.json',
    'parent_commit_id': 'commits.json',
    'commit_sha': 'commits.json',  # Sometimes used as ID
    
    # Directories
    'directory_id': 'directories.json',
    'dir_id': 'directories.json',  # Common alias
    'parent_directory_id': 'directories.json',
    
    # Files
    'file_id': 'files.json',
    'last_commit_id': 'commits.json',
    
    # File contents
    'content_id': 'file_contents.json',
    
    # Code reviews
    'code_review_id': 'code_reviews.json',
    'review_id': 'pull_request_reviews.json',
    
    # Pull requests
    'pull_request_id': 'pull_requests.json',
    'pr_id': 'pull_requests.json',  # Common alias
    # 'pull_request_number': 'pull_requests.json',
    # 'pr_number': 'pull_requests.json',  # Common alias
    
    # Issues
    'issue_id': 'issues.json',
    # 'issue_number': 'issues.json',
    
    # Comments
    'comment_id': 'comments.json',
    'commentable_id': None,  # polymorphic - skip
    
    # Labels
    'label_id': 'labels.json',
    
    # Workflows
    'workflow_id': 'workflows.json',
    
    # Releases
    'release_id': 'releases.json',
    
    # Notifications
    'notification_id': 'notifications.json',
    'reference_id': None,  # polymorphic - skip
    
    # Stars
    'star_id': 'stars.json',
}

# CSV data for offsets
OFFSETS_DATA = """filename,folder1_records,folder2_records,offset,status
access_tokens.json,200,200,0,Found in both
branches.json,800,838,38,Found in both
code_reviews.json,645,658,13,Found in both
comments.json,1642,1655,13,Found in both
commits.json,8000,8052,52,Found in both
directories.json,960,983,23,Found in both
file_contents.json,12892,12927,35,Found in both
files.json,6400,6435,35,Found in both
issues.json,640,658,18,Found in both
labels.json,800,815,15,Found in both
notifications.json,482,494,12,Found in both
organization_members.json,326,340,14,Found in both
organizations.json,43,43,0,Found in both
project_members.json,384,415,31,Found in both
projects.json,63,73,10,Found in both
pull_request_reviews.json,279,295,16,Found in both
pull_requests.json,480,498,18,Found in both
releases.json,320,338,18,Found in both
repositories.json,163,169,6,Found in both
repository_collaborators.json,7029,7044,15,Found in both
stars.json,8004,8015,11,Found in both
users.json,200,200,0,Found in both
workflows.json,320,338,18,Found in both
workspace_members.json,179,179,0,Found in both
workspaces.json,32,32,0,Found in both"""

def parse_offsets_data() -> Dict[str, Dict[str, int]]:
    """Parse the CSV offset data into a dictionary."""
    offsets = {}
    lines = OFFSETS_DATA.strip().split('\n')[1:]  # Skip header
    for line in lines:
        parts = line.split(',')
        filename = parts[0]
        folder1_records = int(parts[1])
        offset = int(parts[3])
        offsets[filename] = {
            'folder1_records': folder1_records,
            'offset': offset
        }
    return offsets

def should_adjust_id(value: Any, folder1_records: int) -> bool:
    """Check if an ID value should be adjusted based on the criteria."""
    if not isinstance(value, (int, str)):
        return False
    
    try:
        numeric_value = int(value)
        # Adjust if ID is greater than the original record count
        # This handles auto-generated IDs from the database
        return numeric_value > folder1_records
    except (ValueError, TypeError):
        return False

def adjust_id_value(value: Any, offset: int) -> Any:
    """Adjust an ID value by the offset, maintaining the original type."""
    if isinstance(value, str):
        try:
            numeric_value = int(value)
            return str(numeric_value + offset)
        except ValueError:
            return value
    elif isinstance(value, int):
        return value + offset
    return value

def adjust_single_field(value: Any, field_name: str, all_offsets: Dict, modifications: List[str], context: Dict = None) -> Any:
    """
    Adjust a single field value based on which table it references.
    Uses ID_FIELD_TO_TABLE_MAPPING to determine the correct table.
    For polymorphic fields like owner_id, uses context to determine the target table.
    """
    if value is None:
        return value
    
    # Check if this field has a known table mapping
    if field_name not in ID_FIELD_TO_TABLE_MAPPING:
        return value
    
    table_file = ID_FIELD_TO_TABLE_MAPPING[field_name]
    
    # Handle context-dependent polymorphic fields
    if table_file is None:
        if not context:
            return value  # No context to resolve polymorphism
            
        # Resolve owner_id based on owner_type
        if field_name == 'owner_id' and 'owner_type' in context:
            owner_type = context['owner_type']
            if owner_type == 'user':
                table_file = 'users.json'
            elif owner_type == 'organization':
                table_file = 'organizations.json'
            else:
                # return value  # Unknown owner_type, skip
                table_file = 'users.json'
        
        # Resolve commentable_id based on commentable_type
        elif field_name == 'commentable_id' and 'commentable_type' in context:
            commentable_type = context['commentable_type']
            if commentable_type == 'issue':
                table_file = 'issues.json'
            elif commentable_type == 'pull_request':
                table_file = 'pull_requests.json'
            else:
                return value  # Unknown commentable_type, skip
        
        # Resolve reference_id based on reference_type
        elif field_name == 'reference_id' and 'reference_type' in context:
            reference_type = context['reference_type']
            if reference_type == 'issue':
                table_file = 'issues.json'
            elif reference_type == 'pull_request':
                table_file = 'pull_requests.json'
            elif reference_type == 'commit':
                table_file = 'commits.json'
            elif reference_type == 'release':
                table_file = 'releases.json'
            else:
                return value  # Unknown reference_type, skip
        
        else:
            return value  # Polymorphic field without resolvable context
    
    # Check if we have offset data for this table
    if table_file not in all_offsets:
        return value
    
    offset_info = all_offsets[table_file]
    folder1_records = offset_info['folder1_records']
    offset = offset_info['offset']
    
    if offset == 0:
        return value
    
    if should_adjust_id(value, folder1_records):
        old_value = value
        new_value = adjust_id_value(value, offset)
        modifications.append(f"  Adjusted {field_name}: {old_value} -> {new_value} (using {table_file})")
        return new_value
    
    return value

def adjust_ids_in_dict(data: Dict[str, Any], all_offsets: Dict, modifications: List[str]) -> Dict[str, Any]:
    """
    Recursively adjust IDs in a dictionary based on ALL table offsets.
    Each field is only adjusted once based on its primary table.
    Handles context-dependent polymorphic fields like owner_id.
    """
    adjusted_data = {}
    
    for key, value in data.items():
        if isinstance(value, dict):
            adjusted_data[key] = adjust_ids_in_dict(value, all_offsets, modifications)
        elif isinstance(value, list):
            adjusted_data[key] = [
                adjust_ids_in_dict(item, all_offsets, modifications)
                if isinstance(item, dict) else item
                for item in value
            ]
        else:
            # Try to adjust this field, passing the current dict as context
            adjusted_data[key] = adjust_single_field(value, key, all_offsets, modifications, context=data)
    
    return adjusted_data

def find_all_task_files(base_path: str) -> List[str]:
    """Find all task.json files in the directory structure."""
    pattern = os.path.join(base_path, "**", "task.json")
    return glob.glob(pattern, recursive=True)

def process_task_file(task_file_path: str, offsets: Dict[str, Dict[str, int]], 
                     output_base_path: str, input_base_path: str) -> tuple:
    """
    Process a single task.json file and adjust IDs based on offsets.
    Returns (success: bool, modifications_count: int, error_message: str or None, modifications: list)
    """
    try:
        # Read the task file
        with open(task_file_path, 'r', encoding='utf-8') as f:
            task_data = json.load(f)
        
        all_modifications = []
        actions = task_data.get("task", {}).get("actions", [])
        
        # Process each action
        for action_idx, action in enumerate(actions):
            action_name = action.get("name", "")
            action_modifications = []
            
            # Adjust IDs in arguments
            if 'arguments' in action:
                action['arguments'] = adjust_ids_in_dict(
                    action['arguments'], 
                    offsets,
                    action_modifications
                )
            
            # Adjust IDs in output
            if 'output' in action:
                action['output'] = adjust_ids_in_dict(
                    action['output'], 
                    offsets,
                    action_modifications
                )
            
            if action_modifications:
                all_modifications.append(f"Action {action_idx} ({action_name}):")
                all_modifications.extend(action_modifications)
        
        # Create output file path with same hierarchy
        relative_path = os.path.relpath(task_file_path, input_base_path)
        output_file_path = os.path.join(output_base_path, relative_path)
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        # Write adjusted task file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2)
        
        return True, len(all_modifications), None, all_modifications
        
    except Exception as e:
        # Copy the original file unchanged to output folder
        try:
            relative_path = os.path.relpath(task_file_path, input_base_path)
            output_file_path = os.path.join(output_base_path, relative_path)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            shutil.copy2(task_file_path, output_file_path)
        except Exception as copy_error:
            return False, 0, f"Processing error: {str(e)}, Copy error: {str(copy_error)}", []
        
        return False, 0, str(e), []

def adjust_all_tasks(input_base_path: str, output_base_path: str):
    """
    Process all task.json files and adjust IDs based on offsets.
    """
    print("Parsing offset data...")
    offsets = parse_offsets_data()
    
    print(f"Finding task files in {input_base_path}...")
    task_files = find_all_task_files(input_base_path)
    
    if not task_files:
        print("No task.json files found.")
        return
    
    print(f"Found {len(task_files)} task files to process\n")
    
    # Create output directory
    os.makedirs(output_base_path, exist_ok=True)
    
    # Track results
    successful_tasks = []
    failed_tasks = []
    total_modifications = 0
    
    # Process each task file
    for idx, task_file in enumerate(task_files, 1):
        success, mod_count, error_message, modifications = process_task_file(
            task_file, offsets, output_base_path, input_base_path
        )
        
        if success:
            successful_tasks.append({
                'file': task_file,
                'modifications': mod_count,
                'details': modifications
            })
            total_modifications += mod_count
        else:
            failed_tasks.append({
                'file': task_file,
                'error': error_message
            })
        
        if idx % 10 == 0:
            print(f"Processed {idx}/{len(task_files)} tasks...")
    
    # Write detailed log
    log_file = os.path.join(output_base_path, "adjustment_log.txt")
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("Task ID Adjustment Log\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total tasks processed: {len(task_files)}\n")
        f.write(f"Successful: {len(successful_tasks)}\n")
        f.write(f"Failed: {len(failed_tasks)}\n")
        f.write(f"Total ID adjustments: {total_modifications}\n\n")
        
        if failed_tasks:
            f.write("FAILED TASKS:\n")
            f.write("=" * 60 + "\n")
            for failed_task in failed_tasks:
                f.write(f"File: {failed_task['file']}\n")
                f.write(f"Error: {failed_task['error']}\n")
                f.write("-" * 40 + "\n")
            f.write("\n")
        
        f.write("SUCCESSFUL TASKS WITH MODIFICATIONS:\n")
        f.write("=" * 60 + "\n")
        for task in successful_tasks:
            if task['modifications'] > 0:
                f.write(f"\nFile: {task['file']}\n")
                f.write(f"Modifications: {task['modifications']}\n")
                for detail in task['details']:
                    f.write(f"  {detail}\n")
                f.write("-" * 40 + "\n")
        
        f.write("\nTASKS WITH NO MODIFICATIONS:\n")
        f.write("=" * 60 + "\n")
        for task in successful_tasks:
            if task['modifications'] == 0:
                f.write(f"{task['file']}\n")
    
    # Print summary
    print("\n" + "=" * 60)
    print("ADJUSTMENT SUMMARY")
    print("=" * 60)
    print(f"Total tasks processed: {len(task_files)}")
    print(f"Successful: {len(successful_tasks)}")
    print(f"Failed: {len(failed_tasks)}")
    print(f"Total ID adjustments: {total_modifications}")
    print(f"\nOutput directory: {output_base_path}")
    print(f"Detailed log: {log_file}")
    
    if failed_tasks:
        print(f"\nFailed tasks: {len(failed_tasks)}")
        for task in failed_tasks[:5]:  # Show first 5
            print(f"  - {task['file']}")
        if len(failed_tasks) > 5:
            print(f"  ... and {len(failed_tasks) - 5} more")
    
    tasks_with_mods = [t for t in successful_tasks if t['modifications'] > 0]
    if tasks_with_mods:
        print(f"\nTasks with modifications: {len(tasks_with_mods)}")
        for task in tasks_with_mods[:5]:  # Show first 5
            print(f"  - {task['file']} ({task['modifications']} changes)")
        if len(tasks_with_mods) > 5:
            print(f"  ... and {len(tasks_with_mods) - 5} more")


if __name__ == "__main__":
    # Example usage
    input_folder = "batch_Batch_version_control_system_20260108_195536"
    output_folder = "batch_Batch_version_control_system_20260108_195536_adjusted"
    
    adjust_all_tasks(input_folder, output_folder)