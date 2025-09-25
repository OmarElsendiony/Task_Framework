#!/usr/bin/python3
""" Flask Application """
import json
import os
import ast
from typing import Dict, Any
import re


session = dict()
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



def env_interface(environment: str, interface: str, envs_path="envs"):
    """ Endpoint to handle environment and interface selection """
    try:
        data = dict()
        if environment != session.get("environment"):
            # ENVS_PATH = "envs"
            DATA_PATH = f"{envs_path}/{environment}/data"
            data_files = os.listdir(DATA_PATH)
            # print("Loaded data:")
            for data_file in data_files:
                if data_file.endswith(".json"):
                    data_file_path = os.path.join(DATA_PATH, data_file)
                    with open(data_file_path, "r") as file:
                        data[data_file.split('.')[0]] = json.load(file)
            session["environment"] = environment
            session["interface"] = interface
            session["data"] = data
            # print("data", g.data)
        
        # print(session["environment"], session["interface"])
        if environment and interface:
            # last_interface = interface
            # last_environment = environment
            # ENVS_PATH = "envs"
            TOOLS_PATH = f"{envs_path}/{environment}/tools"
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
            
            session["imports_set"] = importsSet
            session["invoke_methods"] = invoke_methods
            return ({
                'status': 'success',
                'message': 'Environment and interface selected successfully',
                'functions_info': functionsInfo,
            }), 200
        else:
            return ({
                'status': 'error',
                'message': 'Missing environment or interface data'
            }), 400
            
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return ({
            'status': 'error',
            'message': 'Internal server error'
        }), 500
    

def create_tools_class(imports_set, invoke_methods):
    # Create the class dynamically in memory
    imports_code = '\n'.join(sorted(imports_set))
    
    # Build the class definition as a string
    class_code = f"""
{imports_code}

class Tools:
"""
    for invoke_method in invoke_methods:
        class_code += ("    @staticmethod\n" + invoke_method + "\n\n")
    # Execute the code and return the class
    namespace = {}
    exec(class_code, namespace)
    # return namespace['Tools']
    # session["tools_class_code"] = class_code 
    return namespace['Tools']


def execute_api_utility(api_name, arguments):
    tools_instance = create_tools_class(session.get("imports_set", []), session.get("invoke_methods", []))
    # print('executing ...')
    arguments = arguments_processing(arguments)
    # print(dir(tools_instance))
    if hasattr(tools_instance, api_name):
        result = getattr(tools_instance, api_name)(data=session["data"], **arguments)
        # print(f"Result from API {api_name}: {result}")
        return result
    else:
        raise AttributeError(f"API {api_name} not found")

def arguments_processing(arguments):
    cleaned_arguments = {}
    for argument, argument_value in arguments.items():
        # Skip empty values
        if argument_value == '':
            continue

        # Skip IDs (do not modify or parse)
        if "id" == argument.lower() or "_id" in argument.lower() or "_by" in argument.lower() or "name" in argument.lower() or "_to" in argument.lower():
            cleaned_arguments[argument] = argument_value
            continue
        # Try to evaluate literal (e.g., convert "True" → True, "123" → 123)
        try:
            cleaned_arguments[argument] = ast.literal_eval(argument_value)
        except (ValueError, SyntaxError):
            cleaned_arguments[argument] = argument_value

    return cleaned_arguments



def execute_api(api_name: str, arguments: Dict[str, Any]):
    # ENVS_PATH = "envs"
    # DATA_PATH = f"{ENVS_PATH}/{environment}/data"
    # data_files = os.listdir(DATA_PATH)
    # print("Loaded data:")
    # for data_file in data_files:
    #     if data_file.endswith(".json"):
    #         data_file_path = os.path.join(DATA_PATH, data_file)
    #         with open(data_file_path, "r") as file:
    #             session["data"][data_file.split('.')[0]] = json.load(file)
    # print("hello")
    api_name = api_name + "_invoke" if api_name else None
    # for action in session.get("actions", []):
    #     # print('session:', session.get("actions"))
    #     execute_api_utility(api_name, arguments)

    if not api_name:
        return ({
            'status': 'error',
            'message': 'API name is required'
        }), 400
    
    cleaned_arguments = arguments_processing(arguments)
    arguments = cleaned_arguments
    
    tools_instance = create_tools_class(session.get("imports_set", []), session.get("invoke_methods", []))
    
    # print(dir(tools_instance))
    if hasattr(tools_instance, api_name):
        try:
            # print(g.data)
            # Dynamically call the method with the provided arguments
            # result = getattr(tools_instance, api_name)(data=session["data"], **arguments)
            result = execute_api_utility(api_name, arguments)
            # print(f"Result from API {api_name}: {result}")
            if not session.get("actions"):
                session["actions"] = []
            session["actions"].append({
                'api_name': api_name,
                'arguments': arguments
            })
            return (json.loads(result) if isinstance(result, str) else result
        ), 200
        except Exception as e:
            print(f"Error executing API {api_name}: {str(e)}")
            return ({
                'status': 'error',
                'message': f'Failed to execute API: {str(e)}'
            }), 500
    else:
        return ({
            'status': 'error',
            'message': f'API {api_name} not found'
        }), 404

def clear_session():
    session.clear()