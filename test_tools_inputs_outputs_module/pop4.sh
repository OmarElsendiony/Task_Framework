#!/bin/bash

# Create the directory structure
mkdir -p tools_regression_tests/interface_5

# Create test file for DiscoverPayrollEntities
cat > tools_regression_tests/interface_5/discover_payroll_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "discover_payroll_entities",
                "arguments": {
                    "entity_type": "payroll_records",
                    "filters": {
                        "payroll_id": "payroll_001",
                        "employee_id": "emp_001",
                        "pay_period_start": "2025-09-01",
                        "pay_period_end": "2025-09-15",
                        "hours_worked": 80.0,
                        "hourly_rate": 25.50,
                        "payment_date": "2025-09-20",
                        "status": "approved",
                        "approved_by": "finance_001",
                        "created_at": "2025-09-01T08:00:00",
                        "updated_at": "2025-09-18T16:30:00"
                    }
                }
            },
            {
                "name": "discover_payroll_entities",
                "arguments": {
                    "entity_type": "payroll_deductions",
                    "filters": {
                        "deduction_id": "deduction_001",
                        "payroll_id": "payroll_001",
                        "deduction_type": "tax",
                        "amount": 125.75,
                        "created_by": "payroll_admin_001",
                        "created_at": "2025-09-15T10:30:00"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for DiscoverPerformanceEntities
cat > tools_regression_tests/interface_5/discover_performance_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "discover_performance_entities",
                "arguments": {
                    "entity_type": "performance_reviews",
                    "filters": {
                        "review_id": "review_001",
                        "employee_id": "emp_001",
                        "reviewer_id": "mgr_001",
                        "review_period_start": "2025-01-01",
                        "review_period_end": "2025-12-31",
                        "review_type": "annual",
                        "overall_rating": "exceeds_expectations",
                        "goals_achievement_score": 9.2,
                        "communication_score": 8.7,
                        "teamwork_score": 9.0,
                        "leadership_score": 8.5,
                        "technical_skills_score": 9.3,
                        "status": "approved",
                        "created_at": "2025-01-15T09:00:00",
                        "updated_at": "2025-09-20T14:30:00"
                    }
                }
            },
            {
                "name": "discover_performance_entities",
                "arguments": {
                    "entity_type": "performance_reviews",
                    "filters": {
                        "employee_id": "emp_002",
                        "review_type": "quarterly",
                        "overall_rating": "meets_expectations",
                        "status": "draft",
                        "goals_achievement_score": 7.8
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for DiscoverExpenseEntities
cat > tools_regression_tests/interface_5/discover_expense_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "discover_expense_entities",
                "arguments": {
                    "entity_type": "expense_reimbursements",
                    "filters": {
                        "reimbursement_id": "reimb_001",
                        "employee_id": "emp_001",
                        "expense_date": "2025-09-15",
                        "amount": 125.50,
                        "expense_type": "travel",
                        "receipt_file_path": "/documents/receipts/travel_001.pdf",
                        "status": "approved",
                        "approved_by": "finance_001",
                        "payment_date": "2025-09-25",
                        "created_at": "2025-09-16T08:30:00",
                        "updated_at": "2025-09-22T11:15:00"
                    }
                }
            },
            {
                "name": "discover_expense_entities",
                "arguments": {
                    "entity_type": "expense_reimbursements",
                    "filters": {
                        "employee_id": "emp_002",
                        "expense_type": "meals",
                        "status": "submitted",
                        "amount": 45.75,
                        "expense_date": "2025-09-18"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for DiscoverDocumentEntities
cat > tools_regression_tests/interface_5/discover_document_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "discover_document_entities",
                "arguments": {
                    "entity_type": "document_storage",
                    "filters": {
                        "document_id": "doc_001",
                        "document_name": "Employee Handbook 2025",
                        "document_type": "handbook",
                        "employee_id": "emp_001",
                        "file_path": "/documents/handbooks/employee_handbook_2025.pdf",
                        "upload_date": "2025-01-01T00:00:00",
                        "uploaded_by": "hr_admin_001",
                        "confidentiality_level": "internal",
                        "retention_period_years": 7,
                        "expiry_date": "2032-01-01",
                        "status": "active",
                        "created_at": "2025-01-01T00:00:00"
                    }
                }
            },
            {
                "name": "discover_document_entities",
                "arguments": {
                    "entity_type": "document_storage",
                    "filters": {
                        "document_type": "contract",
                        "confidentiality_level": "confidential",
                        "status": "archived",
                        "retention_period_years": 10,
                        "uploaded_by": "legal_001"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for DiscoverBenefitsEntities
cat > tools_regression_tests/interface_5/discover_benefits_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "discover_benefits_entities",
                "arguments": {
                    "entity_type": "benefits_plans",
                    "filters": {
                        "plan_id": "plan_001",
                        "plan_name": "Premium Health Insurance",
                        "plan_type": "health_insurance",
                        "provider": "BlueCross BlueShield",
                        "employee_cost": 250.00,
                        "employer_cost": 750.00,
                        "status": "active",
                        "effective_date": "2025-01-01",
                        "expiration_date": "2025-12-31",
                        "created_at": "2024-12-01T10:00:00",
                        "updated_at": "2025-09-15T14:30:00"
                    }
                }
            },
            {
                "name": "discover_benefits_entities",
                "arguments": {
                    "entity_type": "employee_benefits",
                    "filters": {
                        "enrollment_id": "enroll_001",
                        "employee_id": "emp_001",
                        "plan_id": "plan_001",
                        "enrollment_date": "2025-01-15",
                        "status": "active",
                        "coverage_level": "family",
                        "beneficiary_name": "Jane Smith",
                        "beneficiary_relationship": "spouse",
                        "created_at": "2025-01-15T09:00:00",
                        "updated_at": "2025-09-10T11:30:00"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for DiscoverTrainingEntities
cat > tools_regression_tests/interface_5/discover_training_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "discover_training_entities",
                "arguments": {
                    "entity_type": "training_programs",
                    "filters": {
                        "program_id": "prog_001",
                        "program_name": "Cybersecurity Awareness Training",
                        "program_type": "compliance",
                        "duration_hours": 8,
                        "delivery_method": "online",
                        "mandatory": true,
                        "status": "active",
                        "created_at": "2025-01-01T08:00:00",
                        "updated_at": "2025-09-15T16:00:00"
                    }
                }
            },
            {
                "name": "discover_training_entities",
                "arguments": {
                    "entity_type": "employee_training",
                    "filters": {
                        "training_record_id": "training_001",
                        "employee_id": "emp_001",
                        "program_id": "prog_001",
                        "enrollment_date": "2025-02-01",
                        "completion_date": "2025-02-15",
                        "status": "completed",
                        "score": 92.5,
                        "certificate_issued": true,
                        "expiry_date": "2026-02-15",
                        "created_at": "2025-02-01T09:00:00",
                        "updated_at": "2025-02-15T17:30:00"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for DiscoverLeaveEntities
cat > tools_regression_tests/interface_5/discover_leave_entities_tests.json << 'EOF'
{
    "env": "hr_experts",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "discover_leave_entities",
                "arguments": {
                    "entity_type": "leave_requests",
                    "filters": {
                        "leave_id": "leave_001",
                        "employee_id": "emp_001",
                        "leave_type": "annual",
                        "start_date": "2025-10-01",
                        "end_date": "2025-10-05",
                        "days_requested": 5.0,
                        "status": "approved",
                        "approved_by": "mgr_001",
                        "approval_date": "2025-09-20T14:30:00",
                        "remaining_balance": 15.0,
                        "created_at": "2025-09-15T10:00:00",
                        "updated_at": "2025-09-20T14:30:00"
                    }
                }
            },
            {
                "name": "discover_leave_entities",
                "arguments": {
                    "entity_type": "leave_requests",
                    "filters": {
                        "employee_id": "emp_002",
                        "leave_type": "sick",
                        "status": "pending",
                        "days_requested": 2.0,
                        "start_date": "2025-09-25"
                    }
                }
            }
        ]
    }
}
EOF

echo "All test files have been created successfully in tools_regression_tests/interface_5/"
echo "Files created:"
echo "- discover_payroll_entities_tests.json"
echo "- discover_performance_entities_tests.json"
echo "- discover_expense_entities_tests.json"
echo "- discover_document_entities_tests.json"
echo "- discover_benefits_entities_tests.json"
echo "- discover_training_entities_tests.json"
echo "- discover_leave_entities_tests.json"