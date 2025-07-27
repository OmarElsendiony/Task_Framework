import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ListSurveysByFilters(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: Optional[str] = None,
               user_id: Optional[str] = None, rating: Optional[int] = None,
               survey_id: Optional[str] = None) -> str:
        surveys = data.get("surveys", {})
        results = []
        
        for survey in surveys.values():
            if incident_id and survey.get("incident_id") != incident_id:
                continue
            if user_id and survey.get("user_id") != user_id:
                continue
            if rating and survey.get("rating") != rating:
                continue
            if survey_id and survey.get("survey_id") != int(survey_id):
                continue
            results.append(survey)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_surveys_by_filters",
                "description": "List surveys with optional filters.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "Filter by incident ID"},
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "rating": {"type": "integer", "description": "Filter by rating"},
                        "survey_id": {"type": "string", "description": "Filter by survey ID"}
                    },
                    "required": []
                }
            }
        }
