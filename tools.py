from typing import Any, Dict
from typing import Any, Dict, Optional
import json

class Tools:
    @staticmethod
    def fetch_sla_policies_invoke(data: Dict[str, Any], category_id: Optional[str] = None, 
               priority: Optional[str] = None) -> str:
        sla_policies = data.get("sla_policies", {})
        results = []
        
        for policy in sla_policies.values():
            if category_id and policy.get("category_id") != category_id:
                continue
            if priority and policy.get("priority") != priority:
                continue
            results.append(policy)
        
        return json.dumps(results)

    @staticmethod
    def create_subcategory_invoke(data: Dict[str, Any], category_id: str, name: str) -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        categories = data.get("categories", {})
        subcategories = data.get("subcategories", {})
        
        # Validate category exists
        if str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        # Check if subcategory already exists in this category
        for subcategory in subcategories.values():
            if (subcategory.get("category_id") == category_id and 
                subcategory.get("name", "").lower() == name.lower()):
                raise ValueError(f"Subcategory '{name}' already exists in category {category_id}")
        
        subcategory_id = generate_id(subcategories)
        timestamp = "2025-10-01T00:00:00Z"
        
        new_subcategory = {
            "subcategory_id": subcategory_id,
            "category_id": category_id,
            "name": name,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        subcategories[str(subcategory_id)] = new_subcategory
        return json.dumps(new_subcategory)

    @staticmethod
    def create_incident_invoke(data: Dict[str, Any], title: str, description: str, 
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
        timestamp = "2025-10-01T00:00:00Z"
        
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
    def get_incident_comments_invoke(data: Dict[str, Any], incident_id: str, is_public: Optional[bool] = None) -> str:
        comments = data.get("incident_comments", {})
        results = []
        
        for comment in comments.values():
            if comment.get("incident_id") != incident_id:
                continue
            if is_public is not None and comment.get("is_public") != is_public:
                continue
            results.append(comment)
        
        return json.dumps(results)

    @staticmethod
    def create_sla_policy_invoke(data: Dict[str, Any], name: str, priority: str, category_id: str,
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
        timestamp = "2025-10-01T00:00:00Z"
        
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
    def fetch_breached_incident_slas_invoke(data: Dict[str, Any], company_id: str) -> str:
        incident_slas = data.get("incident_sla", {})
        incidents = data.get("incidents", {})
        results = []
        
        if incident_slas:
            for sla in incident_slas.values():
                if sla.get("incident_id", {}) and sla.get("breached", False):
                    if sla["incident_id"] in incidents:
                        incident = incidents[sla["incident_id"]]
                        if incident.get("company_id", {}) == company_id:
                            results.append(sla)
        
        return json.dumps(results)

    @staticmethod
    def fetch_users_invoke(
        data: Dict[str, Any],
        company_id: Optional[str] = None,
        department_id: Optional[str] = None,
        role: Optional[str] = None,
        status: Optional[str] = None,
        timezone: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> str:
        users = data.get("users", {})
        results = []

        for user in users.values():
            if company_id and str(user.get("company_id")) != str(company_id):
                continue
            if department_id and str(user.get("department_id")) != str(department_id):
                continue
            if role and user.get("role") != role:
                continue
            if status and user.get("status") != status:
                continue
            if timezone and user.get("timezone") != timezone:
                continue
            if email and user.get("email") != email:
                continue
            if first_name and first_name.lower() not in user.get("first_name", "").lower():
                continue
            if last_name and last_name.lower() not in user.get("last_name", "").lower():
                continue
            results.append(user)

        return json.dumps(results)

    @staticmethod
    def get_company_by_name_invoke(data: Dict[str, Any], name: str) -> str:
        companies = data.get("companies", {})
        
        for company in companies.values():
            if company.get("name", "").lower() == name.lower():
                return json.dumps(company)
        
        raise json.dumps({})

    @staticmethod
    def create_category_invoke(data: Dict[str, Any], name: str) -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        categories = data.get("categories", {})
        
        # Check if category already exists
        for category in categories.values():
            if str(category.get("name", "")).lower() == (str(name)).lower():
                raise ValueError(f"Category '{name}' already exists")
        
        category_id = generate_id(categories)
        timestamp = "2025-10-01T00:00:00Z"
        
        new_category = {
            "category_id": category_id,
            "name": name,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        categories[str(category_id)] = new_category
        return json.dumps(new_category)

    @staticmethod
    def fetch_departments_invoke(data: Dict[str, Any], company_id: Optional[str] = None) -> str:
        departments = data.get("departments", {})
        results = []
        
        for department in departments.values():
            if company_id and department.get("company_id") != company_id:
                continue
            results.append(department)
        
        return json.dumps(results)

    @staticmethod
    def fetch_incident_slas_invoke(data: Dict[str, Any], incident_id: Optional[str] = None, 
               sla_id: Optional[str] = None, status: Optional[str] = None) -> str:
        incident_slas = data.get("incident_sla", {})
        results = []
        
        for sla in incident_slas.values():
            if incident_id and sla.get("incident_id") != incident_id:
                continue
            if sla_id and sla.get("sla_id") != sla_id:
                continue
            if status and sla.get("status") != status:
                continue
            results.append(sla)
        
        return json.dumps(results)

    @staticmethod
    def fetch_incidents_invoke(data: Dict[str, Any], company_id: Optional[str] = None,
               department_id: Optional[str] = None, assigned_to: Optional[str] = None,
               status: Optional[str] = None, priority: Optional[str] = None,
               category_id: Optional[str] = None) -> str:
        incidents = data.get("incidents", {})
        results = []
        
        for incident in incidents.values():
            if company_id and incident.get("company_id") != company_id:
                continue
            if department_id and incident.get("department_id") != department_id:
                continue
            if assigned_to and incident.get("assigned_to") != assigned_to:
                continue
            if status and incident.get("status") != status:
                continue
            if priority and incident.get("priority") != priority:
                continue
            if category_id and incident.get("category_id") != category_id:
                continue
            results.append(incident)
        
        return json.dumps(results)

    @staticmethod
    def update_sla_policy_invoke(data: Dict[str, Any], sla_id: str, name: Optional[str] = None,
               priority: Optional[str] = None, category_id: Optional[str] = None,
               response_time: Optional[int] = None, resolve_time: Optional[int] = None) -> str:
        categories = data.get("categories", {})
        sla_policies = data.get("sla_policies", {})
        
        if str(sla_id) not in sla_policies:
            raise ValueError(f"SLA policy {sla_id} not found")
        
        # Validate category if provided
        if category_id and str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        # Validate priority if provided
        if priority:
            valid_priorities = ["low", "medium", "high", "critical"]
            if priority not in valid_priorities:
                raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
        sla = sla_policies[str(sla_id)]
        
        if name is not None:
            sla["name"] = name
        if priority is not None:
            sla["priority"] = priority
        if category_id is not None:
            sla["category_id"] = category_id
        if response_time is not None:
            sla["response_time"] = response_time
        if resolve_time is not None:
            sla["resolve_time"] = resolve_time
        
        sla["updated_at"] = "2025-10-01T00:00:00Z"
        
        return json.dumps(sla)

    @staticmethod
    def fetch_subcategories_invoke(data: Dict[str, Any], category_id: Optional[str] = None) -> str:
        subcategories = data.get("subcategories", {})
        results = []
        
        for subcategory in subcategories.values():
            if category_id and subcategory.get("category_id") != category_id:
                continue
            results.append(subcategory)
        
        return json.dumps(results)

    @staticmethod
    def get_category_by_name_invoke(data: Dict[str, Any], name: str) -> str:
        categories = data.get("categories", {})
        
        for category in categories.values():
            if category.get("name", "").lower() == name.lower():
                return json.dumps(category)
        
        return json.dumps({})

    @staticmethod
    def update_category_invoke(data: Dict[str, Any], category_id: str, name: str) -> str:
        categories = data.get("categories", {})
        
        if str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        # Check if another category already has this name
        for cid, category in categories.items():
            if (cid != str(category_id) and 
                category.get("name", "").lower() == name.lower()):
                raise ValueError(f"Category '{name}' already exists")
        
        category = categories[str(category_id)]
        category["name"] = name
        category["updated_at"] = "2025-10-01T00:00:00Z"
        
        return json.dumps(category)

    @staticmethod
    def log_incident_change_invoke(data: Dict[str, Any], incident_id: str, changed_by: str,
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
        timestamp = "2025-10-01T00:00:00Z"
        
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
    def update_subcategory_invoke(data: Dict[str, Any], subcategory_id: str, name: str,
               category_id: Optional[str] = None) -> str:
        categories = data.get("categories", {})
        subcategories = data.get("subcategories", {})
        
        if str(subcategory_id) not in subcategories:
            raise ValueError(f"Subcategory {subcategory_id} not found")
        
        subcategory = subcategories[str(subcategory_id)]
        target_category_id = category_id or subcategory.get("category_id")
        
        # Validate category exists if changing
        if category_id and str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        # Check if another subcategory in the same category already has this name
        for sid, sub in subcategories.items():
            if (sid != str(subcategory_id) and 
                sub.get("category_id") == target_category_id and
                sub.get("name", "").lower() == name.lower()):
                raise ValueError(f"Subcategory '{name}' already exists in category {target_category_id}")
        
        subcategory["name"] = name
        if category_id:
            subcategory["category_id"] = category_id
        subcategory["updated_at"] = "2025-10-01T00:00:00Z"
        
        return json.dumps(subcategory)

    @staticmethod
    def update_attached_incident_sla_invoke(data: Dict[str, Any], incident_id: str, sla_id: str,
               response_due: Optional[str] = None, resolve_due: Optional[str] = None,
               breached: Optional[bool] = None, status: Optional[str] = None) -> str:
        incident_slas = data.get("incident_sla", {})
        
        if str(incident_sla_id) not in incident_slas:
            raise ValueError(f"Incident SLA {incident_sla_id} not found")
        
        # Validate status if provided
        if status:
            valid_statuses = ["Pending", "Completed", "Cancelled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        
        sla = incident_slas[str(incident_sla_id)]
        timestamp = "2025-10-01T00:00:00Z"
        
        if response_due is not None:
            sla["response_due"] = response_due
        if resolve_due is not None:
            sla["resolve_due"] = resolve_due
        if breached is not None:
            sla["breached"] = breached
        if status is not None:
            sla["status"] = status
        
        sla["updated_at"] = timestamp
        
        return json.dumps(sla)

