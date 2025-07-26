import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchSLAPolicies(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], category_id: Optional[str] = None, 
               priority: Optional[str] = None) -> str:
        sla_policies = data.get("sla_policies", {})
        results = []
        
        for policy in sla_policies.values():
            if category_id and policy.get("category_id") != category_id:
                continue
            if priority and policy.get("priority") != priority:
                continue
            results.append(policy)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_sla_policies",
                "description": "Fetch SLA policies with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category_id": {"type": "string", "description": "Filter by category ID"},
                        "priority": {"type": "string", "description": "Filter by priority (low, medium, high, critical)"}
                    },
                    "required": []
                }
            }
        }
