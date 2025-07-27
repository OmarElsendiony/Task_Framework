import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool



class AddIncidentComment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, user_id: str, 
               comment_text: str, is_public: bool = True) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        comments = data.get("incident_comments", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        comment_id = generate_id(comments)
        timestamp = "2025-10-01T00:00:00"
        
        new_comment = {
            "incident_comment_id": comment_id,
            "incident_id": incident_id,
            "user_id": user_id,
            "comment_text": comment_text,
            "is_public": is_public,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        comments[str(comment_id)] = new_comment
        return json.dumps({"incident_comment_id": comment_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_incident_comment",
                "description": "Add a comment to an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "user_id": {"type": "string", "description": "ID of the user adding the comment"},
                        "comment_text": {"type": "string", "description": "Text of the comment"},
                        "is_public": {"type": "boolean", "description": "True if the comment is public, False if private"}
                    },
                    "required": ["incident_id", "user_id", "comment_text"]
                }
            }
        }
