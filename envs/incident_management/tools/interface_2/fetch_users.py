import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class FetchUsers(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        company_id: Optional[str] = None,
        department_id: Optional[str] = None,
        role: Optional[str] = None,
        status: Optional[str] = None,
        timezone: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> str:
        users = data.get("users", {})
        results = []

        for user in users.values():
            if company_id and str(user.get("company_id")) != str(company_id):
                continue
            if department_id and str(user.get("department_id")) != str(department_id):
                continue
            if role and user.get("role") != role:
                continue
            if status and user.get("status") != status:
                continue
            if timezone and user.get("timezone") != timezone:
                continue
            if email and user.get("email") != email:
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
                "name": "fetch_users",
                "description": "Fetch users with optional filters like company ID, department ID, role, status, timezone, email, first name, and last name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string", "description": "Filter by company ID"},
                        "department_id": {"type": "string", "description": "Filter by department ID"},
                        "role": {"type": "string", "enum": ["end_user", "agent", "manager", "admin"], "description": "Filter by role"},
                        "status": {"type": "string", "enum": ["active", "inactive"], "description": "Filter by status"},
                        "timezone": {"type": "string", "description": "Filter by timezone"},
                        "email": {"type": "string", "description": "Filter by email"},
                        "first_name": {"type": "string", "description": "Filter by first name (substring, case-insensitive)"},
                        "last_name": {"type": "string", "description": "Filter by last name (substring, case-insensitive)"},
                    },
                    "required": []
                }
            }
        }
