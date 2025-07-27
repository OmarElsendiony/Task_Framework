import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateSubcategory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subcategory_id: str, name: str,
               category_id: Optional[str] = None) -> str:
        categories = data.get("categories", {})
        subcategories = data.get("subcategories", {})
        
        if str(subcategory_id) not in subcategories:
            raise ValueError(f"Subcategory {subcategory_id} not found")
        
        subcategory = subcategories[str(subcategory_id)]
        target_category_id = category_id or subcategory.get("category_id")
        
        # Validate category exists if changing
        if category_id and str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        # Check if another subcategory in the same category already has this name
        for sid, sub in subcategories.items():
            if (sid != str(subcategory_id) and 
                sub.get("category_id") == target_category_id and
                sub.get("name", "").lower() == name.lower()):
                raise ValueError(f"Subcategory '{name}' already exists in category {target_category_id}")
        
        subcategory["name"] = name
        if category_id:
            subcategory["category_id"] = category_id
        subcategory["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(subcategory)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_subcategory",
                "description": "Update a subcategory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subcategory_id": {"type": "string", "description": "ID of the subcategory"},
                        "name": {"type": "string", "description": "New name for the subcategory"},
                        "category_id": {"type": "string", "description": "New category ID (optional)"}
                    },
                    "required": ["subcategory_id", "name"]
                }
            }
        }
