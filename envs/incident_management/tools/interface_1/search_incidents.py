import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SearchIncidents(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], company_id: Optional[str] = None,
               department_id: Optional[str] = None, assigned_to: Optional[str] = None,
               reported_by: Optional[str] = None, status: Optional[str] = None,
               priority: Optional[str] = None, category_id: Optional[str] = None) -> str:
        incidents = data.get("incidents", {})
        results = []
        
        for incident in incidents.values():
            if company_id and incident.get("company_id") != company_id:
                continue
            if department_id and incident.get("department_id") != department_id:
                continue
            if assigned_to and incident.get("assigned_to") != assigned_to:
                continue
            if reported_by and incident.get("reported_by") != reported_by:
                continue
            if status and incident.get("status") != status:
                continue
            if priority and incident.get("priority") != priority:
                continue
            if category_id and incident.get("category_id") != category_id:
                continue
            results.append(incident)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_incidents",
                "description": "Retrieve incidents that match the specified filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string", "description": "Filter by company ID"},
                        "department_id": {"type": "string", "description": "Filter by department ID"},
                        "assigned_to": {"type": "string", "description": "Filter by assigned user ID"},
                        "reported_by": {"type": "string", "description": "Filter by reporter user ID"},
                        "status": {"type": "string", "description": "Filter by status (open, in_progress, resolved, closed)"},
                        "priority": {"type": "string", "description": "Filter by priority (low, medium, high, critical)"},
                        "category_id": {"type": "string", "description": "Filter by category ID"}
                    },
                    "required": []
                }
            }
        }
