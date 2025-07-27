import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool



class UpdateTask(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], task_id: str, description: Optional[str] = None,
               assigned_to: Optional[str] = None, status: Optional[str] = None,
               priority: Optional[str] = None, due_date: Optional[str] = None) -> str:
        
        tasks = data.get("tasks", {})
        users = data.get("users", {})
        
        # Validate task exists
        if str(task_id) not in tasks:
            raise ValueError(f"Task {task_id} not found")
        
        # Validate assigned user if provided
        if assigned_to and str(assigned_to) not in users:
            raise ValueError(f"Assigned user {assigned_to} not found")
        
        # Validate enum values if provided
        if status:
            valid_statuses = ["todo", "in_progress", "blocked", "done", "cancelled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        if priority:
            valid_priorities = ["low", "medium", "high", "critical"]
            if priority not in valid_priorities:
                raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
        task = tasks[str(task_id)]
        timestamp = "2025-10-01T00:00:00"
        
        # Update fields if provided
        if description is not None:
            task["description"] = description
        if assigned_to is not None:
            task["assigned_to"] = assigned_to
        if status is not None:
            task["status"] = status
        if priority is not None:
            task["priority"] = priority
        if due_date is not None:
            task["due_date"] = due_date
        
        task["updated_at"] = timestamp
        
        return json.dumps(task)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update an existing task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "ID of the task to update"},
                        "description": {"type": "string", "description": "New task description"},
                        "assigned_to": {"type": "string", "description": "New assigned user ID"},
                        "status": {"type": "string", "description": "New status (todo, in_progress, blocked, done, cancelled)"},
                        "priority": {"type": "string", "description": "New priority (low, medium, high, critical)"},
                        "due_date": {"type": "string", "description": "New due date in ISO format"}
                    },
                    "required": ["task_id"]
                }
            }
        }

