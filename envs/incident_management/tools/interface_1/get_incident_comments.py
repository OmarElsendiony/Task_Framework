import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetIncidentComments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, is_public: Optional[bool] = None) -> str:
        comments = data.get("incident_comments", {})
        results = []
        
        for comment in comments.values():
            if comment.get("incident_id") != incident_id:
                continue
            if is_public is not None and comment.get("is_public") != is_public:
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
                        "is_public": {"type": "boolean", "description": "Filter by public/private comments using boolean value (True for public, False for private)"}
                    },
                    "required": ["incident_id"]
                }
            }
        }
