#!/bin/bash

# Create the directory structure
mkdir -p tools_regression_tests/interface_1

# Create test file for manage_escalations
cat > tools_regression_tests/interface_1/manage_escalations.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_escalations",
                "arguments": {
                    "action": "create",
                    "escalation_data": {
                        "incident_id": "1",
                        "escalated_from": "303",
                        "escalated_to": "3",
                        "escalation_reason": "Unable to resolve within SLA timeframe. Escalating for additional support resources.",
                        "approver": "4",
                        "status": "pending"
                    }
                }
            },
            {
                "name": "manage_escalations",
                "arguments": {
                    "action": "update",
                    "escalation_id": "1",
                    "escalation_data": {
                        "status": "approved",
                        "approver": "4",
                        "responded_at": "2025-10-01T15:30:00"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for manage_improvement
cat > tools_regression_tests/interface_1/manage_improvement.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_improvement",
                "arguments": {
                    "entity_type": "root_cause_analyses",
                    "action": "create",
                    "improvement_data": {
                        "associated_incident_id": "1",
                        "rca_title": "RCA Report: INC0000001 - Storage System Failure Analysis",
                        "assigned_to": "114",
                        "due_date": "2025-10-31",
                        "reported_by": "447",
                        "analysis_method": "5_whys",
                        "status": "assigned"
                    }
                }
            },
            {
                "name": "manage_improvement",
                "arguments": {
                    "entity_type": "post_incident_reviews",
                    "action": "create",
                    "improvement_data": {
                        "incident_id": "1",
                        "scheduled_date": "2025-10-10",
                        "facilitator": "59",
                        "review_notes": "Comprehensive review of incident response and resolution process",
                        "lessons_learned": "Need to improve monitoring alerts and escalation procedures",
                        "action_items": "1. Update monitoring thresholds 2. Review escalation matrix 3. Conduct training",
                        "status": "scheduled",
                        "created_by": "439"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for manage_incident_reports
cat > tools_regression_tests/interface_1/manage_incident_reports.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_incident_reports",
                "arguments": {
                    "action": "create",
                    "incident_id": "1",
                    "report_title": "Post-Incident Review Report: Storage System Failure",
                    "report_type": "post_incident_review",
                    "report_content": "Comprehensive analysis of the storage system failure incident including timeline, impact assessment, root cause analysis, and recommendations for future prevention.",
                    "generated_by": "114"
                }
            },
            {
                "name": "manage_incident_reports",
                "arguments": {
                    "action": "update",
                    "report_id": "1",
                    "report_title": "Updated Post-Incident Review Report: Storage System Failure",
                    "report_content": "Updated comprehensive analysis with additional findings and revised recommendations.",
                    "report_status": "completed"
                }
            }
        ]
    }
}
EOF

# Create test file for manage_incidents
cat > tools_regression_tests/interface_1/manage_incidents.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_incidents",
                "arguments": {
                    "action": "create",
                    "incident_data": {
                        "title": "Database Connection Timeout Issues",
                        "description": "Multiple users reporting timeout errors when connecting to the primary database server",
                        "category": "Database",
                        "severity": "P2",
                        "impact": "high",
                        "urgency": "high",
                        "status": "open",
                        "reported_by": "347",
                        "assigned_to": "114",
                        "detection_time": "2025-10-01T09:15:00",
                        "problem_id": "1"
                    }
                }
            },
            {
                "name": "manage_incidents",
                "arguments": {
                    "action": "update",
                    "incident_id": "1",
                    "incident_data": {
                        "status": "resolved",
                        "assigned_to": "114",
                        "resolved_at": "2025-10-01T14:30:00"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for manage_incidents_problems_configuration_items
cat > tools_regression_tests/interface_1/manage_incidents_problems_configuration_items.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_incidents_problems_configuration_items",
                "arguments": {
                    "action": "create",
                    "entity_type": "incident_ci",
                    "association_data": {
                        "incident_id": "1",
                        "ci_id": "1"
                    }
                }
            },
            {
                "name": "manage_incidents_problems_configuration_items",
                "arguments": {
                    "action": "create",
                    "entity_type": "problem_ci",
                    "association_data": {
                        "problem_id": "1",
                        "ci_id": "1"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for manage_problem_tickets
cat > tools_regression_tests/interface_1/manage_problem_tickets.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_problem_tickets",
                "arguments": {
                    "action": "create",
                    "problem_data": {
                        "problem_number": "PRB0000001",
                        "title": "Recurring Database Performance Issues",
                        "description": "Systematic analysis of recurring database performance degradation affecting multiple applications",
                        "category": "database",
                        "status": "open",
                        "reported_by": "347",
                        "assigned_to": "114",
                        "detected_at": "2025-10-01T08:00:00"
                    }
                }
            },
            {
                "name": "manage_problem_tickets",
                "arguments": {
                    "action": "update",
                    "problem_id": "1",
                    "problem_data": {
                        "status": "investigating",
                        "resolved_at": "2025-10-15T16:00:00"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for manage_users
cat > tools_regression_tests/interface_1/manage_users.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_users",
                "arguments": {
                    "action": "create",
                    "user_data": {
                        "first_name": "John",
                        "last_name": "Smith",
                        "email": "john.smith@techcorp.com",
                        "role": "technical_support",
                        "timezone": "America/New_York",
                        "status": "active",
                        "client_id": "1"
                    }
                }
            },
            {
                "name": "manage_users",
                "arguments": {
                    "action": "update",
                    "user_id": "1",
                    "user_data": {
                        "role": "incident_manager",
                        "timezone": "America/Los_Angeles",
                        "status": "active"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for manage_work_notes
cat > tools_regression_tests/interface_1/manage_work_notes.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_work_notes",
                "arguments": {
                    "action": "create",
                    "note_data": {
                        "incident_id": "1",
                        "note_text": "Initial investigation shows database connection pool exhaustion. Restarting connection service to provide temporary relief while investigating root cause.",
                        "note_type": "troubleshooting",
                        "created_by": "114"
                    }
                }
            },
            {
                "name": "manage_work_notes",
                "arguments": {
                    "action": "update",
                    "note_id": "1",
                    "note_data": {
                        "note_text": "Updated: Connection service restart successful. Database performance restored. Implementing permanent fix by increasing connection pool size.",
                        "note_type": "resolution"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for manage_work_orders
cat > tools_regression_tests/interface_1/manage_work_orders.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_work_orders",
                "arguments": {
                    "action": "create",
                    "work_order_data": {
                        "work_order_number": "WO0000001",
                        "change_id": "1",
                        "incident_id": "1",
                        "title": "Database Server Maintenance - Connection Pool Optimization",
                        "description": "Scheduled maintenance to optimize database connection pool settings and implement performance improvements",
                        "assigned_to": "114",
                        "status": "pending",
                        "scheduled_date": "2025-10-05T02:00:00"
                    }
                }
            },
            {
                "name": "manage_work_orders",
                "arguments": {
                    "action": "update",
                    "work_order_id": "1",
                    "work_order_data": {
                        "status": "completed",
                        "completed_at": "2025-10-05T04:30:00"
                    }
                }
            }
        ]
    }
}
EOF

echo "All test files for additional functions have been created in tools_regression_tests/interface_1/"
echo "Files created:"
echo "- manage_escalations.json"
echo "- manage_improvement.json"
echo "- manage_incident_reports.json"
echo "- manage_incidents.json"
echo "- manage_incidents_problems_configuration_items.json"
echo "- manage_problem_tickets.json"
echo "- manage_users.json"
echo "- manage_work_notes.json"
echo "- manage_work_orders.json"