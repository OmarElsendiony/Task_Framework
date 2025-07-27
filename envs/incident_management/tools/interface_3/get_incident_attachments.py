import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetIncidentAttachments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, uploaded_by: Optional[str] = None) -> str:
        attachments = data.get("incident_attachments", {})
        incidents = data.get("incidents", {})
        results = []
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        for attachment in attachments.values():
            if attachment.get("incident_id") != incident_id:
                continue
            if uploaded_by and attachment.get("uploaded_by") != uploaded_by:
                continue
            results.append(attachment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_incident_attachments",
                "description": "Get attachments for a specific incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "uploaded_by": {"type": "string", "description": "Filter by user ID who uploaded the attachment"}
                    },
                    "required": ["incident_id"]
                }
            }
        }

