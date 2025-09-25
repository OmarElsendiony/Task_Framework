import json
import random
from typing import Dict, List, Any

def generate_approvals_json(users_file: str, output_file: str = "approvals.json"):
    """
    Generate approvals JSON file based on users and their role privileges.
    Creates approval entries only for actions users are NOT authorized to perform directly.
    """
    
    # Define role authorization mapping
    role_authorizations = {
        "compliance_officer": [
            "investor_onboarding", "investor_offboarding", "subscription_management", 
            "commitments_create", "commitments_fulfill", "redemption_processing"
        ],
        "fund_manager": [
            "fund_management_setup", "fund_management_maintenance", "trade_execution", 
            "portfolio_creation", "portfolio_update", "portfolio_holding_management", 
            "instrument_creation", "nav_record_updates", "instrument_price_updates",
            "reporting_performance", "reporting_financial"
        ],
        "finance_officer": [
            "nav_valuation", "subscription_management", "redemption_processing", 
            "portfolio_creation", "invoice_management", "payment_processing", 
            "nav_record_creation", "nav_record_updates", "reporting_holding"
        ],
        "trader": [
            "trade_execution"
        ],
        "system_administrator": [
            "user_account_management", "system_monitoring"
        ]
    }
    
    # All possible actions in the system
    all_actions = [
        "investor_onboarding", "investor_offboarding", "fund_management_setup", 
        "fund_management_maintenance", "subscription_management", "commitments_create", 
        "commitments_fulfill", "trade_execution", "nav_valuation", "redemption_processing", 
        "portfolio_creation", "portfolio_update", "portfolio_holding_management", 
        "instrument_creation", "instrument_update", "invoice_management", "payment_processing", 
        "nav_record_creation", "nav_record_updates", "instrument_price_updates", 
        "reporting_performance", "reporting_financial", "reporting_holding", 
        "user_account_management", "system_monitoring"
    ]
    
    # Define actions requiring multiple approvers (AND logic)
    and_approval_actions = {
        "fund_management_setup": ["fund_manager", "compliance_officer"],
        "fund_management_maintenance": ["fund_manager", "compliance_officer"],
        "redemption_processing": ["compliance_officer", "finance_officer"],
        "instrument_creation": ["fund_manager", "compliance_officer"],
        "instrument_update": ["fund_manager", "compliance_officer"],
        "nav_record_updates": ["finance_officer", "fund_manager"],
        "instrument_price_updates": ["fund_manager", "compliance_officer"]
    }
    
    # Define actions allowing alternative approvers (OR logic)
    or_approval_actions = {
        "subscription_management": ["compliance_officer", "finance_officer"],
        "portfolio_creation": ["fund_manager", "finance_officer"]
    }
    
    try:
        # Read users file
        with open(users_file, 'r') as f:
            users_data = json.load(f)
        
        # Group users by role for random selection of approvers
        users_by_role = {}
        for user_id, user_info in users_data.items():
            role = user_info.get("role", "").lower()
            if role not in users_by_role:
                users_by_role[role] = []
            users_by_role[role].append(user_id)
        
        approvals = {}
        approval_counter = 2926  # Start from ID 2926
        
        # Process each user
        for user_id, user_info in users_data.items():
            user_role = user_info.get("role", "").lower()
            user_name = user_info.get("name", f"User {user_id}")
            
            # Get actions this role is authorized for
            authorized_actions = role_authorizations.get(user_role, [])
            
            # Focus only on instrument_update action
            action = "instrument_update"
            needs_approval = False
            required_approvers = []
            
            # Check if user is directly authorized for instrument_update
            if action in authorized_actions:
                continue  # Skip - user has direct authorization
            
            # instrument_update requires both fund_manager and compliance_officer approval
            required_approvers = ["fund_manager", "compliance_officer"]
            needs_approval = True
            if needs_approval and required_approvers:
                # Create approval entry for each required approver
                for approver_role in required_approvers:
                    approval_key = str(approval_counter)
                    approval_code = f"{action}_{user_id}"
                    approved_by_id = random.choice(users_by_role.get(approver_role, [])) if users_by_role.get(approver_role) else "N/A"
                    approvals[approval_key] = {
                        "code": approval_code,
                        "requester_id": user_id,
                        "requester_role": user_role,
                        "approved_by_id": approved_by_id,
                        "approved_by": approver_role,
                        # "approval_status": "pending",
                        # "created_date": "2025-10-01T12:00:00Z"
                    }
                    
                    approval_counter += 1
        
        # Write approvals to file
        with open(output_file, 'w') as f:
            json.dump({"approvals": approvals}, f, indent=2)
        
        print(f"Generated {len(approvals)} approval entries in {output_file}")
        print(f"Processed {len(users_data)} users")
        
        # Summary by role
        role_summary = {}
        for approval in approvals.values():
            role = approval["requester_role"]
            role_summary[role] = role_summary.get(role, 0) + 1
        
        print("\nApprovals needed by role:")
        for role, count in role_summary.items():
            print(f"  {role}: {count} approval entries")
        
        return approvals
        
    except FileNotFoundError:
        print(f"Error: Users file '{users_file}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in users file - {e}")
        return None
    except Exception as e:
        print(f"Error generating approvals: {e}")
        return None

# Example usage and test
if __name__ == "__main__":
    # Generate approvals
    approvals = generate_approvals_json("users.json", "approvals.json")
    
    # if approvals:
    #     print(f"\nSample approval entry:")
    #     first_key = list(approvals.keys())[0]
    #     print(json.dumps({first_key: approvals[first_key]}, indent=2))