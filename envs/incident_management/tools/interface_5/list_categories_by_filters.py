import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ListCategoriesByFilters(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], category_id: Optional[str] = None,
               name: Optional[str] = None) -> str:
        categories = data.get("categories", {})
        results = []
        
        for category in categories.values():
            if category_id and category.get("category_id") != int(category_id):
                continue
            if name and name.lower() not in category.get("name", "").lower():
                continue
            results.append(category)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_categories_by_filters",
                "description": "List categories with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category_id": {"type": "string", "description": "Filter by category ID"},
                        "name": {"type": "string", "description": "Filter by category name (partial match)"}
                    },
                    "required": []
                }
            }
        }
