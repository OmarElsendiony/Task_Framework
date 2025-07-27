import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class QueryChangeRequests(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], company_id: Optional[str], incident_id: Optional[str] = None,
               assigned_to: Optional[str] = None, approved_by: Optional[str] = None,
               status: Optional[str] = None, priority: Optional[str] = None,
               risk_level: Optional[str] = None) -> str:
        change_requests = data.get("change_requests", {})
        companies = data.get("companies", {})
        incidents = data.get("incidents", {})
        results = []
        
        for change_request in change_requests.values():
            if incident_id and company_id and incidents.get(incident_id, {}).get("company_id") != company_id:
                continue
            if incident_id and change_request.get("incident_id") != incident_id:
                continue
            if assigned_to and change_request.get("assigned_to") != assigned_to:
                continue
            if approved_by and change_request.get("approved_by") != approved_by:
                continue
            if status and change_request.get("status") != status:
                continue
            if priority and change_request.get("priority") != priority:
                continue
            if risk_level and change_request.get("risk_level") != risk_level:
                continue
            results.append(change_request)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "query_change_requests",
                "description": "Query change requests within a company with optional filters. Returns all change requests for the specified company if no filters are applied.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string", "description": "Filter by company ID"},
                        "incident_id": {"type": "string", "description": "Filter by incident ID"},
                        "assigned_to": {"type": "string", "description": "Filter by assigned user ID"},
                        "approved_by": {"type": "string", "description": "Filter by approver user ID"},
                        "status": {"type": "string", "description": "Filter by status (draft, submitted, approved, rejected, in_progress, implemented, closed)"},
                        "priority": {"type": "string", "description": "Filter by priority (low, medium, high, critical)"},
                        "risk_level": {"type": "string", "description": "Filter by risk level (low, medium, high)"}
                    },
                    "required": ["company_id"]
                }
            }
        }
