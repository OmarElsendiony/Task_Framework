import json

with open('approvals.json', 'r') as f:
    approvals_data = json.load(f)
    
with open('approvals_2.json', 'r') as f:
    approvals_data_2 = json.load(f)

# Merge the two dictionaries
approvals_data_2.update(approvals_data)

with open('approvals3.json', 'w') as f:
    json.dump(approvals_data_2, f, indent=2)