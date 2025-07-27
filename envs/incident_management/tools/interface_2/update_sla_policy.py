import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateSLAPolicy(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], sla_id: str, name: Optional[str] = None,
               priority: Optional[str] = None, category_id: Optional[str] = None,
               response_time: Optional[int] = None, resolve_time: Optional[int] = None) -> str:
        categories = data.get("categories", {})
        sla_policies = data.get("sla_policies", {})
        
        if str(sla_id) not in sla_policies:
            raise ValueError(f"SLA policy {sla_id} not found")
        
        # Validate category if provided
        if category_id and str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        # Validate priority if provided
        if priority:
            valid_priorities = ["low", "medium", "high", "critical"]
            if priority not in valid_priorities:
                raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
        sla = sla_policies[str(sla_id)]
        
        if name is not None:
            sla["name"] = name
        if priority is not None:
            sla["priority"] = priority
        if category_id is not None:
            sla["category_id"] = category_id
        if response_time is not None:
            sla["response_time"] = response_time
        if resolve_time is not None:
            sla["resolve_time"] = resolve_time
        
        sla["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(sla)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_sla_policy",
                "description": "Update an SLA policy",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sla_id": {"type": "string", "description": "ID of the SLA policy"},
                        "name": {"type": "string", "description": "New name for the SLA policy"},
                        "priority": {"type": "string", "description": "New priority (low, medium, high, critical)"},
                        "category_id": {"type": "string", "description": "New category ID"},
                        "response_time": {"type": "integer", "description": "New response time in minutes"},
                        "resolve_time": {"type": "integer", "description": "New resolve time in minutes"}
                    },
                    "required": ["sla_id"]
                }
            }
        }
