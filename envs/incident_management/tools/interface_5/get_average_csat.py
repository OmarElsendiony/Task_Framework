import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class GetAverageCSAT(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], agent_id: Optional[str] = None,
               incident_id: Optional[str] = None) -> str:
        surveys = data.get("surveys", {})
        incidents = data.get("incidents", {})
        
        if not agent_id and not incident_id:
            raise ValueError("Either agent_id or incident_id must be provided")
        
        relevant_surveys = []
        
        if incident_id:
            # Get surveys for specific incident
            for survey in surveys.values():
                if survey.get("incident_id") == incident_id:
                    relevant_surveys.append(survey)
        
        elif agent_id:
            # Get surveys for incidents assigned to this agent
            agent_incident_ids = []
            for incident_id, incident in incidents.items():
                print("incident_id", incident.get("assigned_to"))
                print("agent_id", agent_id)
                print("="*10)
                if incident.get("assigned_to") == agent_id:
                    agent_incident_ids.append(incident_id)
            
            print("agent_incident_ids", agent_incident_ids)
            for survey in surveys.values():
                if survey.get("incident_id") in agent_incident_ids:
                    relevant_surveys.append(survey)
        
        if not relevant_surveys:
            return json.dumps({"average_csat": None, "total_surveys": 0})
        
        print("relevant", relevant_surveys)
        total_rating = sum(int(survey.get("rating", 0)) for survey in relevant_surveys)
        average_csat = total_rating / len(relevant_surveys)
        
        return json.dumps({
            "average_csat": round(average_csat, 2),
            "total_surveys": len(relevant_surveys)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_average_csat",
                "description": "Get average CSAT rating for an agent (across all incidents they've handled) or incident (across all surveys submitted for that incident). You must provide either agent_id or incident_id but not both.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string", "description": "ID of the agent"},
                        "incident_id": {"type": "string", "description": "ID of the incident"}
                    },
                    "required": []
                }
            }
        }
