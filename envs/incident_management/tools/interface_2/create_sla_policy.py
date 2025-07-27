import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateSLAPolicy(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, priority: str, category_id: str,
               response_time: int, resolve_time: int) -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        categories = data.get("categories", {})
        sla_policies = data.get("sla_policies", {})
        
        # Validate category exists
        if str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        # Validate priority
        valid_priorities = ["low", "medium", "high", "critical"]
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
        sla_id = generate_id(sla_policies)
        timestamp = "2025-10-01T00:00:00"
        
        new_sla = {
            "sla_id": sla_id,
            "name": name,
            "priority": priority,
            "category_id": category_id,
            "response_time": response_time,
            "resolve_time": resolve_time,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        sla_policies[str(sla_id)] = new_sla
        return json.dumps(new_sla)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_sla_policy",
                "description": "Create a new SLA policy",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name of the SLA policy"},
                        "priority": {"type": "string", "description": "Priority level (low, medium, high, critical)"},
                        "category_id": {"type": "string", "description": "ID of the category"},
                        "response_time": {"type": "integer", "description": "Response time in minutes"},
                        "resolve_time": {"type": "integer", "description": "Resolve time in minutes"}
                    },
                    "required": ["name", "priority", "category_id", "response_time", "resolve_time"]
                }
            }
        }
