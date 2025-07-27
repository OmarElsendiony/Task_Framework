import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetIncidentHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, changed_by: Optional[str] = None) -> str:
        history = data.get("incident_history", {})
        incidents = data.get("incidents", {})
        results = []
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        for record in history.values():
            if record.get("incident_id") != incident_id:
                continue
            if changed_by and record.get("changed_by") != changed_by:
                continue
            results.append(record)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_incident_history",
                "description": "Get history records for a specific incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "changed_by": {"type": "string", "description": "Filter by user ID who made the change"}
                    },
                    "required": ["incident_id"]
                }
            }
        }

