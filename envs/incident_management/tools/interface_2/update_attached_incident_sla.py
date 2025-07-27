import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateAttachedIncidentSLA(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, sla_id: str,
               response_due: Optional[str] = None, resolve_due: Optional[str] = None,
               breached: Optional[bool] = None, status: Optional[str] = None) -> str:
        incident_slas = data.get("incident_sla", {})
        
        if str(incident_sla_id) not in incident_slas:
            raise ValueError(f"Incident SLA {incident_sla_id} not found")
        
        # Validate status if provided
        if status:
            valid_statuses = ["Pending", "Completed", "Cancelled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        
        sla = incident_slas[str(incident_sla_id)]
        timestamp = "2025-10-01T00:00:00"
        
        if response_due is not None:
            sla["response_due"] = response_due
        if resolve_due is not None:
            sla["resolve_due"] = resolve_due
        if breached is not None:
            sla["breached"] = breached
        if status is not None:
            sla["status"] = status
        
        sla["updated_at"] = timestamp
        
        return json.dumps(sla)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_attached_incident_sla",
                "description": "Update an attached incident SLA",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_sla_id": {"type": "string", "description": "ID of the incident SLA"},
                        "response_due": {"type": "string", "description": "Response due timestamp"},
                        "resolve_due": {"type": "string", "description": "Resolve due timestamp"},
                        "breached": {"type": "boolean", "description": "Whether SLA is breached. True if breached, False otherwise"},
                        "status": {"type": "string", "description": "SLA status (Pending, Completed, Cancelled)"}
                    },
                    "required": ["incident_id", "sla_id"]
                }
            }
        }
