import os
import shutil
import json
import re
from pathlib import Path

def convert_python_bool_to_json(text):
    """
    Convert Python boolean literals (True/False) to JSON boolean literals (true/false)
    Also converts string literals "True"/"False" to boolean true/false and None to null
    """
    # Replace standalone True/False with proper JSON booleans
    text = re.sub(r'\bTrue\b', 'true', text)
    text = re.sub(r'\bFalse\b', 'false', text)
    
    # Replace None with null
    text = re.sub(r'\bNone\b', 'null', text)
    
    # Replace string literals "True"/"False" with boolean true/false
    text = re.sub(r'"True"', 'true', text)
    text = re.sub(r'"False"', 'false', text)
    
    return text

def fix_json_syntax(json_str):
    """
    Fix common JSON syntax issues:
    1. Remove trailing commas
    2. Ensure proper quoting
    3. Fix common typos in boolean values
    """
    # Remove trailing commas before closing braces/brackets
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
    
    # Fix missing quotes around property names
    json_str = re.sub(r'([{,]\s*)(\w+)(\s*:)', r'\1"\2"\3', json_str)
    
    # Fix common boolean typos (case-insensitive)
    json_str = re.sub(r':\s*Te\b', ': true', json_str, flags=re.IGNORECASE)
    json_str = re.sub(r':\s*Fal\b', ': false', json_str, flags=re.IGNORECASE)
    json_str = re.sub(r':\s*Tru\b', ': true', json_str, flags=re.IGNORECASE)
    json_str = re.sub(r':\s*Fals\b', ': false', json_str, flags=re.IGNORECASE)
    
    return json_str

def convert_nested_booleans(obj):
    """
    Recursively convert boolean values in nested dictionaries/lists
    """
    if isinstance(obj, dict):
        return {key: convert_nested_booleans(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_nested_booleans(item) for item in obj]
    elif obj == "True":
        return True
    elif obj == "False":
        return False
    else:
        return obj

def process_json_string(json_str, source_file="unknown"):
    """
    Process a JSON string by converting Python booleans to JSON booleans
    and handling nested structures
    """
    original_json = json_str
    
    try:
        # FIRST, fix JSON syntax issues like trailing commas and typos
        fixed_json_str = fix_json_syntax(json_str)
        
        # THEN convert Python booleans and None to JSON format
        converted_str = convert_python_bool_to_json(fixed_json_str)
        
        # Parse the JSON to validate it
        parsed_json = json.loads(converted_str)
        
        # Recursively process nested structures to convert string booleans
        processed_json = convert_nested_booleans(parsed_json)
        
        # Return the processed JSON object (not a string)
        return processed_json
        
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse JSON string in file: {source_file}")
        print(f"Original JSON: {original_json}")
        print(f"Fixed and converted string was: {convert_python_bool_to_json(fix_json_syntax(json_str))}")
        print(f"Error: {e}")
        
        # If parsing fails, return original string
        return json_str

def is_json_like_string(text):
    """
    Check if a string looks like JSON (starts with { and ends with })
    and contains True, False, or "True", "False" anywhere in the structure
    """
    text = text.strip()
    return (text.startswith('{') and text.endswith('}')) or (text.startswith('[') and text.endswith(']'))

def should_convert_to_object(field_name, json_string):
    """
    Determine if a JSON string field should be converted to an actual object
    """
    # Fields that typically contain JSON objects that should be converted
    object_fields = {
        'holding_data', 'notification_data', 'user_data', 'fund_data', 
        'portfolio_data', 'config', 'settings', 'metadata', 'data'
    }
    
    return (field_name.lower() in object_fields or 
            field_name.lower().endswith('_data') or 
            field_name.lower().endswith('_config'))

def process_file_content(content, source_file="unknown"):
    """
    Process file content to find and convert JSON-like strings with boolean values
    """
    try:
        # First, try to parse the entire content as JSON
        data = json.loads(content)
        
        # Process the JSON structure
        processed_data = process_json_structure(data, source_file)
        
        # Convert back to formatted JSON string
        return json.dumps(processed_data, indent=4)
        
    except json.JSONDecodeError:
        # If it's not valid JSON, fall back to string processing
        return process_file_content_string_mode(content, source_file)

def process_json_structure(obj, source_file="unknown", parent_keys=None):
    """
    Recursively process JSON structure to convert string JSON to objects where appropriate
    Skip processing if any parent key is "traj"
    """
    if parent_keys is None:
        parent_keys = []
    
    # Skip processing if "traj" is in any parent key
    if "traj" in parent_keys:
        return obj
    
    if isinstance(obj, dict):
        processed = {}
        for key, value in obj.items():
            current_keys = parent_keys + [key]
            
            if isinstance(value, str):
                # Check if it's a simple boolean string
                if value == "True":
                    processed[key] = True
                    print(f"Converted '{key}': \"True\" -> true in: {source_file}")
                elif value == "False":
                    processed[key] = False
                    print(f"Converted '{key}': \"False\" -> false in: {source_file}")
                elif value == "None":
                    processed[key] = None
                    print(f"Converted '{key}': \"None\" -> null in: {source_file}")
                elif is_json_like_string(value):
                    # Check if this field should be converted to an object
                    if should_convert_to_object(key, value):
                        try:
                            # Process as JSON string and convert to object
                            processed_json = process_json_string(value, source_file)
                            processed[key] = processed_json
                            print(f"Converted '{key}' from JSON string to object in: {source_file}")
                        except Exception as e:
                            print(f"Failed to convert '{key}' to object in {source_file}: {e}")
                            processed[key] = value
                    else:
                        # Keep as string but process boolean values
                        processed[key] = process_json_string(value, source_file)
                else:
                    # Regular string, keep as is
                    processed[key] = value
            else:
                # Recursively process nested structures
                processed[key] = process_json_structure(value, source_file, current_keys)
        return processed
    elif isinstance(obj, list):
        return [process_json_structure(item, source_file, parent_keys) for item in obj]
    else:
        return obj

def process_file_content_string_mode(content, source_file="unknown"):
    """
    Fallback string processing mode for non-JSON files
    """
    # Improved pattern to capture JSON strings with various quoting styles
    json_pattern = r'\"([^\"]+)\"\s*:\s*\"([^\"]*{(?:[^{}]|{[^{}]*})*}[^\"]*)\"'
    
    def replace_json_match(match):
        field_name = match.group(1)
        json_string = match.group(2)
        
        # Unescape the JSON string
        unescaped = json_string.replace('\\"', '"').replace('\\\\', '\\')
        
        # Check if this looks like JSON AND contains True/False/None
        if (is_json_like_string(unescaped) and 
            re.search(r'\bTrue\b|\bFalse\b|\bNone\b|"True"|"False"', unescaped)):
            try:
                # Process the JSON string with file context
                processed = process_json_string(unescaped, source_file)
                
                if should_convert_to_object(field_name, unescaped) and isinstance(processed, (dict, list)):
                    # Convert to object representation
                    object_str = json.dumps(processed)
                    return f'"{field_name}": {object_str}'
                else:
                    # Keep as escaped string
                    escaped = json.dumps(processed).replace('\\', '\\\\').replace('"', '\\"')
                    return f'"{field_name}": "{escaped}"'
            except Exception as e:
                print(f"Error processing JSON string in {source_file}: {e}")
                return match.group(0)
        else:
            # Not JSON-like with booleans, return original
            return match.group(0)
    
    # Apply JSON string processing
    processed_content = re.sub(json_pattern, replace_json_match, content)
    
    # Handle standalone string boolean values like "field": "True"
    bool_string_pattern = r'("([^"]+)":\s*)"(True|False)"'
    
    def replace_bool_string(match):
        field_part = match.group(1)
        bool_value = match.group(3)
        return f'{field_part}{bool_value.lower()}'
    
    processed_content = re.sub(bool_string_pattern, replace_bool_string, processed_content)
    
    # Also handle unquoted boolean values in JSON-like structures
    unquoted_bool_pattern = r'("([^"]+)":\s*)(True|False|None)(\s*[,}])'
    
    def replace_unquoted_bool(match):
        field_part = match.group(1)
        value = match.group(3)
        suffix = match.group(4)
        
        # Convert Python literals to JSON
        if value == 'True':
            value = 'true'
        elif value == 'False':
            value = 'false'
        elif value == 'None':
            value = 'null'
            
        return f'{field_part}{value}{suffix}'
    
    processed_content = re.sub(unquoted_bool_pattern, replace_unquoted_bool, processed_content)
    
    return processed_content

def replicate_folder_structure(source_root, dest_root):
    """
    Replicate folder structure from source_root to dest_root with JSON processing
    """
    source_path = Path(source_root)
    dest_path = Path(dest_root)
    
    if not source_path.exists():
        raise FileNotFoundError(f"Source folder '{source_root}' does not exist")
    
    # Remove destination if it exists and create fresh
    if dest_path.exists():
        shutil.rmtree(dest_path)
    
    dest_path.mkdir(parents=True, exist_ok=True)
    
    processed_files = 0
    converted_entries = 0
    problematic_files = []
    
    for root, dirs, files in os.walk(source_path):
        rel_path = Path(root).relative_to(source_path)
        dest_dir = dest_path / rel_path
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            source_file = Path(root) / file
            dest_file = dest_dir / file
            
            try:
                # Read file content
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Process content with file context
                processed_content = process_file_content(content, str(source_file))
                
                # Check if any changes were made
                if content != processed_content:
                    # Count conversions by comparing before/after
                    original_bools = len(re.findall(r'\bTrue\b|\bFalse\b|\bNone\b|"True"|"False"', content))
                    processed_bools = len(re.findall(r'\bTrue\b|\bFalse\b|\bNone\b|"True"|"False"', processed_content))
                    conversions = original_bools - processed_bools
                    
                    if conversions > 0 or content != processed_content:
                        converted_entries += max(conversions, 1)  # At least 1 if content changed
                        print(f"Processed file: {source_file}")
                
                # Write processed content to destination
                with open(dest_file, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                
                processed_files += 1
                
            except UnicodeDecodeError:
                # Handle binary files by copying them
                shutil.copy2(source_file, dest_file)
                processed_files += 1
            except Exception as e:
                print(f"Error processing file {source_file}: {e}")
                problematic_files.append(str(source_file))
                shutil.copy2(source_file, dest_file)
    
    # Print summary of problematic files
    if problematic_files:
        print(f"\nProblematic files that may need manual review:")
        for file in problematic_files:
            print(f"  - {file}")
    
    return processed_files, converted_entries, problematic_files

def main():
    source_folder = "week_11"
    destination_folder = "week_11_new"
    
    try:
        print(f"Replicating folder structure from '{source_folder}' to '{destination_folder}'...")
        processed_files, converted_entries, problematic_files = replicate_folder_structure(source_folder, destination_folder)
        
        print(f"\nCompleted successfully!")
        print(f"- Processed {processed_files} files")
        print(f"- Converted {converted_entries} boolean/None values")
        print(f"- Found {len(problematic_files)} files that may need manual review")
        print(f"- Replica created at: {destination_folder}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()