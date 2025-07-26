import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchBreachedIncidentSLAs(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], company_id: str) -> str:
        incident_slas = data.get("incident_sla", {})
        incidents = data.get("incidents", {})
        results = []
        
        if incident_slas:
            for sla in incident_slas.values():
                if sla.get("incident_id", {}) and sla.get("breached", False):
                    if sla["incident_id"] in incidents:
                        incident = incidents[sla["incident_id"]]
                        if incident.get("company_id", {}) == company_id:
                            results.append(sla)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_breached_incident_slas",
                "description": "Fetch all incident SLAs that have been breached within a specific company",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string", "description": "ID of the company to filter SLAs by"},
                    },
                    "required": ["company_id"]
                }
            }
        }
