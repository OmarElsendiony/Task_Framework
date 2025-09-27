import shutil
import os

prompt = """Assume you are an experienced tester. I am going to give you python functions and you are going to give me the inputs to test this function. The inputs are provided in the form of actions. You have to provide two tests for each function with the most number of parameters as possible (if applicable). However, you have to follow the format that I provide to you below.

# Format:
{{
    "env": "{environment_name}",
    "interface_num": {interface_number},
    "task": {{
        "actions": [
            {{
                "name": "discover_user_entities",
                "arguments": {{
                    "entity_type": "users",
                    "filters": {{
                        "email": "sarahcampos144@hotmail.com"
                    }}
                }}
            }},
            {{
                "name": "discover_user_entities",
                "arguments": {{
                    "entity_type": "users",
                    "filters": {{
                        "email": "sarahcampos144@hotmail.com"
                    }}
                }}
            }}
        ]
    }}
}}

where the name of action is the function name and the arguments are the parameters of the function. You have to provide multiple actions for a single file in a single test if applicable. 

# Functions:
{functions}

# Policy:
{policy}

# Database Schema:
{schema}

You have to provide the json file for each function separately including all the tests for that function in the actions part. You are going to provide the bash script that will create and populate those json files in a folder named tools_regression_tests/interface_{interface_number}/.

Note: ids are just numeric strings "1", "2", ...
"""

with open("../domain_context/policy.txt", "r") as f:
    policy = f.read()

with open("../domain_context/schema.txt", "r") as f:
    schema = f.read()
    

def main():
    import argparse
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--env", type=str)
    # argparser.add_argument("--interface", type=int, choices=[1, 2, 3, 4, 5])
    
    args = argparser.parse_args()
    env = args.env
    # interface = args.interface
    
    
    if os.path.exists("tests_prompt/"):
        shutil.rmtree('tests_prompt/', ignore_errors=True)

    os.makedirs("tests_prompt/", exist_ok=True)
    for interface in range(1, 6):
        all_codes = []
        path_interface = f"../envs/{env}/tools/interface_{interface}/"
        if not os.path.exists(path_interface):
            continue
        
        if not os.path.exists(f"tests_prompt/interface_{interface}/"):
            os.makedirs(f"tests_prompt/interface_{interface}/", exist_ok=True)

        files = os.listdir(path_interface)
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(path_interface, file), "r") as f:
                    code = f.read()
                
                # prompt_filled = prompt.format(code=code, policy=policy, schema=schema)
                all_codes.append(code)

        with open(f"tests_prompt/interface_{interface}/all_code_interface_{interface}.txt", "w") as f:
            all_codes_joined = "\n\n# -----------------\n\n".join(all_codes)
            prompt_filled = prompt.format(environment_name=env, interface_number=interface,  functions=all_codes_joined, policy=policy, schema=schema)
            f.write(prompt_filled)

main()