import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetCompanyByName(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str) -> str:
        companies = data.get("companies", {})
        
        for company in companies.values():
            if company.get("name", "").lower() == name.lower():
                return json.dumps(company)
        
        raise json.dumps({})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_company_by_name",
                "description": "Get a company by its name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name of the company"}
                    },
                    "required": ["name"]
                }
            }
        }
