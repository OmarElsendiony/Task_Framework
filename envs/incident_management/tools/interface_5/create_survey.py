
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateSurvey(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, user_id: str,
               rating: int) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        surveys = data.get("surveys", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        # Validate rating range (assuming 1-5 scale)
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        survey_id = generate_id(surveys)
        timestamp = "2025-10-01T00:00:00"
        
        new_survey = {
            "survey_id": survey_id,
            "incident_id": incident_id,
            "user_id": user_id,
            "rating": rating,
            "submitted_at": timestamp,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        surveys[str(survey_id)] = new_survey
        return json.dumps(new_survey)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_survey",
                "description": "Create a new survey for an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "user_id": {"type": "string", "description": "ID of the user submitting the survey"},
                        "rating": {"type": "integer", "description": "Rating (1-5 scale)"},
                    },
                    "required": ["incident_id", "user_id", "rating"]
                }
            }
        }
