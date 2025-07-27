import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ListIncidentsByFilters(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], company_id: Optional[str] = None,
               department_id: Optional[str] = None, status: Optional[str] = None,
               priority: Optional[str] = None, assigned_to: Optional[str] = None,
               reported_by: Optional[str] = None, category_id: Optional[str] = None,
               subcategory_id: Optional[str] = None) -> str:
        incidents = data.get("incidents", {})
        results = []
        
        for incident in incidents.values():
            if company_id and incident.get("company_id") != company_id:
                continue
            if department_id and incident.get("department_id") != department_id:
                continue
            if status and incident.get("status") != status:
                continue
            if priority and incident.get("priority") != priority:
                continue
            if assigned_to and incident.get("assigned_to") != assigned_to:
                continue
            if reported_by and incident.get("reported_by") != reported_by:
                continue
            if category_id and incident.get("category_id") != category_id:
                continue
            if subcategory_id and incident.get("subcategory_id") != subcategory_id:
                continue
            results.append(incident)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_incidents_by_filters",
                "description": "Lists incidents based on provided filters. Returns all incidents if no filters are applied.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string", "description": "Filter by company ID"},
                        "department_id": {"type": "string", "description": "Filter by department ID"},
                        "status": {"type": "string", "description": "Filter by status (open, in_progress, resolved, closed)"},
                        "priority": {"type": "string", "description": "Filter by priority (low, medium, high, critical)"},
                        "assigned_to": {"type": "string", "description": "Filter by assigned user ID"},
                        "reported_by": {"type": "string", "description": "Filter by reporter user ID"},
                        "category_id": {"type": "string", "description": "Filter by category ID"},
                        "subcategory_id": {"type": "string", "description": "Filter by subcategory ID"}
                    },
                    "required": ["company_id"]
                }
            }
        }
