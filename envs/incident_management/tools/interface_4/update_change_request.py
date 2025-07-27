import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateChangeRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], change_request_id: int, 
               description: Optional[str] = None, status: Optional[str] = None,
               priority: Optional[str] = None, risk_level: Optional[str] = None,
               approved_by: Optional[int] = None, assigned_to: Optional[int] = None,
               scheduled_start: Optional[str] = None, scheduled_end: Optional[str] = None,
               affected_scope: Optional[Dict] = None) -> str:
        change_requests = data.get("change_requests", {})
        cr = change_requests.get(str(change_request_id))
        
        if not cr:
            raise ValueError(f"Change request {change_request_id} not found")
        
        # Validate status if provided
        if status:
            valid_statuses = ["draft", "submitted", "approved", "rejected", 
                            "in_progress", "implemented", "closed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate priority if provided
        if priority:
            valid_priorities = ["low", "medium", "high", "critical"]
            if priority not in valid_priorities:
                raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
        # Validate risk level if provided
        if risk_level:
            valid_risk_levels = ["low", "medium", "high"]
            if risk_level not in valid_risk_levels:
                raise ValueError(f"Invalid risk level. Must be one of {valid_risk_levels}")
        
        # Validate users if provided
        users = data.get("users", {})
        if approved_by and str(approved_by) not in users:
            raise ValueError(f"Approver user {approved_by} not found")
        if assigned_to and str(assigned_to) not in users:
            raise ValueError(f"Assigned user {assigned_to} not found")
        
        # Update fields
        if description is not None:
            cr["description"] = description
        if status is not None:
            cr["status"] = status
        if priority is not None:
            cr["priority"] = priority
        if risk_level is not None:
            cr["risk_level"] = risk_level
        if approved_by is not None:
            cr["approved_by"] = approved_by
        if assigned_to is not None:
            cr["assigned_to"] = assigned_to
        if scheduled_start is not None:
            cr["scheduled_start"] = scheduled_start
        if scheduled_end is not None:
            cr["scheduled_end"] = scheduled_end
        if affected_scope is not None:
            cr["affected_scope"] = affected_scope
        
        cr["updated_at"] = "2025-10-01T00:00:00"
        return json.dumps(cr)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_change_request",
                "description": "Update an existing change request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "change_request_id": {"type": "integer", "description": "ID of the change request to update"},
                        "description": {"type": "string", "description": "New description"},
                        "status": {"type": "string", "description": "New status (draft, submitted, approved, rejected, in_progress, implemented, closed)"},
                        "priority": {"type": "string", "description": "New priority (low, medium, high, critical)"},
                        "risk_level": {"type": "string", "description": "New risk level (low, medium, high)"},
                        "approved_by": {"type": "integer", "description": "ID of the approving user"},
                        "assigned_to": {"type": "integer", "description": "New assigned user ID"},
                        "scheduled_start": {"type": "string", "description": "New scheduled start time in ISO format"},
                        "scheduled_end": {"type": "string", "description": "New scheduled end time in ISO format"},
                        "affected_scope": {"type": "object", "description": "New affected scope JSON object"}
                    },
                    "required": ["change_request_id"]
                }
            }
        }
