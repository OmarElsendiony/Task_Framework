import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateSubcategory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], category_id: str, name: str) -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        categories = data.get("categories", {})
        subcategories = data.get("subcategories", {})
        
        # Validate category exists
        if str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        # Check if subcategory already exists in this category
        for subcategory in subcategories.values():
            if (subcategory.get("category_id") == category_id and 
                subcategory.get("name", "").lower() == name.lower()):
                raise ValueError(f"Subcategory '{name}' already exists in category {category_id}")
        
        subcategory_id = generate_id(subcategories)
        timestamp = "2025-10-01T00:00:00"
        
        new_subcategory = {
            "subcategory_id": subcategory_id,
            "category_id": category_id,
            "name": name,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        subcategories[str(subcategory_id)] = new_subcategory
        return json.dumps(new_subcategory)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_subcategory",
                "description": "Create a new subcategory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category_id": {"type": "string", "description": "ID of the parent category"},
                        "name": {"type": "string", "description": "Name of the subcategory"}
                    },
                    "required": ["category_id", "name"]
                }
            }
        }
