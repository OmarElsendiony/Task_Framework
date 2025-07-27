import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetOverdueChangeRequests(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], current_date: Optional[str] = None,
               status: Optional[str] = None, priority: Optional[str] = None,
               assigned_to: Optional[str] = None) -> str:
        
        change_requests = data.get("change_requests", {})
        results = []
        
        # Use provided current_date or default to a fixed date
        if current_date is None:
            current_date = "2025-10-01T00:00:00"
        
        current_datetime = datetime.fromisoformat(current_date.replace('Z', '+00:00'))
        
        for change_request in change_requests.values():
            # Skip change requests without scheduled_end dates
            if not change_request.get("scheduled_end"):
                continue
            
            # Parse scheduled end date
            try:
                end_datetime = datetime.fromisoformat(change_request["scheduled_end"].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                continue
            
            # Check if change request is overdue (past scheduled_end)
            if end_datetime >= current_datetime:
                continue
            
            # Apply filters
            if status and change_request.get("status") != status:
                continue
            if priority and change_request.get("priority") != priority:
                continue
            if assigned_to and change_request.get("assigned_to") != assigned_to:
                continue
            
            results.append(change_request)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_overdue_change_requests",
                "description": "Get change requests that are overdue based on their scheduled end date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "current_date": {"type": "string", "description": "Current date in ISO format for comparison, defaults to 2025-10-01T00:00:00Z"},
                        "status": {"type": "string", "description": "Filter by status (draft, submitted, approved, rejected, in_progress, implemented, closed)"},
                        "priority": {"type": "string", "description": "Filter by priority (low, medium, high, critical)"},
                        "assigned_to": {"type": "string", "description": "Filter by assigned user ID"}
                    },
                    "required": []
                }
            }
        }
