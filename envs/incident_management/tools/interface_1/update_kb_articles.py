import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateKbArticle(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], knowledge_base_id: str, 
               description: Optional[str] = None, category_id: Optional[str] = None,
               subcategory_id: Optional[str] = None, department_id: Optional[str] = None) -> str:
        kb_articles = data.get("knowledge_base", {})
        article = kb_articles.get(str(knowledge_base_id))
        
        if not article:
            raise ValueError(f"Knowledge base article {knowledge_base_id} not found")
        
        # Validate category if provided
        if category_id:
            categories = data.get("categories", {})
            if str(category_id) not in categories:
                raise ValueError(f"Category {category_id} not found")
        
        # Validate subcategory if provided
        if subcategory_id:
            subcategories = data.get("subcategories", {})
            if str(subcategory_id) not in subcategories:
                raise ValueError(f"Subcategory {subcategory_id} not found")
        
        # Validate department if provided
        if department_id:
            departments = data.get("departments", {})
            if str(department_id) not in departments:
                raise ValueError(f"Department {department_id} not found")
        
        # Update fields
        if description is not None:
            article["description"] = description
        if category_id is not None:
            article["category_id"] = category_id
        if subcategory_id is not None:
            article["subcategory_id"] = subcategory_id
        if department_id is not None:
            article["department_id"] = department_id
        
        article["updated_at"] = "2025-10-01T00:00:00"
        return json.dumps(article)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_kb_article",
                "description": "Update a knowledge base article",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "knowledge_base_id": {"type": "string", "description": "ID of the knowledge base article"},
                        "description": {"type": "string", "description": "New description"},
                        "category_id": {"type": "string", "description": "New category ID"},
                        "subcategory_id": {"type": "string", "description": "New subcategory ID"},
                        "department_id": {"type": "string", "description": "New department ID"}
                    },
                    "required": ["knowledge_base_id"]
                }
            }
        }
