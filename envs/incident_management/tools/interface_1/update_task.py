import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateTask(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], task_id: str, description: Optional[str] = None,
               status: Optional[str] = None, priority: Optional[str] = None,
               assigned_to: Optional[str] = None, due_date: Optional[str] = None) -> str:
        tasks = data.get("tasks", {})
        task = tasks.get(str(task_id))
        
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Validate status if provided
        if status:
            valid_statuses = ["todo", "in_progress", "blocked", "done", "cancelled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate priority if provided
        if priority:
            valid_priorities = ["low", "medium", "high", "critical"]
            if priority not in valid_priorities:
                raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
        # Validate assigned user if provided
        if assigned_to:
            users = data.get("users", {})
            if str(assigned_to) not in users:
                raise ValueError(f"Assigned user {assigned_to} not found")
        
        # Update fields
        if description is not None:
            task["description"] = description
        if status is not None:
            task["status"] = status
        if priority is not None:
            task["priority"] = priority
        if assigned_to is not None:
            task["assigned_to"] = assigned_to
        if due_date is not None:
            task["due_date"] = due_date
        
        task["updated_at"] = "2025-10-01T00:00:00"
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
                        "description": {"type": "string", "description": "New description"},
                        "status": {"type": "string", "description": "New status (todo, in_progress, blocked, done, cancelled)"},
                        "priority": {"type": "string", "description": "New priority (low, medium, high, critical)"},
                        "assigned_to": {"type": "string", "description": "New assigned user ID"},
                        "due_date": {"type": "string", "description": "New due date in ISO format"}
                    },
                    "required": ["task_id"]
                }
            }
        }
