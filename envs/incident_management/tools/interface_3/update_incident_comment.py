import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateIncidentComment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_comment_id: str, 
               comment_text: Optional[str] = None, is_public: Optional[bool] = None) -> str:
        
        comments = data.get("incident_comments", {})
        
        # Validate comment exists
        if str(incident_comment_id) not in comments:
            raise ValueError(f"Incident comment {incident_comment_id} not found")
        
        comment = comments[str(incident_comment_id)]
        timestamp = "2025-10-01T00:00:00"
        
        # Update fields if provided
        if comment_text is not None:
            comment["comment_text"] = comment_text
        if is_public is not None:
            comment["is_public"] = is_public
        
        comment["updated_at"] = timestamp
        
        return json.dumps(comment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_incident_comment",
                "description": "Update an existing incident comment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_comment_id": {"type": "string", "description": "ID of the comment to update"},
                        "comment_text": {"type": "string", "description": "New comment text"},
                        "is_public": {"type": "boolean", "description": "New public/private status (True for public, False for private)"}
                    },
                    "required": ["incident_comment_id"]
                }
            }
        }
