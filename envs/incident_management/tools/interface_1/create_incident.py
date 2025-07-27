import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], title: str, description: str, reported_by: str,
               company_id: str, priority: str = "medium", category_id: Optional[str] = None,
               subcategory_id: Optional[str] = None, assigned_to: Optional[str] = None,
               department_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        companies = data.get("companies", {})
        
        # Validate reporter exists
        if str(reported_by) not in users:
            raise ValueError(f"Reporter user {reported_by} not found")
        
        # Validate company exists
        if str(company_id) not in companies:
            raise ValueError(f"Company {company_id} not found")
        
        # Validate assigned user if provided
        if assigned_to and str(assigned_to) not in users:
            raise ValueError(f"Assigned user {assigned_to} not found")
        
        # Validate priority
        valid_priorities = ["low", "medium", "high", "critical"]
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
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
        
        # Validate department if provided
        if department_id:
            departments = data.get("departments", {})
            if str(department_id) not in departments:
                raise ValueError(f"Department {department_id} not found")
        
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
            "status": "open",
            "priority": priority,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        incidents[str(incident_id)] = new_incident
        return json.dumps({"incident_id": incident_id})

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
                        "title": {"type": "string", "description": "Incident title"},
                        "description": {"type": "string", "description": "Detailed description"},
                        "reported_by": {"type": "string", "description": "ID of the user reporting the incident"},
                        "company_id": {"type": "string", "description": "ID of the company"},
                        "priority": {"type": "string", "description": "Priority level (low, medium, high, critical), defaults to medium"},
                        "category_id": {"type": "string", "description": "Category ID"},
                        "subcategory_id": {"type": "string", "description": "Subcategory ID"},
                        "assigned_to": {"type": "string", "description": "ID of the user assigned to handle the incident"},
                        "department_id": {"type": "string", "description": "Department ID"}
                    },
                    "required": ["title", "description", "reported_by", "company_id"]
                }
            }
        }
