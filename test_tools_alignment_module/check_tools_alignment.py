import shutil
import os

prompt = """Assume you are a critique expert. You will be given the implementation of one or more functions/tools that target a database. Your task is to review the implementation and ensure that it aligns with the database schema and the policy that I am going to provide.
You have to check if the parameters align with the policy and schema. You have to check if there is a part of the implementation that is wrong like missing parameters or wrong parameter names or wrong validation.
# Implementation:
{code}

# Policy:
{policy}

# Database Schema:
{schema}
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
    
    
    if os.path.exists("alignment_tests/"):
        shutil.rmtree('/folder_name', ignore_errors=True)

    os.makedirs("alignment_tests/", exist_ok=True)
    for interface in range(5):
        all_codes = []
        path_interface = f"../envs/{env}/tools/interface_{interface}/"
        if not os.path.exists(path_interface):
            continue
        files = os.listdir(path_interface)
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(path_interface, file), "r") as f:
                    code = f.read()
                
                prompt_filled = prompt.format(code=code, policy=policy, schema=schema)
                all_codes.append(code)
                if not os.path.exists(f"alignment_tests/interface_{interface}/"):
                    os.makedirs(f"alignment_tests/interface_{interface}/", exist_ok=True)

                with open(f"alignment_tests/interface_{interface}/{file.replace('.py', '')}_review.txt", "w") as f:
                    f.write(prompt_filled)
                    
        with open(f"alignment_tests/interface_{interface}/all_code_interface_{interface}.txt", "w") as f:
            all_codes_joined = "\n\n# -----------------\n\n".join(all_codes)
            prompt_filled = prompt.format(code=all_codes_joined, policy=policy, schema=schema)
            f.write(prompt_filled)

main()