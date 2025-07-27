import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateUserProfile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, first_name: Optional[str] = None,
               last_name: Optional[str] = None, email: Optional[str] = None,
               role: Optional[str] = None, timezone: Optional[str] = None,
               status: Optional[str] = None) -> str:
        users = data.get("users", {})
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        user = users[str(user_id)]
        
        # Validate role if provided
        if role:
            valid_roles = ["end_user", "agent", "manager", "admin"]
            if role not in valid_roles:
                raise ValueError(f"Invalid role. Must be one of {valid_roles}")
        
        # Validate status if provided
        if status:
            valid_statuses = ["active", "inactive"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate email uniqueness if provided
        if email:
            for uid, existing_user in users.items():
                if uid != str(user_id) and existing_user.get("email", "").lower() == email.lower():
                    raise ValueError(f"Email {email} is already in use")
        
        # Update fields if provided
        if first_name is not None:
            user["first_name"] = first_name
        if last_name is not None:
            user["last_name"] = last_name
        if email is not None:
            user["email"] = email
        if role is not None:
            user["role"] = role
        if timezone is not None:
            user["timezone"] = timezone
        if status is not None:
            user["status"] = status
        
        user["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user_profile",
                "description": "Update a user's profile information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to update"},
                        "first_name": {"type": "string", "description": "User's first name"},
                        "last_name": {"type": "string", "description": "User's last name"},
                        "email": {"type": "string", "description": "User's email address"},
                        "role": {"type": "string", "description": "User's role (end_user, agent, manager, admin)"},
                        "timezone": {"type": "string", "description": "User's timezone"},
                        "status": {"type": "string", "description": "User's status (active, inactive)"}
                    },
                    "required": ["user_id"]
                }
            }
        }
