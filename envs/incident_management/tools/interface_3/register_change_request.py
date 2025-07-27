import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RegisterChangeRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], assigned_to: str, description: str,
               priority: str = "medium", risk_level: str = "low",
               incident_id: Optional[str] = None, affected_scope: Optional[Dict] = None,
               scheduled_start: Optional[str] = None, scheduled_end: Optional[str] = None) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        change_requests = data.get("change_requests", {})
        users = data.get("users", {})
        
        # Validate assigned user exists
        if str(assigned_to) not in users:
            raise ValueError(f"Assigned user {assigned_to} not found")
        
        # Validate incident if provided
        if incident_id:
            incidents = data.get("incidents", {})
            if str(incident_id) not in incidents:
                raise ValueError(f"Incident {incident_id} not found")
        
        # Validate priority
        valid_priorities = ["low", "medium", "high", "critical"]
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
        # Validate risk level
        valid_risk_levels = ["low", "medium", "high"]
        if risk_level not in valid_risk_levels:
            raise ValueError(f"Invalid risk level. Must be one of {valid_risk_levels}")
        
        cr_id = generate_id(change_requests)
        timestamp = "2025-10-01T00:00:00"
        
        new_cr = {
            "change_request_id": cr_id,
            "incident_id": incident_id,
            "assigned_to": assigned_to,
            "approved_by": None,
            "description": description,
            "status": "draft",
            "priority": priority,
            "risk_level": risk_level,
            "affected_scope": affected_scope,
            "scheduled_start": scheduled_start,
            "scheduled_end": scheduled_end,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        change_requests[str(cr_id)] = new_cr
        return json.dumps(new_cr)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "register_change_request",
                "description": "Register a new change request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "assigned_to": {"type": "string", "description": "ID of the user assigned to the change request"},
                        "description": {"type": "string", "description": "Description of the change request"},
                        "priority": {"type": "string", "description": "Priority level (low, medium, high, critical), defaults to medium"},
                        "risk_level": {"type": "string", "description": "Risk level (low, medium, high), defaults to low"},
                        "incident_id": {"type": "string", "description": "Linked incident ID (optional)"},
                        "affected_scope": {"type": "object", "description": "JSON object describing affected scope"},
                        "scheduled_start": {"type": "string", "description": "Scheduled start time in ISO format"},
                        "scheduled_end": {"type": "string", "description": "Scheduled end time in ISO format"}
                    },
                    "required": ["assigned_to", "description"]
                }
            }
        }
