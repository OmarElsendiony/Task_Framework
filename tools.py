from typing import Any, Dict
from typing import Any, Dict, Optional
from typing import Any, Dict, Optional, List
import json

class Tools:
    @staticmethod
    def search_kb_articles_invoke(data: Dict[str, Any], company_id: Optional[str] = None,
               department_id: Optional[str] = None, category_id: Optional[str] = None,
               subcategory_id: Optional[str] = None, created_by: Optional[str] = None) -> str:
        kb_articles = data.get("knowledge_base", {})
        results = []
        
        for article in kb_articles.values():
            if company_id and article.get("company_id") != company_id:
                continue
            if department_id and article.get("department_id") != department_id:
                continue
            if category_id and article.get("category_id") != category_id:
                continue
            if subcategory_id and article.get("subcategory_id") != subcategory_id:
                continue
            if created_by and article.get("created_by") != created_by:
                continue
            results.append(article)
        
        return json.dumps(results)

    @staticmethod
    def get_incident_tasks_invoke(data: Dict[str, Any], incident_id: int, assigned_to: Optional[int] = None,
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
    def create_user_invoke(data: Dict[str, Any], first_name: str, last_name: str, email: str,
               role: str, company_id: str,
               department_id: Optional[str] = None, timezone: Optional[str] = None,
               status: str = "active") -> str:
        
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        companies = data.get("companies", {})
        
        # Validate company exists
        if str(company_id) not in companies:
            raise ValueError(f"Company {company_id} not found")
        
        # Validate department if provided
        if department_id:
            departments = data.get("departments", {})
            if str(department_id) not in departments:
                raise ValueError(f"Department {department_id} not found")
        
        # Check email uniqueness
        for user in users.values():
            if user.get("email", "").lower() == email.lower():
                raise ValueError(f"Email {email} already exists")
        
        # Validate role
        valid_roles = ["end_user", "agent", "manager", "admin"]
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of {valid_roles}")
        
        # Validate status
        valid_statuses = ["active", "inactive"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        user_id = generate_id(users)
        timestamp = "2025-10-01T00:00:00"
        
        new_user = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "role": role,
            "status": status,
            "timezone": timezone,
            "company_id": company_id,
            "department_id": department_id,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        users[str(user_id)] = new_user
        return json.dumps({"user_id": user_id})

    @staticmethod
    def update_change_request_invoke(data: Dict[str, Any], change_request_id: int, 
               description: Optional[str] = None, status: Optional[str] = None,
               priority: Optional[str] = None, risk_level: Optional[str] = None,
               approved_by: Optional[int] = None, assigned_to: Optional[int] = None,
               scheduled_start: Optional[str] = None, scheduled_end: Optional[str] = None,
               affected_scope: Optional[Dict] = None) -> str:
        change_requests = data.get("change_requests", {})
        cr = change_requests.get(str(change_request_id))
        
        if not cr:
            raise ValueError(f"Change request {change_request_id} not found")
        
        # Validate status if provided
        if status:
            valid_statuses = ["draft", "submitted", "approved", "rejected", 
                            "in_progress", "implemented", "closed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate priority if provided
        if priority:
            valid_priorities = ["low", "medium", "high", "critical"]
            if priority not in valid_priorities:
                raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
        # Validate risk level if provided
        if risk_level:
            valid_risk_levels = ["low", "medium", "high"]
            if risk_level not in valid_risk_levels:
                raise ValueError(f"Invalid risk level. Must be one of {valid_risk_levels}")
        
        # Validate users if provided
        users = data.get("users", {})
        if approved_by and str(approved_by) not in users:
            raise ValueError(f"Approver user {approved_by} not found")
        if assigned_to and str(assigned_to) not in users:
            raise ValueError(f"Assigned user {assigned_to} not found")
        
        # Update fields
        if description is not None:
            cr["description"] = description
        if status is not None:
            cr["status"] = status
        if priority is not None:
            cr["priority"] = priority
        if risk_level is not None:
            cr["risk_level"] = risk_level
        if approved_by is not None:
            cr["approved_by"] = approved_by
        if assigned_to is not None:
            cr["assigned_to"] = assigned_to
        if scheduled_start is not None:
            cr["scheduled_start"] = scheduled_start
        if scheduled_end is not None:
            cr["scheduled_end"] = scheduled_end
        if affected_scope is not None:
            cr["affected_scope"] = affected_scope
        
        cr["updated_at"] = "2025-10-01T00:00:00"
        return json.dumps(cr)

    @staticmethod
    def create_incident_invoke(data: Dict[str, Any], title: str, description: str, reported_by: str,
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
    def search_users_invoke(data: Dict[str, Any], company_id: Optional[str] = None, 
               department_id: Optional[str] = None, role: Optional[str] = None,
               status: Optional[str] = None, email: Optional[str] = None) -> str:
        users = data.get("users", {})
        results = []
        
        for user in users.values():
            if company_id and user.get("company_id") != company_id:
                continue
            if department_id and user.get("department_id") != department_id:
                continue
            if role and user.get("role") != role:
                continue
            if status and user.get("status") != status:
                continue
            if email and user.get("email", "").lower() != email.lower():
                continue
            results.append(user)
        
        return json.dumps(results)

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
    def search_surveys_invoke(data: Dict[str, Any], incident_id: Optional[str] = None,
               user_id: Optional[int] = None, min_rating: Optional[int] = None) -> str:
        surveys = data.get("surveys", {})
        results = []
        
        for survey in surveys.values():
            if incident_id and survey.get("incident_id") != incident_id:
                continue
            if user_id and survey.get("user_id") != user_id:
                continue
            if min_rating and int(survey.get("rating", 0)) < int(min_rating):
                continue
            results.append(survey)
        
        return json.dumps(results)

    @staticmethod
    def update_task_invoke(data: Dict[str, Any], task_id: str, description: Optional[str] = None,
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
    def search_incidents_invoke(data: Dict[str, Any], company_id: Optional[str] = None,
               department_id: Optional[str] = None, assigned_to: Optional[str] = None,
               reported_by: Optional[str] = None, status: Optional[str] = None,
               priority: Optional[str] = None, category_id: Optional[str] = None) -> str:
        incidents = data.get("incidents", {})
        results = []
        
        for incident in incidents.values():
            if company_id and incident.get("company_id") != company_id:
                continue
            if department_id and incident.get("department_id") != department_id:
                continue
            if assigned_to and incident.get("assigned_to") != assigned_to:
                continue
            if reported_by and incident.get("reported_by") != reported_by:
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
    def get_company_by_name_invoke(data: Dict[str, Any], name: str) -> str:
        companies = data.get("companies", {})
        for company in companies.values():
            if company.get("name", "").lower() == name.lower():
                return json.dumps(company)
        raise ValueError(f"Company '{name}' not found")

    @staticmethod
    def update_user_profile_invoke(data: Dict[str, Any], user_id: str, first_name: Optional[str] = None,
               last_name: Optional[str] = None, email: Optional[str] = None,
               timezone: Optional[str] = None, department_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        users = data.get("users", {})
        user = users.get(str(user_id))
        
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Check email uniqueness if updating email
        if email and email != user.get("email"):
            for other_user in users.values():
                if (other_user.get("email", "").lower() == email.lower() and 
                    other_user.get("user_id") != user_id):
                    raise ValueError(f"Email {email} already exists")
        
        # Validate department if provided
        if department_id:
            departments = data.get("departments", {})
            if str(department_id) not in departments:
                raise ValueError(f"Department {department_id} not found")
        
        # Validate status if provided
        if status:
            valid_statuses = ["active", "inactive"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Update fields
        if first_name is not None:
            user["first_name"] = first_name
        if last_name is not None:
            user["last_name"] = last_name
        if email is not None:
            user["email"] = email
        if timezone is not None:
            user["timezone"] = timezone
        if department_id is not None:
            user["department_id"] = department_id
        if status is not None:
            user["status"] = status
        
        user["updated_at"] = "2025-10-01T00:00:00"
        return json.dumps(user)

    @staticmethod
    def update_incident_invoke(data: Dict[str, Any], incident_id: str, title: Optional[str] = None,
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
    def link_incident_to_kb_invoke(data: Dict[str, Any], incident_id: str, knowledge_base_id: str) -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incidents = data.get("incidents", {})
        kb_articles = data.get("knowledge_base", {})
        incident_knowledge = data.get("incident_knowledge", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate KB article exists
        if str(knowledge_base_id) not in kb_articles:
            raise ValueError(f"Knowledge base article {knowledge_base_id} not found")
        
        # Check if link already exists
        for link in incident_knowledge.values():
            if (link.get("incident_id") == incident_id and 
                link.get("knowledge_base_id") == knowledge_base_id):
                return json.dumps({"status": "already_linked"})
        
        link_id = generate_id(incident_knowledge)
        timestamp = "2025-10-01T00:00:00"
        
        new_link = {
            "incident_id": incident_id,
            "knowledge_base_id": knowledge_base_id,
            "created_at": timestamp
        }
        
        incident_knowledge[str(link_id)] = new_link
        return json.dumps(new_link)

    @staticmethod
    def add_incident_comment_invoke(data: Dict[str, Any], incident_id: str, user_id: str, 
               comment_text: str, is_public: bool = True) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        comments = data.get("incident_comments", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        comment_id = generate_id(comments)
        timestamp = "2025-10-01T00:00:00"
        
        new_comment = {
            "incident_comment_id": comment_id,
            "incident_id": incident_id,
            "user_id": user_id,
            "comment_text": comment_text,
            "is_public": is_public,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        comments[str(comment_id)] = new_comment
        return json.dumps(new_comment)

    @staticmethod
    def create_incident_task_invoke(data: Dict[str, Any], incident_id: str, description: str,
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
    def update_kb_article_invoke(data: Dict[str, Any], knowledge_base_id: str, 
               description: Optional[str] = None, category_id: Optional[str] = None,
               subcategory_id: Optional[str] = None, department_id: Optional[str] = None) -> str:
        kb_articles = data.get("knowledge_base", {})
        article = kb_articles.get(str(knowledge_base_id))
        
        if not article:
            raise ValueError(f"Knowledge base article {knowledge_base_id} not found")
        
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
        
        # Update fields
        if description is not None:
            article["description"] = description
        if category_id is not None:
            article["category_id"] = category_id
        if subcategory_id is not None:
            article["subcategory_id"] = subcategory_id
        if department_id is not None:
            article["department_id"] = department_id
        
        article["updated_at"] = "2025-10-01T00:00:00"
        return json.dumps(article)

    @staticmethod
    def search_departments_invoke(data: Dict[str, Any], company_id: Optional[str] = None, 
               manager_id: Optional[str] = None, name: Optional[str] = None) -> str:
        departments = data.get("departments", {})
        results = []
        
        for department in departments.values():
            if company_id and department.get("company_id") != company_id:
                continue
            if manager_id and department.get("manager_id") != manager_id:
                continue
            if name and name.lower() not in department.get("name", "").lower():
                continue
            results.append(department)
        
        return json.dumps(results)

    @staticmethod
    def get_category_by_name_invoke(data: Dict[str, Any], name: str) -> str:
        categories = data.get("categories", {})
        for category in categories.values():
            if category.get("name", "").lower() == name.lower():
                return json.dumps(category)
        raise ValueError(f"Category '{name}' not found")

    @staticmethod
    def search_change_requests_invoke(data: Dict[str, Any], incident_id: Optional[str] = None,
               assigned_to: Optional[str] = None, status: Optional[str] = None,
               priority: Optional[str] = None, risk_level: Optional[str] = None) -> str:
        change_requests = data.get("change_requests", {})
        results = []
        
        for cr in change_requests.values():
            if incident_id and cr.get("incident_id") != incident_id:
                continue
            if assigned_to and cr.get("assigned_to") != assigned_to:
                continue
            if status and cr.get("status") != status:
                continue
            if priority and cr.get("priority") != priority:
                continue
            if risk_level and cr.get("risk_level") != risk_level:
                continue
            results.append(cr)
        
        return json.dumps(results)

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
    def search_subcategories_invoke(data: Dict[str, Any], category_id: Optional[str] = None, 
               name: Optional[str] = None) -> str:
        subcategories = data.get("subcategories", {})
        results = []
        
        for subcategory in subcategories.values():
            if category_id and subcategory.get("category_id") != category_id:
                continue
            if name and name.lower() not in subcategory.get("name", "").lower():
                continue
            results.append(subcategory)
        
        return json.dumps(results)

    @staticmethod
    def get_incident_invoke(data: Dict[str, Any], incident_id: str) -> str:
        incidents = data.get("incidents", {})
        incident = incidents.get(incident_id)
        if not incident:
            raise ValueError(f"Incident {incident_id} not found")
        return json.dumps(incident)

    @staticmethod
    def register_change_request_invoke(data: Dict[str, Any], assigned_to: str, description: str,
               priority: str = "medium", risk_level: str = "low",
               incident_id: Optional[str] = None, affected_scope: Optional[Dict] = None,
               scheduled_start: Optional[str] = None, scheduled_end: Optional[str] = None) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        change_requests = data.get("change_requests", {})
        users = data.get("users", {})
        
        # Validate assigned user exists
        if str(assigned_to) not in users:
            raise ValueError(f"Assigned user {assigned_to} not found")
        
        # Validate incident if provided
        if incident_id:
            incidents = data.get("incidents", {})
            if str(incident_id) not in incidents:
                raise ValueError(f"Incident {incident_id} not found")
        
        # Validate priority
        valid_priorities = ["low", "medium", "high", "critical"]
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
        # Validate risk level
        valid_risk_levels = ["low", "medium", "high"]
        if risk_level not in valid_risk_levels:
            raise ValueError(f"Invalid risk level. Must be one of {valid_risk_levels}")
        
        cr_id = generate_id(change_requests)
        timestamp = "2025-10-01T00:00:00"
        
        new_cr = {
            "change_request_id": cr_id,
            "incident_id": incident_id,
            "assigned_to": assigned_to,
            "approved_by": None,
            "description": description,
            "status": "draft",
            "priority": priority,
            "risk_level": risk_level,
            "affected_scope": affected_scope,
            "scheduled_start": scheduled_start,
            "scheduled_end": scheduled_end,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        change_requests[str(cr_id)] = new_cr
        return json.dumps(new_cr)

