import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str) -> str:
        incidents = data.get("incidents", {})
        incident = incidents.get(incident_id)
        if not incident:
            raise ValueError(f"Incident {incident_id} not found")
        return json.dumps(incident)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_incident",
                "description": "Get incident information by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"}
                    },
                    "required": ["incident_id"]
                }
            }
        }
