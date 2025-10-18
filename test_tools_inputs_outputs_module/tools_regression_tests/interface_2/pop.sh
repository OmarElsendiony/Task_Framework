#!/bin/bash

# Create the directory structure
mkdir -p tools_regression_tests/interface_1

# Create test file for discover_workflows
cat > tools_regression_tests/interface_1/discover_workflows.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_workflows",
                "arguments": {
                    "entity_type": "communications",
                    "filters": {
                        "communication_id": "1",
                        "incident_id": "1",
                        "communication_type": "escalation_notice",
                        "recipient_type": "internal",
                        "sender": "213",
                        "recipient": "20",
                        "delivery_method": "sms",
                        "message_content": "Incident INC0000001 has been escalated. Immediate attention required.",
                        "delivery_status": "delivered",
                        "sent_at": "2025-09-25",
                        "created_at": "2025-09-25"
                    }
                }
            },
            {
                "name": "discover_workflows",
                "arguments": {
                    "entity_type": "approval_requests",
                    "filters": {
                        "approval_id": "1",
                        "reference_id": "1",
                        "reference_type": "escalation",
                        "requested_by": "98",
                        "requested_action": "create_escalation",
                        "approver": "368",
                        "status": "denied",
                        "requested_at": "2025-09-25",
                        "responded_at": "2025-09-27",
                        "created_at": "2025-09-25"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for get_sla_breach_incidents
cat > tools_regression_tests/interface_1/get_sla_breach_incidents.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "get_sla_breach_incidents",
                "arguments": {
                    "client_id": "1",
                    "start_date": "2025-09-01",
                    "end_date": "2025-09-30",
                    "status": "resolved"
                }
            },
            {
                "name": "get_sla_breach_incidents",
                "arguments": {
                    "client_id": "12",
                    "start_date": "2025-10-01",
                    "end_date": "2025-10-31",
                    "status": "closed"
                }
            }
        ]
    }
}
EOF

# Create test file for log_audit_records
cat > tools_regression_tests/interface_1/log_audit_records.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "log_audit_records",
                "arguments": {
                    "reference_id": "42",
                    "reference_type": "user",
                    "action": "update",
                    "user_id": "301",
                    "field_name": "email",
                    "old_value": "jonathan77@example.com",
                    "new_value": "jessicabell@example.org"
                }
            },
            {
                "name": "log_audit_records",
                "arguments": {
                    "reference_id": "1",
                    "reference_type": "incident",
                    "action": "create",
                    "user_id": "1"
                }
            }
        ]
    }
}
EOF

# Create test file for manage_approval_requests
cat > tools_regression_tests/interface_1/manage_approval_requests.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_approval_requests",
                "arguments": {
                    "action": "create",
                    "reference_id": "1",
                    "reference_type": "escalation",
                    "requested_by": "98",
                    "requested_action": "create_escalation",
                    "approver": "368"
                }
            },
            {
                "name": "manage_approval_requests",
                "arguments": {
                    "action": "update",
                    "approval_id": "1",
                    "status": "approved"
                }
            }
        ]
    }
}
EOF

# Create test file for manage_assets
cat > tools_regression_tests/interface_1/manage_assets.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_assets",
                "arguments": {
                    "action": "create",
                    "entity_type": "configuration_items",
                    "entity_data": {
                        "ci_name": "Test-Application-Server-001",
                        "ci_type": "application",
                        "environment": "production",
                        "operational_status": "operational",
                        "responsible_owner": "466"
                    }
                }
            },
            {
                "name": "manage_assets",
                "arguments": {
                    "action": "update",
                    "entity_type": "configuration_items",
                    "entity_id": "1",
                    "entity_data": {
                        "ci_name": "Updated-Application-Server-001",
                        "operational_status": "degraded",
                        "responsible_owner": "114"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for manage_attachments
cat > tools_regression_tests/interface_1/manage_attachments.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_attachments",
                "arguments": {
                    "action": "create",
                    "attachment_data": {
                        "reference_id": "1",
                        "reference_type": "incident",
                        "file_name": "test_screenshot_001.pdf",
                        "file_url": "https://s3.amazonaws.com/incident-mgmt-attachments/2025/10/01/incident/1/test_screenshot_001.pdf",
                        "file_type": "pdf",
                        "file_size_bytes": 2048576,
                        "uploaded_by": "598"
                    }
                }
            },
            {
                "name": "manage_attachments",
                "arguments": {
                    "action": "create",
                    "attachment_data": {
                        "reference_id": "1",
                        "reference_type": "change",
                        "file_name": "change_documentation.docx",
                        "file_url": "https://s3.amazonaws.com/incident-mgmt-attachments/2025/10/01/change/1/change_documentation.docx",
                        "file_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "file_size_bytes": 1024000,
                        "uploaded_by": "114"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for manage_change_control
cat > tools_regression_tests/interface_1/manage_change_control.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_change_control",
                "arguments": {
                    "action": "create",
                    "change_request_data": {
                        "title": "Upgrade Database Server to version 12.5",
                        "description": "Critical database upgrade to improve performance and security",
                        "change_type": "normal",
                        "risk_level": "high",
                        "requested_by": "542",
                        "approved_by": "380",
                        "status": "requested",
                        "incident_id": "117",
                        "implementation_date": "2025-11-15T02:00:00"
                    }
                }
            },
            {
                "name": "manage_change_control",
                "arguments": {
                    "action": "update",
                    "change_id": "1",
                    "change_request_data": {
                        "status": "approved",
                        "approved_by": "380",
                        "implementation_date": "2025-11-20T02:00:00"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for manage_clients
cat > tools_regression_tests/interface_1/manage_clients.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_clients",
                "arguments": {
                    "action": "create",
                    "client_data": {
                        "client_name": "Tech Solutions Inc",
                        "registration_number": "REG123456",
                        "company_type": "enterprise",
                        "primary_address": "123 Business Ave, Tech City, TC 12345",
                        "support_coverage": "24x7",
                        "preferred_communication": "email",
                        "status": "active"
                    }
                }
            },
            {
                "name": "manage_clients",
                "arguments": {
                    "action": "update",
                    "client_id": "1",
                    "client_data": {
                        "support_coverage": "business_hours",
                        "preferred_communication": "portal",
                        "primary_address": "456 Updated Street, New City, NC 67890"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for manage_communications
cat > tools_regression_tests/interface_1/manage_communications.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_communications",
                "arguments": {
                    "action": "create",
                    "communication_data": {
                        "incident_id": "1",
                        "communication_type": "status_update",
                        "recipient_type": "client",
                        "sender": "213",
                        "recipient": "20",
                        "delivery_method": "email",
                        "message_content": "Your incident INC0000001 is currently being investigated by our technical team. We will provide updates every 30 minutes.",
                        "delivery_status": "pending"
                    }
                }
            },
            {
                "name": "manage_communications",
                "arguments": {
                    "action": "update",
                    "communication_id": "1",
                    "communication_data": {
                        "delivery_status": "delivered",
                        "sent_at": "2025-10-01T14:30:00"
                    }
                }
            }
        ]
    }
}
EOF

# Create test file for manage_contracts
cat > tools_regression_tests/interface_1/manage_contracts.json << 'EOF'
{
    "env": "incident_management_redos",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_contracts",
                "arguments": {
                    "action": "create",
                    "entity_data": {
                        "client_id": "1",
                        "tier": "premium",
                        "support_coverage": "24x7",
                        "effective_date": "2025-11-01",
                        "expiration_date": "2026-10-31",
                        "created_by": "14",
                        "status": "active"
                    }
                }
            },
            {
                "name": "manage_contracts",
                "arguments": {
                    "action": "update",
                    "entity_id": "1",
                    "entity_data": {
                        "tier": "standard",
                        "support_coverage": "business_hours",
                        "expiration_date": "2027-10-31"
                    }
                }
            }
        ]
    }
}
EOF

echo "All test files for new functions have been created in tools_regression_tests/interface_1/"
echo "Files created:"
echo "- discover_workflows.json"
echo "- get_sla_breach_incidents.json"
echo "- log_audit_records.json"
echo "- manage_approval_requests.json"
echo "- manage_assets.json"
echo "- manage_attachments.json"
echo "- manage_change_control.json"
echo "- manage_clients.json"
echo "- manage_communications.json"
echo "- manage_contracts.json"