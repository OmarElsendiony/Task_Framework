import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ListKBArticlesByFilters(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], company_id,
               department_id: Optional[str] = None, category_id: Optional[str] = None,
               subcategory_id: Optional[str] = None, created_by: Optional[str] = None,
               description: Optional[str] = None) -> str:
        kb_articles = data.get("knowledge_base", {})
        results = []

        for article in kb_articles.values():
            if company_id and article.get("company_id") != company_id:
                continue
            if department_id and article.get("department_id") != department_id:
                continue
            if category_id and article.get("category_id") != category_id:
                continue
            if subcategory_id and article.get("subcategory_id") != subcategory_id:
                continue
            if created_by and article.get("created_by") != created_by:
                continue
            if description and description.lower() not in article.get("description", "").lower():
                continue
            results.append(article)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_kb_articles_by_filters",
                "description": "List knowledge base articles with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string", "description": "Filter by company ID"},
                        "department_id": {"type": "string", "description": "Filter by department ID"},
                        "category_id": {"type": "string", "description": "Filter by category ID"},
                        "subcategory_id": {"type": "string", "description": "Filter by subcategory ID"},
                        "created_by": {"type": "string", "description": "Filter by creator user ID"},
                        "description": {"type": "string", "description": "Filter by description (partial match)"}
                    },
                    "required": ["company_id"]
                }
            }
        }
