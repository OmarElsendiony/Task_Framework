import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCategoryByName(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str) -> str:
        categories = data.get("categories", {})
        for category in categories.values():
            if category.get("name", "").lower() == name.lower():
                return json.dumps(category)
        raise ValueError(f"Category '{name}' not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_category_by_name",
                "description": "Get category information by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name of the category"}
                    },
                    "required": ["name"]
                }
            }
        }
