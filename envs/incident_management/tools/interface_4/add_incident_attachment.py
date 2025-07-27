import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool



class AddIncidentAttachment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, uploaded_by: str,
               file_name: str, file_url: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        attachments = data.get("incident_attachments", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate user exists
        if str(uploaded_by) not in users:
            raise ValueError(f"User {uploaded_by} not found")
        
        attachment_id = generate_id(attachments)
        timestamp = "2025-10-01T00:00:00"
        
        new_attachment = {
            "incident_attachment_id": attachment_id,
            "incident_id": incident_id,
            "uploaded_by": uploaded_by,
            "file_name": file_name,
            "file_url": file_url,
            "uploaded_at": timestamp,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        attachments[str(attachment_id)] = new_attachment
        return json.dumps({"incident_attachment_id": attachment_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_incident_attachment",
                "description": "Add an attachment to an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "uploaded_by": {"type": "string", "description": "ID of the user uploading the attachment"},
                        "file_name": {"type": "string", "description": "Name of the file"},
                        "file_url": {"type": "string", "description": "URL of the file"}
                    },
                    "required": ["incident_id", "uploaded_by", "file_name", "file_url"]
                }
            }
        }

