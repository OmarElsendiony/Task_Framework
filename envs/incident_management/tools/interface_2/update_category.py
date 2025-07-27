import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateCategory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], category_id: str, name: str) -> str:
        categories = data.get("categories", {})
        
        if str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        # Check if another category already has this name
        for cid, category in categories.items():
            if (cid != str(category_id) and 
                category.get("name", "").lower() == name.lower()):
                raise ValueError(f"Category '{name}' already exists")
        
        category = categories[str(category_id)]
        category["name"] = name
        category["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(category)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_category",
                "description": "Update a category name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category_id": {"type": "string", "description": "ID of the category"},
                        "name": {"type": "string", "description": "New name for the category"}
                    },
                    "required": ["category_id", "name"]
                }
            }
        }
