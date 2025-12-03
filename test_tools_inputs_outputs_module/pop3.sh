#!/bin/bash

# Create the directory structure
mkdir -p tools_regression_tests/interface_1

# Test 1: get_assets - Filter by employee_id and status
cat > tools_regression_tests/interface_1/test_get_assets_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "get_assets",
                "arguments": {
                    "employee_id": "1",
                    "status": "assigned"
                }
            }
        ]
    }
}
EOF

# Test 2: get_assets - Filter by status only
cat > tools_regression_tests/interface_1/test_get_assets_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "get_assets",
                "arguments": {
                    "status": "returned"
                }
            }
        ]
    }
}
EOF

# Test 3: create_payslip - Valid employee and cycle
cat > tools_regression_tests/interface_1/test_create_payslip_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "create_payslip",
                "arguments": {
                    "employee_id": "1",
                    "cycle_id": "1"
                }
            }
        ]
    }
}
EOF

# Test 4: create_payslip - Another valid employee and cycle
cat > tools_regression_tests/interface_1/test_create_payslip_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "create_payslip",
                "arguments": {
                    "employee_id": "4",
                    "cycle_id": "1"
                }
            }
        ]
    }
}
EOF

# Test 5: update_benefit_plan - Update all optional parameters
cat > tools_regression_tests/interface_1/test_update_benefit_plan_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "update_benefit_plan",
                "arguments": {
                    "plan_id": "1",
                    "name": "Premium Health PPO Plus",
                    "status": "active",
                    "current_cost": 18500.0,
                    "previous_year_cost": 16000.0,
                    "enrollment_window": "open"
                }
            }
        ]
    }
}
EOF

# Test 6: update_benefit_plan - Update status and enrollment window only
cat > tools_regression_tests/interface_1/test_update_benefit_plan_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "update_benefit_plan",
                "arguments": {
                    "plan_id": "1",
                    "status": "inactive",
                    "enrollment_window": "closed"
                }
            }
        ]
    }
}
EOF

# Test 7: create_payment - With all optional parameters
cat > tools_regression_tests/interface_1/test_create_payment_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "create_payment",
                "arguments": {
                    "employee_id": "1",
                    "payment_method": "bank_transfer",
                    "amount": 4143.13,
                    "cycle_id": "20",
                    "source_payslip_id": "1"
                }
            }
        ]
    }
}
EOF

# Test 8: create_payment - Only required parameters
cat > tools_regression_tests/interface_1/test_create_payment_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "create_payment",
                "arguments": {
                    "employee_id": "4",
                    "payment_method": "check",
                    "amount": 5000.0
                }
            }
        ]
    }
}
EOF

# Test 9: calculate_settlement - Using employee_id and email
cat > tools_regression_tests/interface_1/test_calculate_settlement_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "calculate_settlement",
                "arguments": {
                    "employee_id": "8",
                    "email": "employee8@example.com"
                }
            }
        ]
    }
}
EOF

# Test 10: calculate_settlement - Using email only
cat > tools_regression_tests/interface_1/test_calculate_settlement_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "calculate_settlement",
                "arguments": {
                    "email": "patrick.sanchez@example.com"
                }
            }
        ]
    }
}
EOF

# Test 11: update_payslip - Update both status and net_pay_value
cat > tools_regression_tests/interface_1/test_update_payslip_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "update_payslip",
                "arguments": {
                    "payslip_id": "1",
                    "status": "updated",
                    "net_pay_value": 4500.0
                }
            }
        ]
    }
}
EOF

# Test 12: update_payslip - Update status only
cat > tools_regression_tests/interface_1/test_update_payslip_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "update_payslip",
                "arguments": {
                    "payslip_id": "1",
                    "status": "released"
                }
            }
        ]
    }
}
EOF

# Test 13: update_payment - Update all optional parameters
cat > tools_regression_tests/interface_1/test_update_payment_1.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "update_payment",
                "arguments": {
                    "payment_id": "1",
                    "status": "completed",
                    "payment_date": "2025-11-22",
                    "amount": 4200.0
                }
            }
        ]
    }
}
EOF

# Test 14: update_payment - Update status and payment_date only
cat > tools_regression_tests/interface_1/test_update_payment_2.json << 'EOF'
{
    "env": "hr_admin_management",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "update_payment",
                "arguments": {
                    "payment_id": "1",
                    "status": "failed",
                    "payment_date": "2025-11-23"
                }
            }
        ]
    }
}
EOF

echo "Test files created successfully in tools_regression_tests/interface_1/"
echo "Total test files created: 14 (2 tests per function)"