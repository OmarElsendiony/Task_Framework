from typing import Any, Dict
from typing import Any, Dict, List
from typing import Any, Dict, Optional
import datetime
import json

class Tools:
    @staticmethod
    def discover_department_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover department entities.
        
        Supported entities:
        - departments: Department records by department_id, department_name, manager_id, budget, status, created_at, updated_at
        """
        if entity_type not in ["departments"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'departments'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("departments", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "department_id": entity_id})
            else:
                results.append({**entity_data, "department_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def discover_payroll_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover payroll entities.
        
        Supported entities:
        - payroll_records: Payroll records by payroll_id, employee_id, pay_period_start, pay_period_end, hours_worked, hourly_rate, payment_date, status, approved_by, created_at, updated_at
        - payroll_deductions: Payroll deductions by deduction_id, payroll_id, deduction_type, amount, created_by, created_at
        """
        if entity_type not in ["payroll_records", "payroll_deductions"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'payroll_records' or 'payroll_deductions'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        id_field = "payroll_id" if entity_type == "payroll_records" else "deduction_id"
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def discover_performance_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover performance entities.
        
        Supported entities:
        - performance_reviews: Performance reviews by review_id, employee_id, reviewer_id, review_period_start, review_period_end, review_type, overall_rating, goals_achievement_score, communication_score, teamwork_score, leadership_score, technical_skills_score, status, created_at, updated_at
        """
        if entity_type not in ["performance_reviews"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'performance_reviews'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("performance_reviews", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "review_id": entity_id})
            else:
                results.append({**entity_data, "review_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_training_programs_invoke(
        data: Dict[str, Any],
        operation: str,
        program_id: Optional[str] = None,
        program_name: Optional[str] = None,
        program_type: Optional[str] = None,
        duration_hours: Optional[int] = None,
        delivery_method: Optional[str] = None,
        mandatory: Optional[bool] = None, # Corrected: Default changed from False to None
        status: Optional[str] = None,     # Corrected: Default changed from "active" to None
    ) -> str:
        """
        Executes the specified operation (create or update) on training programs.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        training_programs = data.get("training_programs", {})

        if operation == "create":
            # For 'create', set defaults if not provided
            effective_mandatory = mandatory if mandatory is not None else False
            effective_status = status if status is not None else "active"

            if not all([program_name, program_type, duration_hours, delivery_method]):
                return json.dumps({"error": "Missing required parameters for create operation."})

            valid_types = ["onboarding", "compliance", "technical", "leadership", "safety", "diversity", "ai_ethics"]
            if program_type not in valid_types:
                return json.dumps({"error": f"Invalid program type. Must be one of {valid_types}."})

            valid_methods = ["in_person", "online", "hybrid", "self_paced"]
            if delivery_method not in valid_methods:
                return json.dumps({"error": f"Invalid delivery method. Must be one of {valid_methods}."})
            
            valid_statuses = ["active", "inactive", "draft"]
            if effective_status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}."})

            new_program_id = generate_id(training_programs)
            new_program = {
                "program_id": new_program_id,
                "program_name": program_name,
                "program_type": program_type,
                "duration_hours": duration_hours,
                "delivery_method": delivery_method,
                "mandatory": effective_mandatory,
                "status": effective_status,
                "created_at": timestamp,
                "updated_at": timestamp,
            }
            training_programs[new_program_id] = new_program
            return json.dumps(new_program)

        elif operation == "update":
            if not program_id:
                return json.dumps({"error": "program_id is required for update operation."})
            if program_id not in training_programs:
                return json.dumps({"error": f"Training program with ID {program_id} not found."})

            program_to_update = training_programs[program_id]
            if program_name is not None:
                program_to_update["program_name"] = program_name
            if program_type is not None:
                program_to_update["program_type"] = program_type
            if duration_hours is not None:
                program_to_update["duration_hours"] = duration_hours
            if delivery_method is not None:
                program_to_update["delivery_method"] = delivery_method
            if mandatory is not None:
                program_to_update["mandatory"] = mandatory
            if status is not None:
                program_to_update["status"] = status
            
            program_to_update["updated_at"] = timestamp
            return json.dumps(program_to_update)

        else:
            return json.dumps({"error": "Invalid operation. Must be 'create' or 'update'."})

    @staticmethod
    def transfer_to_human_invoke(
        data: Dict[str, Any],
        summary: str,
    ) -> str:
        return "Transfer successful"

    @staticmethod
    def discover_job_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover job entities.
        
        Supported entities:
        - job_positions: Job position records by position_id, title, department_id, job_level, employment_type, hourly_rate_min, hourly_rate_max, status, created_at, updated_at
        - skills: Skill records by skill_id, skill_name, status
        - job_position_skills: Job position skill relationships by position_id, skill_id
        """
        if entity_type not in ["job_positions", "skills", "job_position_skills"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be one of: 'job_positions', 'skills', 'job_position_skills'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        if entity_type == "job_position_skills":
            # Special handling for many-to-many relationship table
            for relationship in entities.values():
                if filters:
                    match = True
                    for filter_key, filter_value in filters.items():
                        entity_value = relationship.get(filter_key)
                        if entity_value != filter_value:
                            match = False
                            break
                    if match:
                        results.append(relationship)
                else:
                    results.append(relationship)
        else:
            # Handle regular entities with primary keys
            id_field = "position_id" if entity_type == "job_positions" else "skill_id"
            
            for entity_id, entity_data in entities.items():
                if filters:
                    match = True
                    for filter_key, filter_value in filters.items():
                        entity_value = entity_data.get(filter_key)
                        if entity_value != filter_value:
                            match = False
                            break
                    if match:
                        results.append({**entity_data, id_field: entity_id})
                else:
                    results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_audit_logs_invoke(
        data: Dict[str, Any],
        operation: str,
        user_id: str,
        action: str,
        reference_type: str,
        reference_id: str,
        field_name: Optional[str] = None,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
    ) -> str:
        """
        Executes the create operation for audit logs.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        audit_logs = data.get("audit_logs", {})
        users = data.get("users", {})

        if operation != "create":
            return json.dumps({"error": "Invalid operation. Only 'create' is permitted for audit logs."})
        
        if not all([user_id, action, reference_type, reference_id]):
            return json.dumps({"error": "Missing required parameters for create operation."})
        
        if user_id not in users:
            return json.dumps({"error": f"User with ID {user_id} not found."})

        valid_actions = ["create", "read", "update", "delete", "approve", "reject"]
        if action not in valid_actions:
            return json.dumps({"error": f"Invalid action. Must be one of {valid_actions}."})

        new_log_id = generate_id(audit_logs)
        new_log = {
            "log_id": new_log_id,
            "user_id": user_id,
            "action": action,
            "reference_type": reference_type,
            "reference_id": reference_id,
            "field_name": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "timestamp": timestamp,
        }
        audit_logs[new_log_id] = new_log
        return json.dumps(new_log)

    @staticmethod
    def manage_user_invoke(
        data: Dict[str, Any],
        action: str,
        user_id: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        phone_number: Optional[str] = None,
        status: Optional[str] = None,
        mfa_enabled: Optional[bool] = None,
    ) -> str:
        """
        Executes the specified action (create or update) on user accounts.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        users = data.get("users", {})

        # Validate supported roles
        supported_roles = [
            "hr_director", "hr_manager", "recruiter", "payroll_administrator",
            "hiring_manager", "finance_officer", "it_administrator", 
            "compliance_officer", "employee"
        ]

        # Validate supported statuses
        supported_statuses = ["active", "inactive"]

        if action == "create":
            # Required fields for user creation
            if not all([first_name, last_name, email, role]):
                return json.dumps({
                    "error": "Missing required parameters for create operation. Required: first_name, last_name, email, role"
                })

            # Validate role
            if role not in supported_roles:
                return json.dumps({
                    "error": f"Invalid role '{role}'. Must be one of: {', '.join(supported_roles)}"
                })

            # Validate status if provided
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Check for duplicate email
            for existing_user in users.values():
                if existing_user.get("email") == email:
                    return json.dumps({
                        "error": f"User with email '{email}' already exists"
                    })

            # Generate new user ID
            new_user_id = generate_id(users)

            # Create new user record
            new_user = {
                "user_id": new_user_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "role": role,
                "status": status or "active",  # Default to active if not specified
                "mfa_enabled": mfa_enabled if mfa_enabled is not None else False,  # Default to False
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Add phone_number if provided
            if phone_number:
                new_user["phone_number"] = phone_number

            # Add to users data
            users[new_user_id] = new_user

            return json.dumps({
                "success": True,
                "message": f"User created successfully with ID {new_user_id}",
                "user_id": new_user_id,
                "user_data": new_user
            })

        elif action == "update":
            # user_id is required for update
            if not user_id:
                return json.dumps({
                    "error": "Missing required parameter 'user_id' for update operation"
                })

            # Check if user exists
            if user_id not in users:
                return json.dumps({
                    "error": f"User with ID {user_id} not found"
                })

            user_to_update = users[user_id]

            # Validate role if being updated
            if role and role not in supported_roles:
                return json.dumps({
                    "error": f"Invalid role '{role}'. Must be one of: {', '.join(supported_roles)}"
                })

            # Validate status if being updated
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Check for duplicate email if email is being changed
            if email and email != user_to_update.get("email"):
                for existing_user in users.values():
                    if existing_user.get("email") == email:
                        return json.dumps({
                            "error": f"User with email '{email}' already exists"
                        })

            # Track what fields are being updated
            updated_fields = []

            # Update fields if provided
            if first_name:
                user_to_update["first_name"] = first_name
                updated_fields.append("first_name")
            
            if last_name:
                user_to_update["last_name"] = last_name
                updated_fields.append("last_name")
            
            if email:
                user_to_update["email"] = email
                updated_fields.append("email")
            
            if role:
                user_to_update["role"] = role
                updated_fields.append("role")
            
            if phone_number:
                user_to_update["phone_number"] = phone_number
                updated_fields.append("phone_number")
            
            if status:
                user_to_update["status"] = status
                updated_fields.append("status")
            
            if mfa_enabled is not None:
                user_to_update["mfa_enabled"] = mfa_enabled
                updated_fields.append("mfa_enabled")

            # Update timestamp
            user_to_update["updated_at"] = timestamp

            if not updated_fields:
                return json.dumps({
                    "error": "No fields provided to update"
                })

            return json.dumps({
                "success": True,
                "message": f"User {user_id} updated successfully",
                "updated_fields": updated_fields,
                "user_data": user_to_update
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

    @staticmethod
    def manage_employee_invoke(
        data: Dict[str, Any],
        action: str,
        employee_id: Optional[str] = None,
        user_id: Optional[str] = None,
        position_id: Optional[str] = None,
        hire_date: Optional[str] = None,
        manager_id: Optional[str] = None,
        date_of_birth: Optional[str] = None,
        address: Optional[str] = None,
        hourly_rate: Optional[float] = None,
        employment_status: Optional[str] = None,
    ) -> str:
        """
        Executes the specified action (create or update) on employee records.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        def validate_date_format(date_str: str, field_name: str) -> bool:
            """Validates date format YYYY-MM-DD"""
            if not date_str:
                return True
            try:
                parts = date_str.split('-')
                if len(parts) != 3:
                    return False
                year, month, day = map(int, parts)
                if not (1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31):
                    return False
                return True
            except ValueError:
                return False

        timestamp = "2025-10-01T12:00:00"
        employees = data.get("employees", {})
        users = data.get("users", {})
        job_positions = data.get("job_positions", {})

        # Validate supported employment statuses
        supported_employment_statuses = ["active", "inactive", "terminated"]

        if action == "create":
            # Required fields for employee creation (onboarding)
            if not all([user_id, position_id, hire_date]):
                return json.dumps({
                    "error": "Missing required parameters for create operation. Required: user_id, position_id, hire_date"
                })

            # Validate user exists
            if user_id not in users:
                return json.dumps({
                    "error": f"User with ID '{user_id}' not found"
                })

            # Validate position exists
            if position_id not in job_positions:
                return json.dumps({
                    "error": f"Job position with ID '{position_id}' not found"
                })

            # Check if employee record already exists for this user
            for existing_employee in employees.values():
                if existing_employee.get("user_id") == user_id:
                    return json.dumps({
                        "error": f"Employee record already exists for user ID '{user_id}'"
                    })

            # Validate manager exists if provided
            if manager_id:
                manager_exists = False
                for employee in employees.values():
                    if employee.get("employee_id") == manager_id and employee.get("employment_status") == "active":
                        manager_exists = True
                        break
                if not manager_exists:
                    return json.dumps({
                        "error": f"Active manager with employee ID '{manager_id}' not found"
                    })

            # Validate hire_date format
            if not validate_date_format(hire_date, "hire_date"):
                return json.dumps({
                    "error": "Invalid hire_date format. Use YYYY-MM-DD"
                })

            # Validate date_of_birth format if provided
            if date_of_birth and not validate_date_format(date_of_birth, "date_of_birth"):
                return json.dumps({
                    "error": "Invalid date_of_birth format. Use YYYY-MM-DD"
                })

            # Validate employment_status if provided
            if employment_status and employment_status not in supported_employment_statuses:
                return json.dumps({
                    "error": f"Invalid employment_status '{employment_status}'. Must be one of: {', '.join(supported_employment_statuses)}"
                })

            # Validate hourly_rate if provided
            if hourly_rate is not None:
                try:
                    hourly_rate = float(hourly_rate)
                    if hourly_rate < 0:
                        return json.dumps({
                            "error": "Hourly rate must be non-negative"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "error": "Invalid hourly_rate value. Must be a number"
                    })

            # Generate new employee ID
            new_employee_id = generate_id(employees)

            # Create new employee record
            new_employee = {
                "employee_id": new_employee_id,
                "user_id": user_id,
                "position_id": position_id,
                "hire_date": hire_date,
                "employment_status": employment_status if employment_status else "active",
                "manager_id": manager_id,
                "date_of_birth": date_of_birth,
                "address": address,
                "hourly_rate": hourly_rate,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Add to employees data
            employees[new_employee_id] = new_employee

            return json.dumps({
                "success": True,
                "message": f"Employee record created successfully for user ID '{user_id}'",
                "employee_id": new_employee_id,
                "employee_data": new_employee
            })

        elif action == "update":
            # Required field for employee update
            if not employee_id:
                return json.dumps({
                    "error": "Missing required parameter 'employee_id' for update operation"
                })

            # At least one optional field must be provided
            optional_fields = [position_id, employment_status, manager_id, date_of_birth, address, hourly_rate]
            if not any(field is not None for field in optional_fields):
                return json.dumps({
                    "error": "At least one optional parameter (position_id, employment_status, manager_id, date_of_birth, address, hourly_rate) must be provided for update operation"
                })

            # Check if employee exists
            if employee_id not in employees:
                return json.dumps({
                    "error": f"Employee with ID '{employee_id}' not found"
                })

            # Validate position exists if provided
            if position_id and position_id not in job_positions:
                return json.dumps({
                    "error": f"Job position with ID '{position_id}' not found"
                })

            # Validate manager exists if provided
            if manager_id:
                manager_exists = False
                for employee in employees.values():
                    if employee.get("employee_id") == manager_id and employee.get("employment_status") == "active":
                        manager_exists = True
                        break
                if not manager_exists:
                    return json.dumps({
                        "error": f"Active manager with employee ID '{manager_id}' not found"
                    })

            # Validate date_of_birth format if provided
            if date_of_birth and not validate_date_format(date_of_birth, "date_of_birth"):
                return json.dumps({
                    "error": "Invalid date_of_birth format. Use YYYY-MM-DD"
                })

            # Validate employment_status if provided
            if employment_status and employment_status not in supported_employment_statuses:
                return json.dumps({
                    "error": f"Invalid employment_status '{employment_status}'. Must be one of: {', '.join(supported_employment_statuses)}"
                })

            # Validate hourly_rate if provided
            if hourly_rate is not None:
                try:
                    hourly_rate = float(hourly_rate)
                    if hourly_rate < 0:
                        return json.dumps({
                            "error": "Hourly rate must be non-negative"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "error": "Invalid hourly_rate value. Must be a number"
                    })

            # Update employee record
            employee_record = employees[employee_id]
            
            if position_id:
                employee_record["position_id"] = position_id
            if employment_status:
                employee_record["employment_status"] = employment_status
            if manager_id is not None:  # Allow setting to None
                employee_record["manager_id"] = manager_id
            if date_of_birth:
                employee_record["date_of_birth"] = date_of_birth
            if address:
                employee_record["address"] = address
            if hourly_rate is not None:
                employee_record["hourly_rate"] = hourly_rate
            
            employee_record["updated_at"] = timestamp

            return json.dumps({
                "success": True,
                "message": f"Employee with ID '{employee_id}' updated successfully",
                "employee_id": employee_id,
                "employee_data": employee_record
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

    @staticmethod
    def manage_expense_reimbursements_invoke(
        data: Dict[str, Any],
        operation: str,
        employee_id: Optional[str] = None,
        expense_date: Optional[str] = None,
        amount: Optional[float] = None,
        expense_type: Optional[str] = None,
        receipt_file_path: Optional[str] = None,
        reimbursement_id: Optional[str] = None,
        status: Optional[str] = None,
        approved_by: Optional[str] = None,
        payment_date: Optional[str] = None,
    ) -> str:
        """
        Executes the specified operation (create or update) on expense reimbursements.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        expense_reimbursements = data.get("expense_reimbursements", {})
        employees = data.get("employees", {})
        users = data.get("users", {})

        if operation == "create":
            if not all([employee_id, expense_date, amount, expense_type]):
                return json.dumps({"error": "Missing required parameters for create operation."})

            if employee_id not in employees:
                return json.dumps({"error": f"Employee with ID {employee_id} not found."})

            # --- Start of revised validation logic ---
            if amount <= 0:
                return json.dumps({"error": "Validation failed: The amount must be a positive value."})
            
            try:
                # This check is now just to validate the date format is correct.
                datetime.datetime.strptime(expense_date, '%Y-%m-%d').date()
            except ValueError:
                return json.dumps({"error": "Invalid date format. Please use YYYY-MM-DD."})
            # --- End of revised validation logic ---
            
            valid_expense_types = ["travel", "meals", "equipment", "training", "other"]
            if expense_type not in valid_expense_types:
                return json.dumps({"error": f"Invalid expense type. Must be one of {valid_expense_types}."})

            new_reimbursement_id = generate_id(expense_reimbursements)
            new_reimbursement = {
                "reimbursement_id": new_reimbursement_id,
                "employee_id": employee_id,
                "expense_date": expense_date,
                "amount": amount,
                "expense_type": expense_type,
                "receipt_file_path": receipt_file_path,
                "status": "submitted",
                "approved_by": None,
                "payment_date": None,
                "created_at": timestamp,
                "updated_at": timestamp,
            }
            expense_reimbursements[new_reimbursement_id] = new_reimbursement
            return json.dumps(new_reimbursement)

        elif operation == "update":
            if not all([reimbursement_id, status]):
                return json.dumps({"error": "Missing reimbursement_id or status for update operation."})

            if reimbursement_id not in expense_reimbursements:
                return json.dumps({"error": f"Reimbursement with ID {reimbursement_id} not found."})

            valid_statuses = ["approved", "rejected", "paid"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}."})

            if status in ["approved", "rejected"] and not approved_by:
                return json.dumps({"error": f"approved_by is required when status is '{status}'."})
            
            if status == "paid" and not payment_date:
                return json.dumps({"error": "payment_date is required when status is 'paid'."})
            
            if approved_by and approved_by not in users:
                return json.dumps({"error": f"User with ID {approved_by} not found."})

            record_to_update = expense_reimbursements[reimbursement_id]
            record_to_update["status"] = status
            
            if approved_by:
                record_to_update["approved_by"] = approved_by
            if payment_date:
                record_to_update["payment_date"] = payment_date
            
            record_to_update["updated_at"] = timestamp
            return json.dumps(record_to_update)

        else:
            return json.dumps({"error": "Invalid operation. Must be 'create' or 'update'."})

    @staticmethod
    def manage_leave_requests_invoke(
        data: Dict[str, Any],
        operation: str,
        employee_id: Optional[str] = None,
        leave_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        days_requested: Optional[float] = None,
        leave_id: Optional[str] = None,
        status: Optional[str] = None,
        approved_by: Optional[str] = None,
    ) -> str:
        """
        Executes the specified operation (create or update) on leave requests.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        leave_requests = data.get("leave_requests", {})
        employees = data.get("employees", {})
        users = data.get("users", {})

        if operation == "create":
            if not all([employee_id, leave_type, start_date, end_date, days_requested]):
                return json.dumps({"error": "Missing required parameters for create operation."})
            
            if employee_id not in employees:
                return json.dumps({"error": f"Employee with ID {employee_id} not found."})
            
            # --- Start of revised validation logic ---
            try:
                start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

                if start_date_obj > end_date_obj:
                    return json.dumps({"error": "Validation failed: The start_date cannot be after the end_date."})
            except ValueError:
                return json.dumps({"error": "Invalid date format. Please use YYYY-MM-DD."})
            # --- End of revised validation logic ---
            
            valid_leave_types = ["annual", "sick", "fmla", "personal", "bereavement", "jury_duty"]
            if leave_type not in valid_leave_types:
                return json.dumps({"error": f"Invalid leave type. Must be one of {valid_leave_types}."})

            new_leave_id = generate_id(leave_requests)
            new_request = {
                "leave_id": new_leave_id,
                "employee_id": employee_id,
                "leave_type": leave_type,
                "start_date": start_date,
                "end_date": end_date,
                "days_requested": days_requested,
                "status": "pending",
                "approved_by": None,
                "approval_date": None,
                "created_at": timestamp,
                "updated_at": timestamp,
            }
            leave_requests[new_leave_id] = new_request
            return json.dumps(new_request)

        elif operation == "update":
            if not all([leave_id, status, approved_by]):
                return json.dumps({"error": "Missing required parameters for update operation."})

            if leave_id not in leave_requests:
                return json.dumps({"error": f"Leave request with ID {leave_id} not found."})
            
            if approved_by not in users:
                return json.dumps({"error": f"User with ID {approved_by} not found."})

            valid_statuses = ["approved", "rejected", "cancelled"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}."})

            request_to_update = leave_requests[leave_id]
            request_to_update["status"] = status
            request_to_update["approved_by"] = approved_by
            request_to_update["approval_date"] = timestamp
            request_to_update["updated_at"] = timestamp
            return json.dumps(request_to_update)

        else:
            return json.dumps({"error": "Invalid operation. Must be 'create' or 'update'."})

    @staticmethod
    def discover_user_employee_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover user and employee entities. The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - employees: Employee records by employee_id, user_id, position_id, hire_date, employment_status, manager_id, date_of_birth, address, hourly_rate, created_at, updated_at
        - users: User records by user_id, first_name, last_name, email, phone_number, role, status, mfa_enabled, created_at, updated_at
        """
        if entity_type not in ["employees", "users"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'employees' or 'users'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    # Add appropriate ID field based on entity type
                    id_field = "employee_id" if entity_type == "employees" else "user_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                id_field = "employee_id" if entity_type == "employees" else "user_id"
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def discover_expense_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover expense entities.
        
        Supported entities:
        - expense_reimbursements: Expense reimbursements by reimbursement_id, employee_id, expense_date, amount, expense_type, receipt_file_path, status, approved_by, payment_date, created_at, updated_at
        """
        if entity_type not in ["expense_reimbursements"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'expense_reimbursements'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("expense_reimbursements", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "reimbursement_id": entity_id})
            else:
                results.append({**entity_data, "reimbursement_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def discover_document_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover document entities.
        
        Supported entities:
        - document_storage: Document storage records by document_id, document_name, document_type, employee_id, file_path, upload_date, uploaded_by, confidentiality_level, retention_period_years, expiry_date, status, created_at
        """
        if entity_type not in ["document_storage"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'document_storage'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("document_storage", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "document_id": entity_id})
            else:
                results.append({**entity_data, "document_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_job_position_invoke(
        data: Dict[str, Any],
        action: str,
        position_id: Optional[str] = None,
        title: Optional[str] = None,
        department_id: Optional[str] = None,
        job_level: Optional[str] = None,
        employment_type: Optional[str] = None,
        status: Optional[str] = None,
        hourly_rate_min: Optional[float] = None,
        hourly_rate_max: Optional[float] = None,
    ) -> str:
        """
        Executes the specified action (create or update) on job position records.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        job_positions = data.get("job_positions", {})
        departments = data.get("departments", {})

        # Validate supported job levels
        supported_job_levels = ["entry", "junior", "mid", "senior", "lead", "manager", "director", "executive"]
        
        # Validate supported employment types
        supported_employment_types = ["full_time", "part_time", "contract", "intern"]
        
        # Validate supported statuses
        supported_statuses = ["draft", "open", "closed"]

        if action == "create":
            # Required fields for job position creation
            if not all([title, department_id, job_level, employment_type, status]):
                return json.dumps({
                    "error": "Missing required parameters for create operation. Required: title, department_id, job_level, employment_type, status"
                })

            # Validate department_id exists
            if department_id not in departments:
                return json.dumps({
                    "error": f"Department with ID '{department_id}' not found"
                })

            # Validate job_level
            if job_level not in supported_job_levels:
                return json.dumps({
                    "error": f"Invalid job_level '{job_level}'. Must be one of: {', '.join(supported_job_levels)}"
                })

            # Validate employment_type
            if employment_type not in supported_employment_types:
                return json.dumps({
                    "error": f"Invalid employment_type '{employment_type}'. Must be one of: {', '.join(supported_employment_types)}"
                })

            # Validate status
            if status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Validate hourly rates if provided
            if hourly_rate_min is not None and hourly_rate_min < 0:
                return json.dumps({
                    "error": "hourly_rate_min must be non-negative"
                })

            if hourly_rate_max is not None and hourly_rate_max < 0:
                return json.dumps({
                    "error": "hourly_rate_max must be non-negative"
                })

            if (hourly_rate_min is not None and hourly_rate_max is not None and 
                hourly_rate_min > hourly_rate_max):
                return json.dumps({
                    "error": "hourly_rate_min cannot be greater than hourly_rate_max"
                })

            # Generate new position ID
            new_position_id = generate_id(job_positions)

            # Create new job position record
            new_position = {
                "position_id": new_position_id,
                "title": title,
                "department_id": department_id,
                "job_level": job_level,
                "employment_type": employment_type,
                "status": status,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Add hourly rates if provided
            if hourly_rate_min is not None:
                new_position["hourly_rate_min"] = hourly_rate_min
            
            if hourly_rate_max is not None:
                new_position["hourly_rate_max"] = hourly_rate_max

            # Add to job positions data
            job_positions[new_position_id] = new_position

            return json.dumps({
                "success": True,
                "message": f"Job position created successfully with ID {new_position_id}",
                "position_id": new_position_id,
                "position_data": new_position
            })

        elif action == "update":
            # position_id is required for update
            if not position_id:
                return json.dumps({
                    "error": "Missing required parameter 'position_id' for update operation"
                })

            # Check if position exists
            if position_id not in job_positions:
                return json.dumps({
                    "error": f"Job position with ID {position_id} not found"
                })

            position_to_update = job_positions[position_id]

            # Validate department_id if being updated
            if department_id and department_id not in departments:
                return json.dumps({
                    "error": f"Department with ID '{department_id}' not found"
                })

            # Validate job_level if being updated
            if job_level and job_level not in supported_job_levels:
                return json.dumps({
                    "error": f"Invalid job_level '{job_level}'. Must be one of: {', '.join(supported_job_levels)}"
                })

            # Validate employment_type if being updated
            if employment_type and employment_type not in supported_employment_types:
                return json.dumps({
                    "error": f"Invalid employment_type '{employment_type}'. Must be one of: {', '.join(supported_employment_types)}"
                })

            # Validate status if being updated
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Validate hourly rates if being updated
            if hourly_rate_min is not None and hourly_rate_min < 0:
                return json.dumps({
                    "error": "hourly_rate_min must be non-negative"
                })

            if hourly_rate_max is not None and hourly_rate_max < 0:
                return json.dumps({
                    "error": "hourly_rate_max must be non-negative"
                })

            # Check rate relationship if both are being updated
            current_min = position_to_update.get("hourly_rate_min")
            current_max = position_to_update.get("hourly_rate_max")
            
            effective_min = hourly_rate_min if hourly_rate_min is not None else current_min
            effective_max = hourly_rate_max if hourly_rate_max is not None else current_max
            
            if (effective_min is not None and effective_max is not None and 
                effective_min > effective_max):
                return json.dumps({
                    "error": "hourly_rate_min cannot be greater than hourly_rate_max"
                })

            # Track what fields are being updated
            updated_fields = []

            # Update fields if provided
            if title:
                position_to_update["title"] = title
                updated_fields.append("title")
            
            if department_id:
                position_to_update["department_id"] = department_id
                updated_fields.append("department_id")
            
            if job_level:
                position_to_update["job_level"] = job_level
                updated_fields.append("job_level")
            
            if employment_type:
                position_to_update["employment_type"] = employment_type
                updated_fields.append("employment_type")
            
            if status:
                position_to_update["status"] = status
                updated_fields.append("status")
            
            if hourly_rate_min is not None:
                position_to_update["hourly_rate_min"] = hourly_rate_min
                updated_fields.append("hourly_rate_min")
            
            if hourly_rate_max is not None:
                position_to_update["hourly_rate_max"] = hourly_rate_max
                updated_fields.append("hourly_rate_max")

            # Update timestamp
            position_to_update["updated_at"] = timestamp

            if not updated_fields:
                return json.dumps({
                    "error": "No fields provided to update. At least one optional field must be provided"
                })

            return json.dumps({
                "success": True,
                "message": f"Job position {position_id} updated successfully",
                "updated_fields": updated_fields,
                "position_data": position_to_update
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

    @staticmethod
    def manage_employee_training_invoke(
        data: Dict[str, Any],
        operation: str,
        employee_id: Optional[str] = None,
        program_id: Optional[str] = None,
        enrollment_date: Optional[str] = None,
        training_record_id: Optional[str] = None,
        status: Optional[str] = None,
        completion_date: Optional[str] = None,
        score: Optional[float] = None,
        certificate_issued: Optional[bool] = None,
        expiry_date: Optional[str] = None,
    ) -> str:
        """
        Executes the specified operation (create or update) on employee training records.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        employee_trainings = data.get("employee_training", {})
        employees = data.get("employees", {})
        programs = data.get("training_programs", {})

        if operation == "create":
            if not all([employee_id, program_id, enrollment_date]):
                return json.dumps({"error": "Missing required parameters for create operation."})

            if employee_id not in employees:
                return json.dumps({"error": f"Employee with ID {employee_id} not found."})
            if program_id not in programs:
                return json.dumps({"error": f"Training program with ID {program_id} not found."})

            new_record_id = generate_id(employee_trainings)
            new_record = {
                "training_record_id": new_record_id,
                "employee_id": employee_id,
                "program_id": program_id,
                "enrollment_date": enrollment_date,
                "status": "enrolled",
                "completion_date": None,
                "score": None,
                "certificate_issued": False,
                "expiry_date": None,
                "created_at": timestamp,
                "updated_at": timestamp,
            }
            employee_trainings[new_record_id] = new_record
            return json.dumps(new_record)

        elif operation == "update":
            if not all([training_record_id, status]):
                return json.dumps({"error": "Missing required parameters for update operation."})
            
            if training_record_id not in employee_trainings:
                return json.dumps({"error": f"Training record with ID {training_record_id} not found."})
            
            valid_statuses = ["in_progress", "completed", "failed", "cancelled"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}."})

            record_to_update = employee_trainings[training_record_id]
            record_to_update["status"] = status
            if completion_date is not None:
                record_to_update["completion_date"] = completion_date
            if score is not None:
                record_to_update["score"] = score
            if certificate_issued is not None:
                record_to_update["certificate_issued"] = certificate_issued
            if expiry_date is not None:
                record_to_update["expiry_date"] = expiry_date
            
            record_to_update["updated_at"] = timestamp
            return json.dumps(record_to_update)

        else:
            return json.dumps({"error": "Invalid operation. Must be 'create' or 'update'."})

    @staticmethod
    def manage_performance_review_invoke(data: Dict[str, Any], action: str, review_data: Dict[str, Any] = None, review_id: str = None) -> str:
        """
        Create or update performance review records.
        
        Actions:
        - create: Create new performance review (requires review_data with employee_id, reviewer_id, review_period_start, review_period_end, review_type, overall_rating)
        - update: Update existing performance review (requires review_id, review_data)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
            
        def is_valid_date_order(start_date: str, end_date: str) -> bool:
            """Check if start date is before end date - simplified for demo"""
            return start_date <= end_date
            
        def is_valid_status_progression(current_status: str, new_status: str) -> bool:
            """Validate status progression follows proper workflow"""
            # Define proper progression: draft → submitted → approved
            workflow_order = ["draft", "submitted", "approved"]
            
            if current_status not in workflow_order or new_status not in workflow_order:
                return False
            
            current_index = workflow_order.index(current_status)
            new_index = workflow_order.index(new_status)
            
            # Can only move forward or stay the same
            return new_index >= current_index
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for performance reviews"
            })
        
        performance_reviews = data.get("performance_reviews", {})
        employees = data.get("employees", {})
        users = data.get("users", {})
        
        if action == "create":
            if not review_data:
                return json.dumps({
                    "success": False,
                    "error": "review_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["employee_id", "reviewer_id", "review_period_start", "review_period_end", "review_type", "overall_rating"]
            missing_fields = [field for field in required_fields if field not in review_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or reviewer not found or inactive - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that employee exists and has active status
            employee_id = str(review_data["employee_id"])
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or reviewer not found or inactive"
                })
            
            employee = employees[employee_id]
            if employee.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or reviewer not found or inactive"
                })
            
            # Validate that reviewer exists and has active status
            reviewer_id = str(review_data["reviewer_id"])
            if reviewer_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or reviewer not found or inactive"
                })
            
            reviewer = users[reviewer_id]
            if reviewer.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or reviewer not found or inactive"
                })
            
            # Validate that review period dates are logical (start date before end date)
            review_period_start = review_data["review_period_start"]
            review_period_end = review_data["review_period_end"]
            if not is_valid_date_order(review_period_start, review_period_end):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid review period dates or type - start date must be before end date"
                })
            
            # Validate review_type is within accepted categories according to schema
            valid_types = ["annual", "quarterly", "probationary", "project_based"]
            if review_data["review_type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid review period dates or type - review_type must be one of: {', '.join(valid_types)}"
                })
            
            # Validate overall_rating according to schema
            valid_ratings = ["exceeds_expectations", "meets_expectations", "below_expectations", "unsatisfactory"]
            if review_data["overall_rating"] not in valid_ratings:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid rating or scores - overall_rating must be one of: {', '.join(valid_ratings)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["employee_id", "reviewer_id", "review_period_start", "review_period_end", 
                            "review_type", "overall_rating", "goals_achievement_score", "communication_score",
                            "teamwork_score", "leadership_score", "technical_skills_score", "status"]
            invalid_fields = [field for field in review_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for performance review creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new review ID
            new_review_id = generate_id(performance_reviews)
            
            # Create performance review with required information
            new_review = {
                "review_id": str(new_review_id),
                "employee_id": employee_id,
                "reviewer_id": reviewer_id,
                "review_period_start": review_period_start,
                "review_period_end": review_period_end,
                "review_type": review_data["review_type"],
                "overall_rating": review_data["overall_rating"],
                "goals_achievement_score": review_data.get("goals_achievement_score"),
                "communication_score": review_data.get("communication_score"),
                "teamwork_score": review_data.get("teamwork_score"),
                "leadership_score": review_data.get("leadership_score"),
                "technical_skills_score": review_data.get("technical_skills_score"),
                "status": review_data.get("status", "draft"),  # If status is not specified during creation, set it to draft
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            performance_reviews[str(new_review_id)] = new_review
            
            return json.dumps({
                "success": True,
                "action": "create",
                "review_id": str(new_review_id),
                "message": f"Performance review {new_review_id} created successfully",
                "review_data": new_review
            })
        
        elif action == "update":
            if not review_id:
                return json.dumps({
                    "success": False,
                    "error": "review_id is required for update action"
                })
            
            if review_id not in performance_reviews:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Performance review not found"
                })
            
            if not review_data:
                return json.dumps({
                    "success": False,
                    "error": "review_data is required for update action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["employee_id", "reviewer_id", "review_period_start", "review_period_end", "review_type", "overall_rating", "goals_achievement_score", "communication_score", "teamwork_score", "leadership_score", "technical_skills_score", "status"]
            provided_fields = [field for field in update_fields if field in review_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Get current review for validation
            current_review = performance_reviews[review_id]
            current_status = current_review.get("status", "draft")
            
            # Validate only allowed fields for updates
            invalid_fields = [field for field in review_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for performance review update: {', '.join(invalid_fields)}"
                })
            
            # Validate status transitions follow proper workflow if status is being updated
            if "status" in review_data:
                new_status = review_data["status"]
                valid_statuses = ["draft", "submitted", "approved"]
                
                if new_status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Performance review operation failed - status must be one of: {', '.join(valid_statuses)}"
                    })
                
                # Update status through proper progression (draft to submitted to approved)
                if not is_valid_status_progression(current_status, new_status):
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Performance review operation failed - invalid status transition from {current_status} to {new_status}"
                    })
            
            # Validate overall_rating if provided
            if "overall_rating" in review_data:
                valid_ratings = ["exceeds_expectations", "meets_expectations", "below_expectations", "unsatisfactory"]
                if review_data["overall_rating"] not in valid_ratings:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Performance review operation failed - overall_rating must be one of: {', '.join(valid_ratings)}"
                    })
            
            # Validate review_type if provided
            if "review_type" in review_data:
                valid_types = ["annual", "quarterly", "probationary", "project_based"]
                if review_data["review_type"] not in valid_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Performance review operation failed - review_type must be one of: {', '.join(valid_types)}"
                    })
            
            # Update performance review
            updated_review = current_review.copy()
            for key, value in review_data.items():
                updated_review[key] = value
            
            updated_review["updated_at"] = "2025-10-01T12:00:00"
            performance_reviews[review_id] = updated_review
            
            return json.dumps({
                "success": True,
                "action": "update",
                "review_id": review_id,
                "message": f"Performance review {review_id} updated successfully",
                "review_data": updated_review
            })

    @staticmethod
    def manage_job_position_skills_invoke(
        data: Dict[str, Any],
        action: str,
        position_id: str,
        skill_id: Optional[str] = None,
    ) -> str:
        """
        Executes the specified action (add or remove) on job position skills associations.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        job_positions = data.get("job_positions", {})
        job_position_skills = data.get("job_position_skills", {})
        skills = data.get("skills", {})

        # Validate position exists
        if position_id not in job_positions:
            return json.dumps({
                "error": f"Job position with ID '{position_id}' not found"
            })

        if action == "add":
            # skill_id is required for add
            if not skill_id:
                return json.dumps({
                    "error": "Missing required parameter 'skill_id' for add operation"
                })

            # Validate skill exists
            if skill_id not in skills:
                return json.dumps({
                    "error": f"Skill with ID '{skill_id}' not found"
                })

            # Check if association already exists
            for existing_association in job_position_skills.values():
                if (existing_association.get("position_id") == position_id and 
                    existing_association.get("skill_id") == skill_id):
                    return json.dumps({
                        "error": f"Skill {skill_id} is already associated with position {position_id}"
                    })

            # Generate new association ID
            new_association_id = generate_id(job_position_skills)

            # Create new association
            new_association = {
                "position_id": position_id,
                "skill_id": skill_id
            }

            # Add to job position skills data
            job_position_skills[new_association_id] = new_association

            return json.dumps({
                "success": True,
                "message": f"Skill {skill_id} added to position {position_id} successfully",
                "association_id": new_association_id,
                "association_data": new_association
            })

        elif action == "remove":
            # skill_id is required for remove
            if not skill_id:
                return json.dumps({
                    "error": "Missing required parameter 'skill_id' for remove operation"
                })

            # Find the association to remove
            association_to_remove = None
            association_id_to_remove = None
            
            for assoc_id, association in job_position_skills.items():
                if (association.get("position_id") == position_id and 
                    association.get("skill_id") == skill_id):
                    association_to_remove = association
                    association_id_to_remove = assoc_id
                    break

            if not association_to_remove:
                return json.dumps({
                    "error": f"No association found between position {position_id} and skill {skill_id}"
                })

            # Remove the association
            del job_position_skills[association_id_to_remove]

            return json.dumps({
                "success": True,
                "message": f"Skill {skill_id} removed from position {position_id} successfully",
                "removed_association_id": association_id_to_remove
            })

        elif action == "list":
            # List all skills associated with the position
            associated_skills = []
            
            for association in job_position_skills.values():
                if association.get("position_id") == position_id:
                    skill_id = association.get("skill_id")
                    skill_info = skills.get(skill_id, {})
                    associated_skills.append({
                        "skill_id": skill_id,
                        "skill_name": skill_info.get("skill_name", "Unknown"),
                        "skill_category": skill_info.get("category", "Unknown")
                    })

            return json.dumps({
                "success": True,
                "message": f"Found {len(associated_skills)} skills associated with position {position_id}",
                "position_id": position_id,
                "associated_skills": associated_skills
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'add', 'remove', or 'list'"
            })

    @staticmethod
    def manage_department_invoke(
        data: Dict[str, Any],
        action: str,
        department_id: Optional[str] = None,
        department_name: Optional[str] = None,
        manager_id: Optional[str] = None,
        budget: Optional[float] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Executes the specified action (create or update) on department records.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        departments = data.get("departments", {})
        users = data.get("users", {})

        # Validate supported statuses
        supported_statuses = ["active", "inactive"]

        if action == "create":
            # Required fields for department creation
            if not all([department_name, manager_id]):
                return json.dumps({
                    "error": "Missing required parameters for create operation. Required: department_name, manager_id"
                })

            # Validate manager_id exists in users
            if manager_id not in users:
                return json.dumps({
                    "error": f"Manager with ID '{manager_id}' not found in users"
                })

            # Validate status if provided
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Check for duplicate department name
            for existing_dept in departments.values():
                if existing_dept.get("department_name") == department_name:
                    return json.dumps({
                        "error": f"Department with name '{department_name}' already exists"
                    })

            # Generate new department ID
            new_department_id = generate_id(departments)

            # Create new department record
            new_department = {
                "department_id": new_department_id,
                "department_name": department_name,
                "manager_id": manager_id,
                "status": status or "active",  # Default to active if not specified
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Add budget if provided
            if budget is not None:
                if budget < 0:
                    return json.dumps({
                        "error": "Budget must be a non-negative value"
                    })
                new_department["budget"] = budget

            # Add to departments data
            departments[new_department_id] = new_department

            return json.dumps({
                "success": True,
                "message": f"Department created successfully with ID {new_department_id}",
                "department_id": new_department_id,
                "department_data": new_department
            })

        elif action == "update":
            # department_id is required for update
            if not department_id:
                return json.dumps({
                    "error": "Missing required parameter 'department_id' for update operation"
                })

            # Check if department exists
            if department_id not in departments:
                return json.dumps({
                    "error": f"Department with ID {department_id} not found"
                })

            department_to_update = departments[department_id]

            # Validate manager_id if being updated
            if manager_id and manager_id not in users:
                return json.dumps({
                    "error": f"Manager with ID '{manager_id}' not found in users"
                })

            # Validate status if being updated
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Check for duplicate department name if name is being changed
            if department_name and department_name != department_to_update.get("department_name"):
                for existing_dept in departments.values():
                    if existing_dept.get("department_name") == department_name:
                        return json.dumps({
                            "error": f"Department with name '{department_name}' already exists"
                        })

            # Validate budget if provided
            if budget is not None and budget < 0:
                return json.dumps({
                    "error": "Budget must be a non-negative value"
                })

            # Track what fields are being updated
            updated_fields = []

            # Update fields if provided
            if department_name:
                department_to_update["department_name"] = department_name
                updated_fields.append("department_name")
            
            if manager_id:
                department_to_update["manager_id"] = manager_id
                updated_fields.append("manager_id")
            
            if budget is not None:
                department_to_update["budget"] = budget
                updated_fields.append("budget")
            
            if status:
                department_to_update["status"] = status
                updated_fields.append("status")

            # Update timestamp
            department_to_update["updated_at"] = timestamp

            if not updated_fields:
                return json.dumps({
                    "error": "No fields provided to update. At least one optional field must be provided"
                })

            return json.dumps({
                "success": True,
                "message": f"Department {department_id} updated successfully",
                "updated_fields": updated_fields,
                "department_data": department_to_update
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

    @staticmethod
    def manage_interview_invoke(data: Dict[str, Any], action: str, interview_data: Dict[str, Any] = None, interview_id: str = None) -> str:
        """
        Create or update interview records.
        
        Actions:
        - create: Schedule new interview (requires interview_data with application_id, interviewer_id, interview_type, scheduled_date)
        - update: Record interview outcome (requires interview_id and interview_data with outcome details)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
            
        def is_future_datetime(datetime_str: str) -> bool:
            """Check if datetime is in future - simplified for demo"""
            # In real implementation, would compare with current datetime
            # For demo purposes, assume dates starting with "2024" or earlier are not future
            return not (datetime_str.startswith("2024") or datetime_str.startswith("2023"))
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for interviews"
            })
        
        interviews = data.get("interviews", {})
        job_applications = data.get("job_applications", {})
        users = data.get("users", {})
        
        if action == "create":
            if not interview_data:
                return json.dumps({
                    "success": False,
                    "error": "interview_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["application_id", "interviewer_id", "interview_type", "scheduled_date"]
            missing_fields = [field for field in required_fields if field not in interview_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid interview scheduling details - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that application exists
            application_id = str(interview_data["application_id"])
            if application_id not in job_applications:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Application or interviewer not found"
                })
            
            # Validate that interviewer exists
            interviewer_id = str(interview_data["interviewer_id"])
            if interviewer_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Application or interviewer not found"
                })
            
            # Validate interview_type enum according to schema
            valid_types = ["phone_screening", "technical", "behavioral", "panel", "final"]
            if interview_data["interview_type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid interview type or scheduled date - interview_type must be one of: {', '.join(valid_types)}"
                })
            
            # Validate that scheduled date and time is in the future
            scheduled_date = interview_data["scheduled_date"]
            if not is_future_datetime(scheduled_date):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid interview type or scheduled date - scheduled date must be in the future"
                })
            
            # Validate that duration is positive time value with reasonable default
            duration_minutes = interview_data.get("duration_minutes", 60)  # Standard duration default
            if not isinstance(duration_minutes, (int, float)) or duration_minutes <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid interview scheduling details - duration must be positive"
                })
            
            # Validate only allowed fields are present for creation
            allowed_fields = ["application_id", "interviewer_id", "interview_type", "scheduled_date", 
                            "duration_minutes", "status"]
            invalid_fields = [field for field in interview_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for interview creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new interview ID
            new_interview_id = generate_id(interviews)
            
            # Create new interview record
            new_interview = {
                "interview_id": str(new_interview_id),
                "application_id": application_id,
                "interviewer_id": interviewer_id,
                "interview_type": interview_data["interview_type"],
                "scheduled_date": scheduled_date,
                "duration_minutes": duration_minutes,
                "status": interview_data.get("status", "scheduled"),  # If status is not specified, set it to scheduled
                "overall_rating": None,
                "technical_score": None,
                "communication_score": None,
                "cultural_fit_score": None,
                "recommendation": None,
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            interviews[str(new_interview_id)] = new_interview
            
            return json.dumps({
                "success": True,
                "action": "create",
                "interview_id": str(new_interview_id),
                "message": f"Interview {new_interview_id} scheduled successfully",
                "interview_data": new_interview
            })
        
        elif action == "update":
            if not interview_id:
                return json.dumps({
                    "success": False,
                    "error": "interview_id is required for update action"
                })
            
            if interview_id not in interviews:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Interview not found or invalid status"
                })
            
            if not interview_data:
                return json.dumps({
                    "success": False,
                    "error": "interview_data is required for update action"
                })
            
            # Get current interview for validation
            current_interview = interviews[interview_id]
            current_status = current_interview.get("status")
            
            # Validate that interview has scheduled or completed status
            if current_status not in ["scheduled", "completed"]:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Interview not found or invalid status"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["overall_rating", "technical_score", "communication_score", 
                           "cultural_fit_score", "recommendation", "status"]
            provided_fields = [field for field in update_fields if field in interview_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Validate only allowed fields for updates (outcome recording)
            invalid_fields = [field for field in interview_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for interview outcome recording: {', '.join(invalid_fields)}"
                })
            
            # Validate overall rating is within accepted scale if provided
            if "overall_rating" in interview_data:
                valid_ratings = ["excellent", "good", "average", "below_average", "poor"]
                if interview_data["overall_rating"] not in valid_ratings:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid rating, scores, or recommendation - overall_rating must be one of: {', '.join(valid_ratings)}"
                    })
            
            # Validate individual scores are within acceptable numeric range if provided
            score_fields = ["technical_score", "communication_score", "cultural_fit_score"]
            for score_field in score_fields:
                if score_field in interview_data:
                    score = interview_data[score_field]
                    if score is not None and (not isinstance(score, (int, float)) or score < 0 or score > 10):
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Invalid rating, scores, or recommendation - {score_field} must be within 0-10 range"
                        })
            
            # Validate recommendation is within accepted options if provided
            if "recommendation" in interview_data:
                valid_recommendations = ["strong_hire", "hire", "no_hire", "strong_no_hire"]
                if interview_data["recommendation"] not in valid_recommendations:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid rating, scores, or recommendation - recommendation must be one of: {', '.join(valid_recommendations)}"
                    })
            
            # Validate status if provided
            if "status" in interview_data:
                valid_statuses = ["scheduled", "completed", "cancelled", "no_show"]
                if interview_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid status - must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Update interview record with outcome information
            updated_interview = current_interview.copy()
            for key, value in interview_data.items():
                updated_interview[key] = value
            
            # If status is not specified, set it to completed when outcome is being recorded
            if "status" not in interview_data and any(field in interview_data for field in ["overall_rating", "recommendation"]):
                updated_interview["status"] = "completed"
            
            updated_interview["updated_at"] = "2025-10-01T12:00:00"
            interviews[interview_id] = updated_interview
            
            # Update related job application status based on interview outcome
            application_id = current_interview.get("application_id")
            if application_id and application_id in job_applications:
                application = job_applications[application_id]
                current_app_status = application.get("status")
                new_app_status = current_app_status
                
                recommendation = updated_interview.get("recommendation")
                overall_rating = updated_interview.get("overall_rating")
                interview_type = updated_interview.get("interview_type")
                
                # Update job application status based on interview outcome per policy
                if recommendation in ["strong_hire", "hire"]:
                    if current_app_status == "interviewing":
                        new_app_status = "offer_made"
                elif recommendation in ["no_hire", "strong_no_hire"]:
                    new_app_status = "rejected"
                elif not recommendation and overall_rating:
                    # When no recommendation provided, use rating
                    if overall_rating in ["poor", "below_average"]:
                        new_app_status = "rejected"
                    # excellent/good ratings remain at interviewing for potential additional interviews
                
                # Final interviews with positive recommendations automatically advance to offer_made
                if interview_type == "final" and recommendation in ["strong_hire", "hire"]:
                    new_app_status = "offer_made"
                
                # Update application status if changed
                if new_app_status != current_app_status:
                    updated_application = application.copy()
                    updated_application["status"] = new_app_status
                    updated_application["updated_at"] = "2025-10-01T12:00:00"
                    job_applications[application_id] = updated_application
            
            return json.dumps({
                "success": True,
                "action": "update",
                "interview_id": interview_id,
                "message": f"Interview {interview_id} outcome recorded successfully",
                "interview_data": updated_interview
            })

    @staticmethod
    def manage_benefits_plan_invoke(data: Dict[str, Any], action: str, plan_data: Dict[str, Any] = None, plan_id: str = None) -> str:
        """
        Create or update benefits plan records.
        
        Actions:
        - create: Create new benefits plan (requires plan_data with plan_name, plan_type, effective_date)
        - update: Update existing benefits plan (requires plan_id and plan_data with changes)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for benefits plans"
            })
        
        benefits_plans = data.get("benefits_plans", {})
        
        if action == "create":
            if not plan_data:
                return json.dumps({
                    "success": False,
                    "error": "plan_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["plan_name", "plan_type", "effective_date"]
            missing_fields = [field for field in required_fields if field not in plan_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing or invalid inputs - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate plan_type enum according to schema
            valid_types = ["health_insurance", "dental", "vision", "life_insurance", "disability", "retirement_401k", "pto", "flexible_spending"]
            if plan_data["plan_type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid plan type or dates - plan_type must be one of: {', '.join(valid_types)}"
                })
            
            # Validate cost amounts are non-negative monetary values if provided
            for cost_field in ["employee_cost", "employer_cost"]:
                if cost_field in plan_data:
                    cost_value = plan_data[cost_field]
                    if cost_value is not None and (not isinstance(cost_value, (int, float)) or cost_value < 0):
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Invalid plan type or dates - {cost_field} must be non-negative"
                        })
            
            # Validate date consistency - expiration date must occur after effective date if provided
            effective_date = plan_data["effective_date"]
            expiration_date = plan_data.get("expiration_date")
            if expiration_date and expiration_date <= effective_date:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid plan type or dates - expiration date must be after effective date"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["plan_name", "plan_type", "provider", "employee_cost", "employer_cost", 
                            "status", "effective_date", "expiration_date"]
            invalid_fields = [field for field in plan_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for benefits plan creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new plan ID
            new_plan_id = generate_id(benefits_plans)
            
            # Create new benefits plan
            new_plan = {
                "plan_id": str(new_plan_id),
                "plan_name": plan_data["plan_name"],
                "plan_type": plan_data["plan_type"],
                "provider": plan_data.get("provider"),
                "employee_cost": plan_data.get("employee_cost"),
                "employer_cost": plan_data.get("employer_cost"),
                "status": plan_data.get("status", "active"),  # If status is not specified during creation, set it to active
                "effective_date": plan_data["effective_date"],
                "expiration_date": plan_data.get("expiration_date"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            benefits_plans[str(new_plan_id)] = new_plan
            
            return json.dumps({
                "success": True,
                "action": "create",
                "plan_id": str(new_plan_id),
                "message": f"Benefits plan {new_plan_id} created successfully",
                "plan_data": new_plan
            })
        
        elif action == "update":
            if not plan_id:
                return json.dumps({
                    "success": False,
                    "error": "plan_id is required for update action"
                })
            
            if plan_id not in benefits_plans:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Plan not found"
                })
            
            if not plan_data:
                return json.dumps({
                    "success": False,
                    "error": "plan_data is required for update action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["plan_name", "plan_type", "provider", "employee_cost", "employer_cost", 
                           "status", "effective_date", "expiration_date"]
            provided_fields = [field for field in update_fields if field in plan_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Get current plan for validation
            current_plan = benefits_plans[plan_id]
            
            # Validate only allowed fields for updates
            invalid_fields = [field for field in plan_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for benefits plan update: {', '.join(invalid_fields)}"
                })
            
            # Validate status enum if provided
            if "status" in plan_data:
                valid_statuses = ["active", "inactive"]
                if plan_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Benefits plan operation failed - status must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate plan_type enum if provided
            if "plan_type" in plan_data:
                valid_types = ["health_insurance", "dental", "vision", "life_insurance", "disability", "retirement_401k", "pto", "flexible_spending"]
                if plan_data["plan_type"] not in valid_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Benefits plan operation failed - plan_type must be one of: {', '.join(valid_types)}"
                    })
            
            # Validate cost amounts are non-negative monetary values if provided
            for cost_field in ["employee_cost", "employer_cost"]:
                if cost_field in plan_data:
                    cost_value = plan_data[cost_field]
                    if cost_value is not None and (not isinstance(cost_value, (int, float)) or cost_value < 0):
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Benefits plan operation failed - {cost_field} must be non-negative"
                        })
            
            # Validate date consistency
            effective_date = plan_data.get("effective_date", current_plan.get("effective_date"))
            expiration_date = plan_data.get("expiration_date", current_plan.get("expiration_date"))
            
            if effective_date and expiration_date and expiration_date <= effective_date:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Benefits plan operation failed - expiration date must be after effective date"
                })
            
            # Update benefits plan
            updated_plan = current_plan.copy()
            for key, value in plan_data.items():
                updated_plan[key] = value
            
            updated_plan["updated_at"] = "2025-10-01T12:00:00"
            benefits_plans[plan_id] = updated_plan
            
            return json.dumps({
                "success": True,
                "action": "update",
                "plan_id": plan_id,
                "message": f"Benefits plan {plan_id} updated successfully",
                "plan_data": updated_plan
            })

    @staticmethod
    def manage_document_storage_invoke(
        data: Dict[str, Any],
        operation: str,
        document_id: Optional[str] = None,
        document_name: Optional[str] = None,
        document_type: Optional[str] = None,
        file_path: Optional[str] = None,
        uploaded_by: Optional[str] = None,
        employee_id: Optional[str] = None,
        confidentiality_level: Optional[str] = 'internal',
        retention_period_years: Optional[int] = 7,
        status: Optional[str] = None,
        expiry_date: Optional[str] = None,
    ) -> str:
        """
        Executes the specified operation (create or update) on documents.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)


        timestamp = "2025-10-01T12:00:00"
        documents = data.get("documents", {})
        users = data.get("users", {})
        employees = data.get("employees", {})

        if operation == "create":
            if not all([document_name, document_type, file_path, uploaded_by]):
                return json.dumps({"error": "Missing required parameters for create operation."})
            
            if uploaded_by not in users:
                return json.dumps({"error": f"User with ID {uploaded_by} not found."})
            if employee_id and employee_id not in employees:
                return json.dumps({"error": f"Employee with ID {employee_id} not found."})

            valid_types = ["contract", "policy", "handbook", "form", "certificate", "report", "resume", "offer_letter"]
            if document_type not in valid_types:
                return json.dumps({"error": f"Invalid document type. Must be one of {valid_types}."})

            new_doc_id = generate_id(documents)
            new_document = {
                "document_id": new_doc_id,
                "document_name": document_name,
                "document_type": document_type,
                "employee_id": employee_id,
                "file_path": file_path,
                "upload_date": timestamp,
                "uploaded_by": uploaded_by,
                "confidentiality_level": confidentiality_level,
                "retention_period_years": retention_period_years,
                "expiry_date": expiry_date,
                "status": "active",
                "created_at": timestamp,
            }
            documents[new_doc_id] = new_document
            return json.dumps(new_document)

        elif operation == "update":
            if not all([document_id, status]):
                return json.dumps({"error": "Missing required parameters for update operation."})
            
            if document_id not in documents:
                return json.dumps({"error": f"Document with ID {document_id} not found."})

            valid_statuses = ["active", "archived", "deleted"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}."})
            
            doc_to_update = documents[document_id]
            doc_to_update["status"] = status
            if document_name is not None:
                doc_to_update["document_name"] = document_name
            if confidentiality_level is not None:
                doc_to_update["confidentiality_level"] = confidentiality_level
            if expiry_date is not None:
                doc_to_update["expiry_date"] = expiry_date
            
            return json.dumps(doc_to_update)

        else:
            return json.dumps({"error": "Invalid operation. Must be 'create' or 'update'."})

    @staticmethod
    def discover_recruitment_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover recruitment entities.
        
        Supported entities:
        - candidates: Candidate records by candidate_id, first_name, last_name, email, phone_number, address, source, status, created_at, updated_at
        - job_applications: Job application records by application_id, candidate_id, position_id, application_date, status, recruiter_id, ai_screening_score, final_decision, created_at, updated_at
        - interviews: Interview records by interview_id, application_id, interviewer_id, interview_type, scheduled_date, duration_minutes, status, overall_rating, technical_score, communication_score, cultural_fit_score, recommendation, created_at, updated_at
        """
        if entity_type not in ["candidates", "job_applications", "interviews"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be one of: 'candidates', 'job_applications', 'interviews'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        # Determine ID field based on entity type
        id_field_map = {
            "candidates": "candidate_id",
            "job_applications": "application_id", 
            "interviews": "interview_id"
        }
        id_field = id_field_map[entity_type]
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_payroll_record_invoke(data: Dict[str, Any], action: str, payroll_data: Dict[str, Any] = None, payroll_id: str = None) -> str:
        """
        Create or update payroll records.
        
        Actions:
        - create: Process payroll run (requires payroll_data with employee_id, pay_period_start, pay_period_end, hourly_rate)
        - update: Payroll correction (requires payroll_id, payroll_data with correction details)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
            
        def is_valid_date_order(start_date: str, end_date: str) -> bool:
            """Check if start date is before end date - simplified for demo"""
            return start_date <= end_date
            
        def aggregate_approved_timesheet_hours(employee_id: str, pay_period_start: str, pay_period_end: str, timesheets: Dict[str, Any]) -> float:
            """Aggregate approved timesheet hours for the specified pay period"""
            total_hours = 0.0
            for timesheet in timesheets.values():
                if (timesheet.get("employee_id") == employee_id and 
                    timesheet.get("status") == "approved" and
                    pay_period_start <= timesheet.get("work_date", "") <= pay_period_end):
                    total_hours += float(timesheet.get("total_hours", 0))
            return total_hours
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payroll records"
            })
        
        payroll_records = data.get("payroll_records", {})
        employees = data.get("employees", {})
        employee_timesheets = data.get("employee_timesheets", {})
        
        if action == "create":
            if not payroll_data:
                return json.dumps({
                    "success": False,
                    "error": "payroll_data is required for create action"
                })
            
            # Validate that all required information is provided: employee, pay period dates
            required_fields = ["employee_id", "pay_period_start", "pay_period_end", "hourly_rate"]
            missing_fields = [field for field in required_fields if field not in payroll_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing or invalid inputs - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that employee exists in system
            employee_id = str(payroll_data["employee_id"])
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing or invalid inputs - employee not found"
                })
            
            # Validate that pay period dates are logical (start date before end date)
            pay_period_start = payroll_data["pay_period_start"]
            pay_period_end = payroll_data["pay_period_end"]
            if not is_valid_date_order(pay_period_start, pay_period_end):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid pay period dates or hourly rate - start date must be before end date"
                })
            
            # Validate that hourly rate is positive monetary value
            try:
                hourly_rate = float(payroll_data["hourly_rate"])
                if hourly_rate <= 0:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid pay period dates or hourly rate - hourly rate must be positive"
                    })
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid pay period dates or hourly rate - invalid hourly rate format"
                })
            
            # Aggregate approved timesheet hours for the specified pay period
            hours_worked = aggregate_approved_timesheet_hours(employee_id, pay_period_start, pay_period_end, employee_timesheets)
            
            # Check if no approved timesheet hours found
            if hours_worked == 0:
                return json.dumps({
                    "success": False,
                    "error": "Halt: No approved timesheet hours found"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["employee_id", "pay_period_start", "pay_period_end", "hourly_rate", 
                            "hours_worked", "payment_date", "status", "approved_by"]
            invalid_fields = [field for field in payroll_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payroll creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new payroll ID
            new_payroll_id = generate_id(payroll_records)
            
            # Calculate hours worked from approved timesheets if not provided
            final_hours_worked = payroll_data.get("hours_worked", hours_worked)
            
            # Create payroll record with required information
            new_payroll = {
                "payroll_id": str(new_payroll_id),
                "employee_id": employee_id,
                "pay_period_start": pay_period_start,
                "pay_period_end": pay_period_end,
                "hours_worked": final_hours_worked,
                "hourly_rate": hourly_rate,
                "payment_date": payroll_data.get("payment_date"),
                "status": payroll_data.get("status", "pending"),  # If status is not specified, set it to pending
                "approved_by": payroll_data.get("approved_by"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            payroll_records[str(new_payroll_id)] = new_payroll
            
            return json.dumps({
                "success": True,
                "action": "create",
                "payroll_id": str(new_payroll_id),
                "message": f"Payroll record {new_payroll_id} created successfully with {final_hours_worked} hours",
                "payroll_data": new_payroll
            })
        
        elif action == "update":
            if not payroll_id:
                return json.dumps({
                    "success": False,
                    "error": "payroll_id is required for update action"
                })
            
            # Validate that payroll record exists in the system
            if payroll_id not in payroll_records:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Payroll record not found"
                })
            
            if not payroll_data:
                return json.dumps({
                    "success": False,
                    "error": "payroll_data is required for update action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["pay_period_start", "pay_period_end", "hours_worked", "hourly_rate", "payment_date", "status", "approved_by"]
            provided_fields = [field for field in update_fields if field in payroll_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Validate only allowed fields for corrections
            invalid_fields = [field for field in payroll_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payroll correction: {', '.join(invalid_fields)}. Cannot update employee_id."
                })
            
            # Validate that correction information is valid (hours worked and hourly rate must be positive)
            if "hours_worked" in payroll_data:
                try:
                    hours_worked = float(payroll_data["hours_worked"])
                    if hours_worked <= 0:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Invalid correction information - hours worked must be positive"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid correction information - invalid hours worked format"
                    })
            
            if "hourly_rate" in payroll_data:
                try:
                    hourly_rate = float(payroll_data["hourly_rate"])
                    if hourly_rate <= 0:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Invalid correction information - hourly rate must be positive"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid correction information - invalid hourly rate format"
                    })
            
            # Validate pay period dates if provided
            current_payroll = payroll_records[payroll_id]
            if "pay_period_start" in payroll_data or "pay_period_end" in payroll_data:
                start_date = payroll_data.get("pay_period_start", current_payroll.get("pay_period_start"))
                end_date = payroll_data.get("pay_period_end", current_payroll.get("pay_period_end"))
                if not is_valid_date_order(start_date, end_date):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid correction information - start date must be before end date"
                    })
            
            # Validate status enum if provided
            if "status" in payroll_data:
                valid_statuses = ["draft", "approved", "paid", "cancelled"]
                if payroll_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid correction information - status must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Adjust payroll record with correction details
            updated_payroll = current_payroll.copy()
            
            for key, value in payroll_data.items():
                updated_payroll[key] = value
            
            updated_payroll["updated_at"] = "2025-10-01T12:00:00"
            payroll_records[payroll_id] = updated_payroll
            
            return json.dumps({
                "success": True,
                "action": "update",
                "payroll_id": payroll_id,
                "message": f"Payroll record {payroll_id} corrected successfully",
                "payroll_data": updated_payroll
            })

    @staticmethod
    def manage_skill_invoke(
        data: Dict[str, Any],
        action: str,
        skill_id: Optional[str] = None,
        skill_name: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Executes the specified action (create or update) on skills.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        skills = data.get("skills", {})

        # Validate supported statuses
        supported_statuses = ["active", "inactive"]

        if action == "create":
            # Required fields for skill creation
            if not skill_name:
                return json.dumps({
                    "error": "Missing required parameter 'skill_name' for create operation"
                })

            # Validate status if provided
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Check for duplicate skill names
            for existing_skill in skills.values():
                if existing_skill.get("skill_name", "").lower() == skill_name.lower():
                    return json.dumps({
                        "error": f"Skill with name '{skill_name}' already exists"
                    })

            # Generate new skill ID
            new_skill_id = generate_id(skills)

            # Create new skill record
            new_skill = {
                "skill_id": new_skill_id,
                "skill_name": skill_name.strip(),
                "status": status if status else "active",
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Add to skills data
            skills[new_skill_id] = new_skill

            return json.dumps({
                "success": True,
                "message": f"Skill '{skill_name}' created successfully",
                "skill_id": new_skill_id,
                "skill_data": new_skill
            })

        elif action == "update":
            # Required field for skill update
            if not skill_id:
                return json.dumps({
                    "error": "Missing required parameter 'skill_id' for update operation"
                })

            # At least one optional field must be provided
            if not any([skill_name, status]):
                return json.dumps({
                    "error": "At least one optional parameter (skill_name, status) must be provided for update operation"
                })

            # Check if skill exists
            if skill_id not in skills:
                return json.dumps({
                    "error": f"Skill with ID '{skill_id}' not found"
                })

            # Validate status if provided
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Check for duplicate skill names (excluding current skill)
            if skill_name:
                for existing_skill_id, existing_skill in skills.items():
                    if (existing_skill_id != skill_id and 
                        existing_skill.get("skill_name", "").lower() == skill_name.lower()):
                        return json.dumps({
                            "error": f"Skill with name '{skill_name}' already exists"
                        })

            # Update skill record
            skill_record = skills[skill_id]
            
            if skill_name:
                skill_record["skill_name"] = skill_name.strip()
            if status:
                skill_record["status"] = status
            
            skill_record["updated_at"] = timestamp

            return json.dumps({
                "success": True,
                "message": f"Skill with ID '{skill_id}' updated successfully",
                "skill_id": skill_id,
                "skill_data": skill_record
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

    @staticmethod
    def check_approval_invoke(data: Dict[str, Any], action: str, requester_email: str) -> str:
        """
        Check approval for HR actions based on SOPs and approval data.
        
        Args:
            data: Environment data containing users and approvals
            action: The HR action being performed
            requester_email: Email of the user requesting the action  
        """
        # Define role authorization mapping based on SOPs
        role_authorizations = {
            "hr_director": [
                "user_provisioning", "create_department", "update_department", 
                "create_benefits_plan", "update_benefits_plan", "create_job_position", 
                "update_job_position", "skills_management", "job_position_skills_management"
            ],
            "hr_manager": [
                "employee_onboarding", "employee_offboarding", "performance_review_final_approval"
            ],
            "it_administrator": [
                "user_provisioning"
            ],
            "finance_officer": [
                "create_benefits_plan", "update_benefits_plan", "process_payroll_run", 
                "payroll_correction"
            ],
            "hiring_manager": [
                "create_job_position", "update_job_position", "job_position_skills_management",
                "manage_application_stage", "timesheet_approval", "timesheet_correction"
            ],
            "recruiter": [
                "manage_application_stage"
            ],
            "payroll_administrator": [
                "timesheet_approval", "timesheet_correction"
            ],
            "compliance_officer": [
                "employee_onboarding", "employee_offboarding"
            ]
        }
        
        # Define actions requiring multiple approvers (AND logic)
        and_approval_actions = {
            "employee_onboarding": ["hr_manager", "compliance_officer"],
            "employee_offboarding": ["hr_manager", "compliance_officer"]
        }
        
        # Define actions allowing alternative approvers (OR logic)  
        or_approval_actions = {
            "user_provisioning": ["hr_director", "it_administrator"],
            "create_benefits_plan": ["hr_director", "finance_officer"],
            "update_benefits_plan": ["hr_director", "finance_officer"],
            "create_job_position": ["hr_director", "hiring_manager"],
            "update_job_position": ["hr_director", "hiring_manager"],
            "job_position_skills_management": ["hr_director", "hiring_manager"],
            "manage_application_stage": ["recruiter", "hiring_manager"],
            "timesheet_approval": ["payroll_administrator", "hiring_manager"],
            "timesheet_correction": ["payroll_administrator", "hiring_manager"]
        }
        
        # Define simplified action to approval keyword mapping
        action_keywords = {
            "user_provisioning": ["user provisioning", "elevated roles"],
            "create_department": ["department creation"],
            "update_department": ["department update", "department manager"],
            "create_benefits_plan": ["benefits plan creation"],
            "update_benefits_plan": ["benefits plan update"],
            "create_job_position": ["job position", "publishable"],
            "update_job_position": ["job position", "publishable"],
            "job_position_skills_management": ["job position", "skills"],
            "manage_application_stage": ["application stage"],
            "employee_onboarding": ["onboarding"],
            "employee_offboarding": ["offboarding"],
            "timesheet_approval": ["timesheet approval"],
            "timesheet_correction": ["timesheet correction"],
            "process_payroll_run": ["payroll run"],
            "payroll_correction": ["payroll correction"],
            "performance_review_final_approval": ["performance review"],
            "skills_management": ["skills management"]
        }
        
        # Find the requester's role
        users = data.get("users", {})
        role_conducting_action = None
        
        for user in users.values():
            if user.get("email") == requester_email:
                role_conducting_action = user.get("role")
                break
        
        if not role_conducting_action:
            return json.dumps({
                "approval_valid": False,
                "error": f"No user found with email: {requester_email}"
            })
        
        # Check if role is directly authorized for the action (single approver actions)
        single_approver_actions = [
            "create_department", "update_department", "skills_management", 
            "process_payroll_run", "payroll_correction", "performance_review_final_approval"
        ]
        
        if action in single_approver_actions:
            authorized_roles = role_authorizations.get(role_conducting_action, [])
            if action in authorized_roles:
                return json.dumps({
                    "approval_valid": True,
                    "message": f"Role '{role_conducting_action}' is directly authorized for action '{action}'"
                })
            else:
                return json.dumps({
                    "approval_valid": False,
                    "error": f"Role '{role_conducting_action}' is not authorized for action '{action}'"
                })
        
        # For approval-based actions, check the approvals data
        approvals = data.get("approvals", {})
        
        # Find matching approvals using keywords
        matching_approvals = []
        keywords = action_keywords.get(action, [action])
        
        for approval in approvals.values():
            action_name = approval.get("action_name", "").lower()
            
            # Check if any keyword matches the approval action name
            for keyword in keywords:
                if keyword.lower() in action_name:
                    matching_approvals.append(approval)
                    break
        
        if not matching_approvals:
            return json.dumps({
                "approval_valid": False,
                "error": f"No approval found for action '{action}'"
            })
        
        # Extract approver roles from matching approvals
        approver_roles = []
        for approval in matching_approvals:
            approver_role = approval.get("approver_role")
            if approver_role:
                approver_roles.append(approver_role)
        
        # Check AND logic actions (require all specified roles)
        if action in and_approval_actions:
            required_roles = set(and_approval_actions[action])
            approved_roles = set(approver_roles)
            
            if required_roles.issubset(approved_roles):
                return json.dumps({
                    "approval_valid": True,
                    "approved_by": list(required_roles),
                    "message": f"All required approvals received from: {', '.join(required_roles)}"
                })
            else:
                missing_roles = required_roles - approved_roles
                return json.dumps({
                    "approval_valid": False,
                    "error": f"Missing required approvals from roles: {', '.join(missing_roles)}"
                })
        
        # Check OR logic actions (any of the specified roles is sufficient)
        elif action in or_approval_actions:
            allowed_roles = set(or_approval_actions[action])
            approved_roles = set(approver_roles)
            
            if allowed_roles.intersection(approved_roles):
                valid_approver = list(allowed_roles.intersection(approved_roles))[0]
                return json.dumps({
                    "approval_valid": True,
                    "approved_by": valid_approver,
                    "message": f"Approved by authorized role: {valid_approver}"
                })
            else:
                return json.dumps({
                    "approval_valid": False,
                    "error": f"No valid approval from authorized roles: {', '.join(allowed_roles)}"
                })
        
        return json.dumps({
            "approval_valid": False,
            "error": f"No valid approval found for action '{action}'"
        })

    @staticmethod
    def discover_timesheet_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover timesheet entities.
        
        Supported entities:
        - employee_timesheets: Employee timesheet records by timesheet_id, employee_id, work_date, clock_in_time, clock_out_time, break_duration_minutes, total_hours, project_code, approved_by, status, created_at, updated_at
        """
        if entity_type not in ["employee_timesheets"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'employee_timesheets'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("employee_timesheets", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "timesheet_id": entity_id})
            else:
                results.append({**entity_data, "timesheet_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_candidate_invoke(
        data: Dict[str, Any],
        action: str,
        candidate_id: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        source: Optional[str] = None,
        phone_number: Optional[str] = None,
        address: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Executes the specified action (create or update) on candidate records.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        def validate_email_format(email: str) -> bool:
            """Basic email format validation"""
            return "@" in email and "." in email.split("@")[1]

        timestamp = "2025-10-01T12:00:00"
        candidates = data.get("candidates", {})

        # Validate supported sources based on SOPs
        supported_sources = ["website", "referral", "linkedin", "job_board", "recruiter", "other"]
        
        # Map SOPs sources to existing data sources for compatibility
        source_mapping = {
            "website": "company_website",
            "referral": "referral", 
            "linkedin": "social_media",
            "job_board": "job_board",
            "recruiter": "recruiter",
            "other": "career_fair"  # Map 'other' to existing career_fair for compatibility
        }

        # Validate supported statuses
        supported_statuses = ["new", "screening", "interviewing", "offered", "hired", "rejected"]

        if action == "create":
            # Required fields for candidate creation
            if not all([first_name, last_name, email, source]):
                return json.dumps({
                    "error": "Missing required parameters for create operation. Required: first_name, last_name, email, source"
                })

            # Validate source
            if source not in supported_sources:
                return json.dumps({
                    "error": f"Invalid source '{source}'. Must be one of: {', '.join(supported_sources)}"
                })

            # Validate email format
            if not validate_email_format(email):
                return json.dumps({
                    "error": "Invalid email format"
                })

            # Check for duplicate email addresses
            for existing_candidate in candidates.values():
                if existing_candidate.get("email", "").lower() == email.lower():
                    return json.dumps({
                        "error": f"Candidate with email '{email}' already exists"
                    })

            # Validate status if provided
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Generate new candidate ID
            new_candidate_id = generate_id(candidates)

            # Map source to internal format for data consistency
            internal_source = source_mapping.get(source, source)

            # Create new candidate record
            new_candidate = {
                "candidate_id": new_candidate_id,
                "first_name": first_name.strip(),
                "last_name": last_name.strip(),
                "email": email.lower().strip(),
                "phone_number": phone_number.strip() if phone_number else None,
                "address": address.strip() if address else None,
                "source": internal_source,
                "status": status if status else "new",
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Add to candidates data
            candidates[new_candidate_id] = new_candidate

            return json.dumps({
                "success": True,
                "message": f"Candidate '{first_name} {last_name}' created successfully",
                "candidate_id": new_candidate_id,
                "candidate_data": new_candidate
            })

        elif action == "update":
            # Required field for candidate update
            if not candidate_id:
                return json.dumps({
                    "error": "Missing required parameter 'candidate_id' for update operation"
                })

            # At least one optional field must be provided
            optional_fields = [first_name, last_name, email, source, phone_number, address, status]
            if not any(field is not None for field in optional_fields):
                return json.dumps({
                    "error": "At least one optional parameter (first_name, last_name, email, source, phone_number, address, status) must be provided for update operation"
                })

            # Check if candidate exists
            if candidate_id not in candidates:
                return json.dumps({
                    "error": f"Candidate with ID '{candidate_id}' not found"
                })

            # Validate source if provided
            if source and source not in supported_sources:
                return json.dumps({
                    "error": f"Invalid source '{source}'. Must be one of: {', '.join(supported_sources)}"
                })

            # Validate email format if provided
            if email and not validate_email_format(email):
                return json.dumps({
                    "error": "Invalid email format"
                })

            # Check for duplicate email addresses (excluding current candidate)
            if email:
                for existing_candidate_id, existing_candidate in candidates.items():
                    if (existing_candidate_id != candidate_id and 
                        existing_candidate.get("email", "").lower() == email.lower()):
                        return json.dumps({
                            "error": f"Candidate with email '{email}' already exists"
                        })

            # Validate status if provided
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Update candidate record
            candidate_record = candidates[candidate_id]
            
            if first_name:
                candidate_record["first_name"] = first_name.strip()
            if last_name:
                candidate_record["last_name"] = last_name.strip()
            if email:
                candidate_record["email"] = email.lower().strip()
            if source:
                # Map source to internal format for data consistency
                internal_source = source_mapping.get(source, source)
                candidate_record["source"] = internal_source
            if phone_number is not None:  # Allow setting to None
                candidate_record["phone_number"] = phone_number.strip() if phone_number else None
            if address is not None:  # Allow setting to None
                candidate_record["address"] = address.strip() if address else None
            if status:
                candidate_record["status"] = status
            
            candidate_record["updated_at"] = timestamp

            return json.dumps({
                "success": True,
                "message": f"Candidate with ID '{candidate_id}' updated successfully",
                "candidate_id": candidate_id,
                "candidate_data": candidate_record
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

    @staticmethod
    def manage_payroll_deduction_invoke(data: Dict[str, Any], action: str, deduction_data: Dict[str, Any] = None) -> str:
        """
        Create payroll deduction records. Updates are not supported as per schema design.
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Only 'create' is supported for payroll deductions"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payroll deductions"
            })
        
        payroll_deductions = data.get("payroll_deductions", {})
        payroll_records = data.get("payroll_records", {})
        users = data.get("users", {})
        
        if action == "create":
            if not deduction_data:
                return json.dumps({
                    "success": False,
                    "error": "deduction_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["payroll_id", "deduction_type", "amount", "created_by"]
            missing_fields = [field for field in required_fields if field not in deduction_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Payroll record not found - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that payroll record exists in the system
            payroll_id = str(deduction_data["payroll_id"])
            if payroll_id not in payroll_records:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Payroll record not found"
                })
            
            # Validate that creator exists in the user system
            created_by = str(deduction_data["created_by"])
            if created_by not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Creator not found"
                })
            
            # Validate deduction_type enum according to schema
            valid_types = ["tax", "insurance", "retirement", "garnishment", "equipment", "other"]
            if deduction_data["deduction_type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid deduction type or amount - deduction_type must be one of: {', '.join(valid_types)}"
                })
            
            # Validate amount is positive monetary value
            try:
                amount = float(deduction_data["amount"])
                if amount <= 0:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid deduction type or amount - amount must be positive"
                    })
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid deduction type or amount - invalid amount format"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["payroll_id", "deduction_type", "amount", "created_by"]
            invalid_fields = [field for field in deduction_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payroll deduction creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new deduction ID
            new_deduction_id = generate_id(payroll_deductions)
            
            # Create new deduction record
            new_deduction = {
                "deduction_id": str(new_deduction_id),
                "payroll_id": payroll_id,
                "deduction_type": deduction_data["deduction_type"],
                "amount": deduction_data["amount"],
                "created_by": created_by,
                "created_at": "2025-10-01T12:00:00"
            }
            
            payroll_deductions[str(new_deduction_id)] = new_deduction
            
            return json.dumps({
                "success": True,
                "action": "create",
                "deduction_id": str(new_deduction_id),
                "message": f"Payroll deduction {new_deduction_id} created successfully",
                "deduction_data": new_deduction
            })

    @staticmethod
    def discover_benefits_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover benefits entities.
        
        Supported entities:
        - benefits_plans: Benefits plans by plan_id, plan_name, plan_type, provider, employee_cost, employer_cost, status, effective_date, expiration_date, created_at, updated_at
        - employee_benefits: Employee benefits by enrollment_id, employee_id, plan_id, enrollment_date, status, coverage_level, beneficiary_name, beneficiary_relationship, created_at, updated_at
        """
        if entity_type not in ["benefits_plans", "employee_benefits"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'benefits_plans' or 'employee_benefits'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        id_field = "plan_id" if entity_type == "benefits_plans" else "enrollment_id"
        print(filters)
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_employee_benefits_invoke(data: Dict[str, Any], action: str, benefits_data: Dict[str, Any] = None, enrollment_id: str = None) -> str:
        """
        Create or update employee benefits records.
        
        Actions:
        - create: Create new employee benefits enrollment (requires benefits_data with employee_id, plan_id, enrollment_date, coverage_level)
        - update: Update existing enrollment (requires enrollment_id and benefits_data with changes)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
            
        def is_future_date(date_str: str) -> bool:
            """Check if date is in future - simplified for demo"""
            # In real implementation, would compare with current date
            # For demo purposes, assume dates starting with "2026" or later are future
            return date_str.startswith("2026") or date_str.startswith("2027")
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for employee benefits"
            })
        
        employee_benefits = data.get("employee_benefits", {})
        employees = data.get("employees", {})
        benefits_plans = data.get("benefits_plans", {})
        
        if action == "create":
            if not benefits_data:
                return json.dumps({
                    "success": False,
                    "error": "benefits_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["employee_id", "plan_id", "enrollment_date", "coverage_level"]
            missing_fields = [field for field in required_fields if field not in benefits_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or plan not found or inactive - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that employee exists and has active status
            employee_id = str(benefits_data["employee_id"])
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or plan not found or inactive"
                })
            
            employee = employees[employee_id]
            if employee.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or plan not found or inactive"
                })
            
            # Validate that benefits plan exists and has active status
            plan_id = str(benefits_data["plan_id"])
            if plan_id not in benefits_plans:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or plan not found or inactive"
                })
            
            plan = benefits_plans[plan_id]
            if plan.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee or plan not found or inactive"
                })
            
            # Validate that enrollment date is not in future
            enrollment_date = benefits_data["enrollment_date"]
            if is_future_date(enrollment_date):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid enrollment date or coverage level - enrollment date cannot be in future"
                })
            
            # Validate coverage_level enum according to schema
            valid_levels = ["employee_only", "employee_spouse", "employee_children", "family"]
            if benefits_data["coverage_level"] not in valid_levels:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid enrollment date or coverage level - coverage_level must be one of: {', '.join(valid_levels)}"
                })
            
            # Check that employee is not already enrolled in the same plan type
            plan_type = plan.get("plan_type")
            for existing_enrollment in employee_benefits.values():
                if (existing_enrollment.get("employee_id") == employee_id and 
                    existing_enrollment.get("status") == "active"):
                    existing_plan_id = str(existing_enrollment.get("plan_id"))
                    if existing_plan_id in benefits_plans:
                        existing_plan_type = benefits_plans[existing_plan_id].get("plan_type")
                        if existing_plan_type == plan_type:
                            return json.dumps({
                                "success": False,
                                "error": f"Halt: Employee already enrolled in same plan type"
                            })
            
            # Validate only allowed fields are present
            allowed_fields = ["employee_id", "plan_id", "enrollment_date", "coverage_level", "status",
                            "beneficiary_name", "beneficiary_relationship"]
            invalid_fields = [field for field in benefits_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for benefits enrollment: {', '.join(invalid_fields)}"
                })
            
            # Generate new enrollment ID
            new_enrollment_id = generate_id(employee_benefits)
            
            # Create new employee benefits record
            new_benefits = {
                "enrollment_id": str(new_enrollment_id),
                "employee_id": employee_id,
                "plan_id": plan_id,
                "enrollment_date": enrollment_date,
                "status": benefits_data.get("status", "active"),  # If enrollment status is not specified during enrollment, set it to active
                "coverage_level": benefits_data["coverage_level"],
                "beneficiary_name": benefits_data.get("beneficiary_name"),
                "beneficiary_relationship": benefits_data.get("beneficiary_relationship"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            employee_benefits[str(new_enrollment_id)] = new_benefits
            
            return json.dumps({
                "success": True,
                "action": "create",
                "enrollment_id": str(new_enrollment_id),
                "message": f"Employee benefits enrollment {new_enrollment_id} created successfully",
                "benefits_data": new_benefits
            })
        
        elif action == "update":
            if not enrollment_id:
                return json.dumps({
                    "success": False,
                    "error": "enrollment_id is required for update action"
                })
            
            if enrollment_id not in employee_benefits:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Enrollment not found"
                })
            
            if not benefits_data:
                return json.dumps({
                    "success": False,
                    "error": "benefits_data is required for update action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["employee_id", "plan_id", "enrollment_date", "status", "coverage_level", "beneficiary_name", "beneficiary_relationship"]
            provided_fields = [field for field in update_fields if field in benefits_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Get current enrollment for validation
            current_benefits = employee_benefits[enrollment_id]
            
            # Validate only allowed fields for updates
            invalid_fields = [field for field in benefits_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for benefits enrollment update: {', '.join(invalid_fields)}"
                })
            
            # Validate status transitions if status is being updated
            if "status" in benefits_data:
                valid_statuses = ["active", "terminated", "pending"]
                new_status = benefits_data["status"]
                
                if new_status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Benefits enrollment operation failed - status must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate coverage_level enum if provided
            if "coverage_level" in benefits_data:
                valid_levels = ["employee_only", "employee_spouse", "employee_children", "family"]
                if benefits_data["coverage_level"] not in valid_levels:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Benefits enrollment operation failed - coverage_level must be one of: {', '.join(valid_levels)}"
                    })
            
            # Update employee benefits record
            updated_benefits = current_benefits.copy()
            for key, value in benefits_data.items():
                updated_benefits[key] = value
            
            updated_benefits["updated_at"] = "2025-10-01T12:00:00"
            employee_benefits[enrollment_id] = updated_benefits
            
            return json.dumps({
                "success": True,
                "action": "update",
                "enrollment_id": enrollment_id,
                "message": f"Employee benefits enrollment {enrollment_id} updated successfully",
                "benefits_data": updated_benefits
            })

    @staticmethod
    def discover_training_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover training entities.
        
        Supported entities:
        - training_programs: Training programs by program_id, program_name, program_type, duration_hours, delivery_method, mandatory, status, created_at, updated_at
        - employee_training: Employee training records by training_record_id, employee_id, program_id, enrollment_date, completion_date, status, score, certificate_issued, expiry_date, created_at, updated_at
        """
        if entity_type not in ["training_programs", "employee_training"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'training_programs' or 'employee_training'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        id_field = "program_id" if entity_type == "training_programs" else "training_record_id"
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_job_application_invoke(data: Dict[str, Any], action: str, application_data: Dict[str, Any] = None, application_id: str = None) -> str:
        """
        Create or update job application records.
        
        Actions:
        - create: Create new application (requires candidate_id, position_id, application_date, recruiter_id)
        - update: Update existing application (requires application_id, application_data with status updates)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
            
        def is_future_date(date_str: str) -> bool:
            """Check if date is in future - simplified for demo"""
            # In real implementation, would compare with current date
            # For demo purposes, assume dates starting with "2026" or later are future
            return date_str.startswith("2026") or date_str.startswith("2027")
            
        def is_valid_status_transition(current_status: str, new_status: str) -> bool:
            """Validate status transitions follow proper workflow"""
            # Define the linear progression workflow
            workflow_order = ["submitted", "under_review", "screening", "interviewing", "offer_made", "accepted"]
            terminal_states = ["accepted", "rejected", "withdrawn"]
            exit_states = ["rejected", "withdrawn"]
            
            # Cannot transition from terminal states
            if current_status in terminal_states:
                return False
            
            # Can exit to rejected/withdrawn from any active stage
            if new_status in exit_states:
                return True
                
            # Cannot move backward in workflow
            if current_status in workflow_order and new_status in workflow_order:
                current_index = workflow_order.index(current_status)
                new_index = workflow_order.index(new_status)
                # Can only move forward one step or stay the same
                return new_index >= current_index and new_index <= current_index + 1
            
            return False
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for job applications"
            })
        
        applications = data.get("job_applications", {})
        candidates = data.get("candidates", {})
        job_positions = data.get("job_positions", {})
        users = data.get("users", {})
        
        if action == "create":
            if not application_data:
                return json.dumps({
                    "success": False,
                    "error": "application_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["candidate_id", "position_id", "application_date", "recruiter_id"]
            missing_fields = [field for field in required_fields if field not in application_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing or invalid inputs - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that candidate and position exist and are valid
            candidate_id = str(application_data["candidate_id"])
            if candidate_id not in candidates:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Candidate not found"
                })
            
            position_id = str(application_data["position_id"])
            if position_id not in job_positions:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Position not found"
                })
            
            # Validate that assigned recruiter exists and has recruiter role
            recruiter_id = str(application_data["recruiter_id"])
            if recruiter_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Recruiter not found"
                })
            
            recruiter = users[recruiter_id]
            if recruiter.get("role") != "recruiter":
                return json.dumps({
                    "success": False,
                    "error": f"User specified is not a recruiter"
                })
            
            # Validate that application date is not in future
            application_date = application_data["application_date"]
            if is_future_date(application_date):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid status transition - application date cannot be in future"
                })
            
            # Validate AI screening score if provided
            if "ai_screening_score" in application_data:
                score = application_data["ai_screening_score"]
                if score is not None and (not isinstance(score, (int, float)) or score < 0 or score > 100):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid status transition - AI screening score must be within 0-100 range"
                    })
            
            # Validate final_decision enum if provided
            if "final_decision" in application_data:
                valid_decisions = ["hire", "reject", "hold"]
                if application_data["final_decision"] not in valid_decisions:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid status transition - final_decision must be one of: {', '.join(valid_decisions)}"
                    })
            
            # Validate allowed fields
            allowed_fields = ["candidate_id", "position_id", "application_date", "recruiter_id", 
                            "ai_screening_score", "final_decision", "status"]
            invalid_fields = [field for field in application_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for application creation: {', '.join(invalid_fields)}"
                })
            
            # Validate status if provided
            if "status" in application_data:
                valid_statuses = ["submitted", "under_review", "screening", "interviewing", "offer_made", "accepted", "rejected", "withdrawn"]
                if application_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid status transition - status must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Generate new application ID
            new_app_id = generate_id(applications)
            
            # Create new application record
            new_application = {
                "application_id": str(new_app_id),
                "candidate_id": candidate_id,
                "position_id": position_id,
                "application_date": application_date,
                "status": application_data.get("status", "submitted"),  # If status is not specified during creation, set it to submitted
                "recruiter_id": recruiter_id,
                "ai_screening_score": application_data.get("ai_screening_score"),
                "final_decision": application_data.get("final_decision"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            applications[str(new_app_id)] = new_application
            
            return json.dumps({
                "success": True,
                "action": "create",
                "application_id": str(new_app_id),
                "message": f"Job application {new_app_id} created successfully",
                "application_data": new_application
            })
        
        elif action == "update":
            if not application_id:
                return json.dumps({
                    "success": False,
                    "error": "application_id is required for update action"
                })
            
            if application_id not in applications:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Application not found"
                })
            
            if not application_data:
                return json.dumps({
                    "success": False,
                    "error": "application_data is required for update action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["candidate_id", "position_id", "application_date", "recruiter_id", "status", "ai_screening_score", "final_decision"]
            provided_fields = [field for field in update_fields if field in application_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Get current application for validation
            current_application = applications[application_id]
            current_status = current_application.get("status", "submitted")
            
            # Validate allowed update fields
            invalid_fields = [field for field in application_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for application update: {', '.join(invalid_fields)}"
                })
            
            # Validate status transitions if status is being updated
            if "status" in application_data:
                new_status = application_data["status"]
                valid_statuses = ["submitted", "under_review", "screening", "interviewing", "offer_made", "accepted", "rejected", "withdrawn"]
                
                if new_status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid status transition - status must be one of: {', '.join(valid_statuses)}"
                    })
                
                # Validate status transitions follow proper workflow
                if not is_valid_status_transition(current_status, new_status):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid status transition"
                    })
            
            # Validate AI screening score if provided
            if "ai_screening_score" in application_data:
                score = application_data["ai_screening_score"]
                if score is not None and (not isinstance(score, (int, float)) or score < 0 or score > 100):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Application stage management failed - AI screening score must be within 0-100 range"
                    })
            
            # Validate final_decision enum if provided
            if "final_decision" in application_data:
                valid_decisions = ["hire", "reject", "hold"]
                if application_data["final_decision"] not in valid_decisions:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Application stage management failed - final_decision must be one of: {', '.join(valid_decisions)}"
                    })
            
            # Update application record
            updated_application = current_application.copy()
            for key, value in application_data.items():
                updated_application[key] = value
            
            updated_application["updated_at"] = "2025-10-01T12:00:00"
            applications[application_id] = updated_application
            
            return json.dumps({
                "success": True,
                "action": "update",
                "application_id": application_id,
                "message": f"Job application {application_id} updated successfully",
                "application_data": updated_application
            })

    @staticmethod
    def manage_timesheet_entries_invoke(data: Dict[str, Any], action: str, timesheet_data: Dict[str, Any] = None, timesheet_id: str = None) -> str:
        """
        Create or update timesheet entry records.
        
        Actions:
        - create: Create new timesheet entry (requires employee_id, work_date, clock_in_time, clock_out_time)
        - update: Update existing timesheet entry (requires timesheet_id, timesheet_data)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
            
        def is_valid_time_order(clock_in: str, clock_out: str) -> bool:
            """Check if clock_in time is before clock_out time - simplified for demo"""
            return clock_in < clock_out
            
        def calculate_total_hours(clock_in: str, clock_out: str, break_minutes: int = 0) -> float:
            """Calculate total hours worked - simplified calculation for demo"""
            # In a real implementation, this would parse timestamps and calculate actual duration
            # For demo purposes, we'll do a simple calculation
            try:
                # Assuming format like "2025-10-01T08:00:00"
                in_hour = int(clock_in.split('T')[1].split(':')[0])
                out_hour = int(clock_out.split('T')[1].split(':')[0])
                total_minutes = (out_hour - in_hour) * 60 - break_minutes
                return round(total_minutes / 60, 2)
            except:
                return 0.0
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for timesheet entries"
            })
        
        employee_timesheets = data.get("employee_timesheets", {})
        employees = data.get("employees", {})
        users = data.get("users", {})
        
        if action == "create":
            if not timesheet_data:
                return json.dumps({
                    "success": False,
                    "error": "timesheet_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["employee_id", "work_date", "clock_in_time", "clock_out_time"]
            missing_fields = [field for field in required_fields if field not in timesheet_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee not found or inactive - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that employee exists and has active status
            employee_id = str(timesheet_data["employee_id"])
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee not found or inactive"
                })
            
            employee = employees[employee_id]
            if employee.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee not found or inactive"
                })
            
            # Validate that clock_in_time is before clock_out_time
            clock_in_time = timesheet_data["clock_in_time"]
            clock_out_time = timesheet_data["clock_out_time"]
            if not is_valid_time_order(clock_in_time, clock_out_time):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid work date or times - clock_in_time must be before clock_out_time"
                })
            
            # Validate break_duration_minutes if provided
            break_duration = timesheet_data.get("break_duration_minutes", 0)
            try:
                break_duration = int(break_duration)
                if break_duration < 0:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid break duration - break_duration_minutes must be non-negative"
                    })
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid break duration - invalid break_duration_minutes format"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["employee_id", "work_date", "clock_in_time", "clock_out_time", 
                            "break_duration_minutes", "project_code", "total_hours", "status"]
            invalid_fields = [field for field in timesheet_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for timesheet creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new timesheet ID
            new_timesheet_id = generate_id(employee_timesheets)
            
            # Calculate total hours if not provided
            total_hours = timesheet_data.get("total_hours")
            if total_hours is None:
                total_hours = calculate_total_hours(clock_in_time, clock_out_time, break_duration)
            
            # Create timesheet entry with required information
            new_timesheet = {
                "timesheet_id": str(new_timesheet_id),
                "employee_id": employee_id,
                "work_date": timesheet_data["work_date"],
                "clock_in_time": clock_in_time,
                "clock_out_time": clock_out_time,
                "break_duration_minutes": break_duration,
                "total_hours": total_hours,
                "project_code": timesheet_data.get("project_code"),
                "approved_by": None,
                "status": timesheet_data.get("status", "draft"),  # Default to draft if not specified
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            employee_timesheets[str(new_timesheet_id)] = new_timesheet
            
            return json.dumps({
                "success": True,
                "action": "create",
                "timesheet_id": str(new_timesheet_id),
                "message": f"Timesheet entry {new_timesheet_id} created successfully",
                "timesheet_data": new_timesheet
            })
        
        elif action == "update":
            if not timesheet_id:
                return json.dumps({
                    "success": False,
                    "error": "timesheet_id is required for update action"
                })
            
            if timesheet_id not in employee_timesheets:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Timesheet not found"
                })
            
            if not timesheet_data:
                return json.dumps({
                    "success": False,
                    "error": "timesheet_data is required for update action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["clock_in_time", "clock_out_time", "break_duration_minutes", "total_hours", 
                           "project_code", "status", "approved_by"]
            provided_fields = [field for field in update_fields if field in timesheet_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Get current timesheet for validation
            current_timesheet = employee_timesheets[timesheet_id]
            
            # Validate only allowed fields for updates
            invalid_fields = [field for field in timesheet_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for timesheet update: {', '.join(invalid_fields)}"
                })
            
            # Validate status if provided
            if "status" in timesheet_data:
                valid_statuses = ["draft", "submitted", "approved", "rejected"]
                if timesheet_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Timesheet approval/correction failed - status must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate time order if both clock times are being updated
            if "clock_in_time" in timesheet_data or "clock_out_time" in timesheet_data:
                clock_in = timesheet_data.get("clock_in_time", current_timesheet.get("clock_in_time"))
                clock_out = timesheet_data.get("clock_out_time", current_timesheet.get("clock_out_time"))
                
                if clock_in and clock_out and not is_valid_time_order(clock_in, clock_out):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Timesheet approval/correction failed - clock_in_time must be before clock_out_time"
                    })
            
            # Validate break_duration_minutes if provided
            if "break_duration_minutes" in timesheet_data:
                try:
                    break_duration = int(timesheet_data["break_duration_minutes"])
                    if break_duration < 0:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Timesheet approval/correction failed - break_duration_minutes must be non-negative"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Timesheet approval/correction failed - invalid break_duration_minutes format"
                    })
            
            # Validate approved_by user exists if provided
            if "approved_by" in timesheet_data and timesheet_data["approved_by"] is not None:
                approver_id = str(timesheet_data["approved_by"])
                if approver_id not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Timesheet approval/correction failed - approver not found"
                    })
            
            # Update timesheet entry
            updated_timesheet = current_timesheet.copy()
            for key, value in timesheet_data.items():
                updated_timesheet[key] = value
            
            # Recalculate total_hours if times or break changed but total_hours not explicitly provided
            if ("clock_in_time" in timesheet_data or "clock_out_time" in timesheet_data or 
                "break_duration_minutes" in timesheet_data) and "total_hours" not in timesheet_data:
                clock_in = updated_timesheet.get("clock_in_time")
                clock_out = updated_timesheet.get("clock_out_time")
                break_min = updated_timesheet.get("break_duration_minutes", 0)
                if clock_in and clock_out:
                    updated_timesheet["total_hours"] = calculate_total_hours(clock_in, clock_out, break_min)
            
            updated_timesheet["updated_at"] = "2025-10-01T12:00:00"
            employee_timesheets[timesheet_id] = updated_timesheet
            
            return json.dumps({
                "success": True,
                "action": "update",
                "timesheet_id": timesheet_id,
                "message": f"Timesheet entry {timesheet_id} updated successfully",
                "timesheet_data": updated_timesheet
            })

    @staticmethod
    def discover_leave_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover leave entities.
        
        Supported entities:
        - leave_requests: Leave requests by leave_id, employee_id, leave_type, start_date, end_date, days_requested, status, approved_by, approval_date, remaining_balance, created_at, updated_at
        """
        if entity_type not in ["leave_requests"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'leave_requests'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("leave_requests", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "leave_id": entity_id})
            else:
                results.append({**entity_data, "leave_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

