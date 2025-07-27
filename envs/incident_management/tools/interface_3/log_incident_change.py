import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class LogIncidentChange(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, changed_by: str,
               incident_values: Optional[Dict] = None, task_values: Optional[Dict] = None) -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        tasks = data.get("tasks", {})
        incident_history = data.get("incident_history", {})
        if not incident_values and not task_values:
            raise ValueError("Either incident_values or task_values must be provided")

        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate user exists
        if str(changed_by) not in users:
            raise ValueError(f"User {changed_by} not found")
        
        # Get current incident data for old values
        current_incident = incidents[str(incident_id)]
        
        # Process incident values - capture old values and apply new ones
        processed_incident_values = {}
        if incident_values:
            for field, new_value in incident_values.items():
                old_value = current_incident.get(field)
                # If new_value is None, keep the old value
                actual_new_value = old_value if new_value is None else new_value
                processed_incident_values[field] = {
                    "old": old_value,
                    "new": actual_new_value
                }
                # Apply the new value to the incident
                current_incident[field] = actual_new_value
        
        # Process task values - capture old values and apply new ones
        # Structure: {"task_id": {"field_name": "new_value", ...}, ...}
        processed_task_values = {}
        if task_values:
            for task_id, task_changes in task_values.items():
                task_id_str = str(task_id)
                if task_id_str not in tasks:
                    raise ValueError(f"Task {task_id} not found")
                
                current_task = tasks[task_id_str]
                processed_task_values[task_id_str] = {}
                
                for field, new_value in task_changes.items():
                    if field not in current_task:
                        raise ValueError(f"Invalid field '{field}' for task {task_id}")
                    
                    old_value = current_task.get(field)
                    # If new_value is None, keep the old value
                    actual_new_value = old_value if new_value is None else new_value
                    processed_task_values[task_id_str][field] = {
                        "old": old_value,
                        "new": actual_new_value
                    }
                    # Apply the new value to the task
                    current_task[field] = actual_new_value
        
        history_id = generate_id(incident_history)
        timestamp = "2025-10-01T00:00:00"
        
        new_history = {
            "incident_history_id": str(history_id),
            "incident_id": incident_id,
            "changed_by": changed_by,
            "incident_values": processed_incident_values if processed_incident_values else None,
            "task_values": processed_task_values if processed_task_values else None,
            "changed_at": timestamp
        }
        
        incident_history[str(history_id)] = new_history
        return json.dumps(new_history)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_incident_change",
                "description": "Log a change to an incident in the history. Records both old and new values for incident and task changes. Incident values can include title, description, status, priority, assigned_to, category_id, subcategory_id, and department_id. Task values are organized by task ID, where each task can have changes to description, status, priority, assigned_to, and due_date. Only changes are logged using this API.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident"},
                        "changed_by": {"type": "string", "description": "ID of the user making the change"},
                        "incident_values": {
                            "type": "object", 
                            "description": "Object with incident field changes. Each field contains the new value to set. Structure: {'field_name': new_value}. Trackable fields: title, description, status (open/in_progress/resolved/closed), priority (low/medium/high/critical), assigned_to, category_id, subcategory_id, department_id",
                            "additionalProperties": True
                        },
                        "task_values": {
                            "type": "object", 
                            "description": "Object organizing task changes by task ID. Each task ID maps to an object of field changes. Structure: {'task_id': {'field_name': new_value, ...}, ...}. Trackable fields per task: description, status (todo/in_progress/blocked/done/cancelled), priority (low/medium/high/critical), assigned_to, due_date",
                            "properties": {
                                "task_id": {
                                    "type": "object",
                                    "description": "Task changes for a specific task ID",
                                    "properties": {
                                        "description": {"type": "string"},
                                        "status": {"type": "string", "enum": ["todo", "in_progress", "blocked", "done", "cancelled"]},
                                        "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                                        "assigned_to": {"type": "integer"},
                                        "due_date": {"type": "string", "format": "date-time"}
                                    }
                                }
                            },
                        }
                    },
                    "required": ["incident_id", "changed_by"]
                }
            }
        }
