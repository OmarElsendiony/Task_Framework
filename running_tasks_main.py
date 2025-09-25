from running_tasks import *


# env_interface(environment="fund_finance", interface="1")


def run_all_tasks():
    with open('task.json', 'r') as f:
        task_data = json.load(f)
    
    environment = task_data.get("env")
    interface = task_data.get("interface_num")
    env_interface(environment=environment, interface=interface)
    for action in task_data.get("task", []).get("actions", []):
        # print(f"Running task: {action.get('name')}")
        res = execute_api(api_name=action.get("name"), arguments=action.get("arguments", {}))
        # print(f"Result from task {action.get('name')}: {res}\n")
        # print(res[0].values())
        if "error" in res[0].keys():
            print(f"Error encountered in task {action.get('name')}, stopping further execution.\n")
            break
        # print(f"Completed task: {action.get('name')}\n")

run_all_tasks()


# arguments = {
#     "legal_name": "Alpha Capital",
#     "source_of_funds": "retained_earnings",
#     "contact_email": "frf@exrfefwadmple.com",
#     "accreditation_status": "accredited",
#     "compliance_officer_approval": "True"
# }

# execute_api(environment="fund_finance", interface="1", api_name="create_investor", arguments=arguments)

# arguments = {
#     "legal_name": "Alpha Capital",
#     "source_of_funds": "retained_earnings",
#     "contact_email": "frf@lol.com",
#     "accreditation_status": "accredited",
#     "compliance_officer_approval": "True"
# }

# # print("Current investors:", session["data"].get("investors", {}))
# execute_api(environment="fund_finance", interface="1", api_name="create_investor", arguments=arguments)