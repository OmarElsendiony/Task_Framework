import json
from datetime import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class FilterOverdueTasks(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], current_date: Optional[str] = None,
               assigned_to: Optional[str] = None, incident_id: Optional[str] = None,
               priority: Optional[str] = None, status: Optional[str] = None) -> str:
        
        tasks = data.get("tasks", {})
        results = []
        
        # Use provided current_date or default to a fixed date
        if current_date is None:
            current_date = "2025-10-01T00:00:00"
        
        current_datetime = datetime.fromisoformat(current_date.replace('Z', '+00:00'))
        
        for task in tasks.values():
            # Skip tasks without due dates
            if not task.get("due_date"):
                continue
            
            # Parse due date
            try:
                due_datetime = datetime.fromisoformat(task["due_date"].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                continue
            
            # Check if task is overdue
            if due_datetime >= current_datetime:
                continue
            
            # Apply filters
            if assigned_to and task.get("assigned_to") != assigned_to:
                continue
            if incident_id and task.get("incident_id") != incident_id:
                continue
            if priority and task.get("priority") != priority:
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
                "name": "filter_overdue_tasks",
                "description": "Filter and retrieve overdue tasks based on due date and optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "current_date": {"type": "string", "description": "Current date in ISO format for comparison, defaults to 2025-10-01T00:00:00Z"},
                        "assigned_to": {"type": "string", "description": "Filter by assigned user ID"},
                        "incident_id": {"type": "string", "description": "Filter by incident ID"},
                        "priority": {"type": "string", "description": "Filter by priority (low, medium, high, critical)"},
                        "status": {"type": "string", "description": "Filter by status (todo, in_progress, blocked, done, cancelled)"}
                    },
                    "required": []
                }
            }
        }
