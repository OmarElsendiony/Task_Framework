import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetIncidentTasks(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: int, assigned_to: Optional[int] = None,
               status: Optional[str] = None) -> str:
        tasks = data.get("tasks", {})
        results = []
        
        for task in tasks.values():
            if task.get("incident_id") != incident_id:
                continue
            if assigned_to and task.get("assigned_to") != assigned_to:
                continue
            if status and task.get("status") != status:
                continue
            results.append(task)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_incident_tasks",
                "description": "Get tasks for a specific incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "integer", "description": "ID of the incident"},
                        "assigned_to": {"type": "integer", "description": "Filter by assigned user ID"},
                        "status": {"type": "string", "description": "Filter by task status (todo, in_progress, blocked, done, cancelled)"}
                    },
                    "required": ["incident_id"]
                }
            }
        }
