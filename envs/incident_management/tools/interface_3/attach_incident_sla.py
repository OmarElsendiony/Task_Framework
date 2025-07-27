import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AttachIncidentSLA(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, sla_id: str,
               response_due: str, resolve_due: str, breached: bool = False,
               status: str = "Pending") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incident_slas = data.get("incident_sla", {})
        incidents = data.get("incidents", {})
        sla_policies = data.get("sla_policies", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate SLA policy exists
        if str(sla_id) not in sla_policies:
            raise ValueError(f"SLA policy {sla_id} not found")
        
        # Validate status
        valid_statuses = ["Pending", "Completed", "Cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Check if SLA is already attached to this incident
        for sla_record in incident_slas.values():
            if (sla_record.get("incident_id") == incident_id and 
                sla_record.get("sla_id") == sla_id):
                return json.dumps({"status": "already_attached", "incident_sla_id": sla_record.get("incident_sla_id")})
        
        incident_sla_id = generate_id(incident_slas)
        timestamp = "2025-10-01T00:00:00"
        
        new_incident_sla = {
            "incident_sla_id": incident_sla_id,
            "incident_id": incident_id,
            "sla_id": sla_id,
            "response_due": response_due,
            "resolve_due": resolve_due,
            "breached": breached,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        incident_slas[str(incident_sla_id)] = new_incident_sla
        return json.dumps({"incident_sla_id": incident_sla_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "attach_incident_sla",
                "description": "Attach an SLA policy to an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "sla_id": {"type": "string", "description": "ID of the SLA policy"},
                        "response_due": {"type": "string", "description": "Response due date in ISO format"},
                        "resolve_due": {"type": "string", "description": "Resolution due date in ISO format"},
                        "breached": {"type": "boolean", "description": "Whether the SLA is breached, defaults to false"},
                        "status": {"type": "string", "description": "SLA status (Pending, Completed, Cancelled), defaults to Pending"}
                    },
                    "required": ["incident_id", "sla_id", "response_due", "resolve_due"]
                }
            }
        }
