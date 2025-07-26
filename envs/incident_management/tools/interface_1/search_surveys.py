import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class SearchSurveys(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: Optional[str] = None,
               user_id: Optional[int] = None, min_rating: Optional[int] = None) -> str:
        surveys = data.get("surveys", {})
        results = []
        
        for survey in surveys.values():
            if incident_id and survey.get("incident_id") != incident_id:
                continue
            if user_id and survey.get("user_id") != user_id:
                continue
            if min_rating and int(survey.get("rating", 0)) < int(min_rating):
                continue
            results.append(survey)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_surveys",
                "description": "Search surveys with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "integer", "description": "Filter by incident ID"},
                        "user_id": {"type": "integer", "description": "Filter by user ID"},
                        "min_rating": {"type": "integer", "description": "Filter by minimum rating"}
                    },
                    "required": []
                }
            }
        }
