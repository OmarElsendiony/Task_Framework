import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ListUsersByFilters(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], company_id: Optional[str] = None,
               department_id: Optional[str] = None, role: Optional[str] = None,
               status: Optional[str] = None, email: Optional[str] = None,
               first_name: Optional[str] = None, last_name: Optional[str] = None) -> str:
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
            if first_name and first_name.lower() not in user.get("first_name", "").lower():
                continue
            if last_name and last_name.lower() not in user.get("last_name", "").lower():
                continue
            results.append(user)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_users_by_filters",
                "description": "Lists users based on provided filters. Returns all users if no filters are applied.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string", "description": "Filter by company ID"},
                        "department_id": {"type": "string", "description": "Filter by department ID"},
                        "role": {"type": "string", "description": "Filter by role (end_user, agent, manager, admin)"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive)"},
                        "email": {"type": "string", "description": "Filter by email address"},
                        "first_name": {"type": "string", "description": "Filter by first name (partial match)"},
                        "last_name": {"type": "string", "description": "Filter by last name (partial match)"}
                    },
                    "required": []
                }
            }
        }
