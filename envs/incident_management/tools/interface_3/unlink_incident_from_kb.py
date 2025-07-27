import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UnlinkIncidentFromKB(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, knowledge_base_id: str) -> str:
        incidents = data.get("incidents", {})
        kb_articles = data.get("knowledge_base", {})
        incident_knowledge = data.get("incident_knowledge", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate KB article exists
        if str(knowledge_base_id) not in kb_articles:
            raise ValueError(f"Knowledge base article {knowledge_base_id} not found")
        
        # Find and remove the link
        link_to_remove = None
        for link_id, link in incident_knowledge.items():
            if (link.get("incident_id") == incident_id and 
                link.get("knowledge_base_id") == knowledge_base_id):
                link_to_remove = link_id
                break
        
        if link_to_remove is None:
            raise ValueError(f"Link between incident {incident_id} and KB article {knowledge_base_id} not found")
        
        removed_link = incident_knowledge.pop(link_to_remove)
        return json.dumps({"status": "unlinked", "removed_link": removed_link})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "unlink_incident_from_kb",
                "description": "Remove a link between an incident and a knowledge base article",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "knowledge_base_id": {"type": "string", "description": "ID of the knowledge base article"}
                    },
                    "required": ["incident_id", "knowledge_base_id"]
                }
            }
        }
