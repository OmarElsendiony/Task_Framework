#!/bin/bash

# Create directory
mkdir -p tools_regression_tests/interface_2

# Test 1: DiscoverWorkflows - communications
cat > tools_regression_tests/interface_2/discover_workflows_1.json << 'EOF'
{
    "env": "incident_management_redo",
    "interface_num": 2,
    "task": {
        "actions": [
            {
                "name": "discover_workflows",
                "arguments": {
                    "entity_type": "communications",
                    "filters": {
                        "incident_id": "INC001",
                        "communication_type": "status_update",
                        "recipient_type": "client",
                        "delivery_method": "email",
                        "delivery_status": "delivered",
                        "sent_at": "2025-10-01"
                    }
                }
            },
            {
                "name": "discover_workflows",
                "arguments": {
                    "entity_type": "communications",
                    "filters": {
                        "sender": "user_123",
                        "recipient": "user_456",
                        "message_content": "urgent",
                        "delivery_status": "pending"
                    }
                }
            }
        ]
    }
}
EOF

# Test 2: DiscoverWorkflows - approval_requests
cat > tools_regression_tests/interface_2/discover_workflows_2.json << 'EOF'
{
    "env": "incident_management_redo",
    "interface_num": 2,
    "task": {
        "actions": [
            {
                "name": "discover_workflows",
                "arguments": {
                    "entity_type": "approval_requests",
                    "filters": {
                        "reference_id": "CHG001",
                        "reference_type": "change",
                        "requested_by": "user_789",
                        "approver": "user_101",
                        "status": "pending",
                        "requested_at": "2025-10-02"
                    }
                }
            },
            {
                "name": "discover_workflows",
                "arguments": {
                    "entity_type": "approval_requests",
                    "filters": {
                        "reference_type": "escalation",
                        "requested_action": "approve_bridge",
                        "status": "approved",
                        "responded_at": "2025-10-03",
                        "created_at": "2025-10-01"
                    }
                }
            }
        ]
    }
}
EOF

# Test 3: DiscoverImprovement - root_cause_analyses
cat > tools_regression_tests/interface_2/discover_improvement_1.json << 'EOF'
{
    "env": "incident_management_redo",
    "interface_num": 2,
    "task": {
        "actions": [
            {
                "name": "discover_improvement",
                "arguments": {
                    "entity_type": "root_cause_analyses",
                    "filters": {
                        "rca_id": "RCA001",
                        "incident_id": "INC001",
                        "assigned_to": "user_123",
                        "analysis_method": "5_whys",
                        "status": "completed",
                        "due_date": "2025-10-10",
                        "completed_at": "2025-10-05"
                    }
                }
            },
            {
                "name": "discover_improvement",
                "arguments": {
                    "entity_type": "root_cause_analyses",
                    "filters": {
                        "rca_number": "RCA0001234",
                        "rca_title": "Database Outage Analysis",
                        "root_cause_summary": "memory leak",
                        "approved_by": "user_456",
                        "updated_at": "2025-10-06"
                    }
                }
            }
        ]
    }
}
EOF

# Test 4: DiscoverImprovement - post_incident_reviews
cat > tools_regression_tests/interface_2/discover_improvement_2.json << 'EOF'
{
    "env": "incident_management_redo",
    "interface_num": 2,
    "task": {
        "actions": [
            {
                "name": "discover_improvement",
                "arguments": {
                    "entity_type": "post_incident_reviews",
                    "filters": {
                        "review_id": "PIR001",
                        "incident_id": "INC002",
                        "scheduled_date": "2025-10-15",
                        "facilitator": "user_789",
                        "status": "scheduled",
                        "created_at": "2025-10-04"
                    }
                }
            },
            {
                "name": "discover_improvement",
                "arguments": {
                    "entity_type": "post_incident_reviews",
                    "filters": {
                        "review_notes": "communication breakdown",
                        "lessons_learned": "improve monitoring",
                        "action_items": "update runbooks",
                        "status": "completed"
                    }
                }
            }
        ]
    }
}
EOF

# Test 5: DiscoverPerformance - performance_metrics
cat > tools_regression_tests/interface_2/discover_performance_1.json << 'EOF'
{
    "env": "incident_management_redo",
    "interface_num": 2,
    "task": {
        "actions": [
            {
                "name": "discover_performance",
                "arguments": {
                    "entity_type": "performance_metrics",
                    "filters": {
                        "metric_id": "MET001",
                        "incident_id": "INC001",
                        "metric_type": "MTTR",
                        "calculated_value_minutes": 120,
                        "sla_target_minutes": 180,
                        "recorded_by": "user_123",
                        "recorded_date": "2025-10-04"
                    }
                }
            },
            {
                "name": "discover_performance",
                "arguments": {
                    "entity_type": "performance_metrics",
                    "filters": {
                        "metric_type": "MTTA",
                        "calculated_value_minutes": 30,
                        "sla_target_minutes": 60,
                        "recorded_date": "2025-10-03"
                    }
                }
            }
        ]
    }
}
EOF

# Test 6: DiscoverPerformance - performance_metrics with different filters
cat > tools_regression_tests/interface_2/discover_performance_2.json << 'EOF'
{
    "env": "incident_management_redo",
    "interface_num": 2,
    "task": {
        "actions": [
            {
                "name": "discover_performance",
                "arguments": {
                    "entity_type": "performance_metrics",
                    "filters": {
                        "incident_id": "INC002",
                        "metric_type": "MTTD",
                        "calculated_value_minutes": 45,
                        "recorded_by": "user_456"
                    }
                }
            },
            {
                "name": "discover_performance",
                "arguments": {
                    "entity_type": "performance_metrics",
                    "filters": {
                        "metric_type": "FTR",
                        "sla_target_minutes": 95,
                        "recorded_date": "2025-10-02"
                    }
                }
            }
        ]
    }
}
EOF

# Test 7: DiscoverAudit - audit_trails
cat > tools_regression_tests/interface_2/discover_audit_1.json << 'EOF'
{
    "env": "incident_management_redo",
    "interface_num": 2,
    "task": {
        "actions": [
            {
                "name": "discover_audit",
                "arguments": {
                    "entity_type": "audit_trails",
                    "filters": {
                        "audit_id": "AUD001",
                        "reference_id": "INC001",
                        "reference_type": "incident",
                        "action": "update",
                        "user_id": "user_123",
                        "field_name": "status",
                        "created_at": "2025-10-04"
                    }
                }
            },
            {
                "name": "discover_audit",
                "arguments": {
                    "entity_type": "audit_trails",
                    "filters": {
                        "reference_type": "user",
                        "action": "create",
                        "user_id": "user_456",
                        "old_value": "null",
                        "new_value": "active"
                    }
                }
            }
        ]
    }
}
EOF

# Test 8: DiscoverAudit - audit_trails with different filters
cat > tools_regression_tests/interface_2/discover_audit_2.json << 'EOF'
{
    "env": "incident_management_redo",
    "interface_num": 2,
    "task": {
        "actions": [
            {
                "name": "discover_audit",
                "arguments": {
                    "entity_type": "audit_trails",
                    "filters": {
                        "reference_id": "CHG001",
                        "reference_type": "change",
                        "action": "delete",
                        "field_name": "risk_level",
                        "old_value": "high",
                        "new_value": "null"
                    }
                }
            },
            {
                "name": "discover_audit",
                "arguments": {
                    "entity_type": "audit_trails",
                    "filters": {
                        "user_id": "user_789",
                        "action": "create",
                        "reference_type": "communication",
                        "created_at": "2025-10-03"
                    }
                }
            }
        ]
    }
}
EOF

# Test 9: DiscoverChangeControl - change_requests
cat > tools_regression_tests/interface_2/discover_change_control_1.json << 'EOF'
{
    "env": "incident_management_redo",
    "interface_num": 2,
    "task": {
        "actions": [
            {
                "name": "discover_change_control",
                "arguments": {
                    "entity_type": "change_requests",
                    "filters": {
                        "change_id": "CHG001",
                        "incident_id": "INC001",
                        "title": "Database Patch",
                        "change_type": "emergency",
                        "risk_level": "high",
                        "requested_by": "user_123",
                        "approved_by": "user_456",
                        "status": "approved",
                        "implementation_date": "2025-10-05",
                        "created_at": "2025-10-01"
                    }
                }
            },
            {
                "name": "discover_change_control",
                "arguments": {
                    "entity_type": "change_requests",
                    "filters": {
                        "change_number": "CHG0001234",
                        "description": "security update",
                        "risk_level": "medium",
                        "status": "completed",
                        "updated_at": "2025-10-06"
                    }
                }
            }
        ]
    }
}
EOF

# Test 10: DiscoverChangeControl - rollback_requests
cat > tools_regression_tests/interface_2/discover_change_control_2.json << 'EOF'
{
    "env": "incident_management_redo",
    "interface_num": 2,
    "task": {
        "actions": [
            {
                "name": "discover_change_control",
                "arguments": {
                    "entity_type": "rollback_requests",
                    "filters": {
                        "rollback_id": "RBK001",
                        "change_id": "CHG001",
                        "incident_id": "INC001",
                        "title": "Rollback Failed Patch",
                        "requested_by": "user_123",
                        "approved_by": "user_456",
                        "rollback_reason": "performance degradation",
                        "status": "completed",
                        "executed_at": "2025-10-06",
                        "created_at": "2025-10-05"
                    }
                }
            },
            {
                "name": "discover_change_control",
                "arguments": {
                    "entity_type": "rollback_requests",
                    "filters": {
                        "rollback_number": "RBK0001234",
                        "rollback_reason": "system instability",
                        "status": "requested",
                        "executed_at": "2025-10-04"
                    }
                }
            }
        ]
    }
}
EOF

echo "Created 10 test files in tools_regression_tests/interface_2/"