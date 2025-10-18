#!/bin/bash

# Create the directory structure
mkdir -p tools_regression_tests/interface_1

# Create all test files
cat > tools_regression_tests/interface_1/assess_incident_severity.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "assess_incident_severity",
                "arguments": {
                    "complete_outage": true,
                    "no_workaround": true,
                    "enterprise_impact": true,
                    "affected_parties_count": 8,
                    "regulatory_implications": true,
                    "high_priority_customer": true,
                    "recurrent_incident": true,
                    "major_degradation": true,
                    "workaround_available": false,
                    "multiple_departments": true,
                    "sla_breach_risk": true,
                    "single_department": false,
                    "moderate_degradation": false,
                    "minimal_workaround": false
                }
            },
            {
                "name": "assess_incident_severity",
                "arguments": {
                    "complete_outage": false,
                    "no_workaround": false,
                    "enterprise_impact": false,
                    "affected_parties_count": 2,
                    "regulatory_implications": false,
                    "high_priority_customer": false,
                    "recurrent_incident": false,
                    "major_degradation": false,
                    "workaround_available": true,
                    "multiple_departments": false,
                    "sla_breach_risk": false,
                    "single_department": true,
                    "moderate_degradation": true,
                    "minimal_workaround": true
                }
            }
        ]
    }
}
EOF

cat > tools_regression_tests/interface_1/check_authorization.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "check_authorization",
                "arguments": {
                    "action": "create_escalation",
                    "requester_email": "melissa.jones@outlook.com"
                }
            },
            {
                "name": "check_authorization",
                "arguments": {
                    "action": "update_rollback_request",
                    "requester_email": "melissa.jones@outlook.com"
                }
            }
        ]
    }
}
EOF

cat > tools_regression_tests/interface_1/discover_assets.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_assets",
                "arguments": {
                    "entity_type": "configuration_items",
                    "filters": {
                        "ci_id": "1",
                        "ci_name": "Application-193-lA80",
                        "ci_type": "application",
                        "environment": "testing",
                        "operational_status": "operational",
                        "responsible_owner": "466",
                        "created_at": "2025-10-15",
                        "updated_at": "2025-10-16"
                    }
                }
            },
            {
                "name": "discover_assets",
                "arguments": {
                    "entity_type": "ci_client_assignments",
                    "filters": {
                        "assignment_id": "1",
                        "ci_id": "1",
                        "client_id": "12",
                        "created_at": "2025-10-15"
                    }
                }
            }
        ]
    }
}
EOF

cat > tools_regression_tests/interface_1/discover_audit.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_audit",
                "arguments": {
                    "entity_type": "audit_trails",
                    "filters": {
                        "audit_id": "1",
                        "reference_id": "42",
                        "reference_type": "user",
                        "action": "update",
                        "user_id": "301",
                        "field_name": "email",
                        "old_value": "jonathan77@example.com",
                        "new_value": "jessicabell@example.org",
                        "created_at": "2025-06-18"
                    }
                }
            },
            {
                "name": "discover_audit",
                "arguments": {
                    "entity_type": "audit_trails"
                }
            }
        ]
    }
}
EOF

cat > tools_regression_tests/interface_1/discover_change_control.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_change_control",
                "arguments": {
                    "entity_type": "change_requests",
                    "filters": {
                        "change_id": "1",
                        "change_number": "CHG0000001",
                        "incident_id": "117",
                        "problem_ticket_id": null,
                        "title": "Upgrade Application Server to version v1.4.2",
                        "description": "Change request to modify Application Server",
                        "change_type": "normal",
                        "risk_level": "medium",
                        "requested_by": "542",
                        "approved_by": "380",
                        "status": "scheduled",
                        "implementation_date": "2025-10-14",
                        "created_at": "2025-10-14",
                        "updated_at": "2025-10-15"
                    }
                }
            },
            {
                "name": "discover_change_control",
                "arguments": {
                    "entity_type": "rollback_requests",
                    "filters": {
                        "rollback_id": "1",
                        "rollback_number": "RBK0000001",
                        "incident_id": "82",
                        "title": "Rollback: Upgrade Application Server to version v1.4.2",
                        "rollback_reason": "Change implementation caused unexpected side effects",
                        "requested_by": "268",
                        "status": "approved",
                        "executed_at": null,
                        "created_at": "2025-10-15"
                    }
                }
            }
        ]
    }
}
EOF

cat > tools_regression_tests/interface_1/discover_contracts.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_contracts",
                "arguments": {
                    "entity_type": "sla_agreements",
                    "filters": {
                        "sla_id": "1",
                        "client_id": "1",
                        "tier": "basic",
                        "support_coverage": "24x7",
                        "effective_date": "2025-09-19",
                        "expiration_date": null,
                        "created_by": "14",
                        "status": "active",
                        "created_at": "2025-09-19",
                        "updated_at": "2025-09-29"
                    }
                }
            },
            {
                "name": "discover_contracts",
                "arguments": {
                    "entity_type": "sla_agreements"
                }
            }
        ]
    }
}
EOF

cat > tools_regression_tests/interface_1/discover_coordination.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_coordination",
                "arguments": {
                    "entity_type": "escalations",
                    "filters": {
                        "escalation_id": "1",
                        "incident_id": "1",
                        "escalated_from": "303",
                        "escalated_to": "3",
                        "escalation_reason": "Unable to resolve within SLA timeframe. Escalating for additional support resources.",
                        "approver": "4",
                        "status": "pending",
                        "requested_at": "2025-09-25",
                        "responded_at": null
                    }
                }
            },
            {
                "name": "discover_coordination",
                "arguments": {
                    "entity_type": "bridges",
                    "filters": {
                        "bridge_id": "1",
                        "bridge_number": "BRG0000001",
                        "incident_id": "6",
                        "bridge_type": "technical",
                        "bridge_host": "31",
                        "start_time": "2025-10-05",
                        "end_time": null,
                        "status": "active",
                        "created_at": "2025-10-05"
                    }
                }
            }
        ]
    }
}
EOF

cat > tools_regression_tests/interface_1/discover_improvement.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_improvement",
                "arguments": {
                    "entity_type": "root_cause_analyses",
                    "filters": {
                        "rca_id": "1",
                        "rca_number": "RCA0000001",
                        "rca_title": "RCA Report: INC0000001 - Storage System Failure",
                        "associated_incident_id": "1",
                        "assigned_to": "114",
                        "analysis_method": "5_whys",
                        "root_cause_summary": null,
                        "status": "in_progress",
                        "due_date": "2025-10-31",
                        "completed_at": null,
                        "approved_by": null,
                        "reported_by": "447",
                        "created_at": "2025-10-02",
                        "updated_at": "2025-10-15"
                    }
                }
            },
            {
                "name": "discover_improvement",
                "arguments": {
                    "entity_type": "post_incident_reviews",
                    "filters": {
                        "review_id": "1",
                        "incident_id": "1",
                        "scheduled_date": "2025-10-10",
                        "facilitator": "59",
                        "status": "completed",
                        "created_by": "439",
                        "created_at": "2025-09-26"
                    }
                }
            }
        ]
    }
}
EOF

cat > tools_regression_tests/interface_1/discover_incident_tracking.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_incident_tracking",
                "arguments": {
                    "entity_type": "incidents",
                    "filters": {
                        "incident_id": "1",
                        "problem_id": null,
                        "incident_number": "INC0000001",
                        "title": "Software bug: Intermittent application errors",
                        "category": "software",
                        "severity": "P3",
                        "impact": "medium",
                        "urgency": "medium",
                        "status": "open",
                        "reported_by": "347",
                        "assigned_to": null,
                        "detection_time": "2025-09-25",
                        "acknowledged_at": null,
                        "resolved_at": null,
                        "closed_at": null,
                        "created_at": "2025-09-25",
                        "updated_at": "2025-09-25"
                    }
                }
            },
            {
                "name": "discover_incident_tracking",
                "arguments": {
                    "entity_type": "attachments",
                    "filters": {
                        "attachment_id": "1",
                        "reference_id": "1",
                        "reference_type": "incident",
                        "file_name": "incident_screenshot_2086.pdf",
                        "file_type": "pdf",
                        "file_size_bytes": 5919058,
                        "uploaded_by": "598",
                        "uploaded_at": "2025-09-30"
                    }
                }
            }
        ]
    }
}
EOF

cat > tools_regression_tests/interface_1/discover_parties.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_parties",
                "arguments": {
                    "entity_type": "users",
                    "filters": {
                        "user_id": "1",
                        "first_name": "Melissa",
                        "last_name": "Jones",
                        "email": "melissa.jones@outlook.com",
                        "role": "incident_manager",
                        "timezone": "America/Los_Angeles",
                        "status": "active",
                        "created_at": "2025-04-21",
                        "updated_at": "2025-05-14"
                    }
                }
            },
            {
                "name": "discover_parties",
                "arguments": {
                    "entity_type": "clients",
                    "filters": {
                        "client_id": "1",
                        "client_name": "Rodriguez, Figueroa and Sanchez",
                        "registration_number": "REG877572",
                        "company_type": "smb",
                        "support_coverage": "24x7",
                        "preferred_communication": "portal",
                        "status": "active",
                        "created_at": "2024-08-22",
                        "updated_at": "2024-09-10"
                    }
                }
            }
        ]
    }
}
EOF

echo "All test files have been created in tools_regression_tests/interface_1/"
echo "Files created:"
echo "- assess_incident_severity.json"
echo "- check_authorization.json"
echo "- discover_assets.json"
echo "- discover_audit.json"
echo "- discover_change_control.json"
echo "- discover_contracts.json"
echo "- discover_coordination.json"
echo "- discover_improvement.json"
echo "- discover_incident_tracking.json"
echo "- discover_parties.json"