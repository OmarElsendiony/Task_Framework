import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class QueryIncidentSLAs(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], company_id, incident_id: Optional[str] = None,
               sla_id: Optional[str] = None, status: Optional[str] = None) -> str:
        incident_slas = data.get("incident_sla", {})
        incidents = data.get("incidents", {})
        company_incidents_ids = [incident_k for incident_k, incident_v in incidents.items() if incident_v.get("company_id") == company_id]
        results = []

        if not company_incidents_ids:
            return json.dumps(results)

        
        for sla in incident_slas.values():
            if sla_id and sla.get("sla_id") != sla_id:
                continue

            if sla.get("incident_id") not in company_incidents_ids:
                continue

            if incident_id and (sla.get("incident_id") != incident_id or sla.get("incident_id") not in company_incidents_ids):
                # print(f"Skipping SLA {sla.get('sla_id')} for incident {sla.get('incident_id')}, not in company {company_id}")
                # print(f"Incident IDs in company {company_id}: {company_incidents_ids}")
                continue
            
            if sla_id and sla.get("sla_id") != sla_id:
                continue
            
            if sla.get("status") and status and sla.get("status") != status:
                continue
            
            results.append(sla)


        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "query_incident_slas",
                "description": "Fetch incident SLAs of a company with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string", "description": "Filter by company ID"},
                        "incident_id": {"type": "string", "description": "Filter by incident ID"},
                        "sla_id": {"type": "string", "description": "Filter by SLA policy ID"},
                        "status": {"type": "string", "description": "Filter by status (Pending, Completed, Cancelled)"}
                    },
                    "required": ["company_id"]
                }
            }
        }
