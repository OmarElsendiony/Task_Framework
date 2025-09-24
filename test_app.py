import json
import random
from typing import Dict, List, Any

def generate_approvals_json(users_file: str, output_file: str = "approvals.json"):
    """
    Generate approvals JSON file based on users and their role privileges.
    Creates approval entries only for actions users are NOT authorized to perform directly.
    """
    
    # Define role authorization mapping (actions that can be performed WITHOUT approval)
    role_authorizations = {
        "compliance_officer": [],  # Most actions require approval even from compliance officers
        "fund_manager": [
            "trade_execution",  # Direct authorization for trade execution
        ],
        "finance_officer": [],  # Most actions require approval even from finance officers
        "trader": [
            "trade_execution"  # Direct authorization for trade execution
        ],
        "system_administrator": [
            "user_account_management", "system_monitoring"
        ]
    }
    
    # All possible actions in the system (updated to match policy)
    all_actions = [
        "investor_onboarding", "investor_offboarding",
        "fund_management_setup", "fund_management_maintenance",
        "subscription_management", "fund_switch", "commitments_create", 
        "commitments_fulfill", "trade_execution", "nav_valuation", 
        "redemption_processing", "document_intake_governance", "portfolio_creation", 
        "portfolio_update", "portfolio_holding_management", "instrument_creation", 
        "invoice_management", "payment_processing", "nav_record_creation", 
        "nav_record_updates", "instrument_price_updates", "reporting_performance", 
        "reporting_financial", "reporting_holding", "notification_management",
        "user_account_management", "system_monitoring", "entities_lookup"
    ]
    
    # Define actions requiring multiple approvers (AND logic)
    # Format: action -> list of required approver roles
    and_approval_actions = {
        "fund_management_setup": ["fund_manager", "compliance_officer"],
        "fund_management_maintenance": ["fund_manager", "compliance_officer"],
        "subscription_management": ["fund_manager", "compliance_officer"],
        "fund_switch": ["fund_manager", "compliance_officer"],
        "redemption_processing": ["compliance_officer", "finance_officer"],
        "instrument_creation": ["fund_manager", "compliance_officer"],
        "nav_record_updates": ["finance_officer", "fund_manager"],
        "instrument_price_updates": ["fund_manager", "compliance_officer"]
    }
    
    # Define actions allowing alternative approvers (OR logic)
    or_approval_actions = {
        "portfolio_creation": ["fund_manager", "finance_officer"]
    }
    
    # Define single approver actions
    single_approval_actions = {
        "investor_onboarding": "compliance_officer",
        "investor_offboarding": "compliance_officer", 
        "commitments_create": "compliance_officer",
        "commitments_fulfill": "compliance_officer",
        "nav_valuation": "finance_officer",
        "portfolio_update": "fund_manager",
        "portfolio_holding_management": "fund_manager",
        "invoice_management": "finance_officer",
        "payment_processing": "finance_officer", 
        "nav_record_creation": "finance_officer",
        "reporting_performance": "fund_manager",
        "reporting_financial": "fund_manager",
        "reporting_holding": "finance_officer",
        # Note: Following actions don't have clear approval requirements in policy
        # "document_intake_governance": "compliance_officer",  # Assumed
        # "notification_management": "system_administrator",   # Assumed  
        # "entities_lookup": "compliance_officer"              # Assumed
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
        approval_counter = 1
        
        # Process each user
        for user_id, user_info in users_data.items():
            user_role = user_info.get("role", "").lower()
            user_name = user_info.get("name", f"User {user_id}")
            
            # Get actions this role is authorized for
            authorized_actions = role_authorizations.get(user_role, [])
            
            # For each action, check if user needs approval
            for action in all_actions:
                # Check if user is directly authorized
                if action in authorized_actions:
                    continue  # Skip - user has direct authorization
                
                required_approvers = []
                
                # Determine required approvers based on action type
                if action in and_approval_actions:
                    # For AND actions, user needs approval from ALL specified roles (except their own)
                    required_approvers = [role for role in and_approval_actions[action] if role != user_role]
                elif action in or_approval_actions:
                    # For OR actions, user needs approval from ANY of the specified roles (except their own)
                    available_approvers = [role for role in or_approval_actions[action] if role != user_role]
                    if available_approvers:
                        # For OR logic, we still create entries for each possible approver
                        # but in practice, only one approval would be needed
                        required_approvers = available_approvers
                elif action in single_approval_actions:
                    # Single approver action
                    approver_role = single_approval_actions[action]
                    if approver_role != user_role:  # Don't require approval from own role
                        required_approvers = [approver_role]
                
                # Create approval entries
                if required_approvers:
                    for approver_role in required_approvers:
                        if users_by_role.get(approver_role):  # Only if approver role exists
                            approval_key = str(approval_counter)
                            approval_code = f"{action}_{user_id}"
                            approved_by_id = random.choice(users_by_role[approver_role])
                            
                            approvals[approval_key] = {
                                "code": approval_code,
                                "action": action,
                                "requester_id": user_id,
                                "requester_role": user_role,
                                "approved_by_id": approved_by_id,
                                "approved_by_role": approver_role,
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
        
        print("\nApprovals needed by requester role:")
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
    
    if approvals:
        print(f"\nDetailed breakdown:")
        print("Actions requiring AND approvals (all roles must approve):")
        and_actions = ["fund_management_setup", "fund_management_maintenance",
                      "subscription_management", "fund_switch", "redemption_processing", 
                      "instrument_creation", "nav_record_updates", "instrument_price_updates"]
        for action in and_actions:
            print(f"  {action}")
        
        print("\nActions requiring OR approvals (any one role can approve):")
        or_actions = ["portfolio_creation"]
        for action in or_actions:
            print(f"  {action}")
        
        print(f"\nFirst few approval entries:")
        for i, (key, approval) in enumerate(list(approvals.items())[:3]):
            print(f"  {key}: {approval}")