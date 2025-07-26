#!/usr/bin/python3
""" Flask Application """
import json
import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import ast
from typing import Dict, Any
import re

app = Flask(__name__ , static_url_path='')
cors = CORS(app)

###################### GLOBAL ENVIRONMENTS ##################################
last_environment = None
last_interface = None
data = dict()

######################## UTILITY FUNCTIONS ##################################
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
        print(file_path)
        with open(file_path, "r") as file:
            content = file.read()
        
        imports = []
        import_pattern = re.compile(r'^\s*import\s+(\w+)', re.MULTILINE)
        from_import_pattern =  re.compile(r'^\s*from\s+([\w\.]+)\s+import\s+((?:\w+\s*,\s*)*\w+)', re.MULTILINE)
        
        for match in import_pattern.finditer(content):
            imports.append(match.group(0).strip())
        for match in from_import_pattern.finditer(content):
            if match.group(1) == "tau_bench.envs.tool":
                # Skip tau_bench.envs.tool import
                continue
            imports.append(match.group(0).strip())
        
        tree = ast.parse(content)
        
        tool_class = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
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
        
        return_dict = None
        for node in ast.walk(get_info_method):
            if isinstance(node, ast.Return):
                return_dict = node.value
                break
        
        if not return_dict:
            return {"error": "No return dictionary found in get_info method"}
        
        parsed_dict = ast_to_python_value(return_dict)
        function_info = {}
        
        if isinstance(parsed_dict, dict) and 'function' in parsed_dict:
            func_info = parsed_dict['function']
            if isinstance(func_info, dict):
                function_info = {
                    'name': func_info.get('name', ''),
                    'description': func_info.get('description', ''),
                    'parameters': func_info.get('parameters', {}).get('properties', {}),
                    'required': func_info.get('parameters', {}).get('required', [])
                }

        return function_info, invoke_method, imports
        
    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}
######################## END UTILITY FUNCTIONS ##############################


@app.route('/', strict_slashes=False, methods=["POST", "GET"])
def index():
    return render_template('index.html')

@app.route('/choose_env_interface', strict_slashes=False, methods=["POST", "GET"])
def env_interface():
    """ Endpoint to handle environment and interface selection """
    if request.method == "POST":
        try:
            passed_inputs = request.get_json()
            
            environment = passed_inputs.get('environment') if passed_inputs else None
            interface = passed_inputs.get('interface') if passed_inputs else None
            
            global last_environment, last_interface, data
            if (environment != last_environment):
                data.clear()
                last_environment = environment
                ENVS_PATH = "envs"
                DATA_PATH = f"{ENVS_PATH}/{environment}/data"
                data_files = os.listdir(DATA_PATH)
                for data_file in data_files:
                    if data_file.endswith(".json"):
                        data_file_path = os.path.join(DATA_PATH, data_file)
                        with open(data_file_path, "r") as file:
                            data[data_file.split('.')[0]] = json.load(file)
            # print(data)
            
            if environment and interface:
                last_interface = interface
                last_environment = environment
                ENVS_PATH = "envs"
                TOOLS_PATH = f"{ENVS_PATH}/{environment}/tools"
                INTERFACE_PATH = f"{TOOLS_PATH}/interface_{interface}"
                API_files = os.listdir(INTERFACE_PATH)
                invoke_methods = []
                functionsInfo = []
                importsSet = set()
                for api_file in API_files:
                    if api_file.endswith(".py") and not api_file.startswith("__"):
                        file_path = os.path.join(INTERFACE_PATH, api_file)
                        # print(f"Processing file: {file_path}")
                        try:
                            function_info, invoke_method, imports = extract_file_info(file_path)
                            # print(f"Extracted function info: {function_info}")
                            # if not function_info:
                            #     print(f"No function info found in {api_file}, skipping.")
                            #     continue
                            importsSet.update(imports)
                            invoke_method = invoke_method.replace("invoke", function_info.get('name', 'invoke')+"_invoke")
                            invoke_methods.append(invoke_method)
                            functionsInfo.append(function_info)

                        except SyntaxError as e:
                            print(f"Syntax error in {api_file}: {e}")
                        except Exception as e:
                            print(f"Error processing {api_file}: {e}")
                
                with open("tools.py", "w") as new_file:
                    new_file.write('\n'.join(sorted(importsSet)) + "\n\n")
                    new_file.write("class Tools:\n")
                    for invoke_method in invoke_methods:
                        new_file.write("    @staticmethod\n" + invoke_method + "\n\n")
                
                return jsonify({
                    'status': 'success',
                    'message': 'Environment and interface selected successfully',
                    'functions_info': functionsInfo,
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Missing environment or interface data'
                }), 400
                
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': 'Internal server error'
            }), 500
    
    # Handle GET requests
    elif request.method == "GET":
        return jsonify({
            'status': 'success',
            'message': 'Choose environment and interface endpoint is working'
        })


@app.route('/execute_api', strict_slashes=False, methods=["GET", "POST"])
def execute_api():
    global data, last_environment, last_interface  # Add global declaration
    

    passed_data = request.get_json()
    api_name = passed_data.get('api_name')
    api_name = api_name + "_invoke" if api_name else None
    if not api_name:
        return jsonify({
            'status': 'error',
            'message': 'API name is required'
        }), 400
    
    arguments = passed_data.get('parameters', {})
    cleaned_arguments = {}



    for argument, argument_value in arguments.items():
        # Skip empty values
        if argument_value == '':
            continue

        # Skip IDs (do not modify or parse)
        if "id" == argument.lower() or "_id" in argument.lower() or "by" in argument.lower() or "name" in argument.lower():
            cleaned_arguments[argument] = argument_value
            continue

        # Try to evaluate literal (e.g., convert "True" → True, "123" → 123)
        try:
            cleaned_arguments[argument] = ast.literal_eval(argument_value)
        except (ValueError, SyntaxError):
            cleaned_arguments[argument] = argument_value

    # Replace original dict
    arguments = cleaned_arguments
            
    
    # print("Received data for API execution:", passed_data)
    
    import importlib
    import tools  
    importlib.reload(tools) 

    tools_instance = tools.Tools()
    
    if hasattr(tools_instance, api_name):
        try:
            # Dynamically call the method with the provided arguments
            result = getattr(tools_instance, api_name)(data=data, **arguments)
            print(f"Result from API {api_name}: {result}")
            return jsonify({
                'output': json.loads(result) if isinstance(result, str) else result
            }), 200
        except Exception as e:
            print(f"Error executing API {api_name}: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Failed to execute API: {str(e)}'
            }), 500
    else:
        return jsonify({
            'status': 'error',
            'message': f'API {api_name} not found'
        }), 404


if __name__ == "__main__":
    """ Main Function """
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port)
