#!/bin/bash

# Create directory structure
mkdir -p tools_regression_tests/interface_3

# Create attain_permission_test.json
cat > tools_regression_tests/interface_3/attain_permission_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 3,
  "task": {
    "actions": [
      {
        "name": "attain_permission",
        "arguments": {
          "filters": {
            "permission_id": "1"
          }
        }
      },
      {
        "name": "attain_permission",
        "arguments": {
          "filters": {
            "content_id": "1",
            "content_type": "space",
            "operation": "admin"
          }
        }
      },
      {
        "name": "attain_permission",
        "arguments": {
          "filters": {
            "permission_id": "2",
            "content_id": "1",
            "content_type": "space",
            "user_id": "5",
            "operation": "delete",
            "granted_by": "26"
          }
        }
      }
    ]
  }
}
EOF

# Create discover_whiteboard_view_test.json
cat > tools_regression_tests/interface_3/discover_whiteboard_view_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 3,
  "task": {
    "actions": [
      {
        "name": "discover_whiteboard_view",
        "arguments": {
          "whiteboard_view_id": "1"
        }
      },
      {
        "name": "discover_whiteboard_view",
        "arguments": {
          "title": "Brainstorming Session",
          "host_document_id": "48",
          "status": "current"
        }
      },
      {
        "name": "discover_whiteboard_view",
        "arguments": {
          "whiteboard_view_id": "5",
          "title": "Team Goals",
          "host_document_id": "82",
          "status": "current",
          "created_by": "19",
          "updated_by": "28"
        }
      }
    ]
  }
}
EOF

# Create insert_whiteboard_view_test.json
cat > tools_regression_tests/interface_3/insert_whiteboard_view_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 3,
  "task": {
    "actions": [
      {
        "name": "insert_whiteboard_view",
        "arguments": {
          "title": "New Architecture Review",
          "created_by": "1",
          "host_document_id": "1"
        }
      },
      {
        "name": "insert_whiteboard_view",
        "arguments": {
          "title": "Planning Session 2024",
          "created_by": "5",
          "host_document_id": "4"
        }
      },
      {
        "name": "insert_whiteboard_view",
        "arguments": {
          "title": "Q2 Strategy Workshop",
          "created_by": "7",
          "host_document_id": "2",
          "content": "[{\"id\": \"1\", \"type\": \"circle\", \"text\": \"Strategic Goals\", \"x_position\": 100, \"y_position\": 200, \"width\": 120, \"height\": 120, \"color\": \"blue\"}, {\"id\": \"2\", \"type\": \"rectangle\", \"text\": \"Implementation Plan\", \"x_position\": 300, \"y_position\": 200, \"width\": 150, \"height\": 100, \"color\": \"green\"}]",
          "status": "draft"
        }
      }
    ]
  }
}
EOF

# Create insert_document_test.json
cat > tools_regression_tests/interface_3/insert_document_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 3,
  "task": {
    "actions": [
      {
        "name": "insert_document",
        "arguments": {
          "title": "New Engineering Standards",
          "workspace_id": "1",
          "created_by": "1"
        }
      },
      {
        "name": "insert_document",
        "arguments": {
          "title": "Implementation Checklist",
          "workspace_id": "1",
          "created_by": "4",
          "parent_document_id": "4"
        }
      },
      {
        "name": "insert_document",
        "arguments": {
          "title": "Infrastructure Setup Guide",
          "workspace_id": "4",
          "created_by": "10",
          "parent_document_id": "1",
          "body_storage": "<h1>Infrastructure Setup</h1>\n<p>Follow these steps to set up the infrastructure:</p>\n<ol>\n<li>Provision servers and network resources</li>\n<li>Configure security groups and firewalls</li>\n<li>Set up monitoring and alerting</li>\n<li>Deploy application stack</li>\n<li>Run health checks and validation tests</li>\n</ol>\n<p>Ensure all systems are operational before proceeding.</p>",
          "status": "draft"
        }
      }
    ]
  }
}
EOF

echo "✅ Test files created successfully!"
echo "📁 Location: tools_regression_tests/interface_3/"
echo ""
echo "📋 Files created:"
echo "  - attain_permission_test.json"
echo "  - discover_whiteboard_view_test.json"
echo "  - insert_whiteboard_view_test.json"
echo "  - insert_document_test.json"
echo ""
echo "📊 Test Coverage Summary:"
echo "  AttainPermission:"
echo "    ✓ Test 1: Single filter (permission_id)"
echo "    ✓ Test 2: Multiple filters (content_id, content_type, operation)"
echo "    ✓ Test 3: All 6 filters including granted_by"
echo ""
echo "  DiscoverWhiteboardView:"
echo "    ✓ Test 1: Single filter (whiteboard_view_id: 1)"
echo "    ✓ Test 2: Multiple filters (title, host_document_id, status)"
echo "    ✓ Test 3: All filters including created_by and updated_by"
echo ""
echo "  InsertWhiteboardView:"
echo "    ✓ Test 1: Required + host_document_id (3 params)"
echo "    ✓ Test 2: Required + different host_document_id (3 params)"
echo "    ✓ Test 3: All parameters with content and status (5 params)"
echo ""
echo "  InsertDocument:"
echo "    ✓ Test 1: Required only (3 params)"
echo "    ✓ Test 2: Required + parent_document_id (4 params)"
echo "    ✓ Test 3: All parameters with body_storage and status (6 params)"