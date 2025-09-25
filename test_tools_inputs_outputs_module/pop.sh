#!/bin/bash

# Create directory structure
mkdir -p tools_regression_tests/interface_1

# Generate test files for each function
echo "Generating test cases for HR Management System functions..."

# 1. ManagePerformanceReview Tests
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
                        "reviewer_id": "2",
                        "review_period_start": "2025-01-01",
                        "review_period_end": "2025-12-31",
                        "review_type": "annual",
                        "overall_rating": "meets_expectations"
                    }
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "create",
                    "review_data": {
                        "employee_id": "2",
                        "reviewer_id": "3",
                        "review_period_start": "2025-01-01",
                        "review_period_end": "2025-03-31",
                        "review_type": "quarterly",
                        "overall_rating": "exceeds_expectations",
                        "goals_achievement_score": 8.5,
                        "communication_score": 9.0,
                        "teamwork_score": 8.0,
                        "leadership_score": 7.5,
                        "technical_skills_score": 9.2
                    }
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "create",
                    "review_data": {
                        "employee_id": "3",
                        "reviewer_id": "1",
                        "review_period_start": "2025-06-01",
                        "review_period_end": "2025-08-31",
                        "review_type": "probationary",
                        "overall_rating": "below_expectations"
                    }
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "update",
                    "review_id": "1",
                    "review_data": {
                        "overall_rating": "exceeds_expectations",
                        "hr_manager_approval": true
                    }
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "update",
                    "review_id": "2",
                    "review_data": {
                        "status": "approved",
                        "hr_manager_approval": true
                    }
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "create",
                    "review_data": {
                        "employee_id": "999",
                        "reviewer_id": "2",
                        "review_period_start": "2025-01-01",
                        "review_period_end": "2025-12-31",
                        "review_type": "annual",
                        "overall_rating": "meets_expectations"
                    }
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "create",
                    "review_data": {
                        "employee_id": "1",
                        "reviewer_id": "2",
                        "review_period_start": "2025-12-31",
                        "review_period_end": "2025-01-01",
                        "review_type": "annual",
                        "overall_rating": "meets_expectations"
                    }
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "create",
                    "review_data": {
                        "employee_id": "1",
                        "reviewer_id": "2",
                        "review_type": "annual",
                        "overall_rating": "meets_expectations"
                    }
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "create",
                    "review_data": {
                        "employee_id": "1",
                        "reviewer_id": "2",
                        "review_period_start": "2025-01-01",
                        "review_period_end": "2025-12-31",
                        "review_type": "invalid_type",
                        "overall_rating": "meets_expectations"
                    }
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "update",
                    "review_id": "999",
                    "review_data": {
                        "overall_rating": "exceeds_expectations",
                        "hr_manager_approval": true
                    }
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "update",
                    "review_id": "1",
                    "review_data": {
                        "status": "approved"
                    }
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "invalid_action"
                }
            },
            {
                "name": "manage_performance_review",
                "arguments": {
                    "action": "create"
                }
            }
        ]
    }
}
EOF

# 2. ManageInterview Tests
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
                        "interviewer_id": "2",
                        "interview_type": "phone screening",
                        "scheduled_date": "2025-11-15T14:00:00"
                    }
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "create",
                    "interview_data": {
                        "application_id": "2",
                        "interviewer_id": "3",
                        "interview_type": "technical",
                        "scheduled_date": "2025-12-20T10:30:00",
                        "duration_minutes": 90
                    }
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "create",
                    "interview_data": {
                        "application_id": "3",
                        "interviewer_id": "1",
                        "interview_type": "final",
                        "scheduled_date": "2026-01-10T16:00:00",
                        "duration_minutes": 45
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
                        "technical_score": 9.0,
                        "communication_score": 8.5,
                        "cultural_fit_score": 9.2,
                        "recommendation": "strong hire"
                    }
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "update",
                    "interview_id": "2",
                    "interview_data": {
                        "overall_rating": "below_average",
                        "recommendation": "no hire"
                    }
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "create",
                    "interview_data": {
                        "application_id": "999",
                        "interviewer_id": "2",
                        "interview_type": "phone screening",
                        "scheduled_date": "2025-11-15T14:00:00"
                    }
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "create",
                    "interview_data": {
                        "application_id": "1",
                        "interviewer_id": "2",
                        "interview_type": "phone screening",
                        "scheduled_date": "2024-01-15T14:00:00"
                    }
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "create",
                    "interview_data": {
                        "application_id": "1",
                        "interviewer_id": "2",
                        "interview_type": "invalid_type",
                        "scheduled_date": "2025-11-15T14:00:00"
                    }
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "create",
                    "interview_data": {
                        "application_id": "1",
                        "interviewer_id": "2",
                        "interview_type": "phone screening",
                        "scheduled_date": "2025-11-15T14:00:00",
                        "duration_minutes": -30
                    }
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "update",
                    "interview_id": "999",
                    "interview_data": {
                        "overall_rating": "excellent"
                    }
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "update",
                    "interview_id": "1",
                    "interview_data": {
                        "technical_score": 15.0
                    }
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "create",
                    "interview_data": {
                        "interviewer_id": "2",
                        "interview_type": "phone screening",
                        "scheduled_date": "2025-11-15T14:00:00"
                    }
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "invalid_action"
                }
            },
            {
                "name": "manage_interview",
                "arguments": {
                    "action": "create"
                }
            }
        ]
    }
}
EOF

# 3. ManageBenefitsPlan Tests
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
                        "plan_name": "Premium Health Insurance",
                        "plan_type": "health insurance",
                        "effective_date": "2025-01-01",
                        "hr_director_approval": true
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "create",
                    "plan_data": {
                        "plan_name": "Dental Plus",
                        "plan_type": "dental",
                        "provider": "DentalCorp",
                        "employee_cost": 25.50,
                        "employer_cost": 75.00,
                        "effective_date": "2025-01-01",
                        "expiration_date": "2025-12-31",
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "create",
                    "plan_data": {
                        "plan_name": "Vision Care Basic",
                        "plan_type": "vision",
                        "effective_date": "2025-06-01",
                        "status": "inactive",
                        "hr_director_approval": true
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "update",
                    "plan_id": "1",
                    "plan_data": {
                        "employee_cost": 50.00,
                        "employer_cost": 150.00,
                        "hr_director_approval": true
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "update",
                    "plan_id": "2",
                    "plan_data": {
                        "status": "inactive",
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "create",
                    "plan_data": {
                        "plan_name": "401k Plan",
                        "plan_type": "retirement",
                        "effective_date": "2025-01-01"
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "create",
                    "plan_data": {
                        "plan_name": "Invalid Plan",
                        "plan_type": "invalid_type",
                        "effective_date": "2025-01-01",
                        "hr_director_approval": true
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "create",
                    "plan_data": {
                        "plan_name": "Backward Dates Plan",
                        "plan_type": "health insurance",
                        "effective_date": "2025-12-31",
                        "expiration_date": "2025-01-01",
                        "hr_director_approval": true
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "create",
                    "plan_data": {
                        "plan_name": "Negative Cost Plan",
                        "plan_type": "dental",
                        "employee_cost": -10.00,
                        "effective_date": "2025-01-01",
                        "hr_director_approval": true
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "update",
                    "plan_id": "999",
                    "plan_data": {
                        "employee_cost": 50.00,
                        "hr_director_approval": true
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "update",
                    "plan_id": "1",
                    "plan_data": {
                        "employee_cost": 50.00
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "create",
                    "plan_data": {
                        "plan_type": "health insurance",
                        "effective_date": "2025-01-01",
                        "hr_director_approval": true
                    }
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "invalid_action"
                }
            },
            {
                "name": "manage_benefits_plan",
                "arguments": {
                    "action": "create"
                }
            }
        ]
    }
}
EOF

# 4. ManagePayrollRecord Tests
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
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "create",
                    "payroll_data": {
                        "employee_id": "2",
                        "pay_period_start": "2025-10-01",
                        "pay_period_end": "2025-10-15",
                        "hourly_rate": 30.00,
                        "payment_date": "2025-10-20",
                        "approved_by": "finance_manager",
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "create",
                    "payroll_data": {
                        "employee_id": "3",
                        "pay_period_start": "2025-09-16",
                        "pay_period_end": "2025-09-30",
                        "hourly_rate": 22.75,
                        "status": "draft",
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "update",
                    "payroll_id": "1",
                    "payroll_data": {
                        "hours_worked": 80.0,
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "update",
                    "payroll_id": "2",
                    "payroll_data": {
                        "status": "paid",
                        "payment_date": "2025-10-22",
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "create",
                    "payroll_data": {
                        "employee_id": "999",
                        "pay_period_start": "2025-10-01",
                        "pay_period_end": "2025-10-15",
                        "hourly_rate": 25.50,
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "create",
                    "payroll_data": {
                        "employee_id": "1",
                        "pay_period_start": "2025-10-15",
                        "pay_period_end": "2025-10-01",
                        "hourly_rate": 25.50,
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "create",
                    "payroll_data": {
                        "employee_id": "1",
                        "pay_period_start": "2025-10-01",
                        "pay_period_end": "2025-10-15",
                        "hourly_rate": -5.00,
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "create",
                    "payroll_data": {
                        "employee_id": "1",
                        "pay_period_start": "2025-10-01",
                        "pay_period_end": "2025-10-15",
                        "hourly_rate": 25.50
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "update",
                    "payroll_id": "999",
                    "payroll_data": {
                        "hours_worked": 40.0,
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "update",
                    "payroll_id": "1",
                    "payroll_data": {
                        "hours_worked": -10.0,
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "create",
                    "payroll_data": {
                        "pay_period_start": "2025-10-01",
                        "pay_period_end": "2025-10-15",
                        "hourly_rate": 25.50,
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "invalid_action"
                }
            },
            {
                "name": "manage_payroll_record",
                "arguments": {
                    "action": "create"
                }
            }
        ]
    }
}
EOF

# 5. ManagePayrollDeduction Tests
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
                        "amount": 150.75,
                        "created_by": "1",
                        "payroll_administrator_approval": true
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
                        "amount": 85.00,
                        "created_by": "2",
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "create",
                    "deduction_data": {
                        "payroll_id": "1",
                        "deduction_type": "retirement",
                        "amount": 200.00,
                        "created_by": "3",
                        "payroll_administrator_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "create",
                    "deduction_data": {
                        "payroll_id": "3",
                        "deduction_type": "equipment",
                        "amount": 50.25,
                        "created_by": "1",
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "update",
                    "deduction_id": "1",
                    "deduction_data": {
                        "amount": 175.00,
                        "payroll_administrator_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "update",
                    "deduction_id": "2",
                    "deduction_data": {
                        "deduction_type": "other",
                        "finance_officer_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "create",
                    "deduction_data": {
                        "payroll_id": "999",
                        "deduction_type": "tax",
                        "amount": 150.75,
                        "created_by": "1",
                        "payroll_administrator_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "create",
                    "deduction_data": {
                        "payroll_id": "1",
                        "deduction_type": "tax",
                        "amount": 150.75,
                        "created_by": "999",
                        "payroll_administrator_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "create",
                    "deduction_data": {
                        "payroll_id": "1",
                        "deduction_type": "invalid_type",
                        "amount": 150.75,
                        "created_by": "1",
                        "payroll_administrator_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "create",
                    "deduction_data": {
                        "payroll_id": "1",
                        "deduction_type": "tax",
                        "amount": -50.00,
                        "created_by": "1",
                        "payroll_administrator_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "create",
                    "deduction_data": {
                        "payroll_id": "1",
                        "deduction_type": "tax",
                        "amount": 150.75,
                        "created_by": "1"
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "update",
                    "deduction_id": "999",
                    "deduction_data": {
                        "amount": 175.00,
                        "payroll_administrator_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "update",
                    "deduction_id": "1",
                    "deduction_data": {
                        "amount": 175.00
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "create",
                    "deduction_data": {
                        "deduction_type": "tax",
                        "amount": 150.75,
                        "created_by": "1",
                        "payroll_administrator_approval": true
                    }
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "invalid_action"
                }
            },
            {
                "name": "manage_payroll_deduction",
                "arguments": {
                    "action": "create"
                }
            }
        ]
    }
}
EOF

# 6. ManageEmployeeBenefits Tests
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
                        "coverage_level": "employee only"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "create",
                    "benefits_data": {
                        "employee_id": "2",
                        "plan_id": "2",
                        "enrollment_date": "2025-02-01",
                        "coverage_level": "family coverage",
                        "beneficiary_name": "Jane Doe",
                        "beneficiary_relationship": "spouse"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "create",
                    "benefits_data": {
                        "employee_id": "3",
                        "plan_id": "3",
                        "enrollment_date": "2025-03-10",
                        "coverage_level": "employee plus children",
                        "status": "pending"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "update",
                    "enrollment_id": "1",
                    "benefits_data": {
                        "coverage_level": "employee plus spouse",
                        "beneficiary_name": "John Smith",
                        "beneficiary_relationship": "spouse"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "update",
                    "enrollment_id": "2",
                    "benefits_data": {
                        "status": "terminated"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "create",
                    "benefits_data": {
                        "employee_id": "999",
                        "plan_id": "1",
                        "enrollment_date": "2025-01-15",
                        "coverage_level": "employee only"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "create",
                    "benefits_data": {
                        "employee_id": "1",
                        "plan_id": "999",
                        "enrollment_date": "2025-01-15",
                        "coverage_level": "employee only"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "create",
                    "benefits_data": {
                        "employee_id": "1",
                        "plan_id": "1",
                        "enrollment_date": "2026-01-15",
                        "coverage_level": "employee only"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "create",
                    "benefits_data": {
                        "employee_id": "1",
                        "plan_id": "1",
                        "enrollment_date": "2025-01-15",
                        "coverage_level": "invalid_level"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "update",
                    "enrollment_id": "999",
                    "benefits_data": {
                        "coverage_level": "employee plus spouse"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "update",
                    "enrollment_id": "2",
                    "benefits_data": {
                        "status": "active"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "create",
                    "benefits_data": {
                        "plan_id": "1",
                        "enrollment_date": "2025-01-15",
                        "coverage_level": "employee only"
                    }
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "invalid_action"
                }
            },
            {
                "name": "manage_employee_benefits",
                "arguments": {
                    "action": "create"
                }
            }
        ]
    }
}
EOF
