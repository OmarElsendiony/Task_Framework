
import ast
import os
from typing import Dict, Any
import re


def ast_to_python_value(node):
    """Convert AST node to Python value."""
    if isinstance(node, ast.Constant):  # Python 3.8+
        return node.value
    elif isinstance(node, ast.Str):  # Python < 3.8
        return node.s
    elif isinstance(node, ast.Num):  # Python < 3.8
        return node.n
    elif isinstance(node, ast.List):
        return [ast_to_python_value(item) for item in node.elts]
    elif isinstance(node, ast.Dict):
        result = {}
        for key, value in zip(node.keys, node.values):
            result[ast_to_python_value(key)] = ast_to_python_value(value)
        return result
    elif isinstance(node, ast.Name):
        # For variable names, we can't resolve them without execution
        # Return the name as a string for now
        return f"<variable: {node.id}>"
    else:
        # For other node types, return a string representation
        return f"<{type(node).__name__}>"


def extract_method_from_ast(source_code: str, method_name: str) -> str:
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            start = node.lineno - 1
            end = node.end_lineno
            return '\n'.join(source_code.splitlines()[start:end])
    return None


def extract_file_info(file_path: str) -> Dict[str, Any]:
    """
    Extract function information from a Python file containing a Tool class with get_info method.
    """
    try:
        # Read the file content
        with open(file_path, "r") as file:
            content = file.read()
        
        imports = []
        # Extract imports
        import_pattern = re.compile(r'^\s*import\s+(\w+)', re.MULTILINE)
        from_import_pattern =  re.compile(
    r'^\s*from\s+([\w\.]+)\s+import\s+((?:\w+\s*,\s*)*\w+)', 
    re.MULTILINE
)
        for match in import_pattern.finditer(content):
            imports.append(match.group(0).strip())
        for match in from_import_pattern.finditer(content):
            if match.group(1) == "tau_bench.envs.tool":
                # Skip tau_bench.envs.tool import
                continue
            imports.append(match.group(0).strip())
        
        tree = ast.parse(content)
        
        # Find the class that inherits from Tool
        tool_class = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it inherits from Tool
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == 'Tool':
                        tool_class = node
                        # break
            if isinstance(node, ast.FunctionDef) and node.name == "invoke":
                start = node.lineno - 1
                end = node.end_lineno
                invoke_method = '\n'.join(content.splitlines()[start:end])
                # if tool_class:
                #     break
        
        if not tool_class:
            return {"error": "No Tool class found"}
        
        if not invoke_method:
            return {"error": "No invoke method found in Tool class"}
        
        # Find the get_info method
        get_info_method = None
        for node in tool_class.body:
            if isinstance(node, ast.FunctionDef) and node.name == 'get_info':
                get_info_method = node
                break
        
        if not get_info_method:
            return {"error": "No get_info method found"}
        
        # Extract the return dictionary from get_info method
        return_dict = None
        for node in ast.walk(get_info_method):
            if isinstance(node, ast.Return):
                return_dict = node.value
                break
        
        if not return_dict:
            return {"error": "No return dictionary found in get_info method"}
        
        # Parse the dictionary to extract function info
        parsed_dict = ast_to_python_value(return_dict)
        function_info = {}
        
        if isinstance(parsed_dict, dict) and 'function' in parsed_dict:
            func_info = parsed_dict['function']
            if isinstance(func_info, dict):
                function_info = {
                    'name': func_info.get('name', ''),
                    'description': func_info.get('description', ''),
                    'parameters': func_info.get('parameters', {}),
                    'required': func_info.get('parameters', {}).get('required', [])
                }

        return function_info, invoke_method, imports
        
    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}


ENVS_PATH = "envs"
env_name = "hr_payroll"
TOOLS_PATH = f"{ENVS_PATH}/{env_name}/tools"

interface_number = 1
INTERFACE_PATH = f"{TOOLS_PATH}/interface_{interface_number}"

# print(os.path.exists(INTERFACE_PATH))

new_file_header_content = """
#!/usr/bin/python3
import json
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from typing import *


app = Flask(__name__ , static_url_path='')
cors = CORS(app)

class Tools:
"""

new_file_footer_content = """
@app.route('/', strict_slashes=False, methods=["POST", "GET"])
def main():
    return render_template('index.html')

if __name__ == "__main__":
    host = '0.0.0.0'
    port = '5000'
    app.run(host=host, port=port, threaded=True, debug=True)
"""

API_files = os.listdir(INTERFACE_PATH)
invoke_methods = []
importsSet = set()
for api_file in API_files:
    if api_file.endswith(".py") and not api_file.startswith("__"):
        file_path = os.path.join(INTERFACE_PATH, api_file)
        with open(file_path, "r") as file:
            content = file.read()
            try:
                function_info, invoke_method, imports = extract_file_info(file_path)
                importsSet.update(imports)
                invoke_method = invoke_method.replace("invoke", function_info.get('name', 'invoke')+"_invoke")
                invoke_methods.append(invoke_method)
                # break
            except SyntaxError as e:
                print(f"Syntax error in {api_file}: {e}")
            except Exception as e:
                print(f"Error processing {api_file}: {e}")

with open("appTemp.py", "w") as new_file:
    new_file.write('\n'.join(sorted(importsSet)) + "\n\n")
    new_file.write(new_file_header_content)
    for invoke_method in invoke_methods:
        new_file.write(invoke_method + "\n\n")
    new_file.write(new_file_footer_content)