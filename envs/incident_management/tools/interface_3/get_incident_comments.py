import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetIncidentComments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, is_public: Optional[bool] = None,
               user_id: Optional[str] = None) -> str:
        comments = data.get("incident_comments", {})
        incidents = data.get("incidents", {})
        results = []
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        for comment in comments.values():
            if comment.get("incident_id") != incident_id:
                continue
            if is_public is not None and comment.get("is_public") != is_public:
                continue
            if user_id and comment.get("user_id") != user_id:
                continue
            results.append(comment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_incident_comments",
                "description": "Get comments for a specific incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "is_public": {"type": "boolean", "description": "Filter by public/private comments. Takes True for public, False for private"},
                        "user_id": {"type": "string", "description": "Filter by user ID who made the comment"}
                    },
                    "required": ["incident_id"]
                }
            }
        }
