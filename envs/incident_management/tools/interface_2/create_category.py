import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateCategory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str) -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        categories = data.get("categories", {})
        
        # Check if category already exists
        for category in categories.values():
            if str(category.get("name", "")).lower() == (str(name)).lower():
                raise ValueError(f"Category '{name}' already exists")
        
        category_id = generate_id(categories)
        timestamp = "2025-10-01T00:00:00"
        
        new_category = {
            "category_id": category_id,
            "name": name,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        categories[str(category_id)] = new_category
        return json.dumps(new_category)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_category",
                "description": "Create a new category",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name of the category"}
                    },
                    "required": ["name"]
                }
            }
        }
