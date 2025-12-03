#!/bin/bash

# Create the test directory
mkdir -p tools_regression_tests/interface_5

# Test 1: search_assets - Test with all filters (maximum parameters)
cat > tools_regression_tests/interface_5/test_search_assets_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "search_assets",
                "arguments": {
                    "search_criteria": {
                        "employee_id": "1",
                        "status": "assigned"
                    },
                    "email": "patrick.sanchez@example.com"
                }
            }
        ]
    }
}
EOF

# Test 2: search_assets - Test with email only
cat > tools_regression_tests/interface_5/test_search_assets_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "search_assets",
                "arguments": {
                    "email": "patrick.sanchez@example.com"
                }
            }
        ]
    }
}
EOF

# Test 3: construct_payment - Test with all parameters (maximum)
cat > tools_regression_tests/interface_5/test_construct_payment_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "construct_payment",
                "arguments": {
                    "payment_config": {
                        "employee_id": "1",
                        "payment_method": "bank_transfer",
                        "amount": 4143.13
                    },
                    "cycle_id": "20",
                    "source_payslip_id": "1"
                }
            }
        ]
    }
}
EOF

# Test 4: construct_payment - Test with required parameters only
cat > tools_regression_tests/interface_5/test_construct_payment_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "construct_payment",
                "arguments": {
                    "payment_config": {
                        "employee_id": "1",
                        "payment_method": "check",
                        "amount": 5000.00
                    }
                }
            }
        ]
    }
}
EOF

# Test 5: change_payslip - Test with both fields in update_data (maximum)
cat > tools_regression_tests/interface_5/test_change_payslip_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "change_payslip",
                "arguments": {
                    "payslip_id": "1",
                    "update_data": {
                        "status": "updated",
                        "net_pay_value": 4500.00
                    }
                }
            }
        ]
    }
}
EOF

# Test 6: change_payslip - Test with status only
cat > tools_regression_tests/interface_5/test_change_payslip_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "change_payslip",
                "arguments": {
                    "payslip_id": "1",
                    "update_data": {
                        "status": "released"
                    }
                }
            }
        ]
    }
}
EOF

# Test 7: change_benefit_plan - Test with all fields in plan_updates (maximum)
cat > tools_regression_tests/interface_5/test_change_benefit_plan_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "change_benefit_plan",
                "arguments": {
                    "plan_id": "1",
                    "plan_updates": {
                        "name": "Platinum Health PPO Plus",
                        "status": "active",
                        "current_cost": 18500.00,
                        "previous_year_cost": 16000.00,
                        "enrollment_window": "open"
                    }
                }
            }
        ]
    }
}
EOF

# Test 8: change_benefit_plan - Test with partial fields
cat > tools_regression_tests/interface_5/test_change_benefit_plan_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "change_benefit_plan",
                "arguments": {
                    "plan_id": "1",
                    "plan_updates": {
                        "status": "inactive",
                        "enrollment_window": "closed"
                    }
                }
            }
        ]
    }
}
EOF

# Test 9: change_payment - Test with all fields in update_fields (maximum)
cat > tools_regression_tests/interface_5/test_change_payment_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "change_payment",
                "arguments": {
                    "payment_id": "1",
                    "update_fields": {
                        "status": "completed",
                        "payment_date": "2025-11-25",
                        "amount": 4500.00
                    }
                }
            }
        ]
    }
}
EOF

# Test 10: change_payment - Test with status only
cat > tools_regression_tests/interface_5/test_change_payment_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "change_payment",
                "arguments": {
                    "payment_id": "1",
                    "update_fields": {
                        "status": "failed"
                    }
                }
            }
        ]
    }
}
EOF

# Test 11: estimate_settlement - Test with both employee_id and email (maximum)
cat > tools_regression_tests/interface_5/test_estimate_settlement_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "estimate_settlement",
                "arguments": {
                    "employee_data": {
                        "employee_id": "1",
                        "email": "patrick.sanchez@example.com"
                    }
                }
            }
        ]
    }
}
EOF

# Test 12: estimate_settlement - Test with email only
cat > tools_regression_tests/interface_5/test_estimate_settlement_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "estimate_settlement",
                "arguments": {
                    "employee_data": {
                        "email": "patrick.sanchez@example.com"
                    }
                }
            }
        ]
    }
}
EOF

# Test 13: construct_payslip - Test with employee 1 and cycle 1
cat > tools_regression_tests/interface_5/test_construct_payslip_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "construct_payslip",
                "arguments": {
                    "payroll_data": {
                        "employee_id": "1",
                        "cycle_id": "1"
                    }
                }
            }
        ]
    }
}
EOF

# Test 14: construct_payslip - Test with different employee and cycle
cat > tools_regression_tests/interface_5/test_construct_payslip_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 5,
    "task": {
        "actions": [
            {
                "name": "construct_payslip",
                "arguments": {
                    "payroll_data": {
                        "employee_id": "4",
                        "cycle_id": "1"
                    }
                }
            }
        ]
    }
}
EOF

echo "All test JSON files have been created in tools_regression_tests/interface_5/"
echo "Total test files created: 14"