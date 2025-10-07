from datetime import datetime
from typing import Any, Dict
from typing import Any, Dict, List
from typing import Any, Dict, Optional
import json

class Tools:
    @staticmethod
    def discover_knowledge_article_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover knowledge base article entities.
        
        Supported entities:
        - knowledge_base_articles: Knowledge base article records
        """
        if entity_type not in ["knowledge_base_articles"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'knowledge_base_articles'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("knowledge_base_articles", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "article_id": str(entity_id)})
            else:
                results.append({**entity_data, "article_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def discover_incident_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover incident-related entities.
        
        Supported entities:
        - incidents: Incident records
        - incident_reports: Incident report records
        - post_incident_reviews: Post-incident review records
        """
        if entity_type not in ["incidents", "incident_reports", "post_incident_reviews"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'incidents', 'incident_reports', or 'post_incident_reviews'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        # Determine the ID field based on entity type
        id_field_map = {
            "incidents": "incident_id",
            "incident_reports": "report_id",
            "post_incident_reviews": "pir_id"
        }
        id_field = id_field_map[entity_type]
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: str(entity_id)})
            else:
                results.append({**entity_data, id_field: str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_kb_articles_invoke(data: Dict[str, Any], action: str, article_data: Dict[str, Any] = None, article_id: str = None) -> str:
        """
        Create or update knowledge base articles.

        Actions:
        - create: requires article_data with title, article_type, created_by_id, category
        - update: requires article_id and article_data with fields to update
        """

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        kb_articles = data.get("knowledge_base_articles", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})

        valid_article_types = ["troubleshooting", "resolution_steps", "prevention_guide", "faq"]
        valid_categories = [
            "authentication_issues", "payment_processing", "api_integration", "data_synchronization",
            "system_outages", "performance_degradation", "security_incidents", "backup_recovery",
            "user_management", "billing_issues", "compliance_procedures", "vendor_escalations",
            "configuration_changes", "monitoring_alerts", "network_connectivity", "database_issues",
            "file_transfer_problems", "reporting_errors", "mobile_app_issues", "browser_compatibility",
            "third_party_integrations", "scheduled_maintenance", "emergency_procedures", "client_onboarding",
            "account_provisioning", "sla_management", "incident_response", "change_management",
            "capacity_planning", "disaster_recovery"
        ]
        valid_statuses = ["draft", "published", "archived"]

        if action == "create":
            if not article_data:
                return json.dumps({
                    "success": False,
                    "error": "article_data is required for create action"
                })

            required_fields = ["title", "article_type", "created_by_id", "category"]
            missing = [f for f in required_fields if f not in article_data or not article_data.get(f)]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for article creation: {', '.join(missing)}"
                })

            title = article_data["title"]
            article_type = article_data["article_type"]
            created_by_id = str(article_data["created_by_id"])
            category = article_data["category"]
            incident_id = article_data.get("incident_id")
            reviewed_by_id = article_data.get("reviewed_by_id")
            view_count = article_data.get("view_count", 0)
            status = article_data.get("status", "draft")

            # Validations
            if article_type not in valid_article_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid article_type. Must be one of: {', '.join(valid_article_types)}"
                })

            if category not in valid_categories:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid category. Must be one of: {', '.join(valid_categories)}"
                })

            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })

            if incident_id:
                if incident_id not in incidents:
                    return json.dumps({"success": False, "error": f"Incident {incident_id} not found"})
                if incidents[incident_id].get("status") not in ["resolved", "closed"]:
                    return json.dumps({"success": False, "error": f"Incident must be resolved or closed"})

            if reviewed_by_id and reviewed_by_id not in users:
                return json.dumps({"success": False, "error": f"Reviewer {reviewed_by_id} not found"})

            if not isinstance(view_count, int) or view_count < 0:
                return json.dumps({"success": False, "error": "view_count must be a non-negative integer"})

            new_article_id = generate_id(kb_articles)
            new_article = {
                "article_id": str(new_article_id),
                "incident_id": incident_id,
                "title": title,
                "article_type": article_type,
                "created_by_id": created_by_id,
                "reviewed_by_id": reviewed_by_id,
                "category": category,
                "view_count": view_count,
                "status": status,
                "created_at": "2025-10-02T12:00:00",
                "updated_at": "2025-10-02T12:00:00"
            }

            kb_articles[str(new_article_id)] = new_article
            return json.dumps({
                "success": True, 
                "action": "create", 
                "article_id": str(new_article_id),
                "message": f"KB article {new_article_id} created successfully", 
                "article_data": new_article
            })

        elif action == "update":
            if not article_id:
                return json.dumps({"success": False, "error": "article_id is required for update action"})
            if article_id not in kb_articles:
                return json.dumps({"success": False, "error": f"Knowledge base article {article_id} not found"})
            if not article_data:
                return json.dumps({"success": False, "error": "article_data is required for update action"})

            current_article = kb_articles[article_id].copy()
            for key in ["title", "article_type", "incident_id", "reviewed_by_id", "category", "view_count", "status"]:
                if key in article_data:
                    value = article_data[key]
                    # Validation for certain fields
                    if key == "article_type" and value not in valid_article_types:
                        return json.dumps({"success": False, "error": f"Invalid article_type. Must be one of: {', '.join(valid_article_types)}"})
                    if key == "category" and value not in valid_categories:
                        return json.dumps({"success": False, "error": f"Invalid category. Must be one of: {', '.join(valid_categories)}"})
                    if key == "status" and value not in valid_statuses:
                        return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
                    if key == "incident_id" and value and value not in incidents:
                        return json.dumps({"success": False, "error": f"Incident {value} not found"})
                    if key == "reviewed_by_id" and value and value not in users:
                        return json.dumps({"success": False, "error": f"Reviewer {value} not found"})
                    if key == "view_count" and (not isinstance(value, int) or value < 0):
                        return json.dumps({"success": False, "error": "view_count must be a non-negative integer"})
                    current_article[key] = value

            current_article["updated_at"] = "2025-10-02T12:00:00"
            kb_articles[article_id] = current_article
            return json.dumps({
                "success": True, 
                "action": "update", 
                "article_id": article_id,
                "message": f"KB article {article_id} updated successfully",
                "article_data": current_article
            })

    @staticmethod
    def transfer_to_human_invoke(
        data: Dict[str, Any],
        summary: str,
    ) -> str:
        return "Transfer successful"

    @staticmethod
    def discover_workaround_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover workaround entities.
        
        Supported entities:
        - workarounds: Workaround records
        """
        if entity_type not in ["workarounds"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'workarounds'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("workarounds", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "workaround_id": str(entity_id)})
            else:
                results.append({**entity_data, "workaround_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_rollback_requests_invoke(data: Dict[str, Any], action: str, rollback_data: Dict[str, Any], rollback_id: str = None) -> str:
        """
        Create or update rollback request records.

        rollback_data must include:
        - action (required): 'create' or 'update'
        For create:
            - change_id (required)
            - requested_by_id (required)
            - Optional: incident_id, approved_by_id, executed_at, validation_completed, status
        For update:
            - rollback_id (required)
            - Optional: approved_by_id, executed_at, validation_completed, status
        """

        def generate_id(table:  Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def generate_code(prefix: str, table: Dict[str, Any]) -> str:
            max_num = 0
            for record in table.values():
                code = record.get("rollback_code", "")
                if code.startswith(prefix):
                    try:
                        num = int(code.split("-")[-1])
                        max_num = max(max_num, num)
                    except:
                        pass
            return f"{prefix}-{str(max_num + 1).zfill(5)}"

        rollback_requests = data.get("rollback_requests", {})
        change_requests = data.get("change_requests", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        change_id = rollback_data.get("change_id")
        requested_by_id = rollback_data.get("requested_by_id")
        incident_id = rollback_data.get("incident_id")
        approved_by_id = rollback_data.get("approved_by_id")
        executed_at = rollback_data.get("executed_at")
        validation_completed = rollback_data.get("validation_completed")
        status = rollback_data.get("status")

        valid_statuses = ["requested", "approved", "in_progress", "completed", "failed"]

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False, 
                "error": f"Invalid {action}. Must be 'create' or 'update'"
            })

        if action == "create":
            if not all([change_id, requested_by_id]):
                return json.dumps({"success": False, "error": "change_id and requested_by_id are required for create"})

            if change_id not in change_requests:
                return json.dumps({"success": False, "error": f"Change request {change_id} not found"})

            if requested_by_id not in users:
                return json.dumps({"success": False, "error": f"Requesting user {requested_by_id} not found"})

            if users[requested_by_id].get("role") not in ["system_administrator", "executive", "incident_manager"]:
                return json.dumps({"success": False, "error": f"Invalid role for requesting user {requested_by_id}"})

            if incident_id and incident_id not in incidents:
                return json.dumps({"success": False, "error": f"Incident {incident_id} not found"})

            if status and status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})

            new_id = generate_id(rollback_requests)
            rollback_code = generate_code("RBK-2025", rollback_requests)

            new_request = {
                "rollback_id": str(new_id),
                "rollback_code": rollback_code,
                "change_id": change_id,
                "incident_id": incident_id,
                "requested_by_id": requested_by_id,
                "approved_by_id": approved_by_id,
                "executed_at": executed_at,
                "validation_completed": validation_completed if validation_completed is not None else False,
                "status": status if status else "requested",
                "created_at": "2025-10-02T12:00:00"
            }

            rollback_requests[str(new_id)] = new_request

            return json.dumps({
                "success": True, 
                "action": "create", 
                "rollback_id": str(new_id),
                "message": f"Rollback request {new_id} created successfully", 
                "rollback_request_data": new_request
            })

        elif action == "update":
            if not rollback_id:
                return json.dumps({"success": False, "error": "rollback_id is required for update"})

            if rollback_id not in rollback_requests:
                return json.dumps({"success": False, "error": f"Rollback request {rollback_id} not found"})

            if not any([approved_by_id is not None, executed_at, validation_completed is not None, status]):
                return json.dumps({"success": False, "error": "At least one field must be provided for update"})

            if status and status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})

            updated_request = rollback_requests[rollback_id].copy()
            for field, value in [("approved_by_id", approved_by_id), ("executed_at", executed_at),
                                 ("validation_completed", validation_completed), ("status", status)]:
                if value is not None:
                    updated_request[field] = value

            rollback_requests[rollback_id] = updated_request

            return json.dumps({
                "success": True, 
                "action": "update", 
                "rollback_id": rollback_id,
                "message": f"Rollback request {rollback_id} updated successfully", 
                "rollback_request_data": updated_request
            })

    @staticmethod
    def manage_vendors_invoke(data: Dict[str, Any], action: str, vendor_data: Dict[str, Any] = None, vendor_id: str = None) -> str:
        """
        Create or update vendor records.

        Actions:
        - create: Create new vendor (requires vendor_data with vendor_name, vendor_type)
        - update: Update existing vendor (requires vendor_id and vendor_data with fields to change)
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for vendors"
            })

        vendors = data.get("vendors", {})

        valid_vendor_types = ["cloud_provider", "payment_processor", "software_vendor", "infrastructure_provider", "security_vendor"]
        valid_statuses = ["active", "inactive", "suspended"]

        if action == "create":
            if not vendor_data:
                return json.dumps({
                    "success": False,
                    "error": "vendor_data is required for create action"
                })

            # Required fields
            required_fields = ["vendor_name", "vendor_type"]
            missing = [f for f in required_fields if f not in vendor_data or not vendor_data.get(f)]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for vendor creation: {', '.join(missing)}"
                })

            vendor_name = vendor_data["vendor_name"]
            vendor_type = vendor_data["vendor_type"]
            contact_email = vendor_data.get("contact_email")
            contact_phone = vendor_data.get("contact_phone")
            status = vendor_data.get("status", "active")

            # Validate vendor_type
            if vendor_type not in valid_vendor_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid vendor_type. Must be one of: {', '.join(valid_vendor_types)}"
                })

            # Validate status
            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })

            # Check uniqueness of vendor_name
            for existing_vendor in vendors.values():
                if existing_vendor.get("vendor_name") == vendor_name:
                    return json.dumps({
                        "success": False,
                        "error": f"Vendor name '{vendor_name}' already exists"
                    })

            # Create vendor
            new_id = generate_id(vendors)
            new_vendor = {
                "vendor_id": str(new_id),
                "vendor_name": vendor_name,
                "vendor_type": vendor_type,
                "status": status,
                "created_at": "2025-10-04T12:00:00"
            }

            if contact_email:
                new_vendor["contact_email"] = contact_email
            if contact_phone:
                new_vendor["contact_phone"] = contact_phone

            vendors[str(new_id)] = new_vendor

            return json.dumps({
                "success": True,
                "action": "create",
                "vendor_id": str(new_id),
                "message": f"Vendor {new_id} created successfully",
                "vendor_data": new_vendor
            })

        elif action == "update":
            if not vendor_id:
                return json.dumps({
                    "success": False,
                    "error": "vendor_id is required for update action"
                })

            if vendor_id not in vendors:
                return json.dumps({
                    "success": False,
                    "error": f"Vendor {vendor_id} not found"
                })

            if not vendor_data:
                return json.dumps({
                    "success": False,
                    "error": "vendor_data is required for update action"
                })

            current_vendor = vendors[vendor_id].copy()

            # Validate and update vendor_type
            if "vendor_type" in vendor_data:
                vt = vendor_data["vendor_type"]
                if vt not in valid_vendor_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid vendor_type. Must be one of: {', '.join(valid_vendor_types)}"
                    })
                current_vendor["vendor_type"] = vt

            # Validate and update status
            if "status" in vendor_data:
                st = vendor_data["status"]
                if st not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                current_vendor["status"] = st

            # Check uniqueness of vendor_name if updating
            if "vendor_name" in vendor_data:
                new_name = vendor_data["vendor_name"]
                for vid, existing_vendor in vendors.items():
                    if vid != vendor_id and existing_vendor.get("vendor_name") == new_name:
                        return json.dumps({
                            "success": False,
                            "error": f"Vendor name '{new_name}' already exists"
                        })
                current_vendor["vendor_name"] = new_name

            # Update other fields
            for field in ["contact_email", "contact_phone"]:
                if field in vendor_data:
                    current_vendor[field] = vendor_data[field]

            vendors[vendor_id] = current_vendor

            return json.dumps({
                "success": True,
                "action": "update",
                "vendor_id": vendor_id,
                "message": f"Vendor {vendor_id} updated successfully",
                "vendor_data": current_vendor
            })

    @staticmethod
    def manage_communications_invoke(data: Dict[str, Any], action: str, communication_data: Dict[str, Any] = None, communication_id: str = None) -> str:
        """
        Create or update communication records.

        Actions:
        - create: Create new communication (requires communication_data with incident_id, sender_id, recipient_type, communication_type)
        - update: Update existing communication (requires communication_id and communication_data with fields to change)
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for communications"
            })

        communications = data.get("communications", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        # Allowed/enums
        valid_recipient_types = ["client", "internal_team", "executive", "vendor", "regulatory"]
        valid_communication_types = ["email", "sms", "phone_call", "status_page", "portal_update"]
        valid_delivery_statuses = ["sent", "delivered", "failed", "pending"]

        if action == "create":
            if not communication_data:
                return json.dumps({
                    "success": False,
                    "error": "communication_data is required for create action"
                })

            # Validate required fields for creation
            required_fields = ["incident_id", "sender_id", "recipient_type", "communication_type"]
            missing = [f for f in required_fields if f not in communication_data]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for communication creation: {', '.join(missing)}"
                })

            # # Approval: require at least one of the roles
            # if not (communication_data.get("incident_manager") or communication_data.get("technical_support") or communication_data.get("system_administrator") or communication_data.get("account_manager")):
            #     return json.dumps({
            #         "success": False,
            #         "error": "Missing approval for creating communication record. Required: incident_manager OR technical_support OR system_administrator OR account_manager"
            #     })
            
            # Only allow known fields to be supplied
            allowed_fields = [
                "incident_id", "sender_id", "recipient_id", "recipient_type",
                "communication_type", "delivery_status", "sent_at"
            ]
            invalid_fields = [k for k in communication_data.keys() if k not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for communication creation: {', '.join(invalid_fields)}"
                })

            incident_id = str(communication_data["incident_id"])
            sender_id = str(communication_data["sender_id"])
            recipient_id = communication_data.get("recipient_id")
            recipient_type = communication_data["recipient_type"]
            communication_type = communication_data["communication_type"]
            delivery_status = communication_data.get("delivery_status")
            sent_at = communication_data.get("sent_at")

            # Validate incident exists
            if incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident {incident_id} not found"
                })

            # Validate sender exists and is active
            if sender_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Sender {sender_id} not found"
                })
            if users[sender_id].get("status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Sender {sender_id} is not active"
                })

            # Validate recipient if specified
            if recipient_id and str(recipient_id) not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Recipient {recipient_id} not found"
                })

            # Validate enums
            if recipient_type not in valid_recipient_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid recipient_type. Must be one of: {', '.join(valid_recipient_types)}"
                })

            if communication_type not in valid_communication_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid communication_type. Must be one of: {', '.join(valid_communication_types)}"
                })

            if delivery_status and delivery_status not in valid_delivery_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid delivery_status. Must be one of: {', '.join(valid_delivery_statuses)}"
                })

            # Generate ID and create record
            new_id = generate_id(communications)
            new_comm = {
                "communication_id": str(new_id),
                "incident_id": incident_id,
                "sender_id": sender_id,
                "recipient_id": str(recipient_id) if recipient_id is not None else None,
                "recipient_type": recipient_type,
                "communication_type": communication_type,
                "sent_at": sent_at if sent_at else "2025-10-02T12:00:00",
                "delivery_status": delivery_status if delivery_status else "pending",
                "created_at": "2025-10-02T12:00:00",
                "updated_at": "2025-10-02T12:00:00"
            }

            communications[str(new_id)] = new_comm

            return json.dumps({
                "success": True,
                "action": "create",
                "communication_id": str(new_id),
                "message": f"Communication {new_id} created successfully",
                "communication_data": new_comm
            })

        elif action == "update":
            if not communication_id:
                return json.dumps({
                    "success": False,
                    "error": "communication_id is required for update action"
                })

            if communication_id not in communications:
                return json.dumps({
                    "success": False,
                    "error": f"Communication {communication_id} not found"
                })

            if not communication_data:
                return json.dumps({
                    "success": False,
                    "error": "communication_data is required for update action"
                })

            # # Approval required for updates as well
            # if not (communication_data.get("incident_manager") or communication_data.get("technical_support") or communication_data.get("system_administrator") or communication_data.get("account_manager")):
            #     return json.dumps({
            #         "success": False,
            #         "error": "Missing approval for creating communication record. Required: incident_manager OR technical_support OR system_administrator OR account_manager"
            #     })

            # Only allow known update fields
            allowed_update_fields = [
                "incident_id", "sender_id", "recipient_id", "recipient_type",
                "communication_type", "delivery_status", "sent_at"
            ]
            invalid_fields = [k for k in communication_data.keys() if k not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for communication update: {', '.join(invalid_fields)}"
                })

            # At least one valid field must be present
            if not any(field in communication_data for field in allowed_update_fields):
                return json.dumps({
                    "success": False,
                    "error": "At least one updatable field must be provided in communication_data"
                })

            current_comm = communications[communication_id].copy()

            # Validate fields when present
            if "incident_id" in communication_data:
                incident_id = str(communication_data["incident_id"])
                if incident_id not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident {incident_id} not found"
                    })
                current_comm["incident_id"] = incident_id

            if "sender_id" in communication_data:
                sender_id = str(communication_data["sender_id"])
                if sender_id not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Sender {sender_id} not found"
                    })
                if users[sender_id].get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"Sender {sender_id} is not active"
                    })
                current_comm["sender_id"] = sender_id

            if "recipient_id" in communication_data:
                recipient_id = communication_data["recipient_id"]
                if recipient_id and str(recipient_id) not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Recipient {recipient_id} not found"
                    })
                current_comm["recipient_id"] = str(recipient_id) if recipient_id is not None else None

            if "recipient_type" in communication_data:
                recipient_type = communication_data["recipient_type"]
                if recipient_type not in valid_recipient_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid recipient_type. Must be one of: {', '.join(valid_recipient_types)}"
                    })
                current_comm["recipient_type"] = recipient_type

            if "communication_type" in communication_data:
                communication_type = communication_data["communication_type"]
                if communication_type not in valid_communication_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid communication_type. Must be one of: {', '.join(valid_communication_types)}"
                    })
                current_comm["communication_type"] = communication_type

            if "delivery_status" in communication_data:
                delivery_status = communication_data["delivery_status"]
                if delivery_status not in valid_delivery_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid delivery_status. Must be one of: {', '.join(valid_delivery_statuses)}"
                    })
                current_comm["delivery_status"] = delivery_status

            if "sent_at" in communication_data:
                current_comm["sent_at"] = communication_data["sent_at"]

            current_comm["updated_at"] = "2025-10-02T12:00:00"
            communications[communication_id] = current_comm

            return json.dumps({
                "success": True,
                "action": "update",
                "communication_id": str(communication_id),
                "message": f"Communication {communication_id} updated successfully",
                "communication_data": current_comm
            })

    @staticmethod
    def log_audit_records_invoke(data: Dict[str, Any], audit_data: Dict[str, Any]) -> str:
        """
        Create audit log records for tracking changes to system entities.
        
        This tool only supports creation of audit records - no updates are allowed
        as audit logs are immutable for compliance purposes.
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        # Access audit_log data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for audit_log"
            })
        
        audit_log = data.get("audit_log", {})
        
        if not audit_data:
            return json.dumps({
                "success": False,
                "error": "audit_data is required for audit log creation"
            })
        
        # Validate required fields for creation
        required_fields = ["entity_type", "entity_id", "operation_type", "changed_by_id"]
        missing_fields = [field for field in required_fields if field not in audit_data]
        if missing_fields:
            return json.dumps({
                "success": False,
                "error": f"Missing required fields for audit log creation: {', '.join(missing_fields)}"
            })
        
        # Validate only allowed fields are present
        allowed_fields = ["entity_type", "entity_id", "operation_type", "changed_by_id", "field_name", "old_value", "new_value"]
        invalid_fields = [field for field in audit_data.keys() if field not in allowed_fields]
        if invalid_fields:
            return json.dumps({
                "success": False,
                "error": f"Invalid fields for audit log creation: {', '.join(invalid_fields)}"
            })
        
        # Validate enum fields
        valid_operation_types = ["INSERT", "UPDATE", "DELETE"]
        if audit_data["operation_type"] not in valid_operation_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{audit_data['operation_type']}'. Must be one of: {', '.join(valid_operation_types)}"
            })
        
        # Validate entity_type (should be a valid table name)
        valid_entity_types = ["clients", "vendors", "users", "products", "infrastructure_components", 
                             "client_subscriptions", "sla_agreements", "incidents", "workarounds", 
                             "root_cause_analysis", "communications", "escalations", "change_requests", 
                             "rollback_requests", "metrics", "incident_reports", "knowledge_base_articles", 
                             "post_incident_reviews"]
        if audit_data["entity_type"] not in valid_entity_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{audit_data['entity_type']}'. Must be one of: {', '.join(valid_entity_types)}"
            })
        
        # For UPDATE operations, field_name should be provided
        if audit_data["operation_type"] == "UPDATE" and not audit_data.get("field_name"):
            return json.dumps({
                "success": False,
                "error": "field_name is required for UPDATE operations"
            })
        
        # Generate new audit ID
        new_audit_id = generate_id(audit_log)
        
        # Create new audit log record
        new_audit_record = {
            "audit_id": str(new_audit_id),
            "entity_type": audit_data["entity_type"],
            "entity_id": str(audit_data["entity_id"]),
            "operation_type": audit_data["operation_type"],
            "changed_by_id": str(audit_data["changed_by_id"]),
            "field_name": audit_data.get("field_name"),
            "old_value": str(audit_data.get("old_value")) if audit_data.get("old_value") is not None else None,
            "new_value": str(audit_data.get("new_value")) if audit_data.get("new_value") is not None else None,
            "created_at": "2025-10-01T00:00:00"
        }
        
        audit_log[str(new_audit_id)] = new_audit_record
        
        return json.dumps({
            "success": True,
            "action": "create",
            "audit_id": str(new_audit_id),
            "audit_data": new_audit_record
        })

    @staticmethod
    def manage_users_invoke(
        data: Dict[str, Any],
        # approval: bool,
        # For Create
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        timezone: Optional[str] = None,
        phone: Optional[str] = None,
        department: Optional[str] = None,
        client_id: Optional[str] = None,
        vendor_id: Optional[str] = None,
        status: Optional[str] = "active",
        # For Update
        user_id: Optional[str] = None
    ) -> str:

        users = data.get("users", {})
        clients = data.get("clients", {})
        vendors = data.get("vendors", {})

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        valid_roles = [
            "incident_manager", "technical_support", "account_manager",
            "executive", "vendor_contact", "system_administrator",
            "client_contact"
        ]
        valid_status = ["active", "inactive", "on_leave"]

        # ----- Check Approval -----
        # if not approval:
        #     return json.dumps({
        #         "success": False,
        #         "error": "Approval missing for user management action"
        #     })

        # ----- CREATE -----
        if not user_id:
            # Required fields
            if not first_name or not last_name or not email or not role or not timezone:
                return json.dumps({
                    "success": False,
                    "error": "Missing or invalid inputs"
                })

            if role not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid role. Must be one of {valid_roles}"
                })

            if status and status not in valid_status:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_status}"
                })

            # Check email uniqueness
            for user in users.values():
                if user.get("email") == email:
                    return json.dumps({
                        "success": False,
                        "error": "Email already exists"
                    })

            # Validate client
            if client_id:
                client = clients.get(client_id)
                if not client or client.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Client not found or inactive"
                    })

            # Validate vendor
            if vendor_id:
                vendor = vendors.get(vendor_id)
                if not vendor or vendor.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Vendor not found or inactive"
                    })

            # Create new user
            new_id = str(generate_id(users))
            timestamp = "2025-10-01T00:00:00"

            new_user = {
                "user_id": new_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "role": role,
                "timezone": timezone,
                "phone": phone,
                "department": department,
                "client_id": client_id,
                "vendor_id": vendor_id,
                "status": status,
                "created_at": timestamp
            }
            users[new_id] = new_user

            # Simulate audit record logging
            if not data.get("audit_log"):
                data["audit_log"] = []
            data["audit_log"].append({
                "action": "create_user",
                "user_id": new_id,
                "timestamp": timestamp
            })

            return json.dumps(new_user)

        # ----- UPDATE -----
        else:
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "User not found"
                })

            user = users[user_id]

            if email:
                # Check uniqueness
                for uid, existing in users.items():
                    if uid != user_id and existing.get("email") == email:
                        return json.dumps({
                            "success": False,
                            "error": "New email already exists"
                        })
                user["email"] = email

            if role and role not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid role. Must be one of {valid_roles}"
                })

            if status and status not in valid_status:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_status}"
                })

            # Validate client
            if client_id:
                client = clients.get(client_id)
                if not client or client.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Client not found or inactive"
                    })
                user["client_id"] = client_id

            # Validate vendor
            if vendor_id:
                vendor = vendors.get(vendor_id)
                if not vendor or vendor.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Vendor not found or inactive"
                    })
                user["vendor_id"] = vendor_id

            # Update allowed fields
            for field, val in [
                ("first_name", first_name), ("last_name", last_name),
                ("phone", phone), ("role", role),
                ("department", department), ("timezone", timezone),
                ("status", status)
            ]:
                if val is not None:
                    user[field] = val

            # Simulate audit logging
            timestamp = "2025-10-01T00:00:00"
            if not data.get("audit_log"):
                data["audit_log"] = []
            data["audit_log"].append({
                "action": "update_user",
                "user_id": user_id,
                "timestamp": timestamp
            })

            return json.dumps(user)

    @staticmethod
    def discover_components_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover infrastructure component entities.
        
        Supported entities:
        - infrastructure_components: Infrastructure component records by component_id, product_id, component_name, component_type, environment, location, port_number, status
        """
        if entity_type not in ["infrastructure_components"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'infrastructure_components'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("infrastructure_components", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "component_id": str(entity_id)})
            else:
                results.append({**entity_data, "component_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def discover_metrics_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover metrics entities.
        
        Supported entities:
        - metrics: Incident metrics records
        """
        if entity_type not in ["metrics"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'metrics'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("metrics", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "metric_id": str(entity_id)})
            else:
                results.append({**entity_data, "metric_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_work_arounds_invoke(data: Dict[str, Any], action: str, workaround_data: Dict[str, Any] = None, workaround_id: str = None) -> str:
        """
        Create or update workaround records.
        
        Actions:
        - create: Create new workaround record (requires workaround_data with incident_id, implemented_by_id, effectiveness, status, implemented_at)
        - update: Update existing workaround record (requires workaround_id and workaround_data with changes)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        # Access workarounds data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for workarounds"
            })
        
        workarounds = data.get("workarounds", {})
        
        if action == "create":
            if not workaround_data:
                return json.dumps({
                    "success": False,
                    "error": "workaround_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["incident_id", "implemented_by_id", "effectiveness", "status", "implemented_at"]
            missing_fields = [field for field in required_fields if field not in workaround_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for workaround creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["incident_id", "implemented_by_id", "effectiveness", "status", "implemented_at"]
            invalid_fields = [field for field in workaround_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for workaround creation: {', '.join(invalid_fields)}"
                })
            
            # Validate enum fields
            valid_effectiveness = ["complete", "partial", "minimal"]
            if workaround_data["effectiveness"] not in valid_effectiveness:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid effectiveness '{workaround_data['effectiveness']}'. Must be one of: {', '.join(valid_effectiveness)}"
                })
            
            valid_statuses = ["active", "inactive", "replaced"]
            if workaround_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{workaround_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Generate new workaround ID
            new_workaround_id = generate_id(workarounds)
            
            # Create new workaround record
            new_workaround = {
                "workaround_id": str(new_workaround_id),
                "incident_id": str(workaround_data["incident_id"]),
                "implemented_by_id": str(workaround_data["implemented_by_id"]),
                "effectiveness": workaround_data["effectiveness"],
                "status": workaround_data["status"],
                "implemented_at": workaround_data["implemented_at"],
                "created_at": "2025-10-01T00:00:00"
            }
            
            workarounds[str(new_workaround_id)] = new_workaround
            
            return json.dumps({
                "success": True,
                "action": "create",
                "workaround_id": str(new_workaround_id),
                "workaround_data": new_workaround
            })
        
        elif action == "update":
            if not workaround_id:
                return json.dumps({
                    "success": False,
                    "error": "workaround_id is required for update action"
                })
            
            if workaround_id not in workarounds:
                return json.dumps({
                    "success": False,
                    "error": f"Workaround record {workaround_id} not found"
                })
            
            if not workaround_data:
                return json.dumps({
                    "success": False,
                    "error": "workaround_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["effectiveness", "status"]
            invalid_fields = [field for field in workaround_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for workaround update: {', '.join(invalid_fields)}. Cannot update incident_id, implemented_by_id, or implemented_at."
                })
            
            # Validate enum fields if provided
            if "effectiveness" in workaround_data:
                valid_effectiveness = ["complete", "partial", "minimal"]
                if workaround_data["effectiveness"] not in valid_effectiveness:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid effectiveness '{workaround_data['effectiveness']}'. Must be one of: {', '.join(valid_effectiveness)}"
                    })
            
            if "status" in workaround_data:
                valid_statuses = ["active", "inactive", "replaced"]
                if workaround_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{workaround_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Get current workaround data
            current_workaround = workarounds[workaround_id].copy()
            
            # Update workaround record
            updated_workaround = current_workaround.copy()
            for key, value in workaround_data.items():
                updated_workaround[key] = value
            
            workarounds[workaround_id] = updated_workaround
            
            return json.dumps({
                "success": True,
                "action": "update",
                "workaround_id": str(workaround_id),
                "workaround_data": updated_workaround
            })

    @staticmethod
    def manage_escalations_invoke(data: Dict[str, Any], action: str, escalation_data: Dict[str, Any] = None, escalation_id: str = None) -> str:
        """
        Create or update escalation records.

        Actions:
        - create: Create new escalation (requires escalation_data with incident_id, escalated_by_id, escalated_to_id, escalation_reason, escalation_level)
        - update: Update existing escalation (requires escalation_id and escalation_data with fields to change)
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        def generate_code(prefix: str, table: Dict[str, Any]) -> str:
            max_num = 0
            for record in table.values():
                code = record.get("escalation_code", "")
                if code.startswith(prefix):
                    try:
                        num = int(code.split("-")[-1])
                        max_num = max(max_num, num)
                    except:
                        pass
            return f"{prefix}-{str(max_num + 1).zfill(5)}"

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for escalations"
            })

        escalations = data.get("escalations", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        # Allowed/enums
        valid_levels = ["technical", "management", "executive", "vendor"]
        valid_reasons = ["sla_breach", "severity_increase", "resource_unavailable", "executive_request", "client_demand"]
        valid_statuses = ["open", "acknowledged", "resolved"]

        if action == "create":
            if not escalation_data:
                return json.dumps({
                    "success": False,
                    "error": "escalation_data is required for create action"
                })

            # Required fields
            required_fields = ["incident_id", "escalated_by_id", "escalated_to_id", "escalation_reason", "escalated_at", "escalation_level"]
            missing = [f for f in required_fields if f not in escalation_data]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for escalation creation: {', '.join(missing)}"
                })
            
            # Only allow known fields to be supplied
            allowed_fields = [
                "incident_id", "escalated_by_id", "escalated_to_id", "escalation_reason",
                "escalated_at", "escalation_level", "acknowledged_at", "resolved_at, status"
            ]
            invalid_fields = [k for k in escalation_data.keys() if k not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for escalation creation: {', '.join(invalid_fields)}"
                })

            incident_id = str(escalation_data["incident_id"])
            escalated_by_id = str(escalation_data["escalated_by_id"])
            escalated_to_id = str(escalation_data["escalated_to_id"])
            escalation_reason = escalation_data["escalation_reason"]
            escalation_level = escalation_data["escalation_level"]
            acknowledged_at = escalation_data.get("acknowledged_at")
            resolved_at = escalation_data.get("resolved_at")
            status = escalation_data.get("status")

            # Validate incident
            if incident_id not in incidents:
                return json.dumps({"success": False, "error": f"Incident {incident_id} not found"})
            if incidents[incident_id].get("status") not in ["open", "in_progress"]:
                return json.dumps({"success": False, "error": "Incident must be open or in_progress"})

            # Validate users
            if escalated_by_id not in users or users[escalated_by_id].get("status") != "active":
                return json.dumps({"success": False, "error": f"Escalating user {escalated_by_id} not found or inactive"})
            if escalated_to_id not in users:
                return json.dumps({"success": False, "error": f"Target user {escalated_to_id} not found"})

            # Validate level/role and enums
            if escalation_level not in valid_levels:
                return json.dumps({"success": False, "error": f"Invalid escalation_level. Must be one of: {', '.join(valid_levels)}"})
            if escalation_reason not in valid_reasons:
                return json.dumps({"success": False, "error": f"Invalid escalation_reason. Must be one of: {', '.join(valid_reasons)}"})
            if status and status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})

            # Generate and create
            new_id = generate_id(escalations)
            escalation_code = generate_code("ESC-2025", escalations)
            new_escalation = {
                "escalation_id": str(new_id),
                "escalation_code": escalation_code,
                "incident_id": incident_id,
                "escalated_by_id": escalated_by_id,
                "escalated_to_id": escalated_to_id,
                "escalation_reason": escalation_reason,
                "escalation_level": escalation_level,
                "acknowledged_at": acknowledged_at,
                "resolved_at": resolved_at,
                "status": status if status else "open",
                "escalated_at": "2025-10-02T12:00:00",
                "created_at": "2025-10-02T12:00:00",
                "updated_at": "2025-10-02T12:00:00"
            }
            escalations[str(new_id)] = new_escalation

            return json.dumps({
                "success": True,
                "action": "create",
                "escalation_id": str(new_id),
                "message": f"Escalation {new_id} created successfully",
                "escalation_data": new_escalation
            })

        elif action == "update":
            if not escalation_id:
                return json.dumps({"success": False, "error": "escalation_id is required for update action"})
            if escalation_id not in escalations:
                return json.dumps({"success": False, "error": f"Escalation {escalation_id} not found"})
            if not escalation_data:
                return json.dumps({"success": False, "error": "escalation_data is required for update action"})

            current = escalations[escalation_id].copy()

            for field in ["escalation_code", "acknowledged_at", "resolved_at", "status"]:
                if field in escalation_data:
                    value = escalation_data[field]
                    if field == "status" and value not in valid_statuses:
                        return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
                    current[field] = value

            current["updated_at"] = "2025-10-02T12:00:00"
            escalations[escalation_id] = current

            return json.dumps({
                "success": True,
                "action": "update",
                "escalation_id": escalation_id,
                "message": f"Escalation {escalation_id} updated successfully",
                "escalation_data": current
            })

    @staticmethod
    def manage_incidents_invoke(data: Dict[str, Any], action: str, incident_data: Dict[str, Any] = None, incident_id: str = None) -> str:
        """
        Create or update incident records.
        
        Actions:
        - create: Create new incident record (requires incident_data with title, reporter_id, client_id, category, impact, detection_source, urgency, detected_at)
        - update: Update existing incident record (requires incident_id and incident_data with changes)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        # Access incidents data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for incidents"
            })
        
        incidents = data.get("incidents", {})
        
        if action == "create":
            if not incident_data:
                return json.dumps({
                    "success": False,
                    "error": "incident_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["title", "reporter_id", "client_id", "category", "impact", "detection_source", "urgency", "detected_at"]
            missing_fields = [field for field in required_fields if field not in incident_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for incident creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present (incident_code should NOT be in create)
            allowed_fields = ["title", "reporter_id", "assigned_manager_id", "client_id", "component_id", 
                            "severity", "status", "impact", "urgency", "category", "detection_source", "detected_at", 
                            "resolved_at", "closed_at", "rto_breach", "sla_breach", "is_recurring", "downtime_minutes"]
            invalid_fields = [field for field in incident_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for incident creation: {', '.join(invalid_fields)}"
                })
            
            # Validate enum fields (only if provided for optional fields)
            valid_severities = ["P1", "P2", "P3", "P4"]
            if "severity" in incident_data and incident_data["severity"] not in valid_severities:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid severity '{incident_data['severity']}'. Must be one of: {', '.join(valid_severities)}"
                })
            
            valid_statuses = ["open", "in_progress", "resolved", "closed"]
            if "status" in incident_data and incident_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{incident_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                })
            
            valid_impacts = ["critical", "high", "medium", "low"]
            if incident_data["impact"] not in valid_impacts:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid impact '{incident_data['impact']}'. Must be one of: {', '.join(valid_impacts)}"
                })
            
            valid_urgencies = ["critical", "high", "medium", "low"]
            if incident_data["urgency"] not in valid_urgencies:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid urgency '{incident_data['urgency']}'. Must be one of: {', '.join(valid_urgencies)}"
                })
            
            valid_categories = ["system_outage", "performance_degradation", "security_incident", "data_corruption", 
                              "integration_failure", "network_issue", "hardware_failure", "software_bug", 
                              "configuration_error", "capacity_issue", "backup_failure", "authentication_failure", 
                              "api_error", "database_issue", "service_unavailable"]
            if incident_data["category"] not in valid_categories:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid category '{incident_data['category']}'. Must be one of: {', '.join(valid_categories)}"
                })
            
            valid_detection_sources = ["client_reported", "internally_detected", "monitoring_alert", "vendor_reported", 
                                     "scheduled_maintenance", "emergency_maintenance"]
            if incident_data["detection_source"] not in valid_detection_sources:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid detection_source '{incident_data['detection_source']}'. Must be one of: {', '.join(valid_detection_sources)}"
                })
            
            # Validate boolean fields if provided
            if "rto_breach" in incident_data and not isinstance(incident_data["rto_breach"], bool):
                return json.dumps({
                    "success": False,
                    "error": "rto_breach must be a boolean (True/False)"
                })
            
            if "sla_breach" in incident_data and not isinstance(incident_data["sla_breach"], bool):
                return json.dumps({
                    "success": False,
                    "error": "sla_breach must be a boolean (True/False)"
                })
            
            if "is_recurring" in incident_data and not isinstance(incident_data["is_recurring"], bool):
                return json.dumps({
                    "success": False,
                    "error": "is_recurring must be a boolean (True/False)"
                })
            
            # Validate downtime_minutes if provided
            if "downtime_minutes" in incident_data:
                downtime = incident_data["downtime_minutes"]
                if downtime is not None and (not isinstance(downtime, int) or downtime < 0):
                    return json.dumps({
                        "success": False,
                        "error": "downtime_minutes must be a non-negative integer"
                    })
            
            # Generate new incident ID
            new_incident_id = generate_id(incidents)
            
            # Auto-generate incident_code
            max_seq = 0
            for existing_incident in incidents.values():
                code = existing_incident.get("incident_code")
                if code and code.startswith("INC-2025-"):
                    try:
                        seq_num = int(code.split("INC-2025-")[1])
                        if seq_num > max_seq:
                            max_seq = seq_num
                    except Exception:
                        continue
            seq = max_seq + 1
            generated_code = f"INC-2025-{seq:05d}"

            new_incident = {
                "incident_id": str(new_incident_id),
                "incident_code": generated_code,
                "title": incident_data["title"],
                "reporter_id": str(incident_data["reporter_id"]),
                "assigned_manager_id": str(incident_data.get("assigned_manager_id")) if incident_data.get("assigned_manager_id") else None,
                "client_id": str(incident_data["client_id"]),
                "component_id": str(incident_data.get("component_id")) if incident_data.get("component_id") else None,
                "severity": incident_data.get("severity"),
                "status": incident_data.get("status", "open"),
                "impact": incident_data["impact"],
                "urgency": incident_data["urgency"],
                "category": incident_data["category"],
                "detection_source": incident_data["detection_source"],
                "detected_at": incident_data["detected_at"],
                "resolved_at": incident_data.get("resolved_at"),
                "closed_at": incident_data.get("closed_at"),
                "rto_breach": incident_data.get("rto_breach", False),
                "sla_breach": incident_data.get("sla_breach", False),
                "is_recurring": incident_data.get("is_recurring", False),
                "downtime_minutes": incident_data.get("downtime_minutes"),
                "created_at": "2025-10-01T00:00:00",
                "updated_at": "2025-10-01T00:00:00"
            }
            
            incidents[str(new_incident_id)] = new_incident
            
            return json.dumps({
                "success": True,
                "action": "create",
                "incident_id": str(new_incident_id),
                "incident_data": new_incident
            })
        
        elif action == "update":
            if not incident_id:
                return json.dumps({
                    "success": False,
                    "error": "incident_id is required for update action"
                })
            
            if incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident record {incident_id} not found"
                })
            
            if not incident_data:
                return json.dumps({
                    "success": False,
                    "error": "incident_data is required for update action"
                })
            
            # Validate at least one field is provided for update
            if not incident_data:
                return json.dumps({
                    "success": False,
                    "error": "At least one field must be provided for update"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["title", "incident_code", "assigned_manager_id", "component_id", "severity", "status", "impact", 
                                   "urgency", "category", "detection_source", "resolved_at", "closed_at", 
                                   "rto_breach", "sla_breach", "is_recurring", "downtime_minutes"]
            invalid_fields = [field for field in incident_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for incident update: {', '.join(invalid_fields)}. Cannot update reporter_id, client_id, or detected_at."
                })
            
            # Validate incident_code uniqueness if provided
            if "incident_code" in incident_data and incident_data["incident_code"]:
                new_code = incident_data["incident_code"]
                for existing_id, existing in incidents.items():
                    if existing_id != incident_id and existing.get("incident_code") == new_code:
                        return json.dumps({
                            "success": False,
                            "error": f"Incident with code '{new_code}' already exists"
                        })
            
            # Validate enum fields if provided
            if "severity" in incident_data:
                valid_severities = ["P1", "P2", "P3", "P4"]
                if incident_data["severity"] not in valid_severities:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid severity '{incident_data['severity']}'. Must be one of: {', '.join(valid_severities)}"
                    })
            
            if "status" in incident_data:
                valid_statuses = ["open", "in_progress", "resolved", "closed"]
                if incident_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{incident_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            if "impact" in incident_data:
                valid_impacts = ["critical", "high", "medium", "low"]
                if incident_data["impact"] not in valid_impacts:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid impact '{incident_data['impact']}'. Must be one of: {', '.join(valid_impacts)}"
                    })
            
            if "urgency" in incident_data:
                valid_urgencies = ["critical", "high", "medium", "low"]
                if incident_data["urgency"] not in valid_urgencies:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid urgency '{incident_data['urgency']}'. Must be one of: {', '.join(valid_urgencies)}"
                    })
            
            if "category" in incident_data:
                valid_categories = ["system_outage", "performance_degradation", "security_incident", "data_corruption", 
                                  "integration_failure", "network_issue", "hardware_failure", "software_bug", 
                                  "configuration_error", "capacity_issue", "backup_failure", "authentication_failure", 
                                  "api_error", "database_issue", "service_unavailable"]
                if incident_data["category"] not in valid_categories:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid category '{incident_data['category']}'. Must be one of: {', '.join(valid_categories)}"
                    })
            
            if "detection_source" in incident_data:
                valid_detection_sources = ["client_reported", "internally_detected", "monitoring_alert", "vendor_reported", 
                                         "scheduled_maintenance", "emergency_maintenance"]
                if incident_data["detection_source"] not in valid_detection_sources:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid detection_source '{incident_data['detection_source']}'. Must be one of: {', '.join(valid_detection_sources)}"
                    })
            
            # Validate boolean fields if provided
            if "rto_breach" in incident_data and not isinstance(incident_data["rto_breach"], bool):
                return json.dumps({
                    "success": False,
                    "error": "rto_breach must be a boolean (True/False)"
                })
            
            if "sla_breach" in incident_data and not isinstance(incident_data["sla_breach"], bool):
                return json.dumps({
                    "success": False,
                    "error": "sla_breach must be a boolean (True/False)"
                })
            
            if "is_recurring" in incident_data and not isinstance(incident_data["is_recurring"], bool):
                return json.dumps({
                    "success": False,
                    "error": "is_recurring must be a boolean (True/False)"
                })
            
            # Validate downtime_minutes if provided
            if "downtime_minutes" in incident_data:
                downtime = incident_data["downtime_minutes"]
                if downtime is not None and (not isinstance(downtime, int) or downtime < 0):
                    return json.dumps({
                        "success": False,
                        "error": "downtime_minutes must be a non-negative integer"
                    })
            
            # Get current incident data
            current_incident = incidents[incident_id].copy()
            
            # Validate status transitions
            current_status = current_incident.get("status")
            new_status = incident_data.get("status")
            
            if new_status and current_status == "closed" and new_status != "closed":
                return json.dumps({
                    "success": False,
                    "error": "Cannot reopen a closed incident"
                })
            
            # Auto-set resolved_at when status changes to resolved
            if new_status == "resolved" and current_status != "resolved" and "resolved_at" not in incident_data:
                incident_data["resolved_at"] = "2025-10-01T00:00:00"
            
            # Auto-set closed_at when status changes to closed
            if new_status == "closed" and current_status != "closed" and "closed_at" not in incident_data:
                incident_data["closed_at"] = "2025-10-01T00:00:00"
            
            # Update incident record
            updated_incident = current_incident.copy()
            for key, value in incident_data.items():
                if key in ["assigned_manager_id", "component_id"] and value is not None:
                    updated_incident[key] = str(value)
                else:
                    updated_incident[key] = value
            
            updated_incident["updated_at"] = "2025-10-01T00:00:00"
            incidents[incident_id] = updated_incident
            
            return json.dumps({
                "success": True,
                "action": "update",
                "incident_id": str(incident_id),
                "incident_data": updated_incident
            })

    @staticmethod
    def discover_subscription_agreements_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover subscription and SLA agreement entities.
        
        Supported entities:
        - client_subscriptions: Client subscription records by subscription_id, client_id, product_id, subscription_type, start_date, end_date, sla_tier, rto_hours, status
        - sla_agreements: SLA agreement records by sla_id, subscription_id, severity_level, response_time_minutes, resolution_time_hours, availability_percentage
        """
        if entity_type not in ["client_subscriptions", "sla_agreements"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'client_subscriptions' or 'sla_agreements'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        # Determine the ID field based on entity type
        id_field = "subscription_id" if entity_type == "client_subscriptions" else "sla_id"
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: str(entity_id)})
            else:
                results.append({**entity_data, id_field: str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_products_invoke(
        data: Dict[str, Any],
        # approval: bool,
        # For Create
        product_name: Optional[str] = None,
        product_type: Optional[str] = None,
        version: Optional[str] = None,
        vendor_support_id: Optional[str] = None,
        status: Optional[str] = "active",
        # For Update
        product_id: Optional[str] = None
    ) -> str:

        products = data.get("products", {})
        vendors = data.get("vendors", {})

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        valid_types = [
            "payment_processing", "banking_system", "api_gateway",
            "data_integration", "reporting_platform", "security_service",
            "backup_service", "monitoring_tool"
        ]
        valid_status = ["active", "deprecated", "maintenance"]

        # ----- Check Approval -----
        # if not approval:
        #     return json.dumps({
        #         "success": False,
        #         "error": "Approval missing for product management action"
        #     })

        # ----- CREATE -----
        if not product_id:
            # Required fields
            if not product_name or not product_type:
                return json.dumps({
                    "success": False,
                    "error": "Missing or invalid inputs"
                })

            if product_type not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid product_type. Must be one of {valid_types}"
                })

            if status and status not in valid_status:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_status}"
                })

            # Check product_name uniqueness
            for product in products.values():
                if product.get("product_name") == product_name:
                    return json.dumps({
                        "success": False,
                        "error": "Product name already exists"
                    })

            # Validate vendor
            if vendor_support_id:
                vendor = vendors.get(vendor_support_id)
                if not vendor or vendor.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Vendor not found or inactive"
                    })

            # Create new product
            new_id = str(generate_id(products))
            timestamp = "2025-10-01T00:00:00"

            new_product = {
                "product_id": new_id,
                "product_name": product_name,
                "product_type": product_type,
                "version": version,
                "vendor_support_id": vendor_support_id,
                "status": status,
                "created_at": timestamp
            }
            products[new_id] = new_product

            # Simulate audit record logging
            if not data.get("audit_log"):
                data["audit_log"] = []
            data["audit_log"].append({
                "action": "create_product",
                "product_id": new_id,
                "timestamp": timestamp
            })

            return json.dumps(new_product)

        # ----- UPDATE -----
        else:
            if product_id not in products:
                return json.dumps({
                    "success": False,
                    "error": "Product not found"
                })

            product = products[product_id]

            if product_name:
                # Check uniqueness
                for pid, existing in products.items():
                    if pid != product_id and existing.get("product_name") == product_name:
                        return json.dumps({
                            "success": False,
                            "error": "New product_name already exists"
                        })
                product["product_name"] = product_name

            if product_type and product_type not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid product_type. Must be one of {valid_types}"
                })

            if status and status not in valid_status:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_status}"
                })

            if vendor_support_id:
                vendor = vendors.get(vendor_support_id)
                if not vendor or vendor.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Vendor not found or inactive"
                    })
                product["vendor_support_id"] = vendor_support_id

            # Update allowed fields
            for field, val in [
                ("product_type", product_type), ("version", version),
                ("status", status)
            ]:
                if val is not None:
                    product[field] = val

            # Simulate audit logging
            timestamp = "2025-10-01T00:00:00"
            if not data.get("audit_log"):
                data["audit_log"] = []
            data["audit_log"].append({
                "action": "update_product",
                "product_id": product_id,
                "timestamp": timestamp
            })

            return json.dumps(product)

    @staticmethod
    def manage_post_incident_reviews_invoke(data: Dict[str, Any], action: str, pir_data: Dict[str, Any] = None, pir_id: str = None) -> str:
        """
        Create or update post-incident review records.

        pir_data must include:
        - action (required): 'create' or 'update'
        For create:
            - incident_id (required)
            - scheduled_date (required)
            - facilitator_id (required)
            - Optional: timeline_accuracy_rating, communication_effectiveness_rating, technical_response_rating, status
        For update:
            - pir_id (required)
            - Optional: scheduled_date, facilitator_id, timeline_accuracy_rating, communication_effectiveness_rating, technical_response_rating, status
        """

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False, 
                "error": f"Invalid {action}. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for communications"
            })

        post_incident_reviews = data.get("post_incident_reviews", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})

        incident_id = pir_data.get("incident_id")
        scheduled_date = pir_data.get("scheduled_date")
        facilitator_id = pir_data.get("facilitator_id")
        timeline_accuracy_rating = pir_data.get("timeline_accuracy_rating")
        communication_effectiveness_rating = pir_data.get("communication_effectiveness_rating")
        technical_response_rating = pir_data.get("technical_response_rating")
        status = pir_data.get("status")

        valid_statuses = ["scheduled", "completed", "cancelled"]

        def validate_date(date_str: str) -> bool:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return True
            except (ValueError, TypeError):
                return False

        def validate_rating(rating: int) -> bool:
            return isinstance(rating, int) and 1 <= rating <= 10

        

        if action == "create":
            # Validate required fields
            if not all([incident_id, scheduled_date, facilitator_id]):
                return json.dumps({
                    "success": False,
                    "error": "incident_id, scheduled_date, and facilitator_id are required for create action"
                })

            if not validate_date(scheduled_date):
                return json.dumps({"success": False, "error": "scheduled_date must be in format YYYY-MM-DD"})

            if incident_id not in incidents:
                return json.dumps({"success": False, "error": f"Incident {incident_id} not found"})
            if incidents[incident_id].get("status") not in ["resolved", "closed"]:
                return json.dumps({
                    "success": False,
                    "error": f"Incident must be resolved or closed, current status: {incidents[incident_id].get('status')}"
                })

            if facilitator_id not in users:
                return json.dumps({"success": False, "error": f"Facilitator {facilitator_id} not found"})
            if users[facilitator_id].get("role") not in ["incident_manager", "executive"]:
                return json.dumps({"success": False, "error": "Facilitator must have role 'incident_manager' or 'executive'"})

            # Validate ratings
            for rating_field, rating_value in [
                ("timeline_accuracy_rating", timeline_accuracy_rating),
                ("communication_effectiveness_rating", communication_effectiveness_rating),
                ("technical_response_rating", technical_response_rating)
            ]:
                if rating_value is not None and not validate_rating(rating_value):
                    return json.dumps({"success": False, "error": f"{rating_field} must be integer 1-10"})

            if status and status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})

            new_pir_id = generate_id(post_incident_reviews)
            new_pir = {
                "pir_id": str(new_pir_id),
                "incident_id": incident_id,
                "scheduled_date": scheduled_date,
                "facilitator_id": facilitator_id,
                "timeline_accuracy_rating": timeline_accuracy_rating,
                "communication_effectiveness_rating": communication_effectiveness_rating,
                "technical_response_rating": technical_response_rating,
                "status": status if status else "scheduled",
                "created_at": "2025-10-02T12:00:00"
            }

            post_incident_reviews[str(new_pir_id)] = new_pir

            return json.dumps({
                "success": True, 
                "action": "create", 
                "pir_id": str(new_pir_id),
                "message": f"Post incident review {new_pir_id} created successfully", 
                "pir_data": new_pir})

        elif action == "update":
            if not pir_id:
                return json.dumps({"success": False, "error": "pir_id is required for update action"})
            if pir_id not in post_incident_reviews:
                return json.dumps({"success": False, "error": f"Post-incident review {pir_id} not found"})

            # Validate at least one optional field
            if all(field is None for field in [scheduled_date, facilitator_id, timeline_accuracy_rating,
                                               communication_effectiveness_rating, technical_response_rating, status]):
                return json.dumps({"success": False, "error": "At least one optional field must be provided for update"})

            if scheduled_date and not validate_date(scheduled_date):
                return json.dumps({"success": False, "error": "scheduled_date must be in format YYYY-MM-DD"})

            if facilitator_id:
                if facilitator_id not in users:
                    return json.dumps({"success": False, "error": f"Facilitator {facilitator_id} not found"})
                if users[facilitator_id].get("role") not in ["incident_manager", "executive"]:
                    return json.dumps({"success": False, "error": "Facilitator must have role 'incident_manager' or 'executive'"})

            for rating_field, rating_value in [
                ("timeline_accuracy_rating", timeline_accuracy_rating),
                ("communication_effectiveness_rating", communication_effectiveness_rating),
                ("technical_response_rating", technical_response_rating)
            ]:
                if rating_value is not None and not validate_rating(rating_value):
                    return json.dumps({"success": False, "error": f"{rating_field} must be integer 1-10"})

            if status and status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})

            current_pir = post_incident_reviews[pir_id].copy()
            for field_name, field_value in pir_data.items():
                if field_name in ["scheduled_date", "facilitator_id", "timeline_accuracy_rating",
                                  "communication_effectiveness_rating", "technical_response_rating", "status"]:
                    if field_value is not None:
                        current_pir[field_name] = field_value

            post_incident_reviews[pir_id] = current_pir

            return json.dumps({
                "success": True, 
                "action": "update", 
                "pir_id": pir_id,
                "message": f"Post incident review {pir_id} updated successfully", 
                "pir_data": current_pir})

    @staticmethod
    def manage_client_subscriptions_invoke(data: Dict[str, Any], action: str, subscription_data: Dict[str, Any] = None, subscription_id: str = None) -> str:
        """
        Create or update client subscription records.
        
        Actions:
        - create: Create new subscription record (requires subscription_data with client_id, product_id, subscription_type, start_date, sla_tier, rto_hours, status)
        - update: Update existing subscription record (requires subscription_id and subscription_data with changes)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        # Access client_subscriptions data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for client_subscriptions"
            })
        
        client_subscriptions = data.get("client_subscriptions", {})
        
        if action == "create":
            if not subscription_data:
                return json.dumps({
                    "success": False,
                    "error": "subscription_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["client_id", "product_id", "subscription_type", "start_date", "sla_tier", "rto_hours", "status"]
            missing_fields = [field for field in required_fields if field not in subscription_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for subscription creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["client_id", "product_id", "subscription_type", "start_date", "end_date", "sla_tier", "rto_hours", "status"]
            invalid_fields = [field for field in subscription_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for subscription creation: {', '.join(invalid_fields)}"
                })
            
            # Validate enum fields
            valid_subscription_types = ["full_service", "limited_service", "trial", "custom"]
            if subscription_data["subscription_type"] not in valid_subscription_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid subscription_type '{subscription_data['subscription_type']}'. Must be one of: {', '.join(valid_subscription_types)}"
                })
            
            valid_sla_tiers = ["premium", "standard", "basic"]
            if subscription_data["sla_tier"] not in valid_sla_tiers:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid sla_tier '{subscription_data['sla_tier']}'. Must be one of: {', '.join(valid_sla_tiers)}"
                })
            
            valid_statuses = ["active", "expired", "cancelled", "suspended"]
            if subscription_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{subscription_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Validate RTO hours
            rto_hours = subscription_data["rto_hours"]
            if not isinstance(rto_hours, int) or rto_hours <= 0:
                return json.dumps({
                    "success": False,
                    "error": "rto_hours must be a positive integer"
                })
            
            # Validate date logic if end_date is provided
            if "end_date" in subscription_data and subscription_data["end_date"]:
                if subscription_data["end_date"] <= subscription_data["start_date"]:
                    return json.dumps({
                        "success": False,
                        "error": "end_date must be after start_date"
                    })
            
            # Check for duplicate active subscription for same client and product
            client_id = subscription_data["client_id"]
            product_id = subscription_data["product_id"]
            for existing_subscription in client_subscriptions.values():
                if (existing_subscription.get("client_id") == client_id and 
                    existing_subscription.get("product_id") == product_id and
                    existing_subscription.get("status") == "active"):
                    return json.dumps({
                        "success": False,
                        "error": f"Active subscription already exists for client {client_id} and product {product_id}"
                    })
            
            # Generate new subscription ID
            new_subscription_id = generate_id(client_subscriptions)
            
            # Create new subscription record
            new_subscription = {
                "subscription_id": str(new_subscription_id),
                "client_id": str(subscription_data["client_id"]),
                "product_id": str(subscription_data["product_id"]),
                "subscription_type": subscription_data["subscription_type"],
                "start_date": subscription_data["start_date"],
                "end_date": subscription_data.get("end_date"),
                "sla_tier": subscription_data["sla_tier"],
                "rto_hours": subscription_data["rto_hours"],
                "status": subscription_data["status"],
                "created_at": "2025-10-01T00:00:00",
                "updated_at": "2025-10-01T00:00:00"
            }
            
            client_subscriptions[str(new_subscription_id)] = new_subscription
            
            return json.dumps({
                "success": True,
                "action": "create",
                "subscription_id": str(new_subscription_id),
                "subscription_data": new_subscription
            })
        
        elif action == "update":
            if not subscription_id:
                return json.dumps({
                    "success": False,
                    "error": "subscription_id is required for update action"
                })
            
            if subscription_id not in client_subscriptions:
                return json.dumps({
                    "success": False,
                    "error": f"Subscription record {subscription_id} not found"
                })
            
            if not subscription_data:
                return json.dumps({
                    "success": False,
                    "error": "subscription_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["subscription_type", "end_date", "sla_tier", "rto_hours", "status"]
            invalid_fields = [field for field in subscription_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for subscription update: {', '.join(invalid_fields)}. Cannot update client_id, product_id, or start_date."
                })
            
            # Validate enum fields if provided
            if "subscription_type" in subscription_data:
                valid_subscription_types = ["full_service", "limited_service", "trial", "custom"]
                if subscription_data["subscription_type"] not in valid_subscription_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid subscription_type '{subscription_data['subscription_type']}'. Must be one of: {', '.join(valid_subscription_types)}"
                    })
            
            if "sla_tier" in subscription_data:
                valid_sla_tiers = ["premium", "standard", "basic"]
                if subscription_data["sla_tier"] not in valid_sla_tiers:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid sla_tier '{subscription_data['sla_tier']}'. Must be one of: {', '.join(valid_sla_tiers)}"
                    })
            
            if "status" in subscription_data:
                valid_statuses = ["active", "expired", "cancelled", "suspended"]
                if subscription_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{subscription_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate RTO hours if provided
            if "rto_hours" in subscription_data:
                rto_hours = subscription_data["rto_hours"]
                if not isinstance(rto_hours, int) or rto_hours <= 0:
                    return json.dumps({
                        "success": False,
                        "error": "rto_hours must be a positive integer"
                    })
            
            # Get current subscription data
            current_subscription = client_subscriptions[subscription_id].copy()
            
            # Validate date logic if end_date is being updated
            if "end_date" in subscription_data and subscription_data["end_date"]:
                if subscription_data["end_date"] <= current_subscription["start_date"]:
                    return json.dumps({
                        "success": False,
                        "error": "end_date must be after start_date"
                    })
            
            # Check for duplicate active subscription if status is being changed to active
            if "status" in subscription_data and subscription_data["status"] == "active":
                client_id = current_subscription["client_id"]
                product_id = current_subscription["product_id"]
                for existing_id, existing_subscription in client_subscriptions.items():
                    if (existing_id != subscription_id and
                        existing_subscription.get("client_id") == client_id and 
                        existing_subscription.get("product_id") == product_id and
                        existing_subscription.get("status") == "active"):
                        return json.dumps({
                            "success": False,
                            "error": f"Active subscription already exists for client {client_id} and product {product_id}"
                        })
            
            # Update subscription record
            updated_subscription = current_subscription.copy()
            for key, value in subscription_data.items():
                updated_subscription[key] = value
            
            updated_subscription["updated_at"] = "2025-10-01T00:00:00"
            client_subscriptions[subscription_id] = updated_subscription
            
            return json.dumps({
                "success": True,
                "action": "update",
                "subscription_id": str(subscription_id),
                "subscription_data": updated_subscription
            })

    @staticmethod
    def discover_root_cause_analysis_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover root cause analysis entities.
        
        Supported entities:
        - root_cause_analysis: Root cause analysis records
        """
        if entity_type not in ["root_cause_analysis"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'root_cause_analysis'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("root_cause_analysis", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "rca_id": str(entity_id)})
            else:
                results.append({**entity_data, "rca_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_metrics_invoke(data: Dict[str, Any], metric_data: Dict[str, Any]) -> str:
        """
        Record incident performance metrics.

        metric_data must include:
        - incident_id (required)
        - metric_type (required): MTTA, MTTD, MTTR, MTTM, FTR
        - value_minutes (required)
        - target_minutes (optional)
        - recorded_at (optional)
        """

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        # def check_approval(data: Dict[str, Any], required_roles: list) -> bool:
        #     approvals = data.get("approvals", {})
        #     return any(approvals.get(role) for role in required_roles)

        # Check approval
        # if not check_approval(data, ["incident_manager", "system_administrator"]):
        #     return json.dumps({
        #         "success": False,
        #         "error": "Missing approval for recording metrics. Required: incident_manager OR system_administrator"
        #     })

        metrics = data.get("metrics", {})
        incidents = data.get("incidents", {})

        incident_id = metric_data.get("incident_id")
        metric_type = metric_data.get("metric_type")
        value_minutes = metric_data.get("value_minutes")
        target_minutes = metric_data.get("target_minutes")
        recorded_at = metric_data.get("recorded_at")

        # Validate required fields
        if not all([incident_id, metric_type, value_minutes is not None]):
            return json.dumps({
                "success": False,
                "error": "Missing required fields: incident_id, metric_type, value_minutes"
            })

        # Validate incident exists and status
        if incident_id not in incidents:
            return json.dumps({"success": False, "error": f"Incident {incident_id} not found"})

        if incidents[incident_id].get("status") not in ["resolved", "closed"]:
            return json.dumps({
                "success": False,
                "error": f"Incident must be in 'resolved' or 'closed' status for metrics recording. Current status: {incidents[incident_id].get('status')}"
            })

        # Validate metric_type
        valid_metric_types = ["MTTA", "MTTD", "MTTR", "MTTM", "FTR"]
        if metric_type not in valid_metric_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid metric_type. Must be one of: {', '.join(valid_metric_types)}"
            })

        # Validate value_minutes
        try:
            value_minutes = float(value_minutes)
            if value_minutes < 0:
                raise ValueError
        except (ValueError, TypeError):
            return json.dumps({
                "success": False,
                "error": "value_minutes must be a non-negative number"
            })

        # Validate target_minutes
        if target_minutes is not None:
            try:
                target_minutes = float(target_minutes)
                if target_minutes < 0:
                    raise ValueError
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "error": "target_minutes must be a non-negative number"
                })

        # Create new metric
        new_id = generate_id(metrics)
        new_metric = {
            "metric_id": str(new_id),
            "incident_id": incident_id,
            "metric_type": metric_type,
            "value_minutes": int(value_minutes),
            "target_minutes": int(target_minutes) if target_minutes is not None else None,
            "recorded_at": recorded_at if recorded_at else "2025-10-02T12:00:00",
            "created_at": "2025-10-02T12:00:00"
        }

        metrics[str(new_id)] = new_metric

        return json.dumps({
            "success": True,
            "action": "create",
            "metric_id": str(new_id),
            "message": f"Metrics {new_id} created successfully",
            "metric_data": new_metric
        })

    @staticmethod
    def manage_change_requests_invoke(data: Dict[str, Any], action: str, change_data: Dict[str, Any] = None, change_id: str = None) -> str:
        """
        Create or update change request records.

        Actions:
        - create: Create new change request (requires change_data with title, change_type, requested_by_id, risk_level)
        - update: Update existing change request (requires change_id and change_data with fields to change)
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        def generate_code(prefix: str, table: Dict[str, Any]) -> str:
            max_num = 0
            for record in table.values():
                code = record.get("change_code", "")
                if code.startswith(prefix):
                    try:
                        num = int(code.split("-")[-1])
                        max_num = max(max_num, num)
                    except:
                        pass
            return f"{prefix}-{str(max_num + 1).zfill(5)}"

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for change requests"
            })

        change_requests = data.get("change_requests", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        # Enums/allowed values
        valid_change_types = ["emergency", "standard", "normal"]
        valid_risk_levels = ["high", "medium", "low"]
        valid_statuses = ["requested", "approved", "scheduled", "in_progress", "completed", "failed", "rolled_back"]

        # Approval roles allowed (require at least one)
        # approver_roles = ["technical_support", "incident_manager", "system_administrator", "executive"]

        if action == "create":
            if not change_data:
                return json.dumps({
                    "success": False,
                    "error": "change_data is required for create action"
                })

            # Validate required fields
            required_fields = ["title", "change_type", "requested_by_id", "risk_level"]
            missing = [f for f in required_fields if f not in change_data or change_data.get(f) in [None, ""]]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for change creation: {', '.join(missing)}"
                })

            # Approval: require at least one approver flagged True in the change_data
            # if not any(change_data.get(role) for role in approver_roles):
            #     return json.dumps({
            #         "success": False,
            #         "error": "Missing approval for creating change request. Required: technical_support OR incident_manager OR system_administrator OR executive"
            #     })

            # Only allow known fields to be supplied
            allowed_fields = [
                "title", "change_type", "requested_by_id", "approved_by_id", "risk_level",
                "incident_id", "scheduled_start", "scheduled_end", "actual_start", "actual_end", "status"
            ]
            invalid_fields = [k for k in change_data.keys() if k not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for change creation: {', '.join(invalid_fields)}"
                })

            title = change_data["title"]
            change_type = change_data["change_type"]
            requested_by_id = str(change_data["requested_by_id"])
            risk_level = change_data["risk_level"]
            incident_id = change_data.get("incident_id")
            approved_by_id = change_data.get("approved_by_id")
            scheduled_start = change_data.get("scheduled_start")
            scheduled_end = change_data.get("scheduled_end")
            actual_start = change_data.get("actual_start")
            actual_end = change_data.get("actual_end")
            status = change_data.get("status")

            # Validate enums
            if change_type not in valid_change_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid change_type. Must be one of: {', '.join(valid_change_types)}"
                })

            if risk_level not in valid_risk_levels:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid risk_level. Must be one of: {', '.join(valid_risk_levels)}"
                })

            if status and status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })

            # Validate incident if specified
            if incident_id and incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident {incident_id} not found"
                })

            # Validate requested_by exists
            if requested_by_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Requester {requested_by_id} not found"
                })

            # Generate and create
            new_id = generate_id(change_requests)
            change_code = generate_code("CHG-2024", change_requests)
            new_change_request = {
                "change_id": str(new_id),
                "change_code": change_code,
                "incident_id": incident_id,
                "title": title,
                "change_type": change_type,
                "requested_by_id": requested_by_id,
                "approved_by_id": approved_by_id,
                "risk_level": risk_level,
                "scheduled_start": scheduled_start,
                "scheduled_end": scheduled_end,
                "actual_start": actual_start,
                "actual_end": actual_end,
                "status": status if status else "requested",
                "created_at": "2025-10-02T12:00:00",
                "updated_at": "2025-10-02T12:00:00"
            }

            change_requests[str(new_id)] = new_change_request

            return json.dumps({
                "success": True,
                "action": "create",
                "change_id": str(new_id),
                "message": f"Change request {new_id} created successfully",
                "change_request_data": new_change_request
            })

        elif action == "update":
            if not change_id:
                return json.dumps({
                    "success": False,
                    "error": "change_id is required for update action"
                })

            if change_id not in change_requests:
                return json.dumps({
                    "success": False,
                    "error": f"Change request {change_id} not found"
                })

            if not change_data:
                return json.dumps({
                    "success": False,
                    "error": "change_data is required for update action"
                })

            # Approval required for updates as well (at least one)
            # if not any(change_data.get(role) for role in approver_roles):
            #     return json.dumps({
            #         "success": False,
            #         "error": "Missing approval for updating change request. Required: technical_support OR incident_manager OR system_administrator OR executive"
            #     })

            # Only allow known update fields
            allowed_update_fields = [
                "title", "change_type", "requested_by_id", "approved_by_id", "risk_level",
                "incident_id", "scheduled_start", "scheduled_end", "actual_start", "actual_end", "status"
            ]
            invalid_fields = [k for k in change_data.keys() if k not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for change update: {', '.join(invalid_fields)}"
                })

            # At least one valid field must be present
            if not any(field in change_data for field in allowed_update_fields):
                return json.dumps({
                    "success": False,
                    "error": "At least one updatable field must be provided in change_data"
                })

            current_change = change_requests[change_id].copy()

            # Validate and apply updates
            if "title" in change_data:
                current_change["title"] = change_data["title"]

            if "change_type" in change_data:
                ct = change_data["change_type"]
                if ct not in valid_change_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid change_type. Must be one of: {', '.join(valid_change_types)}"
                    })
                current_change["change_type"] = ct

            if "requested_by_id" in change_data:
                rb = str(change_data["requested_by_id"])
                if rb not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Requester {rb} not found"
                    })
                current_change["requested_by_id"] = rb

            if "approved_by_id" in change_data:
                current_change["approved_by_id"] = change_data["approved_by_id"]

            if "risk_level" in change_data:
                rl = change_data["risk_level"]
                if rl not in valid_risk_levels:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid risk_level. Must be one of: {', '.join(valid_risk_levels)}"
                    })
                current_change["risk_level"] = rl

            if "incident_id" in change_data:
                inc = change_data["incident_id"]
                if inc and inc not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident {inc} not found"
                    })
                current_change["incident_id"] = inc

            if "scheduled_start" in change_data:
                current_change["scheduled_start"] = change_data["scheduled_start"]
            if "scheduled_end" in change_data:
                current_change["scheduled_end"] = change_data["scheduled_end"]
            if "actual_start" in change_data:
                current_change["actual_start"] = change_data["actual_start"]
            if "actual_end" in change_data:
                current_change["actual_end"] = change_data["actual_end"]

            if "status" in change_data:
                st = change_data["status"]
                if st not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                current_change["status"] = st

            current_change["updated_at"] = "2025-10-02T12:00:00"
            change_requests[change_id] = current_change

            return json.dumps({
                "success": True,
                "action": "update",
                "change_id": change_id,
                "message": f"Change request {change_id} updated successfully",
                "change_request_data": current_change
            })

    @staticmethod
    def manage_components_invoke(
        data: Dict[str, Any],
        # approval: bool,
        # For Create
        component_name: Optional[str] = None,
        component_type: Optional[str] = None,
        environment: Optional[str] = None,
        product_id: Optional[str] = None,
        location: Optional[str] = None,
        port_number: Optional[int] = None,
        status: Optional[str] = "online",
        # For Update
        component_id: Optional[str] = None
    ) -> str:

        components = data.get("components", {})
        products = data.get("products", {})

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        valid_types = [
            "sftp_server", "api_endpoint", "database", "load_balancer",
            "firewall", "authentication_service", "payment_gateway",
            "file_storage", "monitoring_system"
        ]
        valid_envs = ["production", "staging", "development", "test"]
        valid_status = ["online", "offline", "maintenance", "degraded"]

        # ----- Check Approval -----
        # if not approval:
        #     return json.dumps({
        #         "success": False,
        #         "error": "Approval missing for component management action"
        #     })

        # ----- CREATE -----
        if not component_id:
            if not component_name or not component_type or not environment:
                return json.dumps({
                    "success": False,
                    "error": "Missing or invalid inputs"
                })

            if component_type not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid component_type. Must be one of {valid_types}"
                })

            if environment not in valid_envs:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid environment. Must be one of {valid_envs}"
                })

            if status and status not in valid_status:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_status}"
                })

            # Validate product if provided
            if product_id:
                product = products.get(product_id)
                if not product or product.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Product not found or inactive"
                    })

            # Ensure component_name uniqueness within product_id scope
            for comp in components.values():
                if comp.get("product_id") == product_id and comp.get("component_name") == component_name:
                    return json.dumps({
                        "success": False,
                        "error": "Component name already exists within product"
                    })

            # Create new component
            new_id = str(generate_id(components))
            timestamp = "2025-10-01T00:00:00"

            new_component = {
                "component_id": new_id,
                "component_name": component_name,
                "component_type": component_type,
                "environment": environment,
                "product_id": product_id,
                "location": location,
                "port_number": port_number,
                "status": status,
                "created_at": timestamp
            }
            components[new_id] = new_component

            # Audit logging
            if not data.get("audit_log"):
                data["audit_log"] = []
            data["audit_log"].append({
                "action": "create_component",
                "component_id": new_id,
                "timestamp": timestamp
            })

            return json.dumps(new_component)

        # ----- UPDATE -----
        else:
            if component_id not in components:
                return json.dumps({
                    "success": False,
                    "error": "Component not found"
                })

            component = components[component_id]

            if component_name:
                # Ensure uniqueness within product scope
                for cid, existing in components.items():
                    if cid != component_id and existing.get("product_id") == (product_id or component["product_id"]) and existing.get("component_name") == component_name:
                        return json.dumps({
                            "success": False,
                            "error": "New component_name already exists within product"
                        })
                component["component_name"] = component_name

            if component_type and component_type not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid component_type. Must be one of {valid_types}"
                })

            if environment and environment not in valid_envs:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid environment. Must be one of {valid_envs}"
                })

            if status and status not in valid_status:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_status}"
                })

            if product_id:
                product = products.get(product_id)
                if not product or product.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Product not found or inactive"
                    })
                component["product_id"] = product_id

            # Apply updates
            for field, val in [
                ("component_type", component_type), ("environment", environment),
                ("location", location), ("port_number", port_number),
                ("status", status)
            ]:
                if val is not None:
                    component[field] = val

            # Audit logging
            timestamp = "2025-10-01T00:00:00"
            if not data.get("audit_log"):
                data["audit_log"] = []
            data["audit_log"].append({
                "action": "update_component",
                "component_id": component_id,
                "timestamp": timestamp
            })

            return json.dumps(component)

    @staticmethod
    def manage_sla_agreements_invoke(data: Dict[str, Any], action: str, sla_data: Dict[str, Any] = None, sla_id: str = None) -> str:
        """
        Create or update SLA agreement records.
        
        Actions:
        - create: Create new SLA agreement record (requires sla_data with subscription_id, severity_level, response_time_minutes, resolution_time_hours)
        - update: Update existing SLA agreement record (requires sla_id and sla_data with changes)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        # Access sla_agreements data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for sla_agreements"
            })
        
        sla_agreements = data.get("sla_agreements", {})
        
        if action == "create":
            if not sla_data:
                return json.dumps({
                    "success": False,
                    "error": "sla_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["subscription_id", "severity_level", "response_time_minutes", "resolution_time_hours"]
            missing_fields = [field for field in required_fields if field not in sla_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for SLA agreement creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["subscription_id", "severity_level", "response_time_minutes", "resolution_time_hours", "availability_percentage"]
            invalid_fields = [field for field in sla_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for SLA agreement creation: {', '.join(invalid_fields)}"
                })
            
            # Validate enum fields
            valid_severity_levels = ["P1", "P2", "P3", "P4"]
            if sla_data["severity_level"] not in valid_severity_levels:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid severity_level '{sla_data['severity_level']}'. Must be one of: {', '.join(valid_severity_levels)}"
                })
            
            # Validate response time minutes
            response_time = sla_data["response_time_minutes"]
            if not isinstance(response_time, int) or response_time <= 0:
                return json.dumps({
                    "success": False,
                    "error": "response_time_minutes must be a positive integer"
                })
            
            # Validate resolution time hours
            resolution_time = sla_data["resolution_time_hours"]
            if not isinstance(resolution_time, int) or resolution_time <= 0:
                return json.dumps({
                    "success": False,
                    "error": "resolution_time_hours must be a positive integer"
                })
            
            # Validate availability percentage if provided
            if "availability_percentage" in sla_data:
                availability = sla_data["availability_percentage"]
                if not isinstance(availability, (int, float)) or availability < 0 or availability > 100:
                    return json.dumps({
                        "success": False,
                        "error": "availability_percentage must be a number between 0 and 100"
                    })
            
            # Check for duplicate SLA agreement for same subscription and severity level
            subscription_id = sla_data["subscription_id"]
            severity_level = sla_data["severity_level"]
            for existing_sla in sla_agreements.values():
                if (existing_sla.get("subscription_id") == subscription_id and 
                    existing_sla.get("severity_level") == severity_level):
                    return json.dumps({
                        "success": False,
                        "error": f"SLA agreement already exists for subscription {subscription_id} with severity level {severity_level}"
                    })
            
            # Generate new SLA ID
            new_sla_id = generate_id(sla_agreements)
            
            # Create new SLA agreement record
            new_sla = {
                "sla_id": str(new_sla_id),
                "subscription_id": str(sla_data["subscription_id"]),
                "severity_level": sla_data["severity_level"],
                "response_time_minutes": sla_data["response_time_minutes"],
                "resolution_time_hours": sla_data["resolution_time_hours"],
                "availability_percentage": sla_data.get("availability_percentage"),
                "created_at": "2025-10-01T00:00:00"
            }
            
            sla_agreements[str(new_sla_id)] = new_sla
            
            return json.dumps({
                "success": True,
                "action": "create",
                "sla_id": str(new_sla_id),
                "sla_data": new_sla
            })
        
        elif action == "update":
            if not sla_id:
                return json.dumps({
                    "success": False,
                    "error": "sla_id is required for update action"
                })
            
            if sla_id not in sla_agreements:
                return json.dumps({
                    "success": False,
                    "error": f"SLA agreement record {sla_id} not found"
                })
            
            if not sla_data:
                return json.dumps({
                    "success": False,
                    "error": "sla_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["response_time_minutes", "resolution_time_hours", "availability_percentage"]
            invalid_fields = [field for field in sla_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for SLA agreement update: {', '.join(invalid_fields)}. Cannot update subscription_id or severity_level."
                })
            
            # Validate response time minutes if provided
            if "response_time_minutes" in sla_data:
                response_time = sla_data["response_time_minutes"]
                if not isinstance(response_time, int) or response_time <= 0:
                    return json.dumps({
                        "success": False,
                        "error": "response_time_minutes must be a positive integer"
                    })
            
            # Validate resolution time hours if provided
            if "resolution_time_hours" in sla_data:
                resolution_time = sla_data["resolution_time_hours"]
                if not isinstance(resolution_time, int) or resolution_time <= 0:
                    return json.dumps({
                        "success": False,
                        "error": "resolution_time_hours must be a positive integer"
                    })
            
            # Validate availability percentage if provided
            if "availability_percentage" in sla_data:
                availability = sla_data["availability_percentage"]
                if availability is not None and (not isinstance(availability, (int, float)) or availability < 0 or availability > 100):
                    return json.dumps({
                        "success": False,
                        "error": "availability_percentage must be a number between 0 and 100"
                    })
            
            # Get current SLA data
            current_sla = sla_agreements[sla_id].copy()
            
            # Update SLA agreement record
            updated_sla = current_sla.copy()
            for key, value in sla_data.items():
                updated_sla[key] = value
            
            sla_agreements[sla_id] = updated_sla
            
            return json.dumps({
                "success": True,
                "action": "update",
                "sla_id": str(sla_id),
                "sla_data": updated_sla
            })

    @staticmethod
    def discover_vendors_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover vendor entities.
        
        Supported entities:
        - vendors: Vendor records by vendor_id, vendor_name, vendor_type, contact_email, status
        """
        if entity_type not in ["vendors"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'vendors'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("vendors", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "vendor_id": str(entity_id)})
            else:
                results.append({**entity_data, "vendor_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_root_cause_analysis_invoke(data: Dict[str, Any], action: str, rca_data: Dict[str, Any] = None, rca_id: str = None) -> str:
        """
        Create or update root cause analysis records.
        
        Actions:
        - create: Create new RCA record (requires rca_data with incident_id, analysis_method, conducted_by_id, status)
        - update: Update existing RCA record (requires rca_id and rca_data with changes)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        # Access root_cause_analysis data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for root_cause_analysis"
            })
        
        root_cause_analysis = data.get("root_cause_analysis", {})
        
        if action == "create":
            if not rca_data:
                return json.dumps({
                    "success": False,
                    "error": "rca_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["incident_id", "analysis_method", "conducted_by_id", "status"]
            missing_fields = [field for field in required_fields if field not in rca_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for RCA creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["incident_id", "analysis_method", "conducted_by_id", "completed_at", "status"]
            invalid_fields = [field for field in rca_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for RCA creation: {', '.join(invalid_fields)}"
                })
            
            # Validate enum fields
            valid_analysis_methods = ["five_whys", "fishbone", "timeline_analysis", "fault_tree"]
            if rca_data["analysis_method"] not in valid_analysis_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid analysis_method '{rca_data['analysis_method']}'. Must be one of: {', '.join(valid_analysis_methods)}"
                })
            
            valid_statuses = ["in_progress", "completed", "approved"]
            if rca_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{rca_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Check for existing RCA for the same incident
            incident_id = rca_data["incident_id"]
            for existing_rca in root_cause_analysis.values():
                if existing_rca.get("incident_id") == incident_id:
                    return json.dumps({
                        "success": False,
                        "error": f"Root cause analysis already exists for incident {incident_id}"
                    })
            
            # Generate new RCA ID
            new_rca_id = generate_id(root_cause_analysis)
            
            # Create new RCA record
            new_rca = {
                "rca_id": str(new_rca_id),
                "incident_id": str(rca_data["incident_id"]),
                "analysis_method": rca_data["analysis_method"],
                "conducted_by_id": str(rca_data["conducted_by_id"]),
                "completed_at": rca_data.get("completed_at"),
                "status": rca_data["status"],
                "created_at": "2025-10-01T00:00:00"
            }
            
            root_cause_analysis[str(new_rca_id)] = new_rca
            
            return json.dumps({
                "success": True,
                "action": "create",
                "rca_id": str(new_rca_id),
                "rca_data": new_rca
            })
        
        elif action == "update":
            if not rca_id:
                return json.dumps({
                    "success": False,
                    "error": "rca_id is required for update action"
                })
            
            if rca_id not in root_cause_analysis:
                return json.dumps({
                    "success": False,
                    "error": f"Root cause analysis record {rca_id} not found"
                })
            
            if not rca_data:
                return json.dumps({
                    "success": False,
                    "error": "rca_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["analysis_method", "completed_at", "status"]
            invalid_fields = [field for field in rca_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for RCA update: {', '.join(invalid_fields)}. Cannot update incident_id or conducted_by_id."
                })
            
            # Validate enum fields if provided
            if "analysis_method" in rca_data:
                valid_analysis_methods = ["five_whys", "fishbone", "timeline_analysis", "fault_tree"]
                if rca_data["analysis_method"] not in valid_analysis_methods:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid analysis_method '{rca_data['analysis_method']}'. Must be one of: {', '.join(valid_analysis_methods)}"
                    })
            
            if "status" in rca_data:
                valid_statuses = ["in_progress", "completed", "approved"]
                if rca_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{rca_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Get current RCA data
            current_rca = root_cause_analysis[rca_id].copy()
            
            # Validate status transitions
            current_status = current_rca.get("status")
            new_status = rca_data.get("status")
            
            if new_status and current_status == "approved" and new_status != "approved":
                return json.dumps({
                    "success": False,
                    "error": "Cannot change status from approved to another status"
                })
            
            # If status is being changed to completed, set completed_at if not provided
            if new_status == "completed" and current_status != "completed" and "completed_at" not in rca_data:
                rca_data["completed_at"] = "2025-10-01T00:00:00"
            
            # Update RCA record
            updated_rca = current_rca.copy()
            for key, value in rca_data.items():
                updated_rca[key] = value
            
            root_cause_analysis[rca_id] = updated_rca
            
            return json.dumps({
                "success": True,
                "action": "update",
                "rca_id": str(rca_id),
                "rca_data": updated_rca
            })

    @staticmethod
    def manage_clients_invoke(data: Dict[str, Any], action: str, client_data: Dict[str, Any] = None, client_id: str = None) -> str:
        """
        Create or update client records.

        Actions:
        - create: Create new client (requires client_data with client_name, client_type, country)
        - update: Update existing client (requires client_id and client_data with fields to change)
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for clients"
            })

        clients = data.get("clients", {})

        valid_client_types = ["enterprise", "mid_market", "small_business", "startup"]
        valid_statuses = ["active", "inactive", "suspended"]

        if action == "create":
            if not client_data:
                return json.dumps({
                    "success": False,
                    "error": "client_data is required for create action"
                })

            # Required fields
            required_fields = ["client_name", "client_type", "country"]
            missing = [f for f in required_fields if f not in client_data or not client_data.get(f)]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for client creation: {', '.join(missing)}"
                })

            client_name = client_data["client_name"]
            client_type = client_data["client_type"]
            country = client_data["country"]
            registration_number = client_data.get("registration_number")
            contact_email = client_data.get("contact_email")
            industry = client_data.get("industry")
            status = client_data.get("status", "active")

            # Validate client_type
            if client_type not in valid_client_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid client_type. Must be one of: {', '.join(valid_client_types)}"
                })

            # Validate status
            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })

            # Check uniqueness of client_name
            for existing_client in clients.values():
                if existing_client.get("client_name") == client_name:
                    return json.dumps({
                        "success": False,
                        "error": f"Client name '{client_name}' already exists"
                    })

            # Check uniqueness of registration_number if provided
            if registration_number:
                for existing_client in clients.values():
                    if existing_client.get("registration_number") == registration_number:
                        return json.dumps({
                            "success": False,
                            "error": f"Registration number '{registration_number}' already exists"
                        })

            # Create client
            new_id = generate_id(clients)
            new_client = {
                "client_id": str(new_id),
                "client_name": client_name,
                "client_type": client_type,
                "country": country,
                "status": status,
                "created_at": "2025-10-04T12:00:00",
                "updated_at": "2025-10-04T12:00:00"
            }

            if registration_number:
                new_client["registration_number"] = registration_number
            if contact_email:
                new_client["contact_email"] = contact_email
            if industry:
                new_client["industry"] = industry

            clients[str(new_id)] = new_client

            return json.dumps({
                "success": True,
                "action": "create",
                "client_id": str(new_id),
                "message": f"Client {new_id} created successfully",
                "client_data": new_client
            })

        elif action == "update":
            if not client_id:
                return json.dumps({
                    "success": False,
                    "error": "client_id is required for update action"
                })

            if client_id not in clients:
                return json.dumps({
                    "success": False,
                    "error": f"Client {client_id} not found"
                })

            if not client_data:
                return json.dumps({
                    "success": False,
                    "error": "client_data is required for update action"
                })

            current_client = clients[client_id].copy()

            # Validate and update client_type
            if "client_type" in client_data:
                ct = client_data["client_type"]
                if ct not in valid_client_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid client_type. Must be one of: {', '.join(valid_client_types)}"
                    })
                current_client["client_type"] = ct

            # Validate and update status
            if "status" in client_data:
                st = client_data["status"]
                if st not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                current_client["status"] = st

            # Check uniqueness of client_name if updating
            if "client_name" in client_data:
                new_name = client_data["client_name"]
                for cid, existing_client in clients.items():
                    if cid != client_id and existing_client.get("client_name") == new_name:
                        return json.dumps({
                            "success": False,
                            "error": f"Client name '{new_name}' already exists"
                        })
                current_client["client_name"] = new_name

            # Check uniqueness of registration_number if updating
            if "registration_number" in client_data:
                new_reg = client_data["registration_number"]
                for cid, existing_client in clients.items():
                    if cid != client_id and existing_client.get("registration_number") == new_reg:
                        return json.dumps({
                            "success": False,
                            "error": f"Registration number '{new_reg}' already exists"
                        })
                current_client["registration_number"] = new_reg

            # Update other fields
            for field in ["contact_email", "industry", "country"]:
                if field in client_data:
                    current_client[field] = client_data[field]

            current_client["updated_at"] = "2025-10-04T12:00:00"
            clients[client_id] = current_client

            return json.dumps({
                "success": True,
                "action": "update",
                "client_id": client_id,
                "message": f"Client {client_id} updated successfully",
                "client_data": current_client
            })

    @staticmethod
    def manage_incident_reports_invoke(data: Dict[str, Any], action: str, report_data: Dict[str, Any] = None, report_id: str = None) -> str:
        """
        Generate or update incident reports.

        Actions:
        - create: Generate new incident report (requires report_data with incident_id, report_type, generated_by_id)
        - update: Update existing incident report (requires report_id and report_data with fields to change)
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        incident_reports = data.get("incident_reports", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        valid_report_types = ["executive_summary", "technical_details", "business_impact", "compliance_report", "post_mortem"]
        valid_statuses = ["draft", "completed", "distributed"]
        # valid_roles = ["incident_manager", "executive"]

        if action == "create":
            if not report_data:
                return json.dumps({
                    "success": False,
                    "error": "report_data is required for create action"
                })

            required_fields = ["incident_id", "report_type", "generated_by_id"]
            missing = [f for f in required_fields if f not in report_data or not report_data.get(f)]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for report creation: {', '.join(missing)}"
                })

            incident_id = str(report_data["incident_id"])
            report_type = report_data["report_type"]
            generated_by_id = str(report_data["generated_by_id"])
            status = report_data.get("status")

            # Validate incident
            if incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident {incident_id} not found"
                })

            # Validate user
            if generated_by_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {generated_by_id} not found"
                })

            # Validate report type
            if report_type not in valid_report_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid report_type. Must be one of: {', '.join(valid_report_types)}"
                })

            # Post-mortem incident status validation
            if report_type == "post_mortem":
                incident_status = incidents[incident_id].get("status")
                if incident_status not in ["resolved", "closed"]:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident must be 'resolved' or 'closed' for post_mortem report. Current status: {incident_status}"
                    })

            if status and status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })

            # Generate report
            new_id = generate_id(incident_reports)
            new_report = {
                "report_id": str(new_id),
                "incident_id": incident_id,
                "report_type": report_type,
                "generated_by_id": generated_by_id,
                "generated_at": "2025-10-02T12:00:00",
                "status": status if status else "draft",
                "created_at": "2025-10-02T12:00:00",
                "updated_at": "2025-10-02T12:00:00"
            }

            incident_reports[str(new_id)] = new_report

            return json.dumps({
                "success": True,
                "action": "create",
                "report_id": str(new_id),
                "message": f"Incident report {new_id} created successfully",
                "incident_report_data": new_report
            })

        elif action == "update":
            if not report_id:
                return json.dumps({
                    "success": False,
                    "error": "report_id is required for update action"
                })

            if report_id not in incident_reports:
                return json.dumps({
                    "success": False,
                    "error": f"Incident report {report_id} not found"
                })

            if not report_data:
                return json.dumps({
                    "success": False,
                    "error": "report_data is required for update action"
                })

            current_report = incident_reports[report_id].copy()

            # Update allowed fields
            allowed_update_fields = ["report_type", "status", "generated_by_id"]
            invalid_fields = [k for k in report_data.keys() if k not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for report update: {', '.join(invalid_fields)}"
                })

            if "report_type" in report_data:
                rt = report_data["report_type"]
                if rt not in valid_report_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid report_type. Must be one of: {', '.join(valid_report_types)}"
                    })
                current_report["report_type"] = rt

            if "status" in report_data:
                st = report_data["status"]
                if st not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                current_report["status"] = st

            if "generated_by_id" in report_data:
                gid = str(report_data["generated_by_id"])
                if gid not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"User {gid} not found"
                    })
                
                current_report["generated_by_id"] = gid

            current_report["updated_at"] = "2025-10-02T12:00:00"
            incident_reports[report_id] = current_report

            return json.dumps({
                "success": True,
                "action": "update",
                "report_id": report_id,
                "message": f"Incident report {report_id} updated successfully",
                "incident_report_data": current_report
            })

    @staticmethod
    def discover_users_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover user entities.
        
        Supported entities:
        - users: User records by user_id, client_id, vendor_id, first_name, last_name, email, role, department, timezone, status
        """
        if entity_type not in ["users"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'users'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("users", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "user_id": str(entity_id)})
            else:
                results.append({**entity_data, "user_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def check_approval_invoke(data: Dict[str, Any], action: str, requester_email: str) -> str:
        """
        Check approval for Incident Management actions.
        Uses OR logic with fallback:
        1. If requester has ANY authorized role → approved
        2. If requester lacks an authorized role but has an 'approved' record from someone with an authorized role → approved
        3. Otherwise → denied
        
        Args:
            data: Environment data containing users and approvals
            action: The incident management action being performed
            requester_email: Email of the user requesting the action  
        """
        # Single source of truth for all actions and their authorized roles
        ACTIONS = {
            "create_client": ["system_administrator", "incident_manager", "account_manager"],
            "update_client": ["system_administrator", "incident_manager", "account_manager"],
            "create_user": ["system_administrator", "incident_manager"],
            "update_user": ["system_administrator", "incident_manager"],
            "create_vendor": ["system_administrator", "incident_manager", "executive"],
            "update_vendor": ["system_administrator", "incident_manager", "executive"],
            "create_product": ["system_administrator", "incident_manager", "executive"],
            "update_product": ["system_administrator", "incident_manager", "executive"],
            "create_component": ["system_administrator", "technical_support", "incident_manager"],
            "update_component": ["system_administrator", "technical_support", "incident_manager"],
            "create_subscription": ["account_manager", "incident_manager", "executive"],
            "update_subscription": ["account_manager", "incident_manager", "executive"],
            "create_sla": ["account_manager", "system_administrator", "executive"],
            "update_sla": ["account_manager", "system_administrator", "executive"],
            "create_incident": ["incident_manager", "technical_support", "system_administrator", "executive"],
            "update_incident": ["incident_manager", "technical_support", "system_administrator", "executive"],
            "resolve_incident": ["incident_manager", "technical_support", "executive"],
            "close_incident": ["incident_manager", "executive"],
            "create_communication": ["incident_manager", "technical_support", "system_administrator", "account_manager"],
            "update_communication": ["incident_manager", "technical_support", "system_administrator", "account_manager"],
            "create_workaround": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "update_workaround": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "conduct_rca": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "update_rca": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "create_escalation": ["incident_manager", "technical_support", "system_administrator", "executive"],
            "update_escalation": ["incident_manager", "technical_support", "system_administrator", "executive"],
            "create_change_request": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "update_change_request": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "create_rollback_request": ["system_administrator", "executive"],
            "update_rollback_request": ["incident_manager", "system_administrator", "executive"],
            "record_metrics": ["incident_manager", "system_administrator"],
            "update_metrics": ["incident_manager", "system_administrator"],
            "generate_report": ["incident_manager", "executive"],
            "update_report": ["incident_manager", "executive"],
            "create_kb_article": ["technical_support", "incident_manager"],
            "update_kb_article": ["technical_support", "incident_manager"],
            "create_pir": ["incident_manager", "executive"],
            "update_pir": ["incident_manager", "executive"]
        }
        
        # Find the requester's role
        users = data.get("users", {})
        requester_role = None
        for user in users.values():
            if user.get("email") == requester_email:
                requester_role = user.get("role")
                break
        
        if not requester_role:
            return json.dumps({
                "approval_valid": False,
                "error": f"No user found with email: {requester_email}"
            })
        
        # Check if the action is defined
        if action not in ACTIONS:
            return json.dumps({
                "approval_valid": False,
                "error": f"Unknown action: {action}"
            })
        
        authorized_roles = ACTIONS[action]
        
        # TIER 1: Check if requester has direct authorization
        if requester_role in authorized_roles:
            return json.dumps({
                "approval_valid": True,
                "message": f"User with role '{requester_role}' is directly authorized to perform action '{action}'"
            })
        
        # TIER 2: Requester not directly authorized, check for an explicit approval
        approvals = data.get("approvals", {})
        print(approvals.keys())
        for approval in approvals.values():
            print(action)
            print(approval.get("action_name"))
            # Check for a matching, approved record for the specific requester and action
            if (approval.get("requester_email") == requester_email and
                approval.get("action_name") == action and
                approval.get("status") == "approved"):
                
                # Check if the approver has an authorized role
                approver_role = approval.get("approver_role")
                if approver_role and approver_role in authorized_roles:
                    return json.dumps({
                        "approval_valid": True,
                        "message": f"User '{requester_email}' has a valid approval from '{approver_role}' (authorized role) for action '{action}'"
                    })

        # No direct authorization or valid approval found
        return json.dumps({
            "approval_valid": False,
            "error": f"Role '{requester_role}' is not authorized for action '{action}', and no valid approval was found. Authorized roles: {', '.join(authorized_roles)}."
        })

    @staticmethod
    def discover_products_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover product entities.
        
        Supported entities:
        - products: Product records by product_id, product_name, product_type, version, vendor_support_id, status
        """
        if entity_type not in ["products"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'products'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("products", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "product_id": str(entity_id)})
            else:
                results.append({**entity_data, "product_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def discover_change_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover change and rollback request entities.
        
        Supported entities:
        - change_requests: Change request records
        - rollback_requests: Rollback request records
        """
        if entity_type not in ["change_requests", "rollback_requests"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'change_requests' or 'rollback_requests'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        id_field = "change_id" if entity_type == "change_requests" else "rollback_id"
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: str(entity_id)})
            else:
                results.append({**entity_data, id_field: str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def discover_clients_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover client entities.
        
        Supported entities:
        - clients: Client records by client_id, client_name, client_type, industry, country, status
        """
        if entity_type not in ["clients"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'clients'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("clients", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "client_id": str(entity_id)})
            else:
                results.append({**entity_data, "client_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def discover_escalations_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover escalation entities.
        
        Supported entities:
        - escalations: Escalation records
        """
        if entity_type not in ["escalations"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'escalations'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("escalations", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "escalation_id": str(entity_id)})
            else:
                results.append({**entity_data, "escalation_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

