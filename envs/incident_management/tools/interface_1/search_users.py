import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SearchUsers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], company_id: Optional[str] = None, 
               department_id: Optional[str] = None, role: Optional[str] = None,
               status: Optional[str] = None, email: Optional[str] = None) -> str:
        users = data.get("users", {})
        results = []
        
        for user in users.values():
            if company_id and user.get("company_id") != company_id:
                continue
            if department_id and user.get("department_id") != department_id:
                continue
            if role and user.get("role") != role:
                continue
            if status and user.get("status") != status:
                continue
            if email and user.get("email", "").lower() != email.lower():
                continue
            results.append(user)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_users",
                "description": "Search users with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string", "description": "Filter by company ID"},
                        "department_id": {"type": "string", "description": "Filter by department ID"},
                        "role": {"type": "string", "description": "Filter by role (end_user, agent, manager, admin)"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive)"},
                        "email": {"type": "string", "description": "Filter by email address"}
                    },
                    "required": []
                }
            }
        }
