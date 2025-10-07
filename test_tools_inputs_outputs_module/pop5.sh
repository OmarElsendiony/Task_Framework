#!/bin/bash

# Create the directory structure
mkdir -p tools_regression_tests/interface_1

# Test 1: discover_escalations - Test with multiple filters
cat > tools_regression_tests/interface_1/discover_escalations_test1.json << 'EOF'
{
    "env": "incident_management_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_escalations",
                "arguments": {
                    "entity_type": "escalations",
                    "filters": {
                        "incident_id": "1",
                        "escalation_level": "technical",
                        "status": "open"
                    }
                }
            }
        ]
    }
}
EOF

# Test 2: discover_escalations - Test with single filter
cat > tools_regression_tests/interface_1/discover_escalations_test2.json << 'EOF'
{
    "env": "incident_management_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_escalations",
                "arguments": {
                    "entity_type": "escalations",
                    "filters": {
                        "escalated_by_id": "5"
                    }
                }
            }
        ]
    }
}
EOF

# Test 3: discover_incident_entities - Test incidents with multiple filters
cat > tools_regression_tests/interface_1/discover_incident_entities_test1.json << 'EOF'
{
    "env": "incident_management_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_incident_entities",
                "arguments": {
                    "entity_type": "incidents",
                    "filters": {
                        "severity": "P1",
                        "status": "open",
                        "category": "system_outage"
                    }
                }
            }
        ]
    }
}
EOF

# Test 4: discover_incident_entities - Test post_incident_reviews
cat > tools_regression_tests/interface_1/discover_incident_entities_test2.json << 'EOF'
{
    "env": "incident_management_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_incident_entities",
                "arguments": {
                    "entity_type": "post_incident_reviews",
                    "filters": {
                        "facilitator_id": "2",
                        "status": "completed"
                    }
                }
            }
        ]
    }
}
EOF

# Test 5: discover_subscription_agreements - Test client_subscriptions with multiple filters
cat > tools_regression_tests/interface_1/discover_subscription_agreements_test1.json << 'EOF'
{
    "env": "incident_management_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_subscription_agreements",
                "arguments": {
                    "entity_type": "client_subscriptions",
                    "filters": {
                        "client_id": "1",
                        "sla_tier": "premium",
                        "status": "active"
                    }
                }
            }
        ]
    }
}
EOF

# Test 6: discover_subscription_agreements - Test sla_agreements
cat > tools_regression_tests/interface_1/discover_subscription_agreements_test2.json << 'EOF'
{
    "env": "incident_management_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "discover_subscription_agreements",
                "arguments": {
                    "entity_type": "sla_agreements",
                    "filters": {
                        "subscription_id": "1",
                        "severity_level": "P1"
                    }
                }
            }
        ]
    }
}
EOF

# Test 7: manage_clients - Create client with all parameters
cat > tools_regression_tests/interface_1/manage_clients_test1.json << 'EOF'
{
    "env": "incident_management_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_clients",
                "arguments": {
                    "action": "create",
                    "client_data": {
                        "client_name": "Global Tech Solutions Inc",
                        "client_type": "enterprise",
                        "country": "United States",
                        "registration_number": "REG-2025-9876",
                        "contact_email": "contact@globaltechsolutions.com",
                        "industry": "Technology",
                        "status": "active"
                    }
                }
            }
        ]
    }
}
EOF

# Test 8: manage_clients - Update client with multiple fields
cat > tools_regression_tests/interface_1/manage_clients_test2.json << 'EOF'
{
    "env": "incident_management_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_clients",
                "arguments": {
                    "action": "update",
                    "client_id": "1",
                    "client_data": {
                        "client_type": "mid_market",
                        "contact_email": "newemail@client.com",
                        "industry": "Financial Services",
                        "status": "active"
                    }
                }
            }
        ]
    }
}
EOF

# Test 9: manage_vendors - Create vendor with all parameters
cat > tools_regression_tests/interface_1/manage_vendors_test1.json << 'EOF'
{
    "env": "incident_management_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_vendors",
                "arguments": {
                    "action": "create",
                    "vendor_data": {
                        "vendor_name": "CloudStream Technologies",
                        "vendor_type": "cloud_provider",
                        "contact_email": "support@cloudstream.com",
                        "contact_phone": "+1-555-0199",
                        "status": "active"
                    }
                }
            }
        ]
    }
}
EOF

# Test 10: manage_vendors - Update vendor with multiple fields
cat > tools_regression_tests/interface_1/manage_vendors_test2.json << 'EOF'
{
    "env": "incident_management_experts",
    "interface_num": 1,
    "task": {
        "actions": [
            {
                "name": "manage_vendors",
                "arguments": {
                    "action": "update",
                    "vendor_id": "1",
                    "vendor_data": {
                        "vendor_type": "software_vendor",
                        "contact_email": "newsupport@vendor.com",
                        "contact_phone": "+1-555-0200",
                        "status": "active"
                    }
                }
            }
        ]
    }
}
EOF

echo "All test files have been created successfully in tools_regression_tests/interface_1/"
echo ""
echo "Generated files:"
echo "  - discover_escalations_test1.json"
echo "  - discover_escalations_test2.json"
echo "  - discover_incident_entities_test1.json"
echo "  - discover_incident_entities_test2.json"
echo "  - discover_subscription_agreements_test1.json"
echo "  - discover_subscription_agreements_test2.json"
echo "  - manage_clients_test1.json"
echo "  - manage_clients_test2.json"
echo "  - manage_vendors_test1.json"
echo "  - manage_vendors_test2.json"