import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FetchDepartments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], company_id: Optional[str] = None) -> str:
        departments = data.get("departments", {})
        results = []
        
        for department in departments.values():
            if company_id and department.get("company_id") != company_id:
                continue
            results.append(department)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_departments",
                "description": "Fetch departments within a company",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string", "description": "Filter by company ID"}
                    },
                    "required": ["company_id"]
                }
            }
        }
