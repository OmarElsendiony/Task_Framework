import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class CreateKBArticle(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], description: str, created_by: str,
               company_id: str, category_id: Optional[str] = None,
               subcategory_id: Optional[str] = None, 
               department_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        kb_articles = data.get("knowledge_base", {})
        users = data.get("users", {})
        companies = data.get("companies", {})
        categories = data.get("categories", {})
        subcategories = data.get("subcategories", {})
        departments = data.get("departments", {})
        
        # Validate required entities
        if str(created_by) not in users:
            raise ValueError(f"User {created_by} not found")
        
        if str(company_id) not in companies:
            raise ValueError(f"Company {company_id} not found")
        
        # Validate optional entities if provided
        if category_id and str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        if subcategory_id and str(subcategory_id) not in subcategories:
            raise ValueError(f"Subcategory {subcategory_id} not found")
        
        if department_id and str(department_id) not in departments:
            raise ValueError(f"Department {department_id} not found")
        
        kb_id = generate_id(kb_articles)
        timestamp = "2025-10-01T00:00:00"
        
        new_kb_article = {
            "knowledge_base_id": kb_id,
            "description": description,
            "created_by": created_by,
            "category_id": category_id,
            "subcategory_id": subcategory_id,
            "company_id": company_id,
            "department_id": department_id,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        kb_articles[str(kb_id)] = new_kb_article
        return json.dumps(new_kb_article)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_kb_article",
                "description": "Create a new knowledge base article",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string", "description": "Description of the knowledge base article"},
                        "created_by": {"type": "string", "description": "ID of the user creating the article"},
                        "company_id": {"type": "string", "description": "ID of the company"},
                        "category_id": {"type": "string", "description": "ID of the category"},
                        "subcategory_id": {"type": "string", "description": "ID of the subcategory"},
                        "department_id": {"type": "string", "description": "ID of the department"}
                    },
                    "required": ["description", "created_by", "company_id"]
                }
            }
        }
