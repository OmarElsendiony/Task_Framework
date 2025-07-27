import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, title: Optional[str] = None,
               description: Optional[str] = None, status: Optional[str] = None,
               priority: Optional[str] = None, assigned_to: Optional[str] = None,
               category_id: Optional[str] = None, subcategory_id: Optional[str] = None) -> str:
        incidents = data.get("incidents", {})
        incident = incidents.get(str(incident_id))
        
        if not incident:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate status if provided
        if status:
            valid_statuses = ["open", "in_progress", "resolved", "closed"]
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
        
        # Validate category if provided
        if category_id:
            categories = data.get("categories", {})
            if str(category_id) not in categories:
                raise ValueError(f"Category {category_id} not found")
        
        # Validate subcategory if provided
        if subcategory_id:
            subcategories = data.get("subcategories", {})
            if str(subcategory_id) not in subcategories:
                raise ValueError(f"Subcategory {subcategory_id} not found")
        
        # Update fields
        if title is not None:
            incident["title"] = title
        if description is not None:
            incident["description"] = description
        if status is not None:
            incident["status"] = status
        if priority is not None:
            incident["priority"] = priority
        if assigned_to is not None:
            incident["assigned_to"] = assigned_to
        if category_id is not None:
            incident["category_id"] = category_id
        if subcategory_id is not None:
            incident["subcategory_id"] = subcategory_id
        
        incident["updated_at"] = "2025-10-01T00:00:00"
        return json.dumps(incident)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_incident",
                "description": "Update an existing incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "ID of the incident to update"},
                        "title": {"type": "string", "description": "New title"},
                        "description": {"type": "string", "description": "New description"},
                        "status": {"type": "string", "description": "New status (open, in_progress, resolved, closed)"},
                        "priority": {"type": "string", "description": "New priority (low, medium, high, critical)"},
                        "assigned_to": {"type": "string", "description": "New assigned user ID"},
                        "category_id": {"type": "string", "description": "New category ID"},
                        "subcategory_id": {"type": "string", "description": "New subcategory ID"}
                    },
                    "required": ["incident_id"]
                }
            }
        }
