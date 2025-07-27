from typing import Any, Dict
from typing import Any, Dict, Optional
import json

class Tools:
    @staticmethod
    def list_incidents_by_kb_invoke(data: Dict[str, Any], knowledge_base_id: str) -> str:
        incident_knowledge = data.get("incident_knowledge", {})
        incidents = data.get("incidents", {})
        results = []
        
        # Find all incidents linked to this knowledge base article
        linked_incident_ids = []
        for link in incident_knowledge.values():
            if link.get("knowledge_base_id") == knowledge_base_id:
                linked_incident_ids.append(link.get("incident_id"))
        
        # Get the actual incident records
        for incident_id in linked_incident_ids:
            if str(incident_id) in incidents:
                results.append(incidents[str(incident_id)])
        
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
    def list_surveys_by_filters_invoke(data: Dict[str, Any], incident_id: Optional[str] = None,
               user_id: Optional[str] = None, rating: Optional[int] = None,
               survey_id: Optional[str] = None) -> str:
        surveys = data.get("surveys", {})
        results = []
        
        for survey in surveys.values():
            if incident_id and survey.get("incident_id") != incident_id:
                continue
            if user_id and survey.get("user_id") != user_id:
                continue
            if rating and survey.get("rating") != rating:
                continue
            if survey_id and survey.get("survey_id") != int(survey_id):
                continue
            results.append(survey)
        
        return json.dumps(results)

    @staticmethod
    def update_task_invoke(data: Dict[str, Any], task_id: str, description: Optional[str] = None,
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
    def list_kb_articles_by_filters_invoke(data: Dict[str, Any], company_id,
               department_id: Optional[str] = None, category_id: Optional[str] = None,
               subcategory_id: Optional[str] = None, created_by: Optional[str] = None,
               description: Optional[str] = None) -> str:
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
            if description and description.lower() not in article.get("description", "").lower():
                continue
            results.append(article)

        return json.dumps(results)

    @staticmethod
    def create_survey_invoke(data: Dict[str, Any], incident_id: str, user_id: str,
               rating: int) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        surveys = data.get("surveys", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        # Validate rating range (assuming 1-5 scale)
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        survey_id = generate_id(surveys)
        timestamp = "2025-10-01T00:00:00"
        
        new_survey = {
            "survey_id": survey_id,
            "incident_id": incident_id,
            "user_id": user_id,
            "rating": rating,
            "submitted_at": timestamp,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        surveys[str(survey_id)] = new_survey
        return json.dumps(new_survey)

    @staticmethod
    def list_subcategories_by_filters_invoke(data: Dict[str, Any], category_id: Optional[str] = None,
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
    def update_user_profile_invoke(data: Dict[str, Any], user_id: str, first_name: Optional[str] = None,
               last_name: Optional[str] = None, email: Optional[str] = None,
               role: Optional[str] = None, timezone: Optional[str] = None,
               status: Optional[str] = None) -> str:
        users = data.get("users", {})
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        user = users[str(user_id)]
        
        # Validate role if provided
        if role:
            valid_roles = ["end_user", "agent", "manager", "admin"]
            if role not in valid_roles:
                raise ValueError(f"Invalid role. Must be one of {valid_roles}")
        
        # Validate status if provided
        if status:
            valid_statuses = ["active", "inactive"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate email uniqueness if provided
        if email:
            for uid, existing_user in users.items():
                if uid != str(user_id) and existing_user.get("email", "").lower() == email.lower():
                    raise ValueError(f"Email {email} is already in use")
        
        # Update fields if provided
        if first_name is not None:
            user["first_name"] = first_name
        if last_name is not None:
            user["last_name"] = last_name
        if email is not None:
            user["email"] = email
        if role is not None:
            user["role"] = role
        if timezone is not None:
            user["timezone"] = timezone
        if status is not None:
            user["status"] = status
        
        user["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(user)

    @staticmethod
    def list_users_by_filters_invoke(data: Dict[str, Any], company_id: Optional[str] = None,
               department_id: Optional[str] = None, role: Optional[str] = None,
               status: Optional[str] = None, email: Optional[str] = None,
               first_name: Optional[str] = None, last_name: Optional[str] = None) -> str:
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
            if first_name and first_name.lower() not in user.get("first_name", "").lower():
                continue
            if last_name and last_name.lower() not in user.get("last_name", "").lower():
                continue
            results.append(user)

        return json.dumps(results)

    @staticmethod
    def list_departments_by_filters_invoke(data: Dict[str, Any], company_id: Optional[str] = None,
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
    def create_kb_article_invoke(data: Dict[str, Any], description: str, created_by: str,
               company_id: str, category_id: Optional[str] = None,
               subcategory_id: Optional[str] = None, 
               department_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        kb_articles = data.get("knowledge_base", {})
        users = data.get("users", {})
        companies = data.get("companies", {})
        categories = data.get("categories", {})
        subcategories = data.get("subcategories", {})
        departments = data.get("departments", {})
        
        # Validate required entities
        if str(created_by) not in users:
            raise ValueError(f"User {created_by} not found")
        
        if str(company_id) not in companies:
            raise ValueError(f"Company {company_id} not found")
        
        # Validate optional entities if provided
        if category_id and str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        if subcategory_id and str(subcategory_id) not in subcategories:
            raise ValueError(f"Subcategory {subcategory_id} not found")
        
        if department_id and str(department_id) not in departments:
            raise ValueError(f"Department {department_id} not found")
        
        kb_id = generate_id(kb_articles)
        timestamp = "2025-10-01T00:00:00"
        
        new_kb_article = {
            "knowledge_base_id": kb_id,
            "description": description,
            "created_by": created_by,
            "category_id": category_id,
            "subcategory_id": subcategory_id,
            "company_id": company_id,
            "department_id": department_id,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        kb_articles[str(kb_id)] = new_kb_article
        return json.dumps(new_kb_article)

    @staticmethod
    def list_companies_by_filters_invoke(data: Dict[str, Any], company_id: Optional[str] = None,
               name: Optional[str] = None, industry: Optional[str] = None,
               address: Optional[str] = None) -> str:
        companies = data.get("companies", {})
        results = []
        
        for company in companies.values():
            if company_id and company.get("company_id") != int(company_id):
                continue
            if name and name.lower() not in company.get("name", "").lower():
                continue
            if industry and industry.lower() not in company.get("industry", "").lower():
                continue
            if address and address.lower() not in company.get("address", "").lower():
                continue
            results.append(company)
        
        return json.dumps(results)

    @staticmethod
    def update_incident_invoke(data: Dict[str, Any], incident_id: str, title: Optional[str] = None,
               description: Optional[str] = None, category_id: Optional[str] = None,
               subcategory_id: Optional[str] = None, assigned_to: Optional[str] = None,
               department_id: Optional[str] = None, status: Optional[str] = None,
               priority: Optional[str] = None) -> str:
        
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        categories = data.get("categories", {})
        subcategories = data.get("subcategories", {})
        departments = data.get("departments", {})
        
        # Validate incident exists
        if str(incident_id) not in incidents:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Validate assigned user if provided
        if assigned_to and str(assigned_to) not in users:
            raise ValueError(f"Assigned user {assigned_to} not found")
        
        # Validate category if provided
        if category_id and str(category_id) not in categories:
            raise ValueError(f"Category {category_id} not found")
        
        # Validate subcategory if provided
        if subcategory_id and str(subcategory_id) not in subcategories:
            raise ValueError(f"Subcategory {subcategory_id} not found")
        
        # Validate department if provided
        if department_id and str(department_id) not in departments:
            raise ValueError(f"Department {department_id} not found")
        
        # Validate enum values if provided
        if status:
            valid_statuses = ["open", "in_progress", "resolved", "closed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        if priority:
            valid_priorities = ["low", "medium", "high", "critical"]
            if priority not in valid_priorities:
                raise ValueError(f"Invalid priority. Must be one of {valid_priorities}")
        
        incident = incidents[str(incident_id)]
        timestamp = "2025-10-01T00:00:00"
        
        # Update fields if provided
        if title is not None:
            incident["title"] = title
        if description is not None:
            incident["description"] = description
        if category_id is not None:
            incident["category_id"] = category_id
        if subcategory_id is not None:
            incident["subcategory_id"] = subcategory_id
        if assigned_to is not None:
            incident["assigned_to"] = assigned_to
        if department_id is not None:
            incident["department_id"] = department_id
        if status is not None:
            incident["status"] = status
        if priority is not None:
            incident["priority"] = priority
        
        incident["updated_at"] = timestamp
        
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
    def get_average_csat_invoke(data: Dict[str, Any], agent_id: Optional[str] = None,
               incident_id: Optional[str] = None) -> str:
        surveys = data.get("surveys", {})
        incidents = data.get("incidents", {})
        
        if not agent_id and not incident_id:
            raise ValueError("Either agent_id or incident_id must be provided")
        
        relevant_surveys = []
        
        if incident_id:
            # Get surveys for specific incident
            for survey in surveys.values():
                if survey.get("incident_id") == incident_id:
                    relevant_surveys.append(survey)
        
        elif agent_id:
            # Get surveys for incidents assigned to this agent
            agent_incident_ids = []
            for incident_id, incident in incidents.items():
                print("incident_id", incident.get("assigned_to"))
                print("agent_id", agent_id)
                print("="*10)
                if incident.get("assigned_to") == agent_id:
                    agent_incident_ids.append(incident_id)
            
            print("agent_incident_ids", agent_incident_ids)
            for survey in surveys.values():
                if survey.get("incident_id") in agent_incident_ids:
                    relevant_surveys.append(survey)
        
        if not relevant_surveys:
            return json.dumps({"average_csat": None, "total_surveys": 0})
        
        print("relevant", relevant_surveys)
        total_rating = sum(int(survey.get("rating", 0)) for survey in relevant_surveys)
        average_csat = total_rating / len(relevant_surveys)
        
        return json.dumps({
            "average_csat": round(average_csat, 2),
            "total_surveys": len(relevant_surveys)
        })

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
    def list_incidents_by_filters_invoke(data: Dict[str, Any], company_id: Optional[str] = None,
               department_id: Optional[str] = None, status: Optional[str] = None,
               priority: Optional[str] = None, assigned_to: Optional[str] = None,
               reported_by: Optional[str] = None, category_id: Optional[str] = None,
               subcategory_id: Optional[str] = None) -> str:
        incidents = data.get("incidents", {})
        results = []
        
        for incident in incidents.values():
            if company_id and incident.get("company_id") != company_id:
                continue
            if department_id and incident.get("department_id") != department_id:
                continue
            if status and incident.get("status") != status:
                continue
            if priority and incident.get("priority") != priority:
                continue
            if assigned_to and incident.get("assigned_to") != assigned_to:
                continue
            if reported_by and incident.get("reported_by") != reported_by:
                continue
            if category_id and incident.get("category_id") != category_id:
                continue
            if subcategory_id and incident.get("subcategory_id") != subcategory_id:
                continue
            results.append(incident)
        
        return json.dumps(results)

    @staticmethod
    def list_categories_by_filters_invoke(data: Dict[str, Any], category_id: Optional[str] = None,
               name: Optional[str] = None) -> str:
        categories = data.get("categories", {})
        results = []
        
        for category in categories.values():
            if category_id and category.get("category_id") != int(category_id):
                continue
            if name and name.lower() not in category.get("name", "").lower():
                continue
            results.append(category)
        
        return json.dumps(results)

    @staticmethod
    def update_survey_invoke(data: Dict[str, Any], survey_id: str, rating: int,
               feedback_text: Optional[str] = None) -> str:
        surveys = data.get("surveys", {})
        
        # Validate survey exists
        if str(survey_id) not in surveys:
            raise ValueError(f"Survey {survey_id} not found")
        
        # Validate rating range (assuming 1-5 scale)
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        # Update the survey
        survey = surveys[str(survey_id)]
        survey["rating"] = rating
        survey["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(survey)

    @staticmethod
    def list_incident_comments_invoke(data: Dict[str, Any], incident_id: str, is_public: Optional[bool] = None) -> str:
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
    def update_kb_article_invoke(data: Dict[str, Any], knowledge_base_id: str, description: str) -> str:
        knowledge_base = data.get("knowledge_base", {})
        
        # Validate KB article exists
        if str(knowledge_base_id) not in knowledge_base:
            raise ValueError(f"Knowledge base article {knowledge_base_id} not found")
        
        # Update the article
        article = knowledge_base[str(knowledge_base_id)]
        article["description"] = description
        article["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(article)

    @staticmethod
    def list_low_rated_incidents_invoke(data: Dict[str, Any], company_id: str, threshold: Optional[int] = None) -> str:
        surveys = data.get("surveys", {})
        incidents = data.get("incidents", {})
        if not company_id:
            raise ValueError("Company ID must be provided")
        
        # Validate company_id exists
        if company_id not in data.get("companies", {}):
            raise ValueError(f"Company {company_id} not found")
        
        if threshold is None:
            threshold = 3  # Default threshold for low ratings
        
        # Group surveys by incident_id and calculate average rating
        incident_ratings = {}
        for survey in surveys.values():
            if incidents[survey.get("incident_id")].get("company_id") != company_id:
                continue
            
            incident_id = survey.get("incident_id")
            rating = survey.get("rating")
            
            if incident_id not in incident_ratings:
                incident_ratings[incident_id] = []
            incident_ratings[incident_id].append(rating)
        
        # Find incidents with average rating below threshold
        low_rated_incidents = []
        for incident_id, ratings in incident_ratings.items():
            if ratings:  # Ensure there are ratings
                avg_rating = sum(ratings) / len(ratings)
                if avg_rating <= threshold:
                    if str(incident_id) in incidents:
                        incident_data = incidents[str(incident_id)].copy()
                        incident_data["average_rating"] = round(avg_rating, 2)
                        incident_data["total_surveys"] = len(ratings)
                        low_rated_incidents.append(incident_data)
        
        return json.dumps(low_rated_incidents)

