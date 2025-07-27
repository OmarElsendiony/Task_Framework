import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateUserProfile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, first_name: Optional[str] = None,
               last_name: Optional[str] = None, email: Optional[str] = None,
               timezone: Optional[str] = None, department_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        users = data.get("users", {})
        user = users.get(str(user_id))
        
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Check email uniqueness if updating email
        if email and email != user.get("email"):
            for other_user in users.values():
                if (other_user.get("email", "").lower() == email.lower() and 
                    other_user.get("user_id") != user_id):
                    raise ValueError(f"Email {email} already exists")
        
        # Validate department if provided
        if department_id:
            departments = data.get("departments", {})
            if str(department_id) not in departments:
                raise ValueError(f"Department {department_id} not found")
        
        # Validate status if provided
        if status:
            valid_statuses = ["active", "inactive"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Update fields
        if first_name is not None:
            user["first_name"] = first_name
        if last_name is not None:
            user["last_name"] = last_name
        if email is not None:
            user["email"] = email
        if timezone is not None:
            user["timezone"] = timezone
        if department_id is not None:
            user["department_id"] = department_id
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
                        "first_name": {"type": "string", "description": "New first name"},
                        "last_name": {"type": "string", "description": "New last name"},
                        "email": {"type": "string", "description": "New email address (must be unique)"},
                        "timezone": {"type": "string", "description": "New timezone"},
                        "department_id": {"type": "string", "description": "New department ID"},
                        "status": {"type": "string", "description": "New status (active, inactive)"}
                    },
                    "required": ["user_id"]
                }
            }
        }
