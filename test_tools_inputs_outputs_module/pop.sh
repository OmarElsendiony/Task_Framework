#!/bin/bash

# Create directory structure
mkdir -p tools_regression_tests/interface_2

# Create obtain_user_test.json
cat > tools_regression_tests/interface_2/obtain_user_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 2,
  "task": {
    "actions": [
      {
        "name": "obtain_user",
        "arguments": {
          "user_id": "1"
        }
      },
      {
        "name": "obtain_user",
        "arguments": {
          "email": "susanrogers@example.org"
        }
      },
      {
        "name": "obtain_user",
        "arguments": {
          "user_id": "7",
          "email": "arnoldmaria@example.net",
          "status": "active"
        }
      }
    ]
  }
}
EOF

# Create add_page_test.json
cat > tools_regression_tests/interface_2/add_page_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 2,
  "task": {
    "actions": [
      {
        "name": "add_page",
        "arguments": {
          "title": "Database Migration Guide",
          "site_id": "1",
          "created_by": "1"
        }
      },
      {
        "name": "add_page",
        "arguments": {
          "title": "Performance Optimization",
          "site_id": "4",
          "created_by": "5",
          "parent_page_id": "1"
        }
      },
      {
        "name": "add_page",
        "arguments": {
          "title": "Security Best Practices",
          "site_id": "2",
          "created_by": "10",
          "parent_page_id": "2",
          "body_storage": "<h2>Security Guidelines</h2>\n<p>Follow these security best practices:</p>\n<ul><li>Always use HTTPS for data transmission</li><li>Implement OAuth 2.0 for authentication</li><li>Regularly update dependencies and patches</li><li>Conduct security audits quarterly</li><li>Use environment variables for sensitive data</li></ul>\n<p>For more details, consult the security team.</p>",
          "status": "draft"
        }
      }
    ]
  }
}
EOF

# Create discover_page_test.json
cat > tools_regression_tests/interface_2/discover_page_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 2,
  "task": {
    "actions": [
      {
        "name": "discover_page",
        "arguments": {
          "page_id": "1"
        }
      },
      {
        "name": "discover_page",
        "arguments": {
          "title": "Technical Architecture",
          "site_id": "5",
          "status": "current"
        }
      },
      {
        "name": "discover_page",
        "arguments": {
          "page_id": "4",
          "title": "Release Notes",
          "site_id": "1",
          "parent_page_id": null,
          "status": "current",
          "created_by": "16",
          "created_at": "2023-04-05T17:27:00",
          "updated_by": "18",
          "updated_at": "2023-06-30T07:18:00"
        }
      }
    ]
  }
}
EOF

# Create search_site_test.json
cat > tools_regression_tests/interface_2/search_site_test.json << 'EOF'
{
  "env": "wiki_pages",
  "interface_num": 2,
  "task": {
    "actions": [
      {
        "name": "search_site",
        "arguments": {
          "site_id": "1"
        }
      },
      {
        "name": "search_site",
        "arguments": {
          "site_name": "Rasmussen LLC",
          "status": "current"
        }
      },
      {
        "name": "search_site",
        "arguments": {
          "site_id": "4",
          "site_url": "SPACE004",
          "site_name": "Stewart, Fischer and Ramos",
          "description": "Private collaborative space for team coordination.",
          "status": "current",
          "created_by": "19",
          "created_at": "2023-01-16T05:24:00",
          "updated_at": "2023-01-16T17:40:00"
        }
      }
    ]
  }
}
EOF

echo "✅ Test files created successfully!"
echo "📁 Location: tools_regression_tests/interface_2/"
echo ""
echo "📋 Files created:"
echo "  - obtain_user_test.json"
echo "  - add_page_test.json"
echo "  - discover_page_test.json"
echo "  - search_site_test.json"
echo ""
echo "📊 Test Coverage Summary:"
echo ""
echo "  ObtainUser:"
echo "    ✓ Test 1: Single filter (user_id: '1')"
echo "      Expected: User 'Donald Garcia' with email johnsonjoshua@example.org"
echo "    ✓ Test 2: Email filter only (email: susanrogers@example.org)"
echo "      Expected: User 'Noah Howard' with user_id '5'"
echo "    ✓ Test 3: All 3 parameters (user_id, email, status)"
echo "      Expected: User 'Nicole Ward' matching all filters"
echo ""
echo "  AddPage:"
echo "    ✓ Test 1: Required only (title, site_id, created_by)"
echo "      Creates new page in space '1' by user '1'"
echo "    ✓ Test 2: Required + parent_page_id (4 params)"
echo "      Creates child page under page '1' in space '4'"
echo "    ✓ Test 3: All parameters (6 params)"
echo "      Full page creation with content and draft status"
echo ""
echo "  DiscoverPage:"
echo "    ✓ Test 1: Single filter (page_id: '1')"
echo "      Expected: 'Team Guidelines' page"
echo "    ✓ Test 2: Multiple filters (title, site_id, status)"
echo "      Expected: 'Technical Architecture' in space '5'"
echo "    ✓ Test 3: All 9 parameters"
echo "      Expected: 'Release Notes' with full metadata"
echo ""
echo "  SearchSite:"
echo "    ✓ Test 1: Single filter (site_id: '1')"
echo "      Expected: 'Davis Group' space"
echo "    ✓ Test 2: Multiple filters (site_name, status)"
echo "      Expected: 'Rasmussen LLC' space"
echo "    ✓ Test 3: All 8 parameters"
echo "      Expected: Complete 'Stewart, Fischer and Ramos' space details"