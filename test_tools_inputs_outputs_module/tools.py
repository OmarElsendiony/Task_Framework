from typing import Any, Dict
import json

class Tools:
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
    def manage_payroll_deduction_invoke(data: Dict[str, Any], action: str, deduction_data: Dict[str, Any] = None, deduction_id: str = None) -> str:
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
                    "error": f"Halt: Candidate, position, or recruiter not found"
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

