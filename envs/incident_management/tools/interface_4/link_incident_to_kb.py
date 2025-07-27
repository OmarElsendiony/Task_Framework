import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class LinkIncidentToKb(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, knowledge_base_id: str) -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incidents = data.get("incidents", {})
        kb_articles = data.get("knowledge_base", {})
        incident_knowledge = data.get("incident_knowledge", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate KB article exists
        if str(knowledge_base_id) not in kb_articles:
            raise ValueError(f"Knowledge base article {knowledge_base_id} not found")
        
        # Check if link already exists
        for link in incident_knowledge.values():
            if (link.get("incident_id") == incident_id and 
                link.get("knowledge_base_id") == knowledge_base_id):
                return json.dumps({"status": "already_linked"})
        
        link_id = generate_id(incident_knowledge)
        timestamp = "2025-10-01T00:00:00"
        
        new_link = {
            "incident_id": incident_id,
            "knowledge_base_id": knowledge_base_id,
            "created_at": timestamp
        }
        
        incident_knowledge[str(link_id)] = new_link
        return json.dumps(new_link)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "link_incident_to_kb",
                "description": "Link an incident to a knowledge base article",
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
