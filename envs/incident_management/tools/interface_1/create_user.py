import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], first_name: str, last_name: str, email: str,
               role: str, company_id: str,
               department_id: Optional[str] = None, timezone: Optional[str] = None,
               status: str = "active") -> str:
        
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        companies = data.get("companies", {})
        
        # Validate company exists
        if str(company_id) not in companies:
            raise ValueError(f"Company {company_id} not found")
        
        # Validate department if provided
        if department_id:
            departments = data.get("departments", {})
            if str(department_id) not in departments:
                raise ValueError(f"Department {department_id} not found")
        
        # Check email uniqueness
        for user in users.values():
            if user.get("email", "").lower() == email.lower():
                raise ValueError(f"Email {email} already exists")
        
        # Validate role
        valid_roles = ["end_user", "agent", "manager", "admin"]
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of {valid_roles}")
        
        # Validate status
        valid_statuses = ["active", "inactive"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        user_id = generate_id(users)
        timestamp = "2025-10-01T00:00:00"
        
        new_user = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "role": role,
            "status": status,
            "timezone": timezone,
            "company_id": company_id,
            "department_id": department_id,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        users[str(user_id)] = new_user
        return json.dumps({"user_id": user_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user",
                "description": "Create a new user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string", "description": "User's first name"},
                        "last_name": {"type": "string", "description": "User's last name"},
                        "email": {"type": "string", "description": "User's email address (must be unique)"},
                        "role": {"type": "string", "description": "User role (end_user, agent, manager, admin)"},
                        "company_id": {"type": "string", "description": "ID of the company"},
                        "department_id": {"type": "string", "description": "Department ID"},
                        "timezone": {"type": "string", "description": "User's timezone"},
                        "status": {"type": "string", "description": "User status (active, inactive), defaults to active"},
                    },
                    "required": ["first_name", "last_name", "email", "role", "company_id", "password_hash"]
                }
            }
        }
