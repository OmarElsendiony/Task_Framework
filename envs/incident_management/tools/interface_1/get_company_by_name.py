import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

# Utility function to generate IDs
def generate_id(table: Dict[str, Any]) -> int:
    if not table:
        return 1
    return max(int(k) for k in table.keys()) + 1


class GetCompanyByName(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str) -> str:
        companies = data.get("companies", {})
        for company in companies.values():
            if company.get("name", "").lower() == name.lower():
                return json.dumps(company)
        raise ValueError(f"Company '{name}' not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_company_by_name",
                "description": "Get company information by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "The name of the company to look up"}
                    },
                    "required": ["name"]
                }
            }
        }
