import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ListLowRatedIncidents(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], company_id: str, threshold: Optional[int] = None) -> str:
        surveys = data.get("surveys", {})
        incidents = data.get("incidents", {})
        if not company_id:
            raise ValueError("Company ID must be provided")
        
        # Validate company_id exists
        if company_id not in data.get("companies", {}):
            raise ValueError(f"Company {company_id} not found")
        
        if threshold is None:
            threshold = 3  # Default threshold for low ratings
        
        # Group surveys by incident_id and calculate average rating
        incident_ratings = {}
        for survey in surveys.values():
            if incidents[survey.get("incident_id")].get("company_id") != company_id:
                continue
            
            incident_id = survey.get("incident_id")
            rating = survey.get("rating")
            
            if incident_id not in incident_ratings:
                incident_ratings[incident_id] = []
            incident_ratings[incident_id].append(rating)
        
        # Find incidents with average rating below threshold
        low_rated_incidents = []
        for incident_id, ratings in incident_ratings.items():
            if ratings:  # Ensure there are ratings
                avg_rating = sum(ratings) / len(ratings)
                if avg_rating <= threshold:
                    if str(incident_id) in incidents:
                        incident_data = incidents[str(incident_id)].copy()
                        incident_data["average_rating"] = round(avg_rating, 2)
                        incident_data["total_surveys"] = len(ratings)
                        low_rated_incidents.append(incident_data)
        
        return json.dumps(low_rated_incidents)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_low_rated_incidents",
                "description": "List incidents with low CSAT ratings within a company_id. Returns incidents with average rating below a specified threshold (default is 3).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string", "description": "ID of the company_id"},
                        "threshold": {"type": "integer", "description": "Rating threshold (incidents with average rating <= threshold will be returned). Defaults to 3"}
                    },
                    "required": ["company_id"]
                }
            }
        }

