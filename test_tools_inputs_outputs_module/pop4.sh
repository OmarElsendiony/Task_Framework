#!/bin/bash

# Create directory structure
mkdir -p tools_regression_tests/interface_4

# Create attain_user_test.json
cat > tools_regression_tests/interface_4/attain_user_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 4,
  "task": {
    "actions": [
      {
        "name": "attain_user",
        "arguments": {
          "user_id": "1"
        }
      },
      {
        "name": "attain_user",
        "arguments": {
          "email": "susanrogers@example.org",
          "status": "active"
        }
      },
      {
        "name": "attain_user",
        "arguments": {
          "user_id": "7",
          "email": "arnoldmaria@example.net",
          "display_name": "Nicole Ward",
          "status": "active"
        }
      }
    ]
  }
}
EOF

# Create find_doc_test.json
cat > tools_regression_tests/interface_4/find_doc_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 4,
  "task": {
    "actions": [
      {
        "name": "find_doc",
        "arguments": {
          "doc_id": "1"
        }
      },
      {
        "name": "find_doc",
        "arguments": {
          "space_id": "1",
          "status": "current",
          "created_by": "16"
        }
      },
      {
        "name": "find_doc",
        "arguments": {
          "doc_id": "4",
          "space_id": "1",
          "title": "Release Notes",
          "status": "current",
          "created_by": "16",
          "updated_by": "18"
        }
      }
    ]
  }
}
EOF

# Create locate_space_test.json
cat > tools_regression_tests/interface_4/locate_space_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 4,
  "task": {
    "actions": [
      {
        "name": "locate_space",
        "arguments": {
          "space_id": "1"
        }
      },
      {
        "name": "locate_space",
        "arguments": {
          "type": "global",
          "status": "current"
        }
      },
      {
        "name": "locate_space",
        "arguments": {
          "space_id": "4",
          "space_key": "SPACE004",
          "name": "Stewart, Fischer and Ramos",
          "description": "Private collaborative space for team coordination.",
          "type": "personal",
          "status": "current"
        }
      }
    ]
  }
}
EOF

# Create grant_admin_on_doc_test.json
cat > tools_regression_tests/interface_4/grant_admin_on_doc_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 4,
  "task": {
    "actions": [
      {
        "name": "grant_admin_on_doc",
        "arguments": {
          "user_id": "1",
          "doc_id": "1"
        }
      },
      {
        "name": "grant_admin_on_doc",
        "arguments": {
          "user_id": "5",
          "doc_id": "2"
        }
      },
      {
        "name": "grant_admin_on_doc",
        "arguments": {
          "user_id": "7",
          "doc_id": "5"
        }
      }
    ]
  }
}
EOF

# Create locate_user_permissions_test.json
cat > tools_regression_tests/interface_4/locate_user_permissions_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 4,
  "task": {
    "actions": [
      {
        "name": "locate_user_permissions",
        "arguments": {
          "filter": {
            "user_id": "26"
          }
        }
      },
      {
        "name": "locate_user_permissions",
        "arguments": {
          "filter": {
            "user_id": "5",
            "doc_id": "1"
          }
        }
      },
      {
        "name": "locate_user_permissions",
        "arguments": {
          "filter": {
            "user_id": "22",
            "space_id": "2"
          }
        }
      }
    ]
  }
}
EOF

# Create construct_doc_test.json
cat > tools_regression_tests/interface_4/construct_doc_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 4,
  "task": {
    "actions": [
      {
        "name": "construct_doc",
        "arguments": {
          "fields": {
            "space_id": "1",
            "title": "New Technical Specification",
            "created_by": "1"
          }
        }
      },
      {
        "name": "construct_doc",
        "arguments": {
          "fields": {
            "space_id": "2",
            "title": "Updated Process Documentation",
            "created_by": "5",
            "body_storage": "<h2>Process Overview</h2>\n<p>Follow these documented processes:</p>\n<ol><li>Review all requirements</li><li>Execute test cases</li><li>Document findings</li><li>Generate reports</li></ol>"
          }
        }
      },
      {
        "name": "construct_doc",
        "arguments": {
          "fields": {
            "space_id": "4",
            "title": "Complete Project Plan",
            "created_by": "7",
            "body_storage": "<h1>Project Plan 2024</h1>\n<h2>Phase 1: Planning</h2>\n<p>Define scope and requirements in detail.</p>\n<h2>Phase 2: Development</h2>\n<p>Implement features according to specifications.</p>\n<h2>Phase 3: Testing</h2>\n<p>Execute comprehensive test suite and validation.</p>\n<h2>Phase 4: Deployment</h2>\n<p>Release to production with monitoring.</p>",
            "status": "draft"
          }
        }
      }
    ]
  }
}
EOF

# Create destroy_doc_test.json
cat > tools_regression_tests/interface_4/destroy_doc_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 4,
  "task": {
    "actions": [
      {
        "name": "destroy_doc",
        "arguments": {
          "doc_id": "6"
        }
      },
      {
        "name": "destroy_doc",
        "arguments": {
          "doc_id": "7"
        }
      },
      {
        "name": "destroy_doc",
        "arguments": {
          "doc_id": "8"
        }
      }
    ]
  }
}
EOF

echo "✅ Test files created successfully!"
echo "📁 Location: tools_regression_tests/interface_4/"
echo ""
echo "📋 Files created:"
echo "  - attain_user_test.json"
echo "  - find_doc_test.json"
echo "  - locate_space_test.json"
echo "  - grant_admin_on_doc_test.json"
echo "  - locate_user_permissions_test.json"
echo "  - construct_doc_test.json"
echo "  - destroy_doc_test.json"
echo ""
echo "📊 Test Coverage Summary:"
echo ""
echo "  AttainUser:"
echo "    ✓ Test 1: Single filter (user_id: '1')"
echo "      Expected: User 'Donald Garcia' with email johnsonjoshua@example.org"
echo "    ✓ Test 2: Multiple filters (email, status)"
echo "      Expected: User 'Noah Howard' (user_id '5') with active status"
echo "    ✓ Test 3: All 4 filters"
echo "      Expected: User 'Nicole Ward' (user_id '7') matching all criteria"
echo ""
echo "  FindDoc:"
echo "    ✓ Test 1: Single filter (doc_id: '1')"
echo "      Expected: 'Team Guidelines' page"
echo "    ✓ Test 2: Multiple filters (space_id, status, created_by)"
echo "      Expected: 'Release Notes' document"
echo "    ✓ Test 3: All 6 filters"
echo "      Expected: Complete 'Release Notes' match with all metadata"
echo ""
echo "  LocateSpace:"
echo "    ✓ Test 1: Single filter (space_id: '1')"
echo "      Expected: 'Davis Group' space"
echo "    ✓ Test 2: Multiple filters (type, status)"
echo "      Expected: All global spaces with current status"
echo "    ✓ Test 3: All 6 filters"
echo "      Expected: 'Stewart, Fischer and Ramos' with complete details"
echo ""
echo "  GrantAdminOnDoc:"
echo "    ✓ Test 1: Grant admin to user '1' on doc '1'"
echo "    ✓ Test 2: Grant admin to user '5' on doc '2'"
echo "    ✓ Test 3: Grant admin to user '7' on doc '5'"
echo ""
echo "  LocateUserPermissions:"
echo "    ✓ Test 1: Filter by user_id only (user '26')"
echo "    ✓ Test 2: Filter by user_id + doc_id (user '5' on doc '1')"
echo "    ✓ Test 3: Filter by user_id + space_id (user '22' on space '2')"
echo ""
echo "  ConstructDoc:"
echo "    ✓ Test 1: Required fields only (space_id, title, created_by)"
echo "    ✓ Test 2: With body_storage (4 fields)"
echo "    ✓ Test 3: All fields including status (5 fields)"
echo ""
echo "  DestroyDoc:"
echo "    ✓ Test 1: Destroy doc '6'"
echo "    ✓ Test 2: Destroy doc '7'"
echo "    ✓ Test 3: Destroy doc '8'"