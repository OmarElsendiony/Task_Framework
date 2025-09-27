#!/bin/bash

# Create the directory structure
mkdir -p tools_regression_tests/interface_1

# Create test file for ManagePerformanceReview
cat > tools_regression_tests/interface_1/manage_performance_review_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "create",
                    "review_data": {
                        "employee_id": "1",
                        "reviewer_id": "1",
                        "review_period_start": "2025-01-01",
                        "review_period_end": "2025-12-31",
                        "review_type": "annual",
                        "overall_rating": "exceeds_expectations",
                        "goals_achievement_score": 9.5,
                        "communication_score": 8.7,
                        "teamwork_score": 9.2,
                        "leadership_score": 8.9,
                        "technical_skills_score": 9.1,
                        "status": "draft"
                    }
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "update",
                    "review_id": "1",
                    "review_data": {
                        "employee_id": "2",
                        "reviewer_id": "2",
                        "review_period_start": "2025-04-01",
                        "review_period_end": "2025-06-30",
                        "review_type": "quarterly",
                        "overall_rating": "meets_expectations",
                        "goals_achievement_score": 7.8,
                        "communication_score": 8.2,
                        "teamwork_score": 7.5,
                        "leadership_score": 6.9,
                        "technical_skills_score": 8.4,
                        "status": "submitted"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for ManageInterview
cat > tools_regression_tests/interface_1/manage_interview_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "create",
                    "interview_data": {
                        "application_id": "1",
                        "interviewer_id": "1",
                        "interview_type": "technical",
                        "scheduled_date": "2025-11-15T14:30:00",
                        "duration_minutes": 90,
                        "status": "scheduled"
                    }
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "update",
                    "interview_id": "1",
                    "interview_data": {
                        "overall_rating": "excellent",
                        "technical_score": 9.2,
                        "communication_score": 8.7,
                        "cultural_fit_score": 9.0,
                        "recommendation": "strong_hire",
                        "status": "completed"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for ManageBenefitsPlan
cat > tools_regression_tests/interface_1/manage_benefits_plan_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "create",
                    "plan_data": {
                        "plan_name": "Premium Health Insurance Plan",
                        "plan_type": "health_insurance",
                        "provider": "BlueCross BlueShield",
                        "employee_cost": 250.00,
                        "employer_cost": 750.00,
                        "status": "active",
                        "effective_date": "2025-01-01",
                        "expiration_date": "2025-12-31"
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "update",
                    "plan_id": "1",
                    "plan_data": {
                        "plan_name": "Updated Dental Coverage Plan",
                        "plan_type": "dental",
                        "provider": "Delta Dental",
                        "employee_cost": 45.00,
                        "employer_cost": 85.00,
                        "status": "inactive",
                        "effective_date": "2025-03-01",
                        "expiration_date": "2026-02-28"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for ManagePayrollRecord
cat > tools_regression_tests/interface_1/manage_payroll_record_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "create",
                    "payroll_data": {
                        "employee_id": "1",
                        "pay_period_start": "2025-10-01",
                        "pay_period_end": "2025-10-15",
                        "hourly_rate": 25.50,
                        "hours_worked": 80.0,
                        "payment_date": "2025-10-20",
                        "status": "approved",
                        "approved_by": "payroll_admin_001"
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "update",
                    "payroll_id": "1",
                    "payroll_data": {
                        "pay_period_start": "2025-10-16",
                        "pay_period_end": "2025-10-31",
                        "hours_worked": 85.5,
                        "hourly_rate": 26.00,
                        "payment_date": "2025-11-05",
                        "status": "paid",
                        "approved_by": "finance_officer_001"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for ManagePayrollDeduction
cat > tools_regression_tests/interface_1/manage_payroll_deduction_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "create",
                    "deduction_data": {
                        "payroll_id": "1",
                        "deduction_type": "tax",
                        "amount": 125.75,
                        "created_by": "payroll_admin_001"
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "create",
                    "deduction_data": {
                        "payroll_id": "2",
                        "deduction_type": "insurance",
                        "amount": 89.50,
                        "created_by": "hr_manager_002"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for ManageEmployeeBenefits
cat > tools_regression_tests/interface_1/manage_employee_benefits_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "create",
                    "benefits_data": {
                        "employee_id": "1",
                        "plan_id": "1",
                        "enrollment_date": "2025-01-15",
                        "coverage_level": "family",
                        "status": "active",
                        "beneficiary_name": "Jane Smith",
                        "beneficiary_relationship": "spouse"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "update",
                    "enrollment_id": "1",
                    "benefits_data": {
                        "employee_id": "2",
                        "plan_id": "2",
                        "enrollment_date": "2025-02-01",
                        "status": "terminated",
                        "coverage_level": "employee_spouse",
                        "beneficiary_name": "John Doe",
                        "beneficiary_relationship": "domestic_partner"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for ManageJobApplication
cat > tools_regression_tests/interface_1/manage_job_application_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_job_application",
                "arguments": {
                    "action": "create",
                    "application_data": {
                        "candidate_id": "1",
                        "position_id": "1",
                        "application_date": "2025-09-15",
                        "recruiter_id": "1",
                        "ai_screening_score": 87.5,
                        "final_decision": "hire",
                        "status": "submitted"
                    }
                }
            },
            {
                "name": "manage_job_application",
                "arguments": {
                    "action": "update",
                    "application_id": "1",
                    "application_data": {
                        "candidate_id": "2",
                        "position_id": "2",
                        "application_date": "2025-09-20",
                        "recruiter_id": "2",
                        "status": "interviewing",
                        "ai_screening_score": 92.3,
                        "final_decision": "hold"
                    }
                }
            }
        ]
    }
}
EOF

echo "All test files have been created successfully in tools_regression_tests/interface_1/"
echo "Files created:"
echo "- manage_performance_review_tests.json"
echo "- manage_interview_tests.json"
echo "- manage_benefits_plan_tests.json"
echo "- manage_payroll_record_tests.json"
echo "- manage_payroll_deduction_tests.json"
echo "- manage_employee_benefits_tests.json"
echo "- manage_job_application_tests.json"