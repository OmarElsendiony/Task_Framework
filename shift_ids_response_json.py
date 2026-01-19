import json
import os
import shutil
from typing import Dict, Any, List

# 1. CONFIGURATION
# ----------------
INPUT_ROOT_DIRECTORY = "batch_Batch_version_control_system_20260108_195536"
OUTPUT_ROOT_DIRECTORY = "batch_Batch_version_control_system_20260108_195536_adjusted"

# Define ID field mappings based on schema
ID_FIELD_TO_TABLE_MAPPING = {
    # User references
    'user_id': 'users.json',
    'parent_id': 'users.json',
    'author_id': 'users.json',
    'committer_id': 'users.json',
    'reviewer_id': 'users.json',
    'assignee_id': 'users.json',
    'merged_by': 'users.json',
    'owner_id': None,  # Polymorphic
    
    # Access tokens
    'token_id': 'access_tokens.json',
    
    # Organizations
    'organization_id': 'organizations.json',
    'org_id': 'organizations.json',
    
    # Organization members
    'membership_id': 'organization_members.json',
    
    # Workspaces
    'workspace_id': 'workspaces.json',
    'ws_id': 'workspaces.json',
    
    # Workspace members
    'workspace_member_id': 'workspace_members.json',
    
    # Projects
    'project_id': 'projects.json',
    'proj_id': 'projects.json',
    
    # Project members
    'project_member_id': 'project_members.json',
    
    # Repositories
    'repository_id': 'repositories.json',
    'repo_id': 'repositories.json',
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
    'commit_sha': 'commits.json',
    
    # Directories
    'directory_id': 'directories.json',
    'dir_id': 'directories.json',
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
    'pr_id': 'pull_requests.json',
    'pull_request_number': 'pull_requests.json',
    'pr_number': 'pull_requests.json',
    
    # Issues
    'issue_id': 'issues.json',
    'issue_number': 'issues.json',
    
    # Comments
    'comment_id': 'comments.json',
    'commentable_id': None,
    
    # Labels
    'label_id': 'labels.json',
    
    # Workflows
    'workflow_id': 'workflows.json',
    
    # Releases
    'release_id': 'releases.json',
    
    # Notifications
    'notification_id': 'notifications.json',
    'reference_id': None,
    
    # Stars
    'star_id': 'stars.json',
}

# CSV Data defining offsets and thresholds
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

# 2. HELPER FUNCTIONS
# -------------------

def parse_offsets_data() -> Dict[str, Dict[str, int]]:
    offsets = {}
    lines = OFFSETS_DATA.strip().split('\n')
    for line in lines[1:]:
        if line.startswith('#') or not line.strip(): continue
        parts = line.split(',')
        offsets[parts[0]] = {
            'folder1_records': int(parts[1]),
            'offset': int(parts[3])
        }
    return offsets

def should_adjust_id(value: Any, folder1_records: int) -> bool:
    if value is None: return False
    try:
        return int(value) > folder1_records
    except (ValueError, TypeError):
        return False

def adjust_id_value(value: Any, offset: int) -> Any:
    if isinstance(value, str):
        try:
            return str(int(value) + offset)
        except ValueError:
            return value
    elif isinstance(value, int):
        return value + offset
    return value

def adjust_single_field(value: Any, field_name: str, all_offsets: Dict, 
                        count_container: List[int], context: Dict = None) -> Any:
    if value is None: return value
    if field_name not in ID_FIELD_TO_TABLE_MAPPING: return value
    
    table_file = ID_FIELD_TO_TABLE_MAPPING[field_name]
    
    # Handle Polymorphic Context
    if table_file is None:
        if not context: return value
        
        if field_name == 'owner_id':
            otype = context.get('owner_type')
            table_file = 'organizations.json' if otype == 'organization' else 'users.json'
        elif field_name == 'commentable_id':
            ctype = context.get('commentable_type')
            if ctype == 'issue': table_file = 'issues.json'
            elif ctype == 'pull_request': table_file = 'pull_requests.json'
        elif field_name == 'reference_id':
            rtype = context.get('reference_type')
            if rtype == 'issue': table_file = 'issues.json'
            elif rtype == 'pull_request': table_file = 'pull_requests.json'
            elif rtype == 'commit': table_file = 'commits.json'
            elif rtype == 'release': table_file = 'releases.json'
    
    if not table_file or table_file not in all_offsets: return value
    
    info = all_offsets[table_file]
    if info['offset'] != 0 and should_adjust_id(value, info['folder1_records']):
        count_container[0] += 1
        return adjust_id_value(value, info['offset'])
    
    return value

def recursive_adjust(data: Any, offsets: Dict[str, Dict[str, int]], 
                     count_container: List[int]) -> Any:
    """
    Recursively walks through JSON.
    **NEW:** Detects strings that are actually JSON objects (like 'content') 
    and recurses into them.
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            # 1. Handle regular Dicts/Lists
            if isinstance(value, (dict, list)):
                new_dict[key] = recursive_adjust(value, offsets, count_container)
            
            # 2. Handle Strings (Potential JSON)
            elif isinstance(value, str):
                # Try to parse string as JSON
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, (dict, list)):
                        # It IS a JSON string! Recurse into it.
                        adjusted_parsed = recursive_adjust(parsed, offsets, count_container)
                        # Re-serialize back to string
                        new_dict[key] = json.dumps(adjusted_parsed)
                    else:
                        # It's a string, but not a complex object. Treat as field.
                        new_dict[key] = adjust_single_field(value, key, offsets, count_container, context=data)
                except (json.JSONDecodeError, TypeError):
                    # Not JSON, process as standard field
                    new_dict[key] = adjust_single_field(value, key, offsets, count_container, context=data)
            
            # 3. Handle Primitives (Ints, etc)
            else:
                new_dict[key] = adjust_single_field(value, key, offsets, count_container, context=data)
        
        return new_dict

    elif isinstance(data, list):
        return [recursive_adjust(item, offsets, count_container) for item in data]
    
    else:
        return data

# 3. MAIN PROCESSING LOGIC
# ------------------------

def process_and_copy(input_root: str, output_root: str):
    offsets = parse_offsets_data()
    files_processed = 0
    total_modifications = 0

    if not os.path.exists(input_root):
        print(f"Error: Input directory '{input_root}' does not exist.")
        return

    print(f"Scanning: {input_root}")
    print(f"Output to: {output_root}\n")

    for dirpath, _, filenames in os.walk(input_root):
        rel_path = os.path.relpath(dirpath, input_root)
        target_dir = os.path.join(output_root, rel_path)
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        if 'result.json' in filenames:
            input_file = os.path.join(dirpath, 'result.json')
            output_file = os.path.join(target_dir, 'result.json')
            
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                mod_count_container = [0]
                processed_data = recursive_adjust(data, offsets, mod_count_container)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(processed_data, f, indent=2)
                
                files_processed += 1
                total_modifications += mod_count_container[0]
                print(f"Processed: {input_file} -> {mod_count_container[0]} IDs adjusted")
                
            except Exception as e:
                print(f"Failed to process {input_file}: {e}")
        
        # Copy other files (task.json, etc.)
        for filename in filenames:
            if filename != 'result.json':
                src = os.path.join(dirpath, filename)
                dst = os.path.join(target_dir, filename)
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)

    print("-" * 40)
    print(f"Complete.")
    print(f"Files Processed: {files_processed}")
    print(f"Total IDs Modified: {total_modifications}")

if __name__ == "__main__":
    process_and_copy(INPUT_ROOT_DIRECTORY, OUTPUT_ROOT_DIRECTORY)