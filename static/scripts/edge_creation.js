
var edgeCreationExpanded = false
function toggleEdgeCreation() {
    const content = document.getElementById('edge-creation-content');
    const toggle = document.getElementById('edge-creation-toggle');
    const promptText = document.getElementById('edge-creation-prompt');

    edgeCreationExpanded = !edgeCreationExpanded;

    if (edgeCreationExpanded) {
        content.classList.add('expanded');
        actions = getTaskActions()
        toggle.textContent = '▲';
        promptText.textContent = `
I have a set of actions that are interconnected, and I need to see these connection in terms of edges represented in JSON format. The edges should be realistic and represent how the output(s) of one action connect to the input(s) of other actions. I am going to give you the instructions that will help you decide the edges as well as some example tasks that have the actions and their corresponding edges and your task is to generate for me the new set of edges for the actions I will present along with their number. Please, look at the things from logical perspective. If a value that is provided to an action is not present in the output of a previous action, then that value should come from the "instruction" node (which I will explain more later). You have to take care if it does come from the output of a previous action so you can create the edge from that action to the current action and do not mistakenly create an edge from the "instruction" node. Look multiple times in the output of the actions to be sure. Also, DO NOT REPEAT ANY EDGE. Only if the nodes follow a different path like one is used for a subsequent action and the other for another one, then you can add the same node and the same edge. please, follow the instructions below carefully.

## General Instructions

**Field-by-Field Verification Protocol:**
- For each input parameter in every action, systematically check ALL previous action outputs to determine if that exact value exists
- Do not assume multiple inputs come from the same source - verify each field individually
- Only assign an input to "instruction" source AFTER confirming it does not exist in any prior action output
- Create a mental checklist: "Does input X exist in output of action 1? action 2? action 3?" etc.

**Complete Output Structure Analysis:**
- Before creating any edges, thoroughly examine the full output structure of each action
- Read through all fields, nested objects, and arrays in each output to understand what data is available
- Look for exact value matches between action outputs and subsequent action inputs
- Pay special attention to fields that might be easily overlooked
- When you find a matching value, immediately note it as a potential connection before moving to the next action
- Note that not all inputs to an action should come from a single action, but some may be from multiple actions. So, take care

**Verification Before Assignment:**
- Default assumption should be: "This input probably comes from a previous action output"
- Only assign to "instruction" source as a last resort after systematic verification
- Double-check any edge where multiple inputs come from "instruction"

These instructions enforce the systematic, methodical approach needed to avoid missing obvious connections between action outputs and inputs.

## Edge Mapping Instructions

### 1. **One-to-One Edge Rule**
- **Only one edge** between any two functions (A→B)
- If function B needs multiple inputs from function A, combine them in a **single edge** with comma-separated values
- Example:
\`\`\`json
{
"from": "get_user_details",
"to": "create_profile", 
"connection": {
"output": "first_name, last_name, email",
"input": "name, surname, contact_email"
}
}
\`\`\`

### 2. **Execution Order Consistency**
- In the \`actions\` array: Function A must be executed **before** Function B
- In the \`edges\` array: Edge A→B must exist if B depends on A's output
- The edge list should reflect the **actual execution path only**

### 3. **Instruction-to-Function Edges**
- Add edges from \`"instruction"\` when a function needs inputs **not provided by upstream functions**
- Common cases:
- Static values from the task description
- User-provided parameters
- Configuration values

### 4. **List Output Handling**

#### **Single Item Selection:**
\`\`\`json
{
"from": "get_applications",
"to": "schedule_interview",
"connection": {
"output": "output[0].application_id",
"input": "application_id"
}
}
\`\`\`

#### **Multiple Items Selection:**
\`\`\`json
{
"from": "get_candidates", 
"to": "batch_update_status",
"connection": {
"output": "output[0,1,2].candidate_id",  // First 3 items
"input": "candidate_ids"
}
}
\`\`\`

#### **All Items:**
\`\`\`json
{
"from": "get_all_invoices",
"to": "process_batch",
"connection": {
"output": "output[].invoice_id",  // All items
"input": "invoice_ids"
}
}
\`\`\`

### 5. **Formula/Calculation Edges**
When outputs need to be combined or calculated:
\`\`\`json
{
"from": "get_user_info",
"to": "create_display_name", 
"connection": {
"output": "first_name + ' ' + last_name",
"input": "full_name"
}
}
\`\`\`

### 6. **Multi-Source Dependencies**
If a function needs inputs from **multiple sources**, create separate edges:
\`\`\`json
// Edge 1: From previous function
{
"from": "get_investor",
"to": "create_subscription",
"connection": {
"output": "investor_id",
"input": "investor_id" 
}
},
// Edge 2: From instruction
{
"from": "instruction",
"to": "create_subscription", 
"connection": {
"output": "amount",
"input": "subscription_amount"
}
}
\`\`\`

### 7. **Validation Rules**
- ✅ **Do**: Map only the **executed path** shown in actions
- ✅ **Do**: Ensure chronological consistency (A executes before B if A→B edge exists)
- ❌ **Don't**: Create edges for alternate branches not taken
- ❌ **Don't**: Duplicate edges between the same two functions
- ❌ **Don't**: Create circular dependencies

### 8. **Special Cases**

#### **Conditional Flows:**
Only map the path that was actually executed based on the actions sequence.

#### **Approval Validations:**
\`\`\`json
{
"from": "validate_approval",
"to": "update_subscription",
"connection": {
"output": "approval_valid, approval_valid",  // Same validation used twice
"input": "compliance_approval, finance_approval"
}
}
\`\`\`

#### **Audit Trail Creation:**
Map both the reference ID and any changed values:
\`\`\`json
{
"from": "update_record",
"to": "create_audit_log",
"connection": {
"output": "record_id, new_status", 
"input": "reference_id, new_value"
}
}
\`\`\`

These instructions ensure the edge mapping accurately reflects the **actual execution flow** while maintaining logical consistency and avoiding redundant connections.

## Examples of actions + corresponding edges:

{
"env": "finance",
"model_provider": "openai",
"model": "o4-mini",
"num_trials": 3,
"temperature": 1,
"interface_num": 2,
"task": {
"user_id": "86",
"instruction": "You are Matthew Anderson (email: \"matthewanderson524@outlook.com\"), a fund manager. You want to update the \"pending\" \"subscription\" request from \"Crawford Group\" investor (compliance officer: \"Alan Montoya\") to an amount of \"4823125.1\", using approval codes \"SUBUP0124\" and \"SUBUF0143\". You also want to create a new subscription for the same investor under the Green-Wright Growth Fund \"mutual_funds\" with an amount of \"5123612.45\" using approval code \"SUBCR0035\".",
"actions": [
    {
        "name": "find_user",
        "arguments": {
            "email": "matthewanderson524@outlook.com"
        },
        "output": [
            {
                "created_at": "2023-09-28T01:38:34",
                "email": "matthewanderson524@outlook.com",
                "first_name": "Matthew",
                "last_name": "Anderson",
                "role": "fund_manager",
                "status": "active",
                "timezone": "Asia/Tokyo",
                "updated_at": "2024-01-31T13:44:56",
                "user_id": "86"
            }
        ]
    },
    {
        "name": "find_user",
        "arguments": {
            "first_name": "Alan",
            "last_name": "Montoya"
        },
        "output": [
            {
                "created_at": "2023-11-25T04:53:29",
                "email": "alanmontoya@gmail.com",
                "first_name": "Alan",
                "last_name": "Montoya",
                "role": "compliance_officer",
                "status": "active",
                "timezone": "America/Los_Angeles",
                "updated_at": "2025-04-23T11:21:12",
                "user_id": "79"
            }
        ]
    },
    {
        "name": "get_filtered_investors",
        "arguments": {
            "name_contains": "Crawford Group"
        },
        "output": [
            {
                "accreditation_status": "non_accredited",
                "address": "616 Amy Islands, North Markport, ME 58948",
                "contact_email": "crawford5315@investment.com",
                "country": "Japan",
                "created_at": "2024-03-09T01:38:55",
                "date_of_incorporation": "2022-10-01",
                "investor_id": "25",
                "name": "Crawford Group",
                "registration_number": 992570805,
                "source_of_funds": "asset_sale",
                "status": "onboarded",
                "tax_id": "962-75-7059"
            }
        ]
    },
    {
        "name": "get_investor_subscription_list",
        "arguments": {
            "investor_id": "25",
            "request_assigned_to": "79",
            "status": "pending"
        },
        "output": [
            {
                "amount": 4783567.22,
                "approval_date": null,
                "fund_id": "11",
                "investor_id": "25",
                "request_assigned_to": "79",
                "request_date": "2024-04-03",
                "status": "pending",
                "subscription_id": "336",
                "updated_at": "2025-06-21T14:58:01"
            }
        ]
    },
    {
        "name": "approval_lookup",
        "arguments": {
            "approval_code": "SUBUP0124"
        },
        "output": {
            "approval_valid": true,
            "approved_by": "79"
        }
    },
    {
        "name": "approval_lookup",
        "arguments": {
            "approval_code": "SUBUF0143"
        },
        "output": {
            "approval_valid": true,
            "approved_by": "66"
        }
    },
    {
        "name": "update_investor_subscription",
        "arguments": {
            "compliance_officer_approval": true,
            "field_name": "amount",
            "field_value": 4823125.1,
            "finance_officer_approval": true,
            "subscription_id": "336"
        },
        "output": {
            "subscription_after_update": {
                "amount": 4823125.1,
                "approval_date": null,
                "fund_id": "11",
                "investor_id": "25",
                "request_assigned_to": "79",
                "request_date": "2024-04-03",
                "status": "pending",
                "subscription_id": "336",
                "updated_at": "2025-10-01T00:00:00"
            }
        }
    },
    {
        "name": "insert_audit_trail",
        "arguments": {
            "action": "update",
            "field_name": "amount",
            "new_value": 4823125.1,
            "old_value": 4783567.22,
            "reference_id": "336",
            "reference_type": "subscription"
        },
        "output": {
            "action": "update",
            "audit_trail_id": "3501",
            "created_at": "2025-10-01T00:00:00",
            "field_name": "amount",
            "new_value": 4823125.1,
            "old_value": 4783567.22,
            "reference_id": "336",
            "reference_type": "subscription"
        }
    },
    {
        "name": "filter_funds",
        "arguments": {
            "fund_type": "mutual_funds",
            "investor_id": "25"
        },
        "output": [
            {
                "created_at": "2023-04-21T09:04:46",
                "fund_id": "4",
                "fund_type": "mutual_funds",
                "manager_id": "43",
                "name": "Green-Wright Growth Fund",
                "size": 111576603.84,
                "status": "open",
                "updated_at": "2025-04-27T18:13:30"
            },
            {
                "created_at": "2025-08-10T09:16:03",
                "fund_id": "39",
                "fund_type": "mutual_funds",
                "manager_id": "73",
                "name": "Peters-Black Strategic Fund",
                "size": 207210537.83,
                "status": "open",
                "updated_at": "2025-08-15T17:26:32"
            },
            {
                "created_at": "2023-08-01T08:44:47",
                "fund_id": "64",
                "fund_type": "mutual_funds",
                "manager_id": "12",
                "name": "Kerr and Sons Balanced Fund",
                "size": 147390520.21,
                "status": "open",
                "updated_at": "2024-12-16T09:31:57"
            },
            {
                "created_at": "2024-09-04T16:07:50",
                "fund_id": "85",
                "fund_type": "mutual_funds",
                "manager_id": "88",
                "name": "Bryant and Sons Balanced Fund",
                "size": 62670779.64,
                "status": "open",
                "updated_at": "2025-03-07T01:32:16"
            },
            {
                "created_at": "2024-02-04T06:23:45",
                "fund_id": "90",
                "fund_type": "mutual_funds",
                "manager_id": "83",
                "name": "Hines, Bennett and Cantu Balanced Fund",
                "size": 58944119.88,
                "status": "open",
                "updated_at": "2024-10-19T11:31:32"
            },
            {
                "created_at": "2025-06-29T17:06:44",
                "fund_id": "98",
                "fund_type": "mutual_funds",
                "manager_id": "45",
                "name": "James, Stewart and Higgins Growth Fund",
                "size": 122540879.68,
                "status": "open",
                "updated_at": "2025-08-10T10:19:06"
            }
        ]
    },
    {
        "name": "approval_lookup",
        "arguments": {
            "approval_code": "SUBCR0035"
        },
        "output": {
            "approval_valid": true,
            "approved_by": "79"
        }
    },
    {
        "name": "create_investor_subscription",
        "arguments": {
            "amount": 5123612.45,
            "compliance_officer_approval": true,
            "fund_id": "4",
            "investor_id": "25"
        },
        "output": {
            "amount": 5123612.45,
            "approval_date": "2025-10-01",
            "fund_id": "4",
            "investor_id": "25",
            "request_assigned_to": "6",
            "request_date": "2025-10-01",
            "status": "approved",
            "subscription_id": "2501",
            "updated_at": "2025-10-01T00:00:00"
        }
    },
    {
        "name": "insert_audit_trail",
        "arguments": {
            "action": "create",
            "reference_id": "2501",
            "reference_type": "subscription"
        },
        "output": {
            "action": "create",
            "audit_trail_id": "3502",
            "created_at": "2025-10-01T00:00:00",
            "field_name": null,
            "new_value": null,
            "old_value": null,
            "reference_id": "2501",
            "reference_type": "subscription"
        }
    }
],
"outputs": [
    "4823125.1",
    "Green-Wright Growth Fund",
    "2501"
],
"edges": [
    {
        "from": "instruction",
        "to": "find_user",
        "connection": {
            "output": "email, first_name, last_name",
            "input": "email, first_name, last_name"
        }
    },
    {
        "from": "instruction",
        "to": "get_filtered_investors",
        "connection": {
            "output": "name",
            "input": "name_contains"
        }
    },
    {
        "from": "get_filtered_investors",
        "to": "get_investor_subscription_list",
        "connection": {
            "output": "output[0].investor_id",
            "input": "investor_id"
        }
    },
    {
        "from": "find_user",
        "to": "get_investor_subscription_list",
        "connection": {
            "output": "output[0].user_id",
            "input": "request_assigned_to"
        }
    },
    {
        "from": "instruction",
        "to": "get_investor_subscription_list",
        "connection": {
            "output": "status",
            "input": "status"
        }
    },
    {
        "from": "instruction",
        "to": "approval_lookup",
        "connection": {
            "output": "code",
            "input": "approval_code"
        }
    },
    {
        "from": "approval_lookup",
        "to": "update_investor_subscription",
        "connection": {
            "output": "approval_valid, approval_valid",
            "input": "compliance_officer_approval, finance_officer_approval"
        }
    },
    {
        "from": "instruction",
        "to": "update_investor_subscription",
        "connection": {
            "output": "field_name, field_value",
            "input": "field_name, field_value"
        }
    },
    {
        "from": "get_investor_subscription_list",
        "to": "update_investor_subscription",
        "connection": {
            "output": "output[0].subscription_id",
            "input": "subscription_id"
        }
    },
    {
        "from": "update_investor_subscription",
        "to": "insert_audit_trail",
        "connection": {
            "output": "subscription_after_update.amount, subscription_after_update.subscription_id",
            "input": "new_value, reference_id"
        }
    },
    {
        "from": "instruction",
        "to": "insert_audit_trail",
        "connection": {
            "output": "action, field_name, reference_type",
            "input": "action, field_name, reference_type"
        }
    },
    {
        "from": "get_investor_subscription_list",
        "to": "insert_audit_trail",
        "connection": {
            "output": "amount",
            "input": "old_value"
        }
    },
    {
        "from": "instruction",
        "to": "filter_funds",
        "connection": {
            "output": "fund_type",
            "input": "fund_type"
        }
    },
    {
        "from": "update_investor_subscription",
        "to": "filter_funds",
        "connection": {
            "output": "subscription_after_update.investor_id",
            "input": "investor_id"
        }
    },
    {
        "from": "instruction",
        "to": "create_investor_subscription",
        "connection": {
            "output": "amount",
            "input": "amount"
        }
    },
    {
        "from": "approval_lookup",
        "to": "create_investor_subscription",
        "connection": {
            "output": "approval_valid",
            "input": "compliance_officer_approval"
        }
    },
    {
        "from": "update_investor_subscription",
        "to": "create_investor_subscription",
        "connection": {
            "output": "subscription_after_update.investor_id",
            "input": "investor_id"
        }
    },
    {
        "from": "filter_funds",
        "to": "create_investor_subscription",
        "connection": {
            "output": "output[0].fund_id",
            "input": "target_fund_id"
        }
    },
    {
        "from": "create_investor_subscription",
        "to": "insert_audit_trail",
        "connection": {
            "output": "new_subscription.subscription_id",
            "input": "reference_id"
        }
    }
],
"num_edges": 19
}
}

{
"env": "hr_management",
"model_provider": "openai",
"model": "o4-mini",
"num_trials": 3,
"temperature": 1,
"interface_num": 1,
"task": {
"user_id": "11",
"instruction": "You are Gina Banks, a recruiter with the email 'gina.banks@outlook.com'. You have been informed that the candidate with the email 'kevinwyatt@protonmail.com' was recently interviewed for the role of 'Operations Manager' in the 'Executive Support' department, and hired under conditions of internal bias. You want to ensure interview integrity for this position by scheduling a re-interview with hiring manager Sonya Garcia (email: 'sonya68@protonmail.com') as the interviewer on August 28, 2025, matching the interview type and length conducted for the application with the lowest AI screening score, and updating that application's status to 'interviewing' using your approval code 'APP0002' and Sonya Garcia's approval code 'APP0008'.",
"actions": [
{
"name": "get_users",
"arguments": {
    "email": "gina.banks@outlook.com",
    "role": "recruiter"
},
"output": [
    {
    "created_at": "2020-11-26T13:25:25",
    "email": "gina.banks@outlook.com",
    "first_name": "Gina",
    "last_name": "Banks",
    "mfa_enabled": true,
    "phone_number": "+19298421880",
    "role": "recruiter",
    "status": "active",
    "updated_at": "2023-05-22T14:48:47",
    "user_id": "11"
    }
]
},
{
"name": "get_candidates",
"arguments": {
    "email": "kevinwyatt@protonmail.com"
},
"output": [
    {
    "address": "USNV Walker, FPO AE 71492",
    "candidate_id": "10",
    "created_at": "2021-09-08T08:09:54",
    "email": "kevinwyatt@protonmail.com",
    "first_name": "Kevin",
    "last_name": "Wyatt",
    "phone_number": "+14704232368",
    "source": "company_website",
    "status": "hired",
    "updated_at": "2022-08-08T17:37:35"
    }
]
},
{
"name": "get_departments",
"arguments": {
    "department_name": "Executive Support"
},
"output": [
    {
    "budget": 4227482.77,
    "created_at": "2023-09-06T02:08:33",
    "department_id": "68",
    "department_name": "Executive Support",
    "manager_id": "10",
    "status": "active",
    "updated_at": "2024-11-04T14:18:34"
    }
]
},
{
"name": "get_job_positions",
"arguments": {
    "department_id": "68",
    "title": "Operations Manager"
},
"output": [
    {
    "created_at": "2024-06-09T00:17:08",
    "department_id": "68",
    "employment_type": "full_time",
    "hourly_rate_max": 125,
    "hourly_rate_min": 85,
    "job_level": "manager",
    "position_id": "317",
    "status": "closed",
    "title": "Operations Manager",
    "updated_at": "2025-10-01T00:00:00"
    }
]
},

{
"name": "get_job_applications",
"arguments": {
    "candidate_id": "10",
    "position_id": "317"
},
"output": [
    {
    "ai_screening_score": 71.9,
    "application_date": "2023-11-20",
    "application_id": "18",
    "candidate_id": "10",
    "created_at": "2023-11-20T11:20:58",
    "final_decision": "hire",
    "position_id": "317",
    "recruiter_id": "11",
    "status": "accepted",
    "updated_at": "2024-02-22T19:23:55"
    },
    {
    "ai_screening_score": 87.03,
    "application_date": "2023-07-18",
    "application_id": "19",
    "candidate_id": "10",
    "created_at": "2023-07-18T02:23:10",
    "final_decision": "hire",
    "position_id": "317",
    "recruiter_id": "11",
    "status": "accepted",
    "updated_at": "2024-12-18T22:11:06"
    }
]
},
{
"name": "get_interviews",
"arguments": {
    "application_id": "18"
},
"output": [
    {
    "application_id": "18",
    "communication_score": 9.3,
    "created_at": "2023-11-26T00:09:44",
    "cultural_fit_score": 8.5,
    "duration_minutes": 45,
    "interview_id": "18",
    "interview_type": "technical",
    "interviewer_id": "31",
    "overall_rating": "excellent",
    "recommendation": "strong_hire",
    "scheduled_date": "2023-12-01T21:34:15",
    "status": "completed",
    "technical_score": 7.7,
    "updated_at": "2025-07-27T19:13:51"
    }
]
},
{
"name": "get_users",
"arguments": {
    "email": "sonya68@protonmail.com",
    "role": "hiring_manager"
},
"output": [
    {
    "created_at": "2024-10-03T21:06:44",
    "email": "sonya68@protonmail.com",
    "first_name": "Sonya",
    "last_name": "Garcia",
    "mfa_enabled": true,
    "phone_number": "+17183431042",
    "role": "hiring_manager",
    "status": "active",
    "updated_at": "2025-04-01T03:24:29",
    "user_id": "28"
    }
]
},
{
"name": "schedule_interview",
"arguments": {
    "application_id": "18",
    "duration_minutes": 45,
    "interview_type": "technical",
    "interviewer_id": "28",
    "scheduled_date": "2025-08-28T00:00:00"
},
"output": {
    "interview_id": "348",
    "success": true
}
},
{
"name": "create_audit_log",
"arguments": {
    "action": "create",
    "reference_id": "348",
    "reference_type": "interview",
    "user_id": "11"
},
"output": {
    "log_id": "2885",
    "success": true
}
},
{
"name": "validate_approval",
"arguments": {
    "approval_code": "APP0002"
},
"output": {
    "approval_valid": true,
    "approved_by": "11"
}
},
{
"name": "validate_approval",
"arguments": {
    "approval_code": "APP0008"
},
"output": {
    "approval_valid": true,
    "approved_by": "28"
}
},
{
"name": "update_application_stage",
"arguments": {
    "application_id": "18",
    "hiring_manager_approval": true,
    "recruiter_approval": true,
    "status": "interviewing"
},
"output": {
    "message": "Application stage updated",
    "success": true
}
},
{
"name": "create_audit_log",
"arguments": {
    "action": "update",
    "field_name": "status",
    "new_value": "interviewing",
    "old_value": "accepted",
    "reference_id": "18",
    "reference_type": "job_application",
    "user_id": "11"
},
"output": {
    "log_id": "2886",
    "success": true
}
}
],
"edges": [
{
"from": "instruction",
"to": "get_users",
"connection": {
    "input": "email, role",
    "output": "email, role"
}
},
{
"from": "instruction",
"to": "get_candidates",
"connection": {
    "input": "email",
    "output": "email"
}
},
{
"from": "instruction",
"to": "get_departments",
"connection": {
    "input": "department_name",
    "output": "department_name"
}
},
{
"from": "get_departments",
"to": "get_job_positions",
"connection": {
    "input": "department_id",
    "output": "output[0].department_id"
}
},
{
"from": "instruction",
"to": "get_job_positions",
"connection": {
    "input": "title",
    "output": "title"
}
},
{
"from": "get_candidates",
"to": "get_job_applications",
"connection": {
    "input": "candidate_id",
    "output": "output[0].candidate_id"
}
},
{
"from": "get_job_positions",
"to": "get_job_applications",
"connection": {
    "input": "position_id",
    "output": "output[0].position_id"
}
},
{
"from": "get_job_applications",
"to": "get_interviews",
"connection": {
    "input": "application_id",
    "output": "output[0].application_id"
}
},
{
"from": "get_job_applications",
"to": "schedule_interview",
"connection": {
    "input": "application_id",
    "output": "output[0].application_id"
}
},
{
"from": "get_interviews",
"to": "schedule_interview",
"connection": {
    "input": "duration_minutes, interview_type",
    "output": "output[0].duration_minutes, output[0].interview_type"
}
},
{
"from": "get_users",
"to": "schedule_interview",
"connection": {
    "input": "interviewer_id",
    "output": "output[0].user_id"
}
},
{
"from": "instruction",
"to": "schedule_interview",
"connection": {
    "input": "scheduled_date",
    "output": "scheduled_date"
}
},
{
"from": "instruction",
"to": "create_audit_log",
"connection": {
    "input": "action, field_name, new_value, reference_type",
    "output": "action, field_name, new_value, reference_type"
}
},
{
"from": "schedule_interview",
"to": "create_audit_log",
"connection": {
    "input": "reference_id",
    "output": "interview_id"
}
},
{
"from": "get_users",
"to": "create_audit_log",
"connection": {
    "input": "user_id",
    "output": "output[0].user_id"
}
},
{
"from": "instruction",
"to": "validate_approval",
"connection": {
    "input": "approval_code",
    "output": "approval_code"
}
},
{
"from": "get_job_applications",
"to": "update_application_stage",
"connection": {
    "input": "application_id",
    "output": "output[0].application_id"
}
},
{
"from": "validate_approval",
"to": "update_application_stage",
"connection": {
    "input": "hiring_manager_approval, recruiter_approval",
    "output": "approval_valid, approval_valid"
}
},
{
"from": "instruction",
"to": "update_application_stage",
"connection": {
    "input": "status",
    "output": "status"
}
},
{
"from": "get_job_applications",
"to": "create_audit_log",
"connection": {
    "input": "old_value, reference_id",
    "output": "output[0].status, output[0].application_id"
}
}
],
"num_edges": 20
}
}


## Actions that I want their edges along with their number in JSON format:
${JSON.stringify(actions, null, 2)}
`;

        // promptText.textContent = `Based on the following actions, create edges in JSON format. Actions: ${JSON.stringify(actions, null, 2)}`;

    } else {
        content.classList.remove('expanded');
        toggle.textContent = '▼';
    }
}
