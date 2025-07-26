import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FetchSubcategories(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], category_id: Optional[str] = None) -> str:
        subcategories = data.get("subcategories", {})
        results = []
        
        for subcategory in subcategories.values():
            if category_id and subcategory.get("category_id") != category_id:
                continue
            results.append(subcategory)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_subcategories",
                "description": "Fetch subcategories with optional category ID filter",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category_id": {"type": "string", "description": "Filter by category ID"}
                    },
                    "required": []
                }
            }
        }
