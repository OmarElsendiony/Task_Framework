import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateKBArticle(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], knowledge_base_id: str, description: str) -> str:
        knowledge_base = data.get("knowledge_base", {})
        
        # Validate KB article exists
        if str(knowledge_base_id) not in knowledge_base:
            raise ValueError(f"Knowledge base article {knowledge_base_id} not found")
        
        # Update the article
        article = knowledge_base[str(knowledge_base_id)]
        article["description"] = description
        article["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(article)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_kb_article",
                "description": "Update a knowledge base article's description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "knowledge_base_id": {"type": "string", "description": "ID of the knowledge base article"},
                        "description": {"type": "string", "description": "New description for the article"}
                    },
                    "required": ["knowledge_base_id", "description"]
                }
            }
        }

