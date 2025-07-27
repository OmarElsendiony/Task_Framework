import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FilterChangeRequests(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], status: Optional[str] = None,
               priority: Optional[str] = None, risk_level: Optional[str] = None,
               assigned_to: Optional[str] = None, approved_by: Optional[str] = None,
               incident_id: Optional[str] = None, scheduled_start_from: Optional[str] = None,
               scheduled_start_to: Optional[str] = None) -> str:
        
        change_requests = data.get("change_requests", {})
        results = []
        
        # Parse date filters if provided
        start_from_datetime = None
        start_to_datetime = None
        
        if scheduled_start_from:
            try:
                start_from_datetime = datetime.fromisoformat(scheduled_start_from.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                pass
        
        if scheduled_start_to:
            try:
                start_to_datetime = datetime.fromisoformat(scheduled_start_to.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                pass
        
        for change_request in change_requests.values():
            # Apply filters
            if status and change_request.get("status") != status:
                continue
            if priority and change_request.get("priority") != priority:
                continue
            if risk_level and change_request.get("risk_level") != risk_level:
                continue
            if assigned_to and change_request.get("assigned_to") != assigned_to:
                continue
            if approved_by and change_request.get("approved_by") != approved_by:
                continue
            if incident_id and change_request.get("incident_id") != incident_id:
                continue
            
            # Apply date range filters
            if start_from_datetime or start_to_datetime:
                scheduled_start = change_request.get("scheduled_start")
                if scheduled_start:
                    try:
                        scheduled_datetime = datetime.fromisoformat(scheduled_start.replace('Z', '+00:00'))
                        
                        if start_from_datetime and scheduled_datetime < start_from_datetime:
                            continue
                        if start_to_datetime and scheduled_datetime > start_to_datetime:
                            continue
                    except (ValueError, AttributeError):
                        continue
                else:
                    # Skip records without scheduled_start when date filters are applied
                    if start_from_datetime or start_to_datetime:
                        continue
            
            results.append(change_request)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "filter_change_requests",
                "description": "Filter change requests with various criteria including date ranges",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Filter by status (draft, submitted, approved, rejected, in_progress, implemented, closed)"},
                        "priority": {"type": "string", "description": "Filter by priority (low, medium, high, critical)"},
                        "risk_level": {"type": "string", "description": "Filter by risk level (low, medium, high)"},
                        "assigned_to": {"type": "string", "description": "Filter by assigned user ID"},
                        "approved_by": {"type": "string", "description": "Filter by approver user ID"},
                        "incident_id": {"type": "string", "description": "Filter by linked incident ID"},
                        "scheduled_start_from": {"type": "string", "description": "Filter by scheduled start date from (ISO format)"},
                        "scheduled_start_to": {"type": "string", "description": "Filter by scheduled start date to (ISO format)"}
                    },
                    "required": []
                }
            }
        }

