#!/bin/bash

# Create the test directory
mkdir -p tools_regression_tests/interface_4

# Function 1: DiscoverDepartmentEntities Tests
cat > tools_regression_tests/interface_4/discover_department_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 4,
    "task": {
        "actions": [
            {
                "name": "discover_department_entities",
                "arguments": {
                    "entity_type": "departments"
                }
            },
            {
                "name": "discover_department_entities",
                "arguments": {
                    "entity_type": "departments",
                    "filters": {
                        "department_name": "Engineering"
                    }
                }
            },
            {
                "name": "discover_department_entities",
                "arguments": {
                    "entity_type": "departments",
                    "filters": {
                        "department_id": "DEPT001",
                        "status": "active"
                    }
                }
            },
            {
                "name": "discover_department_entities",
                "arguments": {
                    "entity_type": "departments",
                    "filters": {
                        "department_name": "Human Resources",
                        "manager_id": "EMP123",
                        "budget": 500000.00,
                        "status": "active",
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-03-20T14:45:30Z"
                    }
                }
            },
            {
                "name": "discover_department_entities",
                "arguments": {
                    "entity_type": "invalid_entity"
                }
            },
            {
                "name": "discover_department_entities",
                "arguments": {
                    "entity_type": "departments",
                    "filters": {}
                }
            },
            {
                "name": "discover_department_entities",
                "arguments": {
                    "entity_type": "departments",
                    "filters": {
                        "status": "inactive"
                    }
                }
            }
        ]
    }
}
EOF

# Function 2: DiscoverJobEntities Tests
cat > tools_regression_tests/interface_4/discover_job_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 4,
    "task": {
        "actions": [
            {
                "name": "discover_job_entities",
                "arguments": {
                    "entity_type": "job_positions"
                }
            },
            {
                "name": "discover_job_entities",
                "arguments": {
                    "entity_type": "skills"
                }
            },
            {
                "name": "discover_job_entities",
                "arguments": {
                    "entity_type": "job_position_skills"
                }
            },
            {
                "name": "discover_job_entities",
                "arguments": {
                    "entity_type": "job_positions",
                    "filters": {
                        "title": "Senior Software Engineer"
                    }
                }
            },
            {
                "name": "discover_job_entities",
                "arguments": {
                    "entity_type": "job_positions",
                    "filters": {
                        "position_id": "POS001",
                        "title": "Data Scientist",
                        "department_id": "DEPT002",
                        "job_level": "senior",
                        "employment_type": "full_time",
                        "hourly_rate_min": 75.00,
                        "hourly_rate_max": 95.00,
                        "status": "open",
                        "created_at": "2024-02-01T09:00:00Z",
                        "updated_at": "2024-02-15T11:30:00Z"
                    }
                }
            },
            {
                "name": "discover_job_entities",
                "arguments": {
                    "entity_type": "skills",
                    "filters": {
                        "skill_name": "Python Programming",
                        "status": "active"
                    }
                }
            },
            {
                "name": "discover_job_entities",
                "arguments": {
                    "entity_type": "job_position_skills",
                    "filters": {
                        "position_id": "POS001",
                        "skill_id": "SKILL123"
                    }
                }
            },
            {
                "name": "discover_job_entities",
                "arguments": {
                    "entity_type": "invalid_type"
                }
            },
            {
                "name": "discover_job_entities",
                "arguments": {
                    "entity_type": "job_positions",
                    "filters": {
                        "job_level": "executive",
                        "employment_type": "contract"
                    }
                }
            },
            {
                "name": "discover_job_entities",
                "arguments": {
                    "entity_type": "skills",
                    "filters": {}
                }
            }
        ]
    }
}
EOF

# Function 3: DiscoverEmployeeEntities Tests
cat > tools_regression_tests/interface_4/discover_employee_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 4,
    "task": {
        "actions": [
            {
                "name": "discover_employee_entities",
                "arguments": {
                    "entity_type": "employees"
                }
            },
            {
                "name": "discover_employee_entities",
                "arguments": {
                    "entity_type": "employees",
                    "filters": {
                        "employment_status": "active"
                    }
                }
            },
            {
                "name": "discover_employee_entities",
                "arguments": {
                    "entity_type": "employees",
                    "filters": {
                        "user_id": "USER123",
                        "position_id": "POS001"
                    }
                }
            },
            {
                "name": "discover_employee_entities",
                "arguments": {
                    "entity_type": "employees",
                    "filters": {
                        "employee_id": "EMP001",
                        "user_id": "USER456",
                        "position_id": "POS002",
                        "hire_date": "2024-01-15",
                        "employment_status": "active",
                        "manager_id": "EMP999",
                        "date_of_birth": "1990-05-20",
                        "address": "123 Main St, City, State",
                        "hourly_rate": 85,
                        "created_at": "2024-01-15T08:00:00Z",
                        "updated_at": "2024-03-10T16:45:00Z"
                    }
                }
            },
            {
                "name": "discover_employee_entities",
                "arguments": {
                    "entity_type": "employees",
                    "filters": {
                        "employment_status": "terminated"
                    }
                }
            },
            {
                "name": "discover_employee_entities",
                "arguments": {
                    "entity_type": "employees",
                    "filters": {
                        "hire_date": "2024-03-01"
                    }
                }
            },
            {
                "name": "discover_employee_entities",
                "arguments": {
                    "entity_type": "invalid_employees"
                }
            },
            {
                "name": "discover_employee_entities",
                "arguments": {
                    "entity_type": "employees",
                    "filters": {
                        "employment_status": "on_leave",
                        "manager_id": "EMP555"
                    }
                }
            },
            {
                "name": "discover_employee_entities",
                "arguments": {
                    "entity_type": "employees",
                    "filters": {}
                }
            }
        ]
    }
}
EOF

# Function 4: DiscoverRecruitmentEntities Tests
cat > tools_regression_tests/interface_4/discover_recruitment_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 4,
    "task": {
        "actions": [
            {
                "name": "discover_recruitment_entities",
                "arguments": {
                    "entity_type": "candidates"
                }
            },
            {
                "name": "discover_recruitment_entities",
                "arguments": {
                    "entity_type": "job_applications"
                }
            },
            {
                "name": "discover_recruitment_entities",
                "arguments": {
                    "entity_type": "interviews"
                }
            },
            {
                "name": "discover_recruitment_entities",
                "arguments": {
                    "entity_type": "candidates",
                    "filters": {
                        "status": "new"
                    }
                }
            },
            {
                "name": "discover_recruitment_entities",
                "arguments": {
                    "entity_type": "candidates",
                    "filters": {
                        "candidate_id": "CAND001",
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john.doe@email.com",
                        "phone_number": "+1-555-0123",
                        "address": "456 Oak Ave, City, State",
                        "source": "job_board",
                        "status": "screening",
                        "created_at": "2024-03-01T10:00:00Z",
                        "updated_at": "2024-03-05T14:30:00Z"
                    }
                }
            },
            {
                "name": "discover_recruitment_entities",
                "arguments": {
                    "entity_type": "job_applications",
                    "filters": {
                        "status": "under_review",
                        "recruiter_id": "USER789"
                    }
                }
            },
            {
                "name": "discover_recruitment_entities",
                "arguments": {
                    "entity_type": "job_applications",
                    "filters": {
                        "application_id": "APP001",
                        "candidate_id": "CAND001",
                        "position_id": "POS001",
                        "application_date": "2024-03-01",
                        "status": "interviewing",
                        "recruiter_id": "USER789",
                        "ai_screening_score": 85.5,
                        "final_decision": "hire",
                        "created_at": "2024-03-01T12:00:00Z",
                        "updated_at": "2024-03-10T09:15:00Z"
                    }
                }
            },
            {
                "name": "discover_recruitment_entities",
                "arguments": {
                    "entity_type": "interviews",
                    "filters": {
                        "interview_type": "technical",
                        "status": "completed"
                    }
                }
            },
            {
                "name": "discover_recruitment_entities",
                "arguments": {
                    "entity_type": "interviews",
                    "filters": {
                        "interview_id": "INT001",
                        "application_id": "APP001",
                        "interviewer_id": "USER555",
                        "interview_type": "behavioral",
                        "scheduled_date": "2024-03-15T14:00:00Z",
                        "duration_minutes": 90,
                        "status": "completed",
                        "overall_rating": "excellent",
                        "technical_score": 9.5,
                        "communication_score": 8.8,
                        "cultural_fit_score": 9.2,
                        "recommendation": "strong_hire",
                        "created_at": "2024-03-10T10:00:00Z",
                        "updated_at": "2024-03-15T15:30:00Z"
                    }
                }
            },
            {
                "name": "discover_recruitment_entities",
                "arguments": {
                    "entity_type": "invalid_entity"
                }
            },
            {
                "name": "discover_recruitment_entities",
                "arguments": {
                    "entity_type": "candidates",
                    "filters": {
                        "source": "referral",
                        "status": "hired"
                    }
                }
            },
            {
                "name": "discover_recruitment_entities",
                "arguments": {
                    "entity_type": "job_applications",
                    "filters": {}
                }
            }
        ]
    }
}
EOF

# Function 5: DiscoverTimesheetEntities Tests
cat > tools_regression_tests/interface_4/discover_timesheet_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 4,
    "task": {
        "actions": [
            {
                "name": "discover_timesheet_entities",
                "arguments": {
                    "entity_type": "employee_timesheets"
                }
            },
            {
                "name": "discover_timesheet_entities",
                "arguments": {
                    "entity_type": "employee_timesheets",
                    "filters": {
                        "employee_id": "EMP001"
                    }
                }
            },
            {
                "name": "discover_timesheet_entities",
                "arguments": {
                    "entity_type": "employee_timesheets",
                    "filters": {
                        "status": "submitted",
                        "work_date": "2024-03-15"
                    }
                }
            },
            {
                "name": "discover_timesheet_entities",
                "arguments": {
                    "entity_type": "employee_timesheets",
                    "filters": {
                        "timesheet_id": "TS001",
                        "employee_id": "EMP001",
                        "work_date": "2024-03-15",
                        "clock_in_time": "2024-03-15T08:00:00Z",
                        "clock_out_time": "2024-03-15T17:00:00Z",
                        "break_duration_minutes": 60,
                        "total_hours": 8.0,
                        "project_code": "PROJ001",
                        "approved_by": "USER999",
                        "status": "approved",
                        "created_at": "2024-03-15T18:00:00Z",
                        "updated_at": "2024-03-16T09:30:00Z"
                    }
                }
            },
            {
                "name": "discover_timesheet_entities",
                "arguments": {
                    "entity_type": "employee_timesheets",
                    "filters": {
                        "status": "draft"
                    }
                }
            },
            {
                "name": "discover_timesheet_entities",
                "arguments": {
                    "entity_type": "employee_timesheets",
                    "filters": {
                        "approved_by": "USER555",
                        "status": "approved"
                    }
                }
            },
            {
                "name": "discover_timesheet_entities",
                "arguments": {
                    "entity_type": "invalid_timesheets"
                }
            },
            {
                "name": "discover_timesheet_entities",
                "arguments": {
                    "entity_type": "employee_timesheets",
                    "filters": {
                        "project_code": "PROJ002",
                        "total_hours": 8.5
                    }
                }
            },
            {
                "name": "discover_timesheet_entities",
                "arguments": {
                    "entity_type": "employee_timesheets",
                    "filters": {}
                }
            },
            {
                "name": "discover_timesheet_entities",
                "arguments": {
                    "entity_type": "employee_timesheets",
                    "filters": {
                        "status": "rejected"
                    }
                }
            }
        ]
    }
}
EOF

# Function 6: DiscoverUserEntities Tests
cat > tools_regression_tests/interface_4/discover_user_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 4,
    "task": {
        "actions": [
            {
                "name": "discover_user_entities",
                "arguments": {
                    "entity_type": "users"
                }
            },
            {
                "name": "discover_user_entities",
                "arguments": {
                    "entity_type": "users",
                    "filters": {
                        "status": "active"
                    }
                }
            },
            {
                "name": "discover_user_entities",
                "arguments": {
                    "entity_type": "users",
                    "filters": {
                        "role": "hr_manager"
                    }
                }
            },
            {
                "name": "discover_user_entities",
                "arguments": {
                    "entity_type": "users",
                    "filters": {
                        "email": "sarah.johnson@company.com"
                    }
                }
            },
            {
                "name": "discover_user_entities",
                "arguments": {
                    "entity_type": "users",
                    "filters": {
                        "user_id": "USER001",
                        "first_name": "Sarah",
                        "last_name": "Johnson",
                        "email": "sarah.johnson@company.com",
                        "phone_number": "+1-555-0199",
                        "role": "hr_director",
                        "status": "active",
                        "mfa_enabled": true,
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-03-20T15:45:30Z"
                    }
                }
            },
            {
                "name": "discover_user_entities",
                "arguments": {
                    "entity_type": "users",
                    "filters": {
                        "role": "recruiter",
                        "status": "active"
                    }
                }
            },
            {
                "name": "discover_user_entities",
                "arguments": {
                    "entity_type": "users",
                    "filters": {
                        "mfa_enabled": false
                    }
                }
            },
            {
                "name": "discover_user_entities",
                "arguments": {
                    "entity_type": "invalid_users"
                }
            },
            {
                "name": "discover_user_entities",
                "arguments": {
                    "entity_type": "users",
                    "filters": {
                        "status": "suspended",
                        "role": "employee"
                    }
                }
            },
            {
                "name": "discover_user_entities",
                "arguments": {
                    "entity_type": "users",
                    "filters": {}
                }
            },
            {
                "name": "discover_user_entities",
                "arguments": {
                    "entity_type": "users",
                    "filters": {
                        "role": "compliance_officer",
                        "mfa_enabled": true
                    }
                }
            }
        ]
    }
}
EOF

echo "All test files have been created successfully in tools_regression_tests/interface_4/"
echo "Generated files:"
echo "- discover_department_entities_tests.json"
echo "- discover_job_entities_tests.json"
echo "- discover_employee_entities_tests.json"
echo "- discover_recruitment_entities_tests.json"
echo "- discover_timesheet_entities_tests.json"
echo "- discover_user_entities_tests.json"