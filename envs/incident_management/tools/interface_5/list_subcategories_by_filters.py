import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class listSubcategoriesByFilters(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], category_id: Optional[str] = None,
               name: Optional[str] = None) -> str:
        subcategories = data.get("subcategories", {})
        results = []

        for subcategory in subcategories.values():
            if category_id and subcategory.get("category_id") != category_id:
                continue
            if name and name.lower() not in subcategory.get("name", "").lower():
                continue
            results.append(subcategory)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_subcategories_by_filters",
                "description": "Lists subcategories based on provided filters. Returns all subcategories if no filters are applied.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category_id": {"type": "string", "description": "Filter by category ID"},
                        "name": {"type": "string", "description": "Filter by subcategory name (partial match)"}
                    },
                    "required": []
                }
            }
        }
