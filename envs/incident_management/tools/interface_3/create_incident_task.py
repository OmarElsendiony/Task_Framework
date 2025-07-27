import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool



class CreateIncidentTask(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, description: str,
               assigned_to: str, priority: str = "medium", 
               due_date: Optional[str] = None, status: str = "todo") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        tasks = data.get("tasks", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate assigned user exists
        if str(assigned_to) not in users:
            raise ValueError(f"Assigned user {assigned_to} not found")
        
        # Validate priority
        valid_priorities = ["low", "medium", "high", "critical"]
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
        # Validate status
        valid_statuses = ["todo", "in_progress", "blocked", "done", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        task_id = generate_id(tasks)
        timestamp = "2025-10-01T00:00:00"
        
        new_task = {
            "task_id": task_id,
            "incident_id": incident_id,
            "description": description,
            "assigned_to": assigned_to,
            "status": status,
            "priority": priority,
            "due_date": due_date,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        tasks[str(task_id)] = new_task
        return json.dumps({"task_id": task_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_incident_task",
                "description": "Create a new task for an incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "description": {"type": "string", "description": "Task description"},
                        "assigned_to": {"type": "string", "description": "ID of the user assigned to the task"},
                        "priority": {"type": "string", "description": "Task priority (low, medium, high, critical), defaults to medium"},
                        "due_date": {"type": "string", "description": "Due date in ISO format (optional)"},
                        "status": {"type": "string", "description": "Task status (todo, in_progress, blocked, done, cancelled), defaults to todo"}
                    },
                    "required": ["incident_id", "description", "assigned_to"]
                }
            }
        }
