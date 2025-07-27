import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ListCompaniesByFilters(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], company_id: Optional[str] = None,
               name: Optional[str] = None, industry: Optional[str] = None,
               address: Optional[str] = None) -> str:
        companies = data.get("companies", {})
        results = []
        
        for company in companies.values():
            if company_id and company.get("company_id") != int(company_id):
                continue
            if name and name.lower() not in company.get("name", "").lower():
                continue
            if industry and industry.lower() not in company.get("industry", "").lower():
                continue
            if address and address.lower() not in company.get("address", "").lower():
                continue
            results.append(company)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_companies_by_filters",
                "description": "List companies with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string", "description": "Filter by company ID"},
                        "name": {"type": "string", "description": "Filter by company name (partial match)"},
                        "industry": {"type": "string", "description": "Filter by industry (partial match)"},
                        "address": {"type": "string", "description": "Filter by address (partial match)"}
                    },
                    "required": []
                }
            }
        }
