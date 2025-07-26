import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SearchChangeRequests(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: Optional[str] = None,
               assigned_to: Optional[str] = None, status: Optional[str] = None,
               priority: Optional[str] = None, risk_level: Optional[str] = None) -> str:
        change_requests = data.get("change_requests", {})
        results = []
        
        for cr in change_requests.values():
            if incident_id and cr.get("incident_id") != incident_id:
                continue
            if assigned_to and cr.get("assigned_to") != assigned_to:
                continue
            if status and cr.get("status") != status:
                continue
            if priority and cr.get("priority") != priority:
                continue
            if risk_level and cr.get("risk_level") != risk_level:
                continue
            results.append(cr)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_change_requests",
                "description": "Search change requests with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "Filter by incident ID"},
                        "assigned_to": {"type": "string", "description": "Filter by assigned user ID"},
                        "status": {"type": "string", "description": "Filter by status (draft, submitted, approved, rejected, in_progress, implemented, closed)"},
                        "priority": {"type": "string", "description": "Filter by priority (low, medium, high, critical)"},
                        "risk_level": {"type": "string", "description": "Filter by risk level (low, medium, high)"}
                    },
                    "required": []
                }
            }
        }
