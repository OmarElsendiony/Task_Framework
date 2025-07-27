import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class QuerySLAPolicies(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], priority: Optional[str] = None,
               category_id: Optional[str] = None, name: Optional[str] = None) -> str:
        sla_policies = data.get("sla_policies", {})
        results = []
        
        for policy in sla_policies.values():
            if priority and policy.get("priority") != priority:
                continue
            if category_id and policy.get("category_id") != category_id:
                continue
            if name and name.lower() not in policy.get("name", "").lower():
                continue
            results.append(policy)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "query_sla_policies",
                "description": "Query SLA policies with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "priority": {"type": "string", "description": "Filter by priority (low, medium, high, critical)"},
                        "category_id": {"type": "string", "description": "Filter by category ID"},
                        "name": {"type": "string", "description": "Filter by policy name (partial match)"}
                    },
                    "required": []
                }
            }
        }
