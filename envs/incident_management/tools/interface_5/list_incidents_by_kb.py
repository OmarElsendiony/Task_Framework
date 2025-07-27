import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ListIncidentsByKB(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], knowledge_base_id: str) -> str:
        incident_knowledge = data.get("incident_knowledge", {})
        incidents = data.get("incidents", {})
        results = []
        
        # Find all incidents linked to this knowledge base article
        linked_incident_ids = []
        for link in incident_knowledge.values():
            if link.get("knowledge_base_id") == knowledge_base_id:
                linked_incident_ids.append(link.get("incident_id"))
        
        # Get the actual incident records
        for incident_id in linked_incident_ids:
            if str(incident_id) in incidents:
                results.append(incidents[str(incident_id)])
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_incidents_by_kb",
                "description": "List all incidents linked to a specific knowledge base article",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "knowledge_base_id": {"type": "string", "description": "ID of the knowledge base article"}
                    },
                    "required": ["knowledge_base_id"]
                }
            }
        }
