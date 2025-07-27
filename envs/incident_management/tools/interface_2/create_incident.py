import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], title: str, description: str, 
               reported_by: str, company_id: str, category_id: Optional[str] = None,
               subcategory_id: Optional[str] = None, assigned_to: Optional[str] = None,
               department_id: Optional[str] = None, priority: str = "medium",
               status: str = "open") -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        companies = data.get("companies", {})
        categories = data.get("categories", {})
        subcategories = data.get("subcategories", {})
        departments = data.get("departments", {})
        incidents = data.get("incidents", {})
        
        # Validate required entities
        if str(reported_by) not in users:
            raise ValueError(f"Reporter user {reported_by} not found")
        if str(company_id) not in companies:
            raise ValueError(f"Company {company_id} not found")
        
        # Validate optional entities
        if category_id and str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        if subcategory_id and str(subcategory_id) not in subcategories:
            raise ValueError(f"Subcategory {subcategory_id} not found")
        if assigned_to and str(assigned_to) not in users:
            raise ValueError(f"Assigned user {assigned_to} not found")
        if department_id and str(department_id) not in departments:
            raise ValueError(f"Department {department_id} not found")
        
        # Validate enums
        valid_priorities = ["low", "medium", "high", "critical"]
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
        valid_statuses = ["open", "in_progress", "resolved", "closed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        incident_id = generate_id(incidents)
        timestamp = "2025-10-01T00:00:00"
        
        new_incident = {
            "incident_id": incident_id,
            "title": title,
            "description": description,
            "category_id": category_id,
            "subcategory_id": subcategory_id,
            "reported_by": reported_by,
            "assigned_to": assigned_to,
            "department_id": department_id,
            "company_id": company_id,
            "status": status,
            "priority": priority,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        incidents[str(incident_id)] = new_incident
        return json.dumps(new_incident)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_incident",
                "description": "Create a new incident",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Title of the incident"},
                        "description": {"type": "string", "description": "Description of the incident"},
                        "reported_by": {"type": "string", "description": "ID of the user reporting the incident"},
                        "company_id": {"type": "string", "description": "ID of the company"},
                        "category_id": {"type": "string", "description": "ID of the category"},
                        "subcategory_id": {"type": "string", "description": "ID of the subcategory"},
                        "assigned_to": {"type": "string", "description": "ID of the assigned user"},
                        "department_id": {"type": "string", "description": "ID of the department"},
                        "priority": {"type": "string", "description": "Priority (low, medium, high, critical), defaults to medium"},
                        "status": {"type": "string", "description": "Status (open, in_progress, resolved, closed), defaults to open"}
                    },
                    "required": ["title", "description", "reported_by", "company_id"]
                }
            }
        }
