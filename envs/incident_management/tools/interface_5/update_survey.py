import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateSurvey(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], survey_id: str, rating: int,
               feedback_text: Optional[str] = None) -> str:
        surveys = data.get("surveys", {})
        
        # Validate survey exists
        if str(survey_id) not in surveys:
            raise ValueError(f"Survey {survey_id} not found")
        
        # Validate rating range (assuming 1-5 scale)
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        # Update the survey
        survey = surveys[str(survey_id)]
        survey["rating"] = rating
        survey["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(survey)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_survey",
                "description": "Update an existing survey's rating and feedback",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "survey_id": {"type": "string", "description": "ID of the survey to update"},
                        "rating": {"type": "integer", "description": "New rating (1-5 scale)"},
                        "feedback_text": {"type": "string", "description": "Optional new feedback text"}
                    },
                    "required": ["survey_id", "rating"]
                }
            }
        }
