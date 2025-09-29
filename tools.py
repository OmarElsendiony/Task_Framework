from datetime import datetime
from typing import Any, Dict
from typing import Any, Dict, List
from typing import Any, Dict, Optional
import json
import re

class Tools:
    @staticmethod
    def create_investor_invoke(data: Dict[str, Any], legal_name: str, source_of_funds: str, 
               contact_email: str, accreditation_status: str,
               compliance_officer_approval: bool,
               registration_number: Optional[str] = None,
               date_of_incorporation: Optional[str] = None,
               country_of_incorporation: Optional[str] = None,
               registered_address: Optional[str] = None,
               tax_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        
        # Validate required approvals first
        if not compliance_officer_approval:
            return json.dumps({
                "success": False,
                "error": "Compliance Officer approval is required for investor onboarding"
            })
        
        # Validate required fields
        if not legal_name or not legal_name.strip():
            return json.dumps({
                "success": False,
                "error": "Legal name is required"
            })
        
        if not contact_email or not contact_email.strip():
            return json.dumps({
                "success": False,
                "error": "Contact email is required"
            })
        
        # Validate source_of_funds
        valid_sources = ['retained_earnings', 'shareholder_capital', 'asset_sale', 'loan_facility', 'external_investment', 'government_grant', 'merger_or_acquisition_proceeds', 'royalty_or_licensing_income', 'dividend_income', 'other']
        if source_of_funds not in valid_sources:
            return json.dumps({
                "success": False,
                "error": f"Invalid source_of_funds. Must be one of {valid_sources}"
            })
        
        # Validate accreditation_status
        valid_accreditation = ["accredited", "non_accredited"]
        if accreditation_status not in valid_accreditation:
            return json.dumps({
                "success": False,
                "error": f"Invalid accreditation_status. Must be one of {valid_accreditation}"
            })
        
        # Check if investor with same email already exists
        for investor in investors.values():
            if investor.get("contact_email") == contact_email:
                return json.dumps({
                    "success": False,
                    "error": "An investor with this email already exists"
                })
        
        investor_id = generate_id(investors)
        timestamp = "2025-10-01T00:00:00"
        
        new_investor = {
            "investor_id": str(investor_id) if investor_id is not None else None,
            "name": legal_name,
            "registration_number": registration_number,
            "date_of_incorporation": date_of_incorporation,
            "country": country_of_incorporation,
            "address": registered_address,
            "tax_id": str(tax_id) if tax_id is not None else None,
            "source_of_funds": source_of_funds,
            "status": "onboarded",
            "contact_email": contact_email,
            "accreditation_status": accreditation_status,
            "created_at": timestamp
        }
        
        investors[str(investor_id)] = new_investor
        
        return json.dumps(new_investor)

    @staticmethod
    def upload_document_invoke(data: Dict[str, Any], name: str, format: str, uploaded_by: str,
               size_bytes: Optional[int] = None, report_id: Optional[str] = None,
               confidentiality_level: str = "internal", status: str = "available") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        documents = data.get("documents", {})
        users = data.get("users", {})
        reports = data.get("reports", {})
        
        # Validate uploaded_by user exists
        if str(uploaded_by) not in users:
            return json.dumps({"error": f"User {uploaded_by} not found"})
        
        # Validate format
        valid_formats = ["pdf", "xlsx", "docx", "csv", "other"]
        if format not in valid_formats:
            return json.dumps({"error": f"Invalid format. Must be one of {valid_formats}"})
        
        # Validate confidentiality_level
        valid_confidentiality = ["public", "internal", "confidential", "restricted"]
        if confidentiality_level not in valid_confidentiality:
            return json.dumps({"error": f"Invalid confidentiality level. Must be one of {valid_confidentiality}"})
        
        # Validate status
        valid_statuses = ["available", "archived", "deleted"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        # Validate report_id if provided
        if report_id and str(report_id) not in reports:
            return json.dumps({"error": f"Report {report_id} not found"})
        
        # Check if document name already exists (file name is unique key)
        for doc in documents.values():
            if doc.get("name") == name:
                return json.dumps({"error": f"Document with name '{name}' already exists"})
        
        document_id = generate_id(documents)
        timestamp = "2025-10-01T00:00:00"
        
        new_document = {
            "document_id": str(document_id) if document_id else None,
            "name": name,
            "format": format,
            "uploaded_by": uploaded_by,
            "upload_date": timestamp,
            "report_id": str(report_id) if report_id else None,
            "size_bytes": size_bytes,
            "confidentiality_level": confidentiality_level,
            "status": status
        }
        
        documents[str(document_id)] = new_document
        return json.dumps(new_document)

    @staticmethod
    def manage_nav_record_invoke(data: Dict[str, Any], action: str, nav_data: Dict[str, Any] = None, nav_id: str = None) -> str:
        """
        Create or update NAV records.
        
        Actions:
        - create: Create new NAV record (requires nav_data with fund_id, nav_date, nav_value, finance_officer_approval)
        - update: Update existing NAV record (requires nav_id and nav_data with changes, finance_officer_approval, fund_manager_approval)
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
        
        # Access nav_records data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for nav_records"
            })
        
        nav_records = data.get("nav_records", {})
        
        if action == "create":
            if not nav_data:
                return json.dumps({
                    "success": False,
                    "error": "nav_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["fund_id", "nav_date", "nav_value", "finance_officer_approval"]
            missing_fields = [field for field in required_fields if field not in nav_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for NAV creation: {', '.join(missing_fields)}. Finance Officer approval is required."
                })
            
            # Validate that finance_officer_approval is True
            if not nav_data.get("finance_officer_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Finance Officer approval must be True for NAV creation"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["fund_id", "nav_date", "nav_value", "finance_officer_approval"]
            invalid_fields = [field for field in nav_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for NAV creation: {', '.join(invalid_fields)}"
                })
            
            # Validate NAV value is positive
            if nav_data["nav_value"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "NAV value must be positive - negative or zero values are not allowed"
                })
            
            # Validate that nav_date is not in the future (using current system date)
            current_date = "2025-10-01"  # Based on policy current date
            if nav_data["nav_date"] > current_date:
                return json.dumps({
                    "success": False,
                    "error": "Invalid NAV date: cannot create NAV record with future date"
                })
            
            # Check for existing NAV for the same fund and date
            fund_id = nav_data["fund_id"]
            nav_date = nav_data["nav_date"]
            for existing_nav in nav_records.values():
                if (existing_nav.get("fund_id") == fund_id and 
                    existing_nav.get("nav_date") == nav_date):
                    return json.dumps({
                        "success": False,
                        "error": f"NAV already exists for fund {fund_id} on date {nav_date}. Only one NAV per fund per date is allowed."
                    })
            
            # Generate new NAV ID using the same pattern as other tools
            new_nav_id = generate_id(nav_records)
            
            # Create new NAV record
            new_nav = {
                "nav_id": str(new_nav_id),
                "fund_id": str(nav_data["fund_id"]),
                "nav_date": nav_data["nav_date"],
                "nav_value": nav_data["nav_value"],
                "updated_at": "2025-10-01T12:00:00"
            }
            
            nav_records[str(new_nav_id)] = new_nav
            
            return json.dumps({
                "success": True,
                "action": "create",
                "nav_id": str(new_nav_id),
                "message": f"NAV record {new_nav_id} created successfully for fund {fund_id} on {nav_date}",
                "nav_data": new_nav
            })
        
        elif action == "update":
            if not nav_id:
                return json.dumps({
                    "success": False,
                    "error": "nav_id is required for update action"
                })
            
            if nav_id not in nav_records:
                return json.dumps({
                    "success": False,
                    "error": f"NAV record {nav_id} not found"
                })
            
            if not nav_data:
                return json.dumps({
                    "success": False,
                    "error": "nav_data is required for update action"
                })
            
            # Validate required approvals for updates (both Finance Officer and Fund Manager required)
            required_approvals = ["finance_officer_approval", "fund_manager_approval"]
            missing_approvals = [field for field in required_approvals if field not in nav_data]
            if missing_approvals:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required approvals for NAV update: {', '.join(missing_approvals)}. Both Finance Officer and Fund Manager approvals are required."
                })
            
            # Validate that both approvals are True
            if not (nav_data.get("finance_officer_approval") and nav_data.get("fund_manager_approval")):
                return json.dumps({
                    "success": False,
                    "error": "Both Finance Officer and Fund Manager approvals must be True for NAV update"
                })
            
            # Validate only allowed fields are present for updates (cannot update fund_id or nav_date)
            allowed_update_fields = ["nav_value", "finance_officer_approval", "fund_manager_approval"]
            invalid_fields = [field for field in nav_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for NAV update: {', '.join(invalid_fields)}. Cannot update fund_id or nav_date."
                })
            
            # Validate NAV value is positive if provided
            if "nav_value" in nav_data and nav_data["nav_value"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "NAV value must be positive - negative or zero values are not allowed"
                })
            
            # Update NAV record
            updated_nav = nav_records[nav_id].copy()
            for key, value in nav_data.items():
                if key not in ["finance_officer_approval", "fund_manager_approval"]:  # Skip approval codes from being stored
                    updated_nav[key] = value
            
            updated_nav["updated_at"] = "2025-10-01T12:00:00"
            nav_records[nav_id] = updated_nav
            
            return json.dumps({
                "success": True,
                "action": "update",
                "nav_id": str(nav_id) if nav_id is not None else None,
                "message": f"NAV record {nav_id} updated successfully",
                "nav_data": updated_nav
            })

    @staticmethod
    def discover_fund_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover fund entities.
        
        Supported entities:
        - funds: Fund records by fund_id, name, fund_type, manager_id, size, status
        """
        if entity_type not in ["funds"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'funds'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("funds", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "fund_id": str(entity_id)})
            else:
                results.append({**entity_data, "fund_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_portfolio_holdings_invoke(data: Dict[str, Any], action: str, holding_data: Dict[str, Any] = None, holding_id: str = None) -> str:
        """
        Create or update portfolio holdings records.
        
        Actions:
        - create: Create new holding (requires holding_data with portfolio_id, fund_id, quantity, cost_basis, fund_manager_approval)
        - update: Update existing holding (requires holding_id and holding_data with changes like quantity, cost_basis, fund_manager_approval)
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
                "error": "Invalid data format for portfolio_holdings"
            })
        
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        if action == "create":
            if not holding_data:
                return json.dumps({
                    "success": False,
                    "error": "holding_data is required for create action"
                })
            
            required_fields = ["portfolio_id", "fund_id", "quantity", "cost_basis", "fund_manager_approval"]
            missing_fields = [field for field in required_fields if field not in holding_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for holding creation: {', '.join(missing_fields)}. Fund Manager approval is required."
                })
            
            if not holding_data.get("fund_manager_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Fund Manager approval is required for holding creation"
                })
            
            allowed_fields = ["portfolio_id", "fund_id", "quantity", "cost_basis", "fund_manager_approval"]
            invalid_fields = [field for field in holding_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for holding creation: {', '.join(invalid_fields)}"
                })
            
            if holding_data["quantity"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Quantity must be positive"
                })
            
            if holding_data["cost_basis"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Cost basis must be positive"
                })
            
            portfolio_id = holding_data["portfolio_id"]
            fund_id = holding_data["fund_id"]
            for existing_holding in portfolio_holdings.values():
                if (existing_holding.get("portfolio_id") == portfolio_id and 
                    existing_holding.get("fund_id") == fund_id):
                    return json.dumps({
                        "success": False,
                        "error": f"Fund {fund_id} already exists in portfolio {portfolio_id}. Only one holding per fund per portfolio is allowed."
                    })
            
            new_holding_id = generate_id(portfolio_holdings)
            
            new_holding = {
                "holding_id": str(new_holding_id) if new_holding_id else None,
                "portfolio_id": str(holding_data["portfolio_id"]) if holding_data["portfolio_id"] else None,
                "fund_id": str(holding_data["fund_id"]) if holding_data["fund_id"] else None,
                "quantity": holding_data["quantity"],
                "cost_basis": holding_data["cost_basis"],
                "created_at": "2025-10-01T12:00:00"
            }
            
            portfolio_holdings[str(new_holding_id)] = new_holding
            
            return json.dumps({
                "success": True,
                "action": "create",
                "holding_id": str(new_holding_id) if new_holding_id else None,
                "message": f"Portfolio holding {new_holding_id} created successfully for portfolio {portfolio_id} with fund {fund_id}",
                "holding_data": new_holding
            })
        
        elif action == "update":
            if not holding_id:
                return json.dumps({
                    "success": False,
                    "error": "holding_id is required for update action"
                })
            
            if holding_id not in portfolio_holdings:
                return json.dumps({
                    "success": False,
                    "error": f"Portfolio holding record {holding_id} not found"
                })
            
            if not holding_data:
                return json.dumps({
                    "success": False,
                    "error": "holding_data is required for update action"
                })
            
            if "fund_manager_approval" not in holding_data:
                return json.dumps({
                    "success": False,
                    "error": "Fund Manager approval is required for holding update"
                })
            
            if not holding_data.get("fund_manager_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Fund Manager approval must be True for holding update"
                })
            
            allowed_update_fields = ["quantity", "cost_basis", "fund_manager_approval"]
            invalid_fields = [field for field in holding_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for holding update: {', '.join(invalid_fields)}. Cannot update portfolio_id or fund_id."
                })
            
            if "quantity" in holding_data and holding_data["quantity"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Quantity must be positive"
                })
            
            if "cost_basis" in holding_data and holding_data["cost_basis"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Cost basis must be positive"
                })
            
            updated_holding = portfolio_holdings[holding_id].copy()
            for key, value in holding_data.items():
                if key != "fund_manager_approval":
                    updated_holding[key] = value
            
            portfolio_holdings[holding_id] = updated_holding
            
            return json.dumps({
                "success": True,
                "action": "update",
                "holding_id": str(holding_id),
                "message": f"Portfolio holding {holding_id} updated successfully",
                "holding_data": updated_holding
            })

    @staticmethod
    def discover_system_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover system entities: notifications and audit trails.
        
        Supported entities:
        - notifications: Notification records by notification_id, email, type, class, reference_id, status, sent_at
        - audit_trails: Audit trail records by audit_trail_id, reference_id, reference_type, action, user_id, field_name, old_value, new_value
        """
        if entity_type not in ["notifications", "audit_trails"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'notifications' or 'audit_trails'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "notifications": "notification_id",
            "audit_trails": "audit_trail_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def transfer_to_human_invoke(
        data: Dict[str, Any],
        summary: str,
    ) -> str:
        return "Transfer successful"

    @staticmethod
    def manage_portfolio_invoke(data: Dict[str, Any], action: str, portfolio_data: Dict[str, Any] = None, portfolio_id: str = None) -> str:
        """
        Create or update portfolio records.
        
        Actions:
        - create: Create new portfolio (requires portfolio_data with investor_id, fund_manager_approval OR finance_officer_approval, optional status)
        - update: Update existing portfolio (requires portfolio_id and portfolio_data with changes like status, fund_manager_approval)
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
        
        # Access portfolios data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for portfolios"
            })
        
        portfolios = data.get("portfolios", {})
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        if action == "create":
            if not portfolio_data:
                return json.dumps({
                    "success": False,
                    "error": "portfolio_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["investor_id"]
            missing_fields = [field for field in required_fields if field not in portfolio_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for portfolio creation: {', '.join(missing_fields)}"
                })
            
            # Validate approval - Fund Manager OR Finance Officer approval required
            has_fund_manager_approval = portfolio_data.get("fund_manager_approval", False)
            has_finance_officer_approval = portfolio_data.get("finance_officer_approval", False)
            
            if not (has_fund_manager_approval or has_finance_officer_approval):
                return json.dumps({
                    "success": False,
                    "error": "Either Fund Manager approval or Finance Officer approval is required for portfolio creation"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["investor_id", "status", "fund_manager_approval", "finance_officer_approval"]
            invalid_fields = [field for field in portfolio_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for portfolio creation: {', '.join(invalid_fields)}"
                })
            
            # Validate status enum if provided
            if "status" in portfolio_data:
                valid_statuses = ["active", "inactive", "archived"]
                if portfolio_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Check if investor already has an active portfolio (policy constraint)
            investor_id = portfolio_data["investor_id"]
            for existing_portfolio in portfolios.values():
                if (existing_portfolio.get("investor_id") == investor_id and 
                    existing_portfolio.get("status") == "active"):
                    return json.dumps({
                        "success": False,
                        "error": f"Investor {investor_id} already has an active portfolio. One investor is only allowed to have one portfolio."
                    })
            
            # Generate new portfolio ID using consistent pattern
            new_portfolio_id = generate_id(portfolios)
            
            # Create new portfolio record
            new_portfolio = {
                "portfolio_id": str(new_portfolio_id) if new_portfolio_id else None ,
                "investor_id": str(portfolio_data["investor_id"]) if portfolio_data["investor_id"] else None,
                "status": portfolio_data.get("status", "active"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            portfolios[str(new_portfolio_id)] = new_portfolio
            
            return json.dumps({
                "success": True,
                "action": "create",
                "portfolio_id": str(new_portfolio_id) if new_portfolio_id else None ,
                "message": f"Portfolio {new_portfolio_id} created successfully for investor {investor_id}",
                "portfolio_data": new_portfolio
            })
        
        elif action == "update":
            if not portfolio_id:
                return json.dumps({
                    "success": False,
                    "error": "portfolio_id is required for update action"
                })
            
            if portfolio_id not in portfolios:
                return json.dumps({
                    "success": False,
                    "error": f"Portfolio record {portfolio_id} not found"
                })
            
            if not portfolio_data:
                return json.dumps({
                    "success": False,
                    "error": "portfolio_data is required for update action"
                })
            
            # Validate required approvals for updates - Fund Manager approval required
            if not portfolio_data.get("fund_manager_approval", False):
                return json.dumps({
                    "success": False,
                    "error": "Fund Manager approval is required for portfolio update"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["status", "fund_manager_approval"]
            invalid_fields = [field for field in portfolio_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for portfolio update: {', '.join(invalid_fields)}. Cannot update investor_id."
                })
            
            # Validate status enum if provided
            if "status" in portfolio_data:
                valid_statuses = ["active", "inactive", "archived"]
                if portfolio_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                
                # Check if closing a portfolio with active holdings (policy constraint)
                current_portfolio = portfolios[portfolio_id]
                if (current_portfolio.get("status") == "active" and 
                    portfolio_data["status"] in ["inactive", "archived"]):
                    
                    # Check for active holdings in this portfolio
                    has_active_holdings = any(
                        holding.get("portfolio_id") == portfolio_id 
                        for holding in portfolio_holdings.values()
                    )
                    
                    if has_active_holdings:
                        return json.dumps({
                            "success": False,
                            "error": f"Cannot close portfolio {portfolio_id} because it has active holdings. Please remove all holdings before closing the portfolio."
                        })
            
            # Update portfolio record
            updated_portfolio = portfolios[portfolio_id].copy()
            for key, value in portfolio_data.items():
                if key not in ["fund_manager_approval"]:
                    updated_portfolio[key] = value
            
            updated_portfolio["updated_at"] = "2025-10-01T12:00:00"
            portfolios[portfolio_id] = updated_portfolio
            
            return json.dumps({
                "success": True,
                "action": "update",
                "portfolio_id": str(portfolio_id),
                "message": f"Portfolio {portfolio_id} updated successfully",
                "portfolio_data": updated_portfolio
            })

    @staticmethod
    def generate_report_invoke(data: Dict[str, Any], fund_id: str, report_date: str, export_period_end: str, generated_by: str, investor_id: Optional[str] = None, report_type: str = "performance", status: str = "pending") -> str:
        """
        Generates a new report record.

        Args:
            data: The database json.
            fund_id: ID of the fund for the report.
            report_date: The date the report is generated.
            export_period_end: The end date for the reporting period.
            generated_by: ID of the user generating the report.
            investor_id: Optional ID of the investor for the report.
            report_type: The type of report.
            status: The initial status of the report.

        Returns:
            A json string of the new report record or an error.
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        reports = data.get("reports", {})
        funds = data.get("funds", {})
        users = data.get("users", {})
        investors = data.get("investors", {})

        if fund_id not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        if generated_by not in users:
            return json.dumps({"error": f"User {generated_by} not found"})
        if investor_id and investor_id not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        valid_report_types = ["performance", "holding", "financial"]
        if report_type not in valid_report_types:
            return json.dumps({"error": f"Invalid report_type. Must be one of {valid_report_types}"})
            
        valid_statuses = ["pending", "completed", "failed"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        report_id = str(generate_id(reports))
        timestamp = "2025-10-01T00:00:00"
        
        new_report = {
            "report_id": str(report_id) if report_id is not None else None,
            "fund_id": str(fund_id) if fund_id is not None else None,
            "investor_id": str(investor_id) if investor_id is not None else None,
            "report_date": report_date,
            "report_type": report_type,
            "generated_by": generated_by,
            "status": status,
            "created_at": timestamp,
            "export_period_end": export_period_end
        }
        
        reports[report_id] = new_report
        return json.dumps(new_report)

    @staticmethod
    def discover_portfolio_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover portfolio entities: portfolios and portfolio holdings.
        
        Supported entities:
        - portfolios: Portfolio records by portfolio_id, investor_id, status
        - portfolio_holdings: Portfolio holding records by holding_id, portfolio_id, fund_id, quantity, cost_basis
        """
        if entity_type not in ["portfolios", "portfolio_holdings"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'portfolios' or 'portfolio_holdings'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "portfolios": "portfolio_id",
            "portfolio_holdings": "holding_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_instrument_price_invoke(data: Dict[str, Any], action: str, price_data: Dict[str, Any] = None, price_id: str = None) -> str:
        """
        Create or update instrument price records.
        
        Actions:
        - create: Create new price record (requires price_data with instrument_id, price_date, open_price, high_price, low_price, close_price, fund_manager_approval, compliance_officer_approval)
        - update: Update existing price record (requires price_id and price_data with changes, fund_manager_approval, compliance_officer_approval)
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
        
        # Access instrument_prices data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for instrument_prices"
            })
        
        instrument_prices = data.get("instrument_prices", {})
        
        if action == "create":
            if not price_data:
                return json.dumps({
                    "success": False,
                    "error": "price_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["instrument_id", "price_date", "open_price", "high_price", "low_price", "close_price", "fund_manager_approval", "compliance_officer_approval"]
            missing_fields = [field for field in required_fields if field not in price_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for price creation: {', '.join(missing_fields)}. Both Fund Manager and Compliance Officer approvals are required."
                })
            if not (price_data.get("fund_manager_approval") and price_data.get("compliance_officer_approval")):
                return json.dumps({
                    "success": False,
                    "error": "Both Fund Manager and Compliance Officer approvals are required for price creation"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["instrument_id", "price_date", "open_price", "high_price", "low_price", "close_price", "fund_manager_approval", "compliance_officer_approval"]
            invalid_fields = [field for field in price_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for price creation: {', '.join(invalid_fields)}"
                })
            
            # Validate all prices are positive
            price_fields = ["open_price", "high_price", "low_price", "close_price"]
            for field in price_fields:
                if price_data[field] <= 0:
                    return json.dumps({
                        "success": False,
                        "error": f"{field} must be positive - negative values are not allowed"
                    })
            
            # Validate price logic (high >= low)
            if price_data["high_price"] < price_data["low_price"]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid price data: high price must be greater than or equal to low price"
                })
            
            # Check for existing price for the same instrument and date
            instrument_id = price_data["instrument_id"]
            price_date = price_data["price_date"]
            for existing_price in instrument_prices.values():
                if (existing_price.get("instrument_id") == instrument_id and 
                    existing_price.get("price_date") == price_date):
                    return json.dumps({
                        "success": False,
                        "error": f"Price already exists for instrument {instrument_id} on date {price_date}. Only one price per instrument per date is allowed."
                    })
            
            # Generate new price ID using the same pattern as CreateFund
            new_price_id = generate_id(instrument_prices)
            
            # Create new price record
            new_price = {
                "price_id": str(new_price_id),
                "instrument_id": str(price_data["instrument_id"]),
                "price_date": price_data["price_date"],
                "open_price": price_data["open_price"],
                "high_price": price_data["high_price"],
                "low_price": price_data["low_price"],
                "close_price": price_data["close_price"]
            }
            
            instrument_prices[str(new_price_id)] = new_price
            
            return json.dumps({
                "success": True,
                "action": "create",
                "price_id": str(new_price_id),
                "message": f"Instrument price {new_price_id} created successfully for instrument {instrument_id} on {price_date}",
                "price_data": new_price
            })
        
        elif action == "update":
            if not price_id:
                return json.dumps({
                    "success": False,
                    "error": "price_id is required for update action"
                })
            
            if price_id not in instrument_prices:
                return json.dumps({
                    "success": False,
                    "error": f"Instrument price record {price_id} not found"
                })
            
            if not price_data:
                return json.dumps({
                    "success": False,
                    "error": "price_data is required for update action"
                })
            
            # Validate required approvals for updates
            required_approvals = ["fund_manager_approval", "compliance_officer_approval"]
            missing_approvals = [field for field in required_approvals if field not in price_data]
            if missing_approvals:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required approvals for price update: {', '.join(missing_approvals)}. Both Fund Manager and Compliance Officer approvals are required."
                })
            
            if not (price_data.get("fund_manager_approval") and price_data.get("compliance_officer_approval")):
                return json.dumps({
                    "success": False,
                    "error": "Both Fund Manager and Compliance Officer approvals are required for price update"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["open_price", "high_price", "low_price", "close_price", "fund_manager_approval", "compliance_officer_approval"]
            invalid_fields = [field for field in price_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for price update: {', '.join(invalid_fields)}. Cannot update instrument_id or price_date."
                })
            
            # Get current price data for validation
            current_price = instrument_prices[price_id].copy()
            
            # Update current price with new values for validation
            for key, value in price_data.items():
                if key not in ["fund_manager_approval", "compliance_officer_approval"]:
                    current_price[key] = value
            
            # Validate all prices are positive if provided
            price_fields = ["open_price", "high_price", "low_price", "close_price"]
            for field in price_fields:
                if field in price_data and price_data[field] <= 0:
                    return json.dumps({
                        "success": False,
                        "error": f"{field} must be positive - negative values are not allowed"
                    })
            
            # Validate price logic after update
            if current_price["high_price"] < current_price["low_price"]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid price data: high price must be greater than or equal to low price"
                })
            
            # Update price record
            updated_price = instrument_prices[price_id].copy()
            for key, value in price_data.items():
                if key not in ["fund_manager_approval", "compliance_officer_approval"]:
                    updated_price[key] = value
            
            instrument_prices[price_id] = updated_price
            
            return json.dumps({
                "success": True,
                "action": "update",
                "price_id": str(price_id) if price_id is not None else None,
                "message": f"Instrument price {price_id} updated successfully",
                "price_data": updated_price
            })

    @staticmethod
    def discover_trading_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover trading entities.
        
        Supported entities:
        - trades: Trade records by trade_id, fund_id, instrument_id, trade_date, quantity, price, side, status
        """
        if entity_type not in ["trades"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'trades'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("trades", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "trade_id": str(entity_id)})
            else:
                results.append({**entity_data, "trade_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def approval_lookup_invoke(data: Dict[str, Any], action: str, requester_email: str) -> str:
        # Define role authorization mapping
        role_authorizations = {
            "compliance_officer": [
                "investor_onboarding", "investor_offboarding", "subscription_management", 
                "commitments_create", "commitments_fulfill", "redemption_processing",
                "instrument_creation", "instrument_update",
            ],
            "fund_manager": [
                "fund_management_setup", "fund_management_maintenance", "trade_execution", 
                "portfolio_creation", "portfolio_update", "portfolio_holding_management", 
                "instrument_creation", "instrument_update", "nav_record_updates", "instrument_price_updates",
                "reporting_performance", "reporting_financial", "subscription_management"
            ],
            "finance_officer": [
                "nav_valuation", "redemption_processing", 
                "portfolio_creation", "invoice_management", "payment_processing", 
                "nav_record_creation", "nav_record_updates", "reporting_holding"
            ],
            "trader": [
                "trade_execution"
            ],
            "system_administrator": [
                "user_account_management", "system_monitoring"
            ]
        }
        
        # Define actions requiring multiple approvers (AND logic)
        and_approval_actions = {
            "fund_management_setup": ["fund_manager", "compliance_officer"],
            "fund_management_maintenance": ["fund_manager", "compliance_officer"],
            "redemption_processing": ["compliance_officer", "finance_officer"],
            "instrument_creation": ["fund_manager", "compliance_officer"],
            "instrument_update": ["fund_manager", "compliance_officer"],
            "nav_record_updates": ["finance_officer", "fund_manager"],
            "instrument_price_updates": ["fund_manager", "compliance_officer"],
            "subscription_management": ["compliance_officer", "fund_manager"]
        }
        
        # Define actions allowing alternative approvers (OR logic)
        or_approval_actions = {
            "portfolio_creation": ["fund_manager", "finance_officer"]
        }
        
        users = data.get("users", {})
        for user in users.values():
            if user.get("email") == requester_email:
                role_conducting_action = user.get("role")
                requester_id = user.get("user_id")
                break
        else:
            return json.dumps({
                "approval_valid": False,
                "error": f"No user found with email: {requester_email}"
            })
        # Check if role is directly authorized for the action
        authorized_roles = role_authorizations.get(role_conducting_action, [])
        if action in authorized_roles:
            return json.dumps({
                "approval_valid": True, 
                # "authorized_by_role": True,
                "message": f"Role '{role_conducting_action}' is directly authorized for action '{action}'",
            })
        
        # If not directly authorized, calculate and check approval code
        # Generate calculated approval code: action + requester_id
        calculated_approval_code = f"{action}_{requester_id}"
        
        approvals = data.get("approvals", {})
        
        # Check if calculated approval code exists
        approvals_found_for_code = []
        for approval in approvals.values():
            if approval.get("code") == calculated_approval_code:
                approvals_found_for_code.append(approval)
                # break
        # print(f"Approvals found for code '{calculated_approval_code}': {approvals_found_for_code}")
        if not approvals_found_for_code:
            return json.dumps({
                "approval_valid": False,
                "error": f"No approval found"
            })

        approvals_approved_by = [ approvals_found.get("approved_by") for approvals_found in approvals_found_for_code if "approved_by" in approvals_found ]
        # Check AND logic actions
        if action in and_approval_actions:
            required_roles = and_approval_actions[action]
            for approved_by in approvals_approved_by:
                if required_roles and approved_by in required_roles:
                    required_roles.remove(approved_by)
                    # return json.dumps({
                    #     "approval_valid": True,
                    #     "approved_by": approved_by,
                    #     "approval_type": "and_logic",
                    #     "note": f"Requires all roles: {', '.join(required_roles)}"
                    # })
            if not required_roles:
                return json.dumps({
                    "approval_valid": True,
                    "approved_by": approvals_approved_by,
                })
            else:
                return json.dumps({
                    "approval_valid": False,
                    "error": f"Requires additional approvals from roles: {', '.join(required_roles)}"
                })
        
        # Check OR logic actions
        elif action in or_approval_actions:
            allowed_roles = or_approval_actions[action]
            for approved_by in approvals_approved_by:
                if approved_by in allowed_roles:
                    return json.dumps({
                        "approval_valid": True,
                        "approved_by": approved_by,
                    })
        
        # Check single approver actions
        else:
            for role, actions in role_authorizations.items():
                approved_by = approvals_found_for_code[0].get("approved_by")
                if action in actions and approved_by == role:
                    # print("single approver match found")
                    return json.dumps({
                        "approval_valid": True,
                        "approved_by": approved_by,
                    })
        
        return json.dumps({
            "approval_valid": False,
            "error": f"No valid approval found"
        })

    @staticmethod
    def manage_invoice_invoke(data: Dict[str, Any], action: str, invoice_data: Dict[str, Any] = None, invoice_id: str = None) -> str:
        """
        Create or update invoice records.
        
        Actions:
        - create: Create new invoice record (requires invoice_data with invoice_date, due_date, amount, finance_officer_approval)
        - update: Update existing invoice record (requires invoice_id and invoice_data with changes, finance_officer_approval)
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
        
        # Access invoices data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for invoices"
            })
        
        invoices = data.get("invoices", {})
        
        if action == "create":
            if not invoice_data:
                return json.dumps({
                    "success": False,
                    "error": "invoice_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["invoice_date", "due_date", "amount", "finance_officer_approval"]
            missing_fields = [field for field in required_fields if field not in invoice_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for invoice creation: {', '.join(missing_fields)}. Finance Officer approval is required."
                })
            
            # Validate that finance_officer_approval is True
            if not invoice_data.get("finance_officer_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Finance Officer approval must be True for invoice creation"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["commitment_id", "invoice_date", "due_date", "amount", "status", "finance_officer_approval"]
            invalid_fields = [field for field in invoice_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for invoice creation: {', '.join(invalid_fields)}"
                })
            
            # Validate amount is positive
            if invoice_data["amount"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Invoice amount must be positive - negative or zero values are not allowed"
                })
            
            # Validate status enum if provided
            if "status" in invoice_data:
                valid_statuses = ["issued", "paid"]
                if invoice_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{invoice_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate date logic (due_date should not be before invoice_date)
            if invoice_data["due_date"] < invoice_data["invoice_date"]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid date logic: due date cannot be before invoice date"
                })
            
            # Validate that invoice_date is not in the future (using current system date)
            from datetime import datetime
            current_date = "2025-10-01"  # Based on policy current date
            if invoice_data["invoice_date"] > current_date:
                return json.dumps({
                    "success": False,
                    "error": "Invalid invoice date: cannot create invoice with future date"
                })
            
            # Check for existing invoice with same commitment_id and invoice_date if commitment_id is provided
            if "commitment_id" in invoice_data and invoice_data["commitment_id"]:
                commitment_id = invoice_data["commitment_id"]
                invoice_date = invoice_data["invoice_date"]
                for existing_invoice in invoices.values():
                    if (existing_invoice.get("commitment_id") == commitment_id and 
                        existing_invoice.get("invoice_date") == invoice_date):
                        return json.dumps({
                            "success": False,
                            "error": f"Invoice already exists for commitment {commitment_id} on date {invoice_date}. Only one invoice per commitment per date is allowed."
                        })
            
            # Generate new invoice ID using the same pattern as other tools
            new_invoice_id = generate_id(invoices)
            
            # Create new invoice record
            new_invoice = {
                "invoice_id": str(new_invoice_id),
                "commitment_id": str(invoice_data.get("commitment_id")),
                "invoice_date": invoice_data["invoice_date"],
                "due_date": invoice_data["due_date"],
                "amount": invoice_data["amount"],
                "status": invoice_data.get("status", "issued"),
                "updated_at": "2025-10-01T12:00:00"
            }
            
            invoices[str(new_invoice_id)] = new_invoice
            
            return json.dumps({
                "success": True,
                "action": "create",
                "invoice_id": str(new_invoice_id),
                "message": f"Invoice {new_invoice_id} created successfully for commitment {invoice_data.get('commitment_id', 'N/A')} on {invoice_data['invoice_date']}",
                "invoice_data": new_invoice
            })
        
        elif action == "update":
            if not invoice_id:
                return json.dumps({
                    "success": False,
                    "error": "invoice_id is required for update action"
                })
            
            if invoice_id not in invoices:
                return json.dumps({
                    "success": False,
                    "error": f"Invoice record {invoice_id} not found"
                })
            
            if not invoice_data:
                return json.dumps({
                    "success": False,
                    "error": "invoice_data is required for update action"
                })
            
            # Validate required approval for updates
            if "finance_officer_approval" not in invoice_data:
                return json.dumps({
                    "success": False,
                    "error": "Missing required approval for invoice update: finance_officer_approval. Finance Officer approval is required."
                })
            
            # Validate that finance_officer_approval is True
            if not invoice_data.get("finance_officer_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Finance Officer approval must be True for invoice update"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["status", "due_date", "amount", "commitment_id", "finance_officer_approval"]
            invalid_fields = [field for field in invoice_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for invoice update: {', '.join(invalid_fields)}. Cannot update invoice_date."
                })
            
            # Get current invoice data for validation
            current_invoice = invoices[invoice_id].copy()
            current_status = current_invoice.get("status", "issued")
            
            # Check if invoice is already paid (cannot modify paid invoices except specific fields)
            if current_status == "paid" and "status" in invoice_data and invoice_data["status"] != "paid":
                return json.dumps({
                    "success": False,
                    "error": "Cannot change status from paid to issued - paid invoices cannot be unpaid"
                })
            
            # Validate amount if provided
            if "amount" in invoice_data and invoice_data["amount"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Invoice amount must be positive - negative or zero values are not allowed"
                })
            
            # Validate status if provided
            if "status" in invoice_data:
                valid_statuses = ["issued", "paid"]
                if invoice_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{invoice_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Update current invoice with new values for validation
            temp_invoice = current_invoice.copy()
            for key, value in invoice_data.items():
                if key not in ["finance_officer_approval"]:
                    temp_invoice[key] = value
            
            # Validate date logic after update if due_date is being changed
            if "due_date" in invoice_data:
                if temp_invoice["due_date"] < temp_invoice["invoice_date"]:
                    return json.dumps({
                        "success": False,
                        "error": "Invalid date logic: due date cannot be before invoice date"
                    })
            
            # Check for duplicate commitment_id and invoice_date combination if commitment_id is being updated
            if "commitment_id" in invoice_data and invoice_data["commitment_id"]:
                commitment_id = invoice_data["commitment_id"]
                invoice_date = temp_invoice["invoice_date"]
                for existing_id, existing_invoice in invoices.items():
                    if (existing_id != invoice_id and 
                        existing_invoice.get("commitment_id") == commitment_id and 
                        existing_invoice.get("invoice_date") == invoice_date):
                        return json.dumps({
                            "success": False,
                            "error": f"Invoice already exists for commitment {commitment_id} on date {invoice_date}. Only one invoice per commitment per date is allowed."
                        })
            
            # Update invoice record
            updated_invoice = current_invoice.copy()
            for key, value in invoice_data.items():
                if key not in ["finance_officer_approval"]:
                    updated_invoice[key] = value
            
            updated_invoice["updated_at"] = "2025-10-01T12:00:00"
            invoices[invoice_id] = updated_invoice
            
            return json.dumps({
                "success": True,
                "action": "update",
                "invoice_id": str(invoice_id) if invoice_id is not None else None,
                "message": f"Invoice {invoice_id} updated successfully",
                "invoice_data": updated_invoice
            })

    @staticmethod
    def discover_investment_flow_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover investment flow entities: subscriptions, commitments, and redemptions.
        
        Supported entities:
        - subscriptions: Subscription records by subscription_id, fund_id, investor_id, amount, status, request_assigned_to, request_date, approval_date
        - commitments: Commitment records by commitment_id, fund_id, investor_id, commitment_amount, commitment_date, status
        - redemptions: Redemption records by redemption_id, subscription_id, request_date, redemption_amount, status, processed_date, redemption_fee
        """
        if entity_type not in ["subscriptions", "commitments", "redemptions"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'subscriptions', 'commitments', or 'redemptions'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "subscriptions": "subscription_id",
            "commitments": "commitment_id",
            "redemptions": "redemption_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_fund_invoke(data: Dict[str, Any], action: str, fund_data: Dict[str, Any] = None, fund_id: str = None) -> str:
        """
        Create or update fund records.
        
        Actions:
        - create: Create new fund (requires fund_data with name, fund_type, manager_id, fund_manager_approval, compliance_officer_approval, 
                 optional size, base_currency, status)
        - update: Update existing fund (requires fund_id and fund_data with changes, fund_manager_approval, 
                 compliance_officer_approval)
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
        
        # Access funds data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for funds"
            })
        
        funds = data.get("funds", {})
        
        if action == "create":
            if not fund_data:
                return json.dumps({
                    "success": False,
                    "error": "fund_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["name", "fund_type", "manager_id", "fund_manager_approval", "compliance_officer_approval"]
            missing_fields = [field for field in required_fields if field not in fund_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for fund creation: {', '.join(missing_fields)}. Both Fund Manager and Compliance Officer approvals are required."
                })
            
            # Validate both approvals are present and true
            if not (fund_data.get("fund_manager_approval") and fund_data.get("compliance_officer_approval")):
                return json.dumps({
                    "success": False,
                    "error": "Both Fund Manager and Compliance Officer approvals are required for fund creation"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["name", "fund_type", "size", "base_currency", "manager_id", "status", "fund_manager_approval", "compliance_officer_approval"]
            invalid_fields = [field for field in fund_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for fund creation: {', '.join(invalid_fields)}"
                })
            
            # Validate fund_type enum
            valid_fund_types = ["equity_funds", "bond_funds", "multi_asset_funds", "money_market_funds", "hedge_funds", "private_equity_funds", "real_estate_funds"]
            if fund_data["fund_type"] not in valid_fund_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fund_type. Must be one of: {', '.join(valid_fund_types)}"
                })
            
            # Validate size if provided (must be positive number)
            if "size" in fund_data:
                try:
                    size_value = float(fund_data["size"])
                    if size_value <= 0:
                        return json.dumps({
                            "success": False,
                            "error": "Fund size must be a positive number"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Fund size must be a valid number"
                    })
            
            # Validate status if provided
            if "status" in fund_data:
                valid_statuses = ["open", "closed"]
                if fund_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Check for duplicate fund name
            fund_name = fund_data["name"].strip()
            for existing_fund in funds.values():
                if existing_fund.get("name", "").strip().lower() == fund_name.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"Fund with name '{fund_name}' already exists"
                    })
            
            # Generate new fund ID using the same pattern as manage_instrument_price
            new_fund_id = generate_id(funds)
            
            # Create new fund record
            new_fund = {
                "fund_id": str(new_fund_id) if new_fund_id is not None else None,
                "name": fund_data["name"],
                "fund_type": fund_data["fund_type"],
                "size": fund_data.get("size"),
                "base_currency": fund_data.get("base_currency", "USD"),
                "manager_id": str(fund_data["manager_id"]) if fund_data.get("manager_id") is not None else None,
                "status": fund_data.get("status", "open"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            funds[str(new_fund_id)] = new_fund
            
            return json.dumps({
                "success": True,
                "action": "create",
                "fund_id": str(new_fund_id),
                "message": f"Fund {new_fund_id} created successfully with name '{fund_data['name']}'",
                "fund_data": new_fund
            })
        
        elif action == "update":
            if not fund_id:
                return json.dumps({
                    "success": False,
                    "error": "fund_id is required for update action"
                })
            
            if fund_id not in funds:
                return json.dumps({
                    "success": False,
                    "error": f"Fund {fund_id} not found"
                })
            
            if not fund_data:
                return json.dumps({
                    "success": False,
                    "error": "fund_data is required for update action"
                })
            
            # Validate required approvals for updates
            required_approvals = ["fund_manager_approval", "compliance_officer_approval"]
            missing_approvals = [field for field in required_approvals if field not in fund_data]
            if missing_approvals:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required approvals for fund update: {', '.join(missing_approvals)}. Both Fund Manager and Compliance Officer approvals are required."
                })
            
            # Validate both approvals are present and true
            if not (fund_data.get("fund_manager_approval") and fund_data.get("compliance_officer_approval")):
                return json.dumps({
                    "success": False,
                    "error": "Both Fund Manager and Compliance Officer approvals are required for fund update"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["name", "fund_type", "size", "base_currency", "manager_id", "status", 
                                   "fund_manager_approval", "compliance_officer_approval"]
            invalid_fields = [field for field in fund_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for fund update: {', '.join(invalid_fields)}"
                })
            
            # Validate fund_type enum if provided
            if "fund_type" in fund_data:
                valid_fund_types = ["equity_funds", "bond_funds", "multi_asset_funds", "money_market_funds", "hedge_funds", "private_equity_funds", "real_estate_funds"]
                if fund_data["fund_type"] not in valid_fund_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fund_type. Must be one of: {', '.join(valid_fund_types)}"
                    })
            
            # Validate size if provided
            if "size" in fund_data:
                try:
                    size_value = float(fund_data["size"])
                    if size_value <= 0:
                        return json.dumps({
                            "success": False,
                            "error": "Fund size must be a positive number"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Fund size must be a valid number"
                    })
            
            # Validate status transitions
            current_fund = funds[fund_id]
            current_status = current_fund.get("status", "open")
            if "status" in fund_data:
                new_status = fund_data["status"]
                valid_statuses = ["open", "closed"]
                
                if new_status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                
                # Define invalid status transitions
                invalid_transitions = {
                    "closed": ["open"]  # Cannot reopen closed fund
                }
                
                if current_status in invalid_transitions and new_status in invalid_transitions[current_status]:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid transition from {current_status} to {new_status}"
                    })
            
            # Check for duplicate fund name if updating name
            if "name" in fund_data:
                new_fund_name = fund_data["name"].strip()
                for existing_fund_id, existing_fund in funds.items():
                    if (existing_fund_id != fund_id and 
                        existing_fund.get("name", "").strip().lower() == new_fund_name.lower()):
                        return json.dumps({
                            "success": False,
                            "error": f"Fund with name '{new_fund_name}' already exists"
                        })
            
            # Update fund record
            updated_fund = current_fund.copy()
            for key, value in fund_data.items():
                if key not in ["fund_manager_approval", "compliance_officer_approval"]:  # Skip approval codes
                    updated_fund[key] = value
            
            updated_fund["updated_at"] = "2025-10-01T12:00:00"
            funds[fund_id] = updated_fund
            
            return json.dumps({
                "success": True,
                "action": "update",
                "fund_id": str(fund_id),
                "message": f"Fund {fund_id} updated successfully",
                "fund_data": updated_fund
            })

    @staticmethod
    def process_redemption_invoke(data: Dict[str, Any], redemption_id: str, status: str, 
               compliance_officer_approval: bool, finance_officer_approval: bool,
               processed_date: Optional[str] = None) -> str:
        """
        Processes a redemption request by updating its status.

        Args:
            data: The database json.
            redemption_id: The ID of the redemption to process.
            status: The new status for the redemption.
            compliance_officer_approval: Compliance Officer approval (required).
            finance_officer_approval: Finance Officer approval (required).
            processed_date: The date the redemption was processed.

        Returns:
            A json string representing the updated redemption record or an error.
        """
        redemptions = data.get("redemptions", {})

        # Validate required approvals first
        if not compliance_officer_approval:
            return json.dumps({
                "success": False,
                "error": "Compliance Officer approval is required for redemption processing"
            })
        
        if not finance_officer_approval:
            return json.dumps({
                "success": False,
                "error": "Finance Officer approval is required for redemption processing"
            })

        if redemption_id not in redemptions:
            return json.dumps({
                "success": False,
                "error": f"Redemption {redemption_id} not found"
            })

        valid_statuses = ["pending", "approved", "processed", "cancelled"]
        if status not in valid_statuses:
            return json.dumps({
                "success": False,
                "error": f"Invalid status. Must be one of {valid_statuses}"
            })

        if status == "processed" and not processed_date:
            return json.dumps({
                "success": False,
                "error": "processed_date is required when status is 'processed'"
            })

        redemption = redemptions[redemption_id]
        current_status = redemption.get("status", "").lower()
        
        # Validate status transitions
        if current_status == "processed" and status != "processed":
            return json.dumps({
                "success": False,
                "error": "Cannot change status of already processed redemption"
            })
        
        if current_status == "cancelled" and status != "cancelled":
            return json.dumps({
                "success": False,
                "error": "Cannot change status of cancelled redemption"
            })

        redemption["status"] = status
        if processed_date:
            redemption["processed_date"] = processed_date
        redemption["updated_at"] = "2025-10-01T00:00:00"

        return json.dumps(redemption)

    @staticmethod
    def manage_payment_invoke(data: Dict[str, Any], action: str, payment_data: Dict[str, Any] = None, payment_id: str = None) -> str:
        """
        Create or update payment records.
        
        Actions:
        - create: Create new payment (requires payment_data with invoice_id, subscription_id, payment_date, amount, payment_method, finance_officer_approval)
        - update: Update existing payment (requires payment_id and payment_data with changes like status, amount, finance_officer_approval)
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
        
        # Access payments data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payments"
            })
        
        payments = data.get("payments", {})
        
        if action == "create":
            if not payment_data:
                return json.dumps({
                    "success": False,
                    "error": "payment_data is required for create action"
                })
            
            # Validate required fields for creation - updated per policy
            required_fields = ["invoice_id", "subscription_id", "payment_date", "amount", "payment_method", "finance_officer_approval"]
            missing_fields = [field for field in required_fields if field not in payment_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for payment creation: {', '.join(missing_fields)}. Finance Officer approval is required."
                })
            
            # Validate required approval for creation
            if not payment_data.get("finance_officer_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Finance Officer approval is required for payment creation"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["invoice_id", "subscription_id", "payment_date", "amount", "payment_method", "status", "finance_officer_approval"]
            invalid_fields = [field for field in payment_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payment creation: {', '.join(invalid_fields)}"
                })
            
            # Validate amount is positive
            if payment_data["amount"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Payment amount must be positive"
                })
            
            # Validate payment_method enum
            valid_payment_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
            if payment_data["payment_method"] not in valid_payment_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid payment_method. Must be one of: {', '.join(valid_payment_methods)}"
                })
            
            # Validate status if provided
            if "status" in payment_data:
                valid_statuses = ["draft", "completed", "failed"]
                if payment_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Generate new payment ID using the same pattern as ManageInstrumentPrice
            new_payment_id = generate_id(payments)
            
            # Create new payment record
            new_payment = {
                "payment_id": str(new_payment_id) if new_payment_id else None ,
                "invoice_id": str(payment_data["invoice_id"]) if payment_data["invoice_id"] else None,
                "subscription_id": str(payment_data["subscription_id"]) if payment_data["subscription_id"] else None,
                "payment_date": payment_data["payment_date"],
                "amount": payment_data["amount"],
                "payment_method": payment_data["payment_method"],
                "status": payment_data.get("status", "draft"),
                "created_at": "2025-10-01T12:00:00"
            }
            
            payments[str(new_payment_id)] = new_payment
            
            return json.dumps({
                "success": True,
                "action": "create",
                "payment_id": str(new_payment_id) if new_payment_id else None ,
                "message": f"Payment {new_payment_id} created successfully for invoice {payment_data['invoice_id']}",
                "payment_data": new_payment
            })
        
        elif action == "update":
            if not payment_id:
                return json.dumps({
                    "success": False,
                    "error": "payment_id is required for update action"
                })
            
            if payment_id not in payments:
                return json.dumps({
                    "success": False,
                    "error": f"Payment {payment_id} not found"
                })
            
            if not payment_data:
                return json.dumps({
                    "success": False,
                    "error": "payment_data is required for update action"
                })
            
            # Validate required approval for updates
            if "finance_officer_approval" not in payment_data:
                return json.dumps({
                    "success": False,
                    "error": "finance_officer_approval is required for payment updates"
                })
            
            if not payment_data.get("finance_officer_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Finance Officer approval is required for payment update"
                })
            
            # Validate only allowed fields are present for updates (cannot update core fields)
            allowed_update_fields = ["status", "amount", "payment_date", "payment_method", "finance_officer_approval"]
            invalid_fields = [field for field in payment_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payment update: {', '.join(invalid_fields)}. Cannot update invoice_id or subscription_id."
                })
            
            # Get current payment for validation
            current_payment = payments[payment_id]
            current_status = current_payment.get("status", "draft")
            new_status = payment_data.get("status")
            
            # Validate status if provided
            if new_status and new_status not in ["draft", "completed", "failed"]:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: draft, completed, failed"
                })
            
            # Validate status transitions - cannot modify completed/processed payments per policy
            if current_status == "completed" and new_status and new_status != "completed":
                return json.dumps({
                    "success": False,
                    "error": "Cannot modify completed payment - cannot change status from completed to draft or failed"
                })
            
            if current_status == "failed" and new_status == "completed":
                return json.dumps({
                    "success": False,
                    "error": "Cannot change status from failed to completed - create new payment instead"
                })
            
            # Validate amount if provided
            if "amount" in payment_data and payment_data["amount"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Payment amount must be positive"
                })
            
            # Validate payment_method if provided
            if "payment_method" in payment_data:
                valid_payment_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
                if payment_data["payment_method"] not in valid_payment_methods:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid payment_method. Must be one of: {', '.join(valid_payment_methods)}"
                    })
            
            # Update payment record
            updated_payment = current_payment.copy()
            for key, value in payment_data.items():
                if key != "finance_officer_approval":  # Skip approval from being stored
                    updated_payment[key] = value
            
            updated_payment["updated_at"] = "2025-10-01T12:00:00"
            payments[payment_id] = updated_payment
            
            return json.dumps({
                "success": True,
                "action": "update",
                "payment_id": str(payment_id),
                "message": f"Payment {payment_id} updated successfully",
                "payment_data": updated_payment
            })

    @staticmethod
    def manage_instrument_invoke(data: Dict[str, Any], fund_manager_approval: bool = False, 
               compliance_officer_approval: bool = False,
               instrument_id: Optional[str] = None, ticker: Optional[str] = None, 
               name: Optional[str] = None, instrument_type: Optional[str] = None, 
               status: Optional[str] = None) -> str:
        """
        Creates a new financial instrument or updates an existing one.

        Args:
            data: The database json.
            fund_manager_approval: Fund Manager approval (required for creation and updates).
            compliance_officer_approval: Compliance Officer approval (required for creation and critical updates).
            instrument_id: The ID of the instrument to update. If None, a new one is created.
            ticker: The unique ticker symbol for the instrument.
            name: The name of the instrument.
            instrument_type: The type of the instrument.
            status: The status of the instrument.

        Returns:
            A json string of the created/updated instrument or an error.
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        instruments = data.get("instruments", {})

        valid_statuses = ["active", "inactive"]
        valid_instrument_types = [
            'equities_common_shares','equities_preferred_shares','equities_indexed','equities_domestic','equities_international','bonds_corporate','bonds_municipal','bonds_government','bonds_inflation_linked','bonds_high_yield','bonds_distressed','money_market_treasury_bills','money_market_commercial_paper','certificates_of_deposit','repurchase_agreements','short_term_municipal_notes','bankers_acceptances','commodities_gold_oil_futures','commodities_spot','commodities_futures','derivatives_options','derivatives_futures','derivatives_swaps','real_estate_direct_property','real_estate_reits','mortgage_backed_securities','property_development_loans','private_equity','equity_stakes_private_companies','equity_stakes_infrastructure_assets','mezzanine_financing','convertible_preferred_stock','leveraged_buyout_debt','distressed_debt','project_finance_debt','infrastructure_bonds','ppp_investments','infrastructure_debt_equity','infrastructure_projects','alternative_assets_hedge_funds','alternative_assets_commodities'
        ]

        # Update logic
        if instrument_id:
            if instrument_id not in instruments:
                return json.dumps({
                    "success": False,
                    "error": f"Instrument {instrument_id} not found"
                })

            # Fund Manager approval always required for updates
            if not fund_manager_approval:
                return json.dumps({
                    "success": False,
                    "error": "Fund Manager approval is required for instrument updates"
                })

            instrument = instruments[instrument_id]
            critical_change = False
            
            # Check if this is a critical change (ticker or instrument_type)
            if ticker is not None and instrument.get('ticker') != ticker:
                critical_change = True
            if instrument_type is not None and instrument.get('instrument_type') != instrument_type:
                critical_change = True
            
            # Compliance Officer approval required for critical changes
            if critical_change and not compliance_officer_approval:
                return json.dumps({
                    "success": False,
                    "error": "Compliance Officer approval is required for ticker or instrument type changes"
                })

            # Validate and update ticker if provided
            if ticker is not None:
                if not ticker.strip():
                    return json.dumps({
                        "success": False,
                        "error": "Ticker cannot be empty"
                    })
                
                # Check for ticker uniqueness if it's being changed
                if instrument.get('ticker') != ticker:
                    for inst_id, inst_data in instruments.items():
                        if inst_id != instrument_id and inst_data.get('ticker') == ticker:
                            return json.dumps({
                                "success": False,
                                "error": f"Ticker '{ticker}' already exists for another instrument."
                            })
                
                instrument['ticker'] = ticker

            # Validate and update name if provided
            if name is not None:
                if not name.strip():
                    return json.dumps({
                        "success": False,
                        "error": "Name cannot be empty"
                    })
                instrument['name'] = name

            # Validate and update instrument_type if provided
            if instrument_type is not None:
                if instrument_type not in valid_instrument_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid instrument_type '{instrument_type}' provided."
                    })
                instrument['instrument_type'] = instrument_type

            # Validate and update status if provided
            if status is not None:
                if status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of {valid_statuses}"
                    })
                instrument['status'] = status

            instrument['updated_at'] = "2025-10-01T00:00:00"
            return json.dumps(instrument)

        # Create logic
        else:
            # For creation, both approvals are required
            if not fund_manager_approval:
                return json.dumps({
                    "success": False,
                    "error": "Fund Manager approval is required for instrument creation"
                })
            
            if not compliance_officer_approval:
                return json.dumps({
                    "success": False,
                    "error": "Compliance Officer approval is required for instrument creation"
                })

            # All fields required for creation
            if not ticker or not ticker.strip():
                return json.dumps({
                    "success": False,
                    "error": "Ticker is required for instrument creation"
                })
            
            if not name or not name.strip():
                return json.dumps({
                    "success": False,
                    "error": "Name is required for instrument creation"
                })

            if not instrument_type:
                return json.dumps({
                    "success": False,
                    "error": "Instrument type is required for instrument creation"
                })

            if instrument_type not in valid_instrument_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid instrument_type '{instrument_type}' provided."
                })

            if status and status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_statuses}"
                })

            # Check for ticker uniqueness
            for inst in instruments.values():
                if inst.get('ticker') == ticker:
                    return json.dumps({
                        "success": False,
                        "error": f"Ticker '{ticker}' already exists."
                    })

            new_id = str(generate_id(instruments))
            timestamp = "2025-10-01T00:00:00"
            new_instrument = {
                "instrument_id": str(new_id) if new_id is not None else None,
                "ticker": ticker,
                "name": name,
                "instrument_type": instrument_type,
                "status": status or "active",
                "created_at": timestamp,
                "updated_at": timestamp
            }
            instruments[str(new_id)] = new_instrument
            return json.dumps(new_instrument)

    @staticmethod
    def discover_reporting_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover reporting entities: reports and documents.
        
        Supported entities:
        - reports: Report records by report_id, fund_id, investor_id, report_date, report_type, generated_by, status, export_period_end
        - documents: Document records by document_id, name, format, uploaded_by, upload_date, report_id, size_bytes, confidentiality_level, status
        """
        if entity_type not in ["reports", "documents"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'reports' or 'documents'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "reports": "report_id",
            "documents": "document_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_notifications_invoke(data: Dict[str, Any], action: str, notification_data: Dict[str, Any] = None, notification_id: str = None) -> str:
        """
        Create or update notification records.
        
        Actions:
        - create: Create new notification (requires notification_data with email, type, class, optional reference_id)
        - update: Update existing notification (requires notification_id and notification_data with changes like status)
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
        
        # Access notifications data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for notifications"
            })
        
        notifications = data.get("notifications", {})
        
        if action == "create":
            if not notification_data:
                return json.dumps({
                    "success": False,
                    "error": "notification_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["email", "type", "class"]
            missing_fields = [field for field in required_fields if field not in notification_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for notification creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["email", "type", "class", "reference_id", "status"]
            invalid_fields = [field for field in notification_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for notification creation: {', '.join(invalid_fields)}"
                })
            
            # Validate enum fields
            valid_types = ["alert", "report", "reminder", "subscription_update"]
            if notification_data["type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid type. Must be one of: {', '.join(valid_types)}"
                })
            
            valid_classes = ["funds", "investors", "portfolios", "trades", "invoices", "reports", "documents", "subscriptions", "commitments"]
            if notification_data["class"] not in valid_classes:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid class. Must be one of: {', '.join(valid_classes)}"
                })
            
            # Validate type-class combinations per policy
            notification_type = notification_data["type"]
            notification_class = notification_data["class"]
            
            valid_combinations = {
                "alert": ["funds", "investors", "portfolios", "trades", "invoices", "subscriptions", "commitments"],
                "report": ["funds", "investors", "portfolios", "reports", "documents"],
                "reminder": ["invoices", "subscriptions", "commitments"],
                "subscription_update": ["subscriptions", "commitments"]
            }
            
            if notification_class not in valid_combinations[notification_type]:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid type-class combination: {notification_type} notifications are not valid for {notification_class}. Valid classes for {notification_type}: {', '.join(valid_combinations[notification_type])}"
                })
            
            # Validate status if provided
            if "status" in notification_data:
                valid_statuses = ["pending", "sent", "failed"]
                if notification_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Basic email validation
            email = notification_data["email"]
            if "@" not in email or "." not in email.split("@")[-1]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid email format"
                })
            
            new_notification_id = generate_id(notifications)
            
            # Create new notification record
            new_notification = {
                "notification_id": str(new_notification_id) if new_notification_id else None,
                "email": notification_data["email"],
                "type": notification_data["type"],
                "class": notification_data["class"],
                "reference_id": str(notification_data.get("reference_id")) if notification_data.get("reference_id") else None,
                "status": notification_data.get("status", "pending"),
                "sent_at": None,
                "created_at": "2025-10-01T12:00:00"
            }
            
            notifications[str(new_notification_id)] = new_notification
            
            return json.dumps({
                "success": True,
                "action": "create",
                "notification_id": str(new_notification_id) if new_notification_id else None,
                "message": f"Notification {new_notification_id} created successfully for {notification_data['email']}",
                "notification_data": new_notification
            })
        
        elif action == "update":
            if not notification_id:
                return json.dumps({
                    "success": False,
                    "error": "notification_id is required for update action"
                })
            
            if notification_id not in notifications:
                return json.dumps({
                    "success": False,
                    "error": f"Notification {notification_id} not found"
                })
            
            if not notification_data:
                return json.dumps({
                    "success": False,
                    "error": "notification_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["status", "sent_at"]
            invalid_fields = [field for field in notification_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for notification update: {', '.join(invalid_fields)}. Cannot update email, type, class, or reference_id."
                })
            
            if "status" in notification_data:
                valid_statuses = ["pending", "sent", "failed"]
                if notification_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            current_notification = notifications[notification_id]
            current_status = current_notification.get("status", "pending")
            new_status = notification_data.get("status")
            
            if new_status and current_status == "sent" and new_status in ["pending", "failed"]:
                return json.dumps({
                    "success": False,
                    "error": "Cannot change status from 'sent' to 'pending' or 'failed'"
                })
            
            if new_status == "sent" and current_status != "sent":
                notification_data["sent_at"] = "2025-10-01T12:00:00"
            
            updated_notification = current_notification.copy()
            for key, value in notification_data.items():
                updated_notification[key] = value
            
            notifications[notification_id] = updated_notification
            
            return json.dumps({
                "success": True,
                "action": "update",
                "notification_id": str(notification_id),
                "message": f"Notification {notification_id} updated successfully",
                "notification_data": updated_notification
            })

    @staticmethod
    def fulfill_commitment_invoke(data: Dict[str, Any], commitment_id: str, compliance_officer_approval: bool = False) -> str:
        
        commitments = data.get("commitments", {})
        
        # Validate required approvals first
        if not compliance_officer_approval:
            return json.dumps({
                "success": False,
                "error": "Compliance Officer approval is required for commitment fulfillment"
            })
        
        # Validate commitment exists
        if str(commitment_id) not in commitments:
            return json.dumps({"error": f"Commitment {commitment_id} not found"})
        
        commitment = commitments[str(commitment_id)]
        
        # Check if already fulfilled
        if commitment.get("status") == "fulfilled":
            return json.dumps({"error": "Commitment is already fulfilled"})
        
        # Update commitment status
        timestamp = "2025-10-01T00:00:00"
        commitment["status"] = "fulfilled"
        commitment["updated_at"] = timestamp
        
        return json.dumps(commitment)

    @staticmethod
    def offboard_investor_invoke(data: Dict[str, Any], investor_id: str, 
               compliance_officer_approval: bool, reason: str = None) -> str:
        # Access investors data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for investors"
            })
        
        investors = data.get("investors", {})
        
        # Validate required approval first
        if not compliance_officer_approval:
            return json.dumps({
                "success": False,
                "error": "Compliance Officer approval is required for investor offboarding"
            })
        
        # Validate required parameters
        if not investor_id:
            return json.dumps({
                "success": False,
                "error": "investor_id is required for offboarding"
            })
        
        # Check if investor exists
        if investor_id not in investors:
            return json.dumps({
                "success": False,
                "error": f"Investor {investor_id} not found"
            })
        
        investor = investors[investor_id]
        
        # Check if investor is already deactivated
        current_status = investor.get("status", "").lower()
        if current_status in ["deactivated", "inactive", "archived", "offboarded"]:
            return json.dumps({
                "success": False,
                "error": f"Investor {investor_id} is already deactivated with status: {current_status}"
            })
        
        # Validate reason if provided
        if reason is not None and not isinstance(reason, str):
            return json.dumps({
                "success": False,
                "error": "Reason must be a string if provided"
            })
        
        # Update investor record directly
        investor["status"] = "offboarded"

        # Update the investor in the data
        investors[investor_id] = investor

        return json.dumps({
            "success": True,
            "investor_id": str(investor_id) if investor_id else None,
            "message": f"Investor {investor_id} successfully offboarded",
            "investor_data": {
                "investor_id": str(investor.get("investor_id")) if investor.get("investor_id") else None,
                "name": investor.get("name"),
                "status": investor.get("status"),
                "contact_email": investor.get("contact_email"),
            }
        })

    @staticmethod
    def discover_valuation_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover valuation entities: NAV records and instrument prices.
        
        Supported entities:
        - nav_records: Net Asset Value records by nav_id, fund_id, nav_date, nav_value
        - instrument_prices: Price data by price_id, instrument_id, price_date, open_price, high_price, low_price, close_price
        """
        if entity_type not in ["nav_records", "instrument_prices"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'nav_records' or 'instrument_prices'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "nav_records": "nav_id",
            "instrument_prices": "price_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def discover_user_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover user entities.
        
        Supported entities:
        - users: User records by user_id, first_name, last_name, email, role, timezone, status
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
    def discover_instrument_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover instrument entities.
        
        Supported entities:
        - instruments: Instrument records by instrument_id, ticker, name, status, instrument_type
        """
        if entity_type not in ["instruments"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'instruments'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("instruments", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "instrument_id": str(entity_id)})
            else:
                results.append({**entity_data, "instrument_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def create_new_audit_trail_invoke(data: Dict[str, Any], reference_id: str, reference_type: str,
               action: str, field_name: Optional[str] = None,
               old_value: Optional[str] = None, new_value: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        audit_trails = data.get("audit_trails", {})        
        
        # Validate reference_type - Added instrument_price
        valid_reference_types = [
            "user", "fund", "investor", "subscription", "commitment", "redemption",
            "trade", "portfolio", "holding", "instrument", "instrument_price", "invoice", "payment",
            "document", "report", "nav", "notification"
        ]
        if reference_type not in valid_reference_types:
            raise ValueError(f"Invalid reference_type. Must be one of {valid_reference_types}")
        
        # Validate action
        valid_actions = ["create", "update", "delete", "approve", "cancel", "process"]
        if action not in valid_actions:
            raise ValueError(f"Invalid action. Must be one of {valid_actions}")
        
        # Business rule validation
        if action in ["create", "delete"] and field_name is not None:
            raise ValueError(f"field_name should be null for {action} actions")
        
        if action == "create" and old_value is not None:
            raise ValueError("old_value should be null for create actions")
        
        if action == "delete" and new_value is not None:
            raise ValueError("new_value should be null for delete actions")
        
        # Validate that the referenced entity exists based on reference_type - Added instrument_price mapping
        reference_tables = {
            "user": "users",
            "fund": "funds",
            "investor": "investors",
            "subscription": "subscriptions",
            "commitment": "commitments",
            "redemption": "redemptions",
            "trade": "trades",
            "portfolio": "portfolios",
            "holding": "portfolio_holdings",
            "instrument": "instruments",
            "instrument_price": "instrument_prices",
            "invoice": "invoices",
            "payment": "payments",
            "document": "documents",
            "report": "reports",
            "nav": "nav_records",
            "notification": "notifications"
        }
        
        reference_table = reference_tables.get(reference_type)
        if reference_table and reference_table in data:
            if str(reference_id) not in data[reference_table]:
                raise ValueError(f"{reference_type.title()} {reference_id} not found")
        
        audit_trail_id = generate_id(audit_trails)
        timestamp = "2025-10-01T00:00:00"
        
        new_audit_trail = {
            "audit_trail_id": str(audit_trail_id) if audit_trail_id is not None else None,
            "reference_id": str(reference_id) if reference_id is not None else None,
            "reference_type": reference_type,
            "action": action,
            "field_name": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "created_at": timestamp
        }
        
        audit_trails[str(audit_trail_id)] = new_audit_trail
        return json.dumps(new_audit_trail)

    @staticmethod
    def discover_investor_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover investor entities.
        
        Supported entities:
        - investors: Investor records by investor_id, name, registration_number, date_of_incorporation, country, address, tax_id, source_of_funds, status, contact_email, accreditation_status
        """
        if entity_type not in ["investors"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'investors'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("investors", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "investor_id": str(entity_id)})
            else:
                results.append({**entity_data, "investor_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def manage_subscription_invoke(data: Dict[str, Any], action: str, subscription_data: Dict[str, Any], 
           subscription_id: Optional[str] = None) -> str:
        """
        Create, update, or cancel subscription records.
        
        Actions:
        - create: Create new subscription (requires subscription_data with fund_id, investor_id, amount, request_assigned_to, request_date, fund_manager_approval, compliance_officer_approval)
        - update: Update existing subscription (requires subscription_id and subscription_data with changes, fund_manager_approval, compliance_officer_approval)
        - cancel: Cancel subscription (requires subscription_id, fund_manager_approval, compliance_officer_approval)
        """
        
        if isinstance(subscription_data, str):
            try:
                subscription_data = json.loads(subscription_data)
            except json.JSONDecodeError:
                return json.dumps({
                    "success": False,
                    "error": "Invalid JSON format in subscription_data"
                })

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def validate_date_format(date_str: str, field_name: str) -> Optional[str]:
            if date_str:
                date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                if not re.match(date_pattern, date_str):
                    return f"Invalid {field_name} format. Must be YYYY-MM-DD"
            return None
        
        def validate_boolean_field(value: Any, field_name: str) -> Optional[str]:
            if not isinstance(value, bool):
                return f"Invalid {field_name}. Must be boolean (True/False)"
            return None
        
        # Validate action
        if action not in ["create", "update", "cancel"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create', 'update', or 'cancel'"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for subscriptions"
            })
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        subscriptions = data.get("subscriptions", {})
        
        if action == "create":
            if not subscription_data:
                return json.dumps({
                    "success": False,
                    "error": "subscription_data is required for create action"
                })
            
            # Require both Fund Manager and Compliance Officer approvals
            required_fields = ["fund_id", "investor_id", "amount", "request_assigned_to", "request_date", "fund_manager_approval", "compliance_officer_approval"]
            missing_fields = [field for field in required_fields if field not in subscription_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for subscription creation: {', '.join(missing_fields)}. Both Fund Manager and Compliance Officer approvals are required."
                })
            
            # Updated allowed fields to include compliance_officer_approval
            allowed_fields = ["fund_id", "investor_id", "amount", "request_assigned_to", "request_date", "status", "approval_date", "notify_investor", "fund_manager_approval", "compliance_officer_approval"]
            invalid_fields = [field for field in subscription_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for subscription creation: {', '.join(invalid_fields)}"
                })
            
            # Extract and validate core fields
            fund_id = subscription_data["fund_id"]
            investor_id = subscription_data["investor_id"]
            amount = subscription_data["amount"]
            request_assigned_to = subscription_data["request_assigned_to"]
            request_date = subscription_data["request_date"]
            status = subscription_data.get("status", "pending")
            
            # Validate fund exists
            if str(fund_id) not in funds:
                return json.dumps({"success": False, "error": f"Fund {fund_id} not found"})
            
            # Validate investor exists
            if str(investor_id) not in investors:
                return json.dumps({"success": False, "error": f"Investor {investor_id} not found"})
            
            # Validate assigned user exists
            if str(request_assigned_to) not in users:
                return json.dumps({"success": False, "error": f"User {request_assigned_to} not found"})
            
            # Check for duplicate subscriptions
            for subscription in subscriptions.values():
                if (subscription.get("fund_id") == fund_id and 
                    subscription.get("investor_id") == investor_id):
                    return json.dumps({
                        "success": False,
                        "error": f"Subscription already exists for investor {investor_id} and fund {fund_id}."
                    })
            
            # Validate amount is positive
            try:
                if float(amount) <= 0:
                    return json.dumps({"success": False, "error": "Subscription amount must be positive"})
            except ValueError:
                return json.dumps({"success": False, "error": "Invalid amount format"})
            
            # Validate status enum
            if status not in ["pending", "approved", "cancelled"]:
                return json.dumps({"success": False, "error": "Invalid status"})
            
            # Validate date formats
            date_error = validate_date_format(request_date, "request_date")
            if date_error:
                return json.dumps({"success": False, "error": date_error})
            
            if "approval_date" in subscription_data:
                date_error = validate_date_format(subscription_data["approval_date"], "approval_date")
                if date_error:
                    return json.dumps({"success": False, "error": date_error})
            
            # Validate both approval fields
            bool_error = validate_boolean_field(subscription_data["fund_manager_approval"], "fund_manager_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            bool_error = validate_boolean_field(subscription_data["compliance_officer_approval"], "compliance_officer_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            if "notify_investor" in subscription_data:
                bool_error = validate_boolean_field(subscription_data["notify_investor"], "notify_investor")
                if bool_error:
                    return json.dumps({"success": False, "error": bool_error})
            
            # Generate new subscription ID and create record
            new_subscription_id = generate_id(subscriptions)
            new_subscription = {
                "subscription_id": str(new_subscription_id) if new_subscription_id else None, "fund_id": str(fund_id) if fund_id else None, "investor_id": str(investor_id) if investor_id else None,
                "amount": amount, "status": status, "request_assigned_to": request_assigned_to,
                "request_date": request_date, "approval_date": subscription_data.get("approval_date"),
                "updated_at": "2025-10-01T00:00:00"
            }
            subscriptions[str(new_subscription_id)] = new_subscription
            
            return json.dumps({
                "success": True, "action": "create", "subscription_id": str(new_subscription_id),
                "message": f"Subscription {new_subscription_id} created successfully.",
                "subscription_data": new_subscription
            })
        
        elif action == "update":
            if not subscription_id or subscription_id not in subscriptions:
                return json.dumps({"success": False, "error": f"Subscription {subscription_id} not found"})
            
            if not subscription_data:
                return json.dumps({"success": False, "error": "subscription_data is required for update action"})
            
            # Require both approvals for updates
            missing_approvals = []
            if "fund_manager_approval" not in subscription_data:
                missing_approvals.append("fund_manager_approval")
            if "compliance_officer_approval" not in subscription_data:
                missing_approvals.append("compliance_officer_approval")
            
            if missing_approvals:
                return json.dumps({
                    "success": False, 
                    "error": f"Missing required approvals: {', '.join(missing_approvals)}. Both Fund Manager and Compliance Officer approvals are required."
                })
            
            # Validate both approval fields
            bool_error = validate_boolean_field(subscription_data["fund_manager_approval"], "fund_manager_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            bool_error = validate_boolean_field(subscription_data["compliance_officer_approval"], "compliance_officer_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            # Update subscription record
            current_subscription = subscriptions[subscription_id]
            updated_subscription = current_subscription.copy()
            for key, value in subscription_data.items():
                if key not in ["fund_manager_approval", "compliance_officer_approval"]:
                    updated_subscription[key] = value
            
            updated_subscription["updated_at"] = "2025-10-01T00:00:00"
            subscriptions[subscription_id] = updated_subscription
            
            return json.dumps({
                "success": True, "action": "update", "subscription_id": str(subscription_id),
                "message": f"Subscription {subscription_id} updated successfully.",
                "subscription_data": updated_subscription
            })
        
        elif action == "cancel":
            if not subscription_id or subscription_id not in subscriptions:
                return json.dumps({"success": False, "error": f"Subscription {subscription_id} not found"})
            
            # Require both approvals for cancellation
            if not subscription_data:
                return json.dumps({
                    "success": False,
                    "error": "subscription_data with fund_manager_approval and compliance_officer_approval is required for cancel action"
                })
            
            missing_approvals = []
            if "fund_manager_approval" not in subscription_data:
                missing_approvals.append("fund_manager_approval")
            if "compliance_officer_approval" not in subscription_data:
                missing_approvals.append("compliance_officer_approval")
            
            if missing_approvals:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required approvals: {', '.join(missing_approvals)}. Both Fund Manager and Compliance Officer approvals are required for cancellation."
                })

            # Validate both approval fields
            bool_error = validate_boolean_field(subscription_data["fund_manager_approval"], "fund_manager_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            bool_error = validate_boolean_field(subscription_data["compliance_officer_approval"], "compliance_officer_approval")
            if bool_error:
                return json.dumps({"success": False, "error": bool_error})
            
            subscription = subscriptions[subscription_id]
            if subscription.get("status") == "cancelled":
                return json.dumps({"success": False, "error": "Subscription is already cancelled"})
            
            subscription["status"] = "cancelled"
            subscription["updated_at"] = "2025-10-01T00:00:00"
            
            return json.dumps({
                "success": True, "action": "cancel", "subscription_id": str(subscription_id),
                "message": f"Subscription {subscription_id} cancelled successfully.",
                "subscription_data": subscription
            })

    @staticmethod
    def create_commitment_invoke(data: Dict[str, Any], fund_id: str, investor_id: str, 
               commitment_amount: float, commitment_date: str, 
               status: str = "pending", compliance_officer_approval: bool = False) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})
        
        # Validate required approvals first
        if not compliance_officer_approval:
            return json.dumps({
                "success": False,
                "error": "Compliance Officer approval is required for commitment creation"
            })
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        # Validate investor exists  
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        # Validate status
        valid_statuses = ["pending", "fulfilled"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        # Check if commitment already exists for this investor-fund combination
        for commitment in commitments.values():
            if (commitment.get("fund_id") == fund_id and 
                commitment.get("investor_id") == investor_id):
                return json.dumps({"error": "An investor can have only one commitment per fund"})
        
        commitment_id = generate_id(commitments)
        timestamp = "2025-10-01T00:00:00"
        
        new_commitment = {
            "commitment_id": str(commitment_id) if commitment_id is not None else None,
            "fund_id": str(fund_id) if fund_id is not None else None,
            "investor_id": str(investor_id) if investor_id is not None else None,
            "commitment_amount": commitment_amount,
            "commitment_date": commitment_date,
            "status": status,
            "updated_at": timestamp
        }
        
        commitments[str(commitment_id)] = new_commitment
        return json.dumps(new_commitment)

    @staticmethod
    def discover_billing_entities_invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover billing entities: invoices and payments.
        
        Supported entities:
        - invoices: Invoice records by invoice_id, commitment_id, invoice_date, due_date, amount, status
        - payments: Payment records by payment_id, invoice_id, subscription_id, payment_date, amount, payment_method, status
        """
        if entity_type not in ["invoices", "payments"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'invoices' or 'payments'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        
        id_field = {
            "invoices": "invoice_id",
            "payments": "payment_id"
        }[entity_type]
        
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: entity_id})
            else:
                results.append({**entity_data, id_field: entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })

    @staticmethod
    def execute_trade_invoke(data: Dict[str, Any], fund_id: str, instrument_id: str, 
               quantity: float, side: str, trade_date: str, price: float,
               fund_manager_approval: bool) -> str:
        """
        Execute a trade for a fund after all approvals are obtained.
        
        This tool performs step 3 of the Trade Execution & Post-Trade Controls SOP.
        Prerequisites: Fund Manager approval must be verified before calling this tool.
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        instruments = data.get("instruments", {})
        trades = data.get("trades", {})
        
        # Validate required approval first
        if not fund_manager_approval:
            return json.dumps({
                "success": False,
                "error": "Fund Manager approval is required for trade execution"
            })
        
        # Validate required parameters
        if not fund_id:
            return json.dumps({
                "success": False,
                "error": "fund_id is required"
            })
        
        if not instrument_id:
            return json.dumps({
                "success": False,
                "error": "instrument_id is required"
            })
        
        if not side:
            return json.dumps({
                "success": False,
                "error": "side is required"
            })
        
        if not trade_date:
            return json.dumps({
                "success": False,
                "error": "trade_date is required"
            })
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({
                "success": False,
                "error": f"Fund {fund_id} not found"
            })
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            return json.dumps({
                "success": False,
                "error": f"Instrument {instrument_id} not found"
            })
        
        # Validate side
        valid_sides = ["buy", "sell"]
        if side.lower() not in valid_sides:
            return json.dumps({
                "success": False,
                "error": f"Invalid side. Must be one of {valid_sides}"
            })
        
        # Validate quantity
        try:
            quantity = float(quantity)
            if quantity <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Quantity must be positive"
                })
        except (ValueError, TypeError):
            return json.dumps({
                "success": False,
                "error": "Invalid quantity format"
            })
        
        # Validate price
        try:
            price = float(price)
            if price <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Price must be positive"
                })
        except (ValueError, TypeError):
            return json.dumps({
                "success": False,
                "error": "Invalid price format"
            })
        
        # Validate fund status is open
        fund = funds[str(fund_id)]
        if fund.get("status", "").lower() != "open":
            return json.dumps({
                "success": False,
                "error": f"Fund {fund_id} is not open for trading"
            })
        
        # Validate instrument status is active
        instrument = instruments[str(instrument_id)]
        if instrument.get("status", "").lower() != "active":
            return json.dumps({
                "success": False,
                "error": f"Instrument {instrument_id} is not active for trading"
            })
        
        # Execute the trade
        trade_id = generate_id(trades)
        timestamp = "2025-10-01T00:00:00"
        
        new_trade = {
            "trade_id": str(trade_id),
            "fund_id": str(fund_id),
            "instrument_id": str(instrument_id),
            "trade_date": trade_date,
            "quantity": quantity,
            "price": price,
            "side": side.lower(),
            "status": "executed",
            "created_at": timestamp
        }
        
        trades[str(trade_id)] = new_trade
        
        return json.dumps({
            "success": True,
            "trade_id": str(trade_id) if trade_id is not None else None,
            "message": f"Trade {trade_id} executed successfully",
            "trade_data": {
                "trade_id": str(new_trade["trade_id"]) if new_trade["trade_id"] is not None else None,
                "fund_id": str(new_trade["fund_id"]) if new_trade["fund_id"] is not None else None,
                "instrument_id": str(new_trade["instrument_id"]) if new_trade["instrument_id"] is not None else None,
                "quantity": new_trade["quantity"],
                "price": new_trade["price"],
                "side": new_trade["side"],
                "status": new_trade["status"],
                "trade_date": new_trade["trade_date"],
                "created_at": new_trade["created_at"]
            }
        })

