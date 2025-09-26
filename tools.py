from datetime import datetime
from datetime import datetime, timezone
from typing import Any, Dict
from typing import Any, Dict, List, Optional
from typing import Any, Dict, Optional
from typing import Any, Dict, Optional, List
import json
import re

class Tools:
    @staticmethod
    def query_rollback_requests_invoke(
        data: Dict[str, Any],
        rollback_id: str = None,
        change_id: str = None,
        incident_id: str = None,
        requested_by_id: str = None,
        status: str = None,
        executed_since: str = None
    ) -> str:
        try:
            # Helper inside query_rollback_requests_invoke per requirement
            def parse_iso(ts: Optional[str]) -> Optional[datetime]:
                if not ts:
                    return None
                ts_local = ts.replace("Z", "+00:00")
                return datetime.fromisoformat(ts_local)

            rollbacks: Dict[str, Any] = data.get("rollback_requests", {})
            results: List[Dict[str, Any]] = []

            since_dt = parse_iso(executed_since) if executed_since else None

            for rb in rollbacks.values():
                if rollback_id and rb.get("rollback_id") != rollback_id:
                    continue
                if change_id and rb.get("change_id") != change_id:
                    continue
                if incident_id and rb.get("incident_id") != incident_id:
                    continue
                if requested_by_id and rb.get("requested_by_id") != requested_by_id:
                    continue
                if status and rb.get("status") != status:
                    continue

                if since_dt:
                    ex = rb.get("executed_at")
                    if not ex:
                        continue
                    try:
                        ex_dt = parse_iso(ex)
                        if ex_dt is None or ex_dt < since_dt:
                            continue
                    except Exception:
                        continue

                results.append(rb)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def edit_rollback_request_invoke(
        data: Dict[str, Any],
        rollback_id: str,
        change_id: str = None,
        incident_id: str = None,
        requested_by_id: str = None,
        approved_by_id: str = None,
        executed_at: str = None,
        validation_completed: bool = None,
        status: str = None            # requested|approved|in_progress|completed|failed
    ) -> str:
        try:
            # Helper inside edit_rollback_request_invoke per requirement
            def is_iso(ts: str) -> bool:
                try:
                    datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    return True
                except Exception:
                    return False

            rolls = data.get("rollback_requests", {})
            if rollback_id not in rolls:
                return json.dumps({"success": False, "error": f"Rollback request {rollback_id} not found"})

            valid_status = {"requested","approved","in_progress","completed","failed"}
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
            if executed_at is not None and not is_iso(executed_at):
                return json.dumps({"success": False, "error": "executed_at must be ISO timestamp"})

            r = rolls[rollback_id]
            if change_id is not None: r["change_id"] = change_id
            if incident_id is not None: r["incident_id"] = incident_id
            if requested_by_id is not None: r["requested_by_id"] = requested_by_id
            if approved_by_id is not None: r["approved_by_id"] = approved_by_id
            if executed_at is not None: r["executed_at"] = executed_at
            if validation_completed is not None: r["validation_completed"] = bool(validation_completed)
            if status is not None: r["status"] = status

            return json.dumps(r)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def edit_workaround_invoke(
        data: Dict[str, Any],
        workaround_id: str,
        incident_id: str = None,
        implemented_by_id: str = None,
        effectiveness: str = None,   # complete|partial|minimal
        status: str = None,          # active|inactive|replaced
        implemented_at: str = None
    ) -> str:
        try:
            # Helper inside edit_workaround_invoke per requirement
            def is_iso(ts: str) -> bool:
                try:
                    datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    return True
                except Exception:
                    return False

            wars = data.get("workarounds", {})
            if workaround_id not in wars:
                return json.dumps({"success": False, "error": f"Workaround {workaround_id} not found"})

            valid_eff = {"complete","partial","minimal"}
            valid_status = {"active","inactive","replaced"}

            if effectiveness and effectiveness not in valid_eff:
                return json.dumps({"success": False, "error": f"Invalid effectiveness. Must be one of {sorted(valid_eff)}"})
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
            if implemented_at is not None and not is_iso(implemented_at):
                return json.dumps({"success": False, "error": "implemented_at must be ISO timestamp"})

            w = wars[workaround_id]
            if incident_id is not None: w["incident_id"] = incident_id
            if implemented_by_id is not None: w["implemented_by_id"] = implemented_by_id
            if effectiveness is not None: w["effectiveness"] = effectiveness
            if status is not None: w["status"] = status
            if implemented_at is not None: w["implemented_at"] = implemented_at

            return json.dumps(w)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def record_change_request_invoke(
        data: Dict[str, Any],
        title: str,
        change_type: str,
        risk_level: str,
        requested_by_id: str,
        incident_id: str = None,
        approved_by_id: str = None,
        scheduled_start: str = None,
        scheduled_end: str = None
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            changes = data.setdefault("change_requests", {})

            valid_types = {"emergency","standard","normal"}
            if change_type not in valid_types:
                return json.dumps({"success": False, "error": f"Invalid change_type. Must be one of {sorted(valid_types)}"})

            valid_risk = {"high","medium","low"}
            if risk_level not in valid_risk:
                return json.dumps({"success": False, "error": f"Invalid risk_level. Must be one of {sorted(valid_risk)}"})

            change_id = generate_id(changes)
            timestamp = "2025-09-02T23:59:59"

            new_change = {
                "change_id": change_id,
                "incident_id": incident_id,
                "title": title,
                "change_type": change_type,
                "requested_by_id": requested_by_id,
                "approved_by_id": approved_by_id,
                "risk_level": risk_level,
                "scheduled_start": scheduled_start,
                "scheduled_end": scheduled_end,
                "actual_start": None,
                "actual_end": None,
                "status": "requested",
                "created_at": timestamp,
                "updated_at": timestamp  # same as created_at on insert
            }

            changes[change_id] = new_change
            return json.dumps({"change_id": change_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def query_users_invoke(
        data: Dict[str, Any],
        user_id: str = None,
        email: str = None,
        role: str = None,
        department: str = None,
        client_id: str = None,
        vendor_id: str = None,
        status: str = None,
        first_name: str = None,
        last_name: str = None,
    ) -> str:
        users = data.get("users", {})
        results = []

        valid_roles = {"incident_manager","technical_support","account_manager","executive","vendor_contact","system_administrator","client_contact"}
        valid_status = {"active","inactive","on_leave"}
        if role and role not in valid_roles:
            return json.dumps({"error": f"Invalid role. Must be one of {sorted(valid_roles)}"})
        if status and status not in valid_status:
            return json.dumps({"error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        for u in users.values():
            if user_id and u.get("user_id") != user_id:
                continue
            if email and u.get("email") != email:
                continue
            if role and u.get("role") != role:
                continue
            if department and u.get("department") != department:
                continue
            if client_id and u.get("client_id") != client_id:
                continue
            if vendor_id and u.get("vendor_id") != vendor_id:
                continue
            if status and u.get("status") != status:
                continue
            if first_name and u.get("first_name") != first_name:
                continue
            if last_name and u.get("last_name") != last_name:
                continue
            results.append(u)

        return json.dumps(results)

    @staticmethod
    def record_communication_invoke(
        data: Dict[str, Any],
        incident_id: str,
        sender_id: str,
        recipient_type: str,
        communication_type: str,
        recipient_id: str = None,
        delivery_status: str = "sent"
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            communications = data.setdefault("communications", {})

            valid_recipient_types = {"client","internal_team","executive","vendor","regulatory"}
            if recipient_type not in valid_recipient_types:
                return json.dumps({"success": False, "error": f"Invalid recipient_type. Must be one of {sorted(valid_recipient_types)}"})

            valid_comm_types = {"email","sms","phone_call","status_page","portal_update"}
            if communication_type not in valid_comm_types:
                return json.dumps({"success": False, "error": f"Invalid communication_type. Must be one of {sorted(valid_comm_types)}"})

            valid_delivery = {"sent","delivered","failed","pending"}
            if delivery_status not in valid_delivery:
                return json.dumps({"success": False, "error": f"Invalid delivery_status. Must be one of {sorted(valid_delivery)}"})

            communication_id = generate_id(communications)
            timestamp = "2025-09-02T23:59:59"

            new_comm = {
                "communication_id": communication_id,
                "incident_id": incident_id,
                "sender_id": sender_id,
                "recipient_id": recipient_id,
                "recipient_type": recipient_type,
                "communication_type": communication_type,
                "sent_at": timestamp,           # NOW surrogate
                "delivery_status": delivery_status,
                "created_at": timestamp
            }

            communications[communication_id] = new_comm
            return json.dumps({"communication_id": communication_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def edit_change_request_invoke(
        data: Dict[str, Any],
        change_id: str,
        incident_id: str = None,
        title: str = None,
        change_type: str = None,     # emergency|standard|normal
        requested_by_id: str = None,
        approved_by_id: str = None,
        risk_level: str = None,      # high|medium|low
        scheduled_start: str = None,
        scheduled_end: str = None,
        actual_start: str = None,
        actual_end: str = None,
        status: str = None           # requested|approved|scheduled|in_progress|completed|failed|rolled_back
    ) -> str:
        try:
            # Helper inside edit_change_request_invoke per requirement
            def is_iso(ts: str) -> bool:
                try:
                    datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    return True
                except Exception:
                    return False

            changes = data.get("change_requests", {})
            if change_id not in changes:
                return json.dumps({"success": False, "error": f"Change request {change_id} not found"})

            valid_change_type = {"emergency","standard","normal"}
            valid_risk = {"high","medium","low"}
            valid_status = {"requested","approved","scheduled","in_progress","completed","failed","rolled_back"}

            if change_type and change_type not in valid_change_type:
                return json.dumps({"success": False, "error": f"Invalid change_type. Must be one of {sorted(valid_change_type)}"})
            if risk_level and risk_level not in valid_risk:
                return json.dumps({"success": False, "error": f"Invalid risk_level. Must be one of {sorted(valid_risk)}"})
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            for ts in [scheduled_start, scheduled_end, actual_start, actual_end]:
                if ts is not None and not is_iso(ts):
                    return json.dumps({"success": False, "error": "All timestamp fields must be ISO format"})

            c = changes[change_id]
            if incident_id is not None: c["incident_id"] = incident_id
            if title is not None: c["title"] = title
            if change_type is not None: c["change_type"] = change_type
            if requested_by_id is not None: c["requested_by_id"] = requested_by_id
            if approved_by_id is not None: c["approved_by_id"] = approved_by_id
            if risk_level is not None: c["risk_level"] = risk_level
            if scheduled_start is not None: c["scheduled_start"] = scheduled_start
            if scheduled_end is not None: c["scheduled_end"] = scheduled_end
            if actual_start is not None: c["actual_start"] = actual_start
            if actual_end is not None: c["actual_end"] = actual_end
            if status is not None: c["status"] = status

            return json.dumps(c)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def query_components_invoke(
        data: Dict[str, Any],
        component_id: str = None,
        product_id: str = None,
        component_name: str = None,
        component_name_contains: str = None,
        component_type: str = None,
        environment: str = None,
        status: str = None,
        location: str = None
    ) -> str:
        components = data.get("infrastructure_components", {})
        results = []

        for comp in components.values():
            if component_id and comp.get("component_id") != component_id:
                continue
            if product_id and comp.get("product_id") != product_id:
                continue
            if component_name and comp.get("component_name") != component_name:
                continue
            if component_name_contains and component_name_contains.lower() not in (comp.get("component_name","").lower()):
                continue
            if component_type and comp.get("component_type") != component_type:
                continue
            if environment and comp.get("environment") != environment:
                continue
            if status and comp.get("status") != status:
                continue
            if location and comp.get("location") != location:
                continue
            results.append(comp)

        return json.dumps(results)

    @staticmethod
    def edit_incident_invoke(
        data: Dict[str, Any],
        incident_id: str,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        assigned_manager_id: Optional[str] = None,
        component_id: Optional[str] = None,
        category: Optional[str] = None,
        impact: Optional[str] = None,
        urgency: Optional[str] = None
    ) -> str:
        incidents = data.setdefault("incidents", {})
        # Ensure a dict exists for the target key without validating presence
        incident = incidents.setdefault(incident_id, {"incident_id": incident_id})

        valid_status = {"open","in_progress","resolved","closed"}
        valid_sev = {"P1","P2","P3","P4"}
        valid_level = {"critical","high","medium","low"}

        # Enum checks only
        if status is not None and status not in valid_status:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
        if severity is not None and severity not in valid_sev:
            return json.dumps({"success": False, "error": f"Invalid severity. Must be one of {sorted(valid_sev)}"})
        if impact is not None and impact not in valid_level:
            return json.dumps({"success": False, "error": f"Invalid impact. Must be one of {sorted(valid_level)}"})
        if urgency is not None and urgency not in valid_level:
            return json.dumps({"success": False, "error": f"Invalid urgency. Must be one of {sorted(valid_level)}"})

        ts = "2025-09-02T23:59:59"

        # Apply changes (no audit rows here)
        if status is not None:
            prev = incident.get("status")
            incident["status"] = status
            # Lifecycle timestamps on transitions (if not already present)
            if status == "resolved" and not incident.get("resolved_at"):
                incident["resolved_at"] = ts
            if status == "closed" and not incident.get("closed_at"):
                incident["closed_at"] = ts

        if severity is not None:
            incident["severity"] = severity

        if assigned_manager_id is not None:
            incident["assigned_manager_id"] = assigned_manager_id

        if component_id is not None:
            incident["component_id"] = component_id

        if category is not None:
            incident["category"] = category

        if impact is not None:
            incident["impact"] = impact

        if urgency is not None:
            incident["urgency"] = urgency

        incident["updated_at"] = ts
        return json.dumps({"success": True, "data": incident})

    @staticmethod
    def query_client_subscriptions_invoke(
        data: Dict[str, Any],
        subscription_id: str = None,
        client_id: str = None,
        product_id: str = None,
        subscription_type: str = None,
        sla_tier: str = None,
        status: str = None,
        start_date_from: str = None,  # YYYY-MM-DD
        start_date_to: str = None     # YYYY-MM-DD
    ) -> str:
        subs = data.get("client_subscriptions", {})
        results = []

        # Local, strict YYYY-MM-DD parser (no ISO datetimes)
        def parse_ymd(s: str):
            try:
                return datetime.strptime(s.strip(), "%Y-%m-%d").date()
            except Exception:
                raise ValueError(f"Expected YYYY-MM-DD, got {s!r}")

        # Pre-parse bounds (strict format)
        try:
            start_from = parse_ymd(start_date_from) if start_date_from else None
            start_to   = parse_ymd(start_date_to) if start_date_to else None
        except ValueError as e:
            return json.dumps({"error": str(e)})

        if start_from and start_to and start_from > start_to:
            return json.dumps({"error": "start_date_from must be <= start_date_to"})

        for sub in subs.values():
            if subscription_id and sub.get("subscription_id") != subscription_id:
                continue
            if client_id and sub.get("client_id") != client_id:
                continue
            if product_id and sub.get("product_id") != product_id:
                continue
            if subscription_type and sub.get("subscription_type") != subscription_type:
                continue
            if sla_tier and sub.get("sla_tier") != sla_tier:
                continue
            if status and sub.get("status") != status:
                continue

            # Apply start_date range if provided (inclusive)
            if start_from or start_to:
                sub_start_str = sub.get("start_date")
                if not isinstance(sub_start_str, str):
                    continue
                try:
                    sub_start = parse_ymd(sub_start_str)
                except ValueError:
                    # Skip malformed start_date entries
                    continue
                if start_from and sub_start < start_from:
                    continue
                if start_to and sub_start > start_to:
                    continue

            results.append(sub)

        return json.dumps(results)

    @staticmethod
    def query_knowledge_base_articles_invoke(
        data: Dict[str, Any],
        article_id: str = None,
        incident_id: str = None,
        created_by_id: str = None,
        reviewed_by_id: str = None,
        article_type: str = None,   # troubleshooting|resolution_steps|prevention_guide|faq
        category: str = None,       # full enum string
        status: str = None,         # draft|published|archived
        title_contains: str = None
    ) -> str:
        try:
            kbs: Dict[str, Any] = data.get("knowledge_base_articles", {})
            results: List[Dict[str, Any]] = []
            needle = title_contains.lower() if title_contains else None

            for a in kbs.values():
                if article_id and a.get("article_id") != article_id:
                    continue
                if incident_id and a.get("incident_id") != incident_id:
                    continue
                if created_by_id and a.get("created_by_id") != created_by_id:
                    continue
                if reviewed_by_id and a.get("reviewed_by_id") != reviewed_by_id:
                    continue
                if article_type and a.get("article_type") != article_type:
                    continue
                if category and a.get("category") != category:
                    continue
                if status and a.get("status") != status:
                    continue
                if needle and needle not in (a.get("title","").lower()):
                    continue
                results.append(a)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def query_incident_reports_invoke(
        data: Dict[str, Any],
        report_id: str = None,
        incident_id: str = None,
        report_type: str = None,   # executive_summary|technical_details|business_impact|compliance_report|post_mortem
        status: str = None,        # draft|completed|distributed
        generated_since: str = None
    ) -> str:
        try:
            # Helper inside query_incident_reports_invoke per requirement
            def parse_iso(ts: Optional[str]) -> Optional[datetime]:
                if not ts:
                    return None
                ts_local = ts.replace("Z", "+00:00")
                return datetime.fromisoformat(ts_local)

            reports: Dict[str, Any] = data.get("incident_reports", {})
            results: List[Dict[str, Any]] = []
            since_dt = parse_iso(generated_since) if generated_since else None

            for r in reports.values():
                if report_id and r.get("report_id") != report_id:
                    continue
                if incident_id and r.get("incident_id") != incident_id:
                    continue
                if report_type and r.get("report_type") != report_type:
                    continue
                if status and r.get("status") != status:
                    continue

                if since_dt:
                    ga = r.get("generated_at")
                    if not ga:
                        continue
                    try:
                        ga_dt = parse_iso(ga)
                        if ga_dt is None or ga_dt < since_dt:
                            continue
                    except Exception:
                        continue

                results.append(r)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def query_sla_agreements_invoke(
        data: Dict[str, Any],
        sla_id: str = None,
        subscription_id: str = None,
        severity_level: str = None
    ) -> str:
        slas = data.get("sla_agreements", {})
        results = []

        for sla in slas.values():
            if sla_id and sla.get("sla_id") != sla_id:
                continue
            if subscription_id and sla.get("subscription_id") != subscription_id:
                continue
            if severity_level and sla.get("severity_level") != severity_level:
                continue
            results.append(sla)

        return json.dumps(results)

    @staticmethod
    def query_vendors_invoke(
        data: Dict[str, Any],
        vendor_id: str = None,
        vendor_name: str = None,
        vendor_name_contains: str = None,
        vendor_type: str = None,
        status: str = None,
        contact_email: str = None,   # new: case-insensitive exact match
        contact_phone: str = None,   # new: digits-only, suffix match
    ) -> str:
        vendors = data.get("vendors", {})
        results = []

        valid_types = {"cloud_provider","payment_processor","software_vendor","infrastructure_provider","security_vendor"}
        valid_status = {"active","inactive","suspended"}
        if vendor_type and vendor_type not in valid_types:
            return json.dumps({"success": False, "error": f"Invalid vendor_type. Must be one of {sorted(valid_types)}"})
        if status and status not in valid_status:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        def normalize_phone(p) -> str:
            if p is None:
                return ""
            return re.sub(r"\D", "", str(p))

        target_phone = normalize_phone(contact_phone)
        target_email = contact_email.lower() if contact_email is not None else None

        for v in vendors.values():
            if vendor_id and v.get("vendor_id") != vendor_id:
                continue
            if vendor_name and v.get("vendor_name") != vendor_name:
                continue
            if vendor_type and v.get("vendor_type") != vendor_type:
                continue
            if status and v.get("status") != status:
                continue
            if vendor_name_contains:
                vn = v.get("vendor_name", "")
                if not isinstance(vn, str) or vendor_name_contains.lower() not in vn.lower():
                    continue
            if target_email:
                v_email = (v.get("contact_email") or "").lower()
                if v_email != target_email:
                    continue
            if target_phone:
                # Support both "contact_phone" and generic "phone" fields
                v_phone = normalize_phone(v.get("contact_phone") or v.get("phone"))
                if not v_phone.endswith(target_phone):
                    continue

            results.append(v)

        return json.dumps(results)

    @staticmethod
    def query_clients_invoke(
        data: Dict[str, Any],
        client_id: str = None,
        registration_number: str = None,
        contact_email: str = None,
        client_name_contains: str = None,
        client_type: str = None,
        status: str = None,
    ) -> str:
        clients = data.get("clients", {})
        results = []

        # Validate enums if provided
        valid_types = {"enterprise", "mid_market", "small_business", "startup"}
        valid_status = {"active", "inactive", "suspended"}
        if client_type and client_type not in valid_types:
            return json.dumps({"error": f"Invalid client_type. Must be one of {sorted(valid_types)}"})
        if status and status not in valid_status:
            return json.dumps({"error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        for c in clients.values():
            if client_id and c.get("client_id") != client_id:
                continue
            if registration_number and c.get("registration_number") != registration_number:
                continue
            if contact_email and c.get("contact_email") != contact_email:
                continue
            if client_type and c.get("client_type") != client_type:
                continue
            if status and c.get("status") != status:
                continue
            if client_name_contains:
                if not isinstance(c.get("client_name", ""), str):
                    continue
                if client_name_contains.lower() not in c.get("client_name", "").lower():
                    continue
            results.append(c)

        return json.dumps(results)

    @staticmethod
    def record_root_cause_analysis_invoke(
        data: Dict[str, Any],
        incident_id: str,
        conducted_by_id: str,
        analysis_method: str,
        status: str = "in_progress"
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            rcas = data.setdefault("root_cause_analysis", {})

            valid_methods = {"five_whys","fishbone","timeline_analysis","fault_tree"}
            if analysis_method not in valid_methods:
                return json.dumps({"success": False, "error": f"Invalid analysis_method. Must be one of {sorted(valid_methods)}"})

            valid_status = {"in_progress","completed","approved"}
            if status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            rca_id = generate_id(rcas)
            timestamp = "2025-09-02T23:59:59"

            new_rca = {
                "rca_id": rca_id,
                "incident_id": incident_id,
                "analysis_method": analysis_method,
                "conducted_by_id": conducted_by_id,
                "completed_at": None,
                "status": status,
                "created_at": timestamp
            }

            rcas[rca_id] = new_rca
            return json.dumps({"rca_id": rca_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def query_products_invoke(
        data: Dict[str, Any],
        product_id: str = None,
        product_name: str = None,
        product_name_contains: str = None,
        product_type: str = None,
        vendor_support_id: str = None,
        status: str = None,
        internal_team_lead_id: str = None,  # new
    ) -> str:
        products = data.get("products", {})
        results = []

        for prod in products.values():
            if product_id and prod.get("product_id") != product_id:
                continue
            if product_name and prod.get("product_name") != product_name:
                continue
            if product_name_contains and product_name_contains.lower() not in (prod.get("product_name", "").lower()):
                continue
            if product_type and prod.get("product_type") != product_type:
                continue
            if vendor_support_id and prod.get("vendor_support_id") != vendor_support_id:
                continue
            if status and prod.get("status") != status:
                continue
            if internal_team_lead_id and prod.get("internal_team_lead_id") != internal_team_lead_id:
                continue
            results.append(prod)

        return json.dumps(results)

    @staticmethod
    def record_rollback_request_invoke(
        data: Dict[str, Any],
        change_id: str,
        requested_by_id: str,
        incident_id: str = None,
        status: str = "requested"
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            rollbacks = data.setdefault("rollback_requests", {})

            valid_status = {"requested","approved","in_progress","completed","failed"}
            if status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            rollback_id = generate_id(rollbacks)
            timestamp = "2025-09-02T23:59:59"

            new_rb = {
                "rollback_id": rollback_id,
                "change_id": change_id,
                "incident_id": incident_id,
                "requested_by_id": requested_by_id,
                "approved_by_id": None,
                "executed_at": None,
                "validation_completed": False,
                "status": status,
                "created_at": timestamp
            }

            rollbacks[rollback_id] = new_rb
            return json.dumps({"rollback_id": rollback_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def record_workaround_invoke(
        data: Dict[str, Any],
        incident_id: str,
        implemented_by_id: str,
        effectiveness: str,                          # complete|partial|minimal
        status: str = "active",                      # active|inactive|replaced
        implemented_at: Optional[str] = None,        # optional, if omitted we set to ts
    ) -> str:
        workarounds = data.setdefault("workarounds", {})

        valid_eff = {"complete", "partial", "minimal"}
        valid_status = {"active", "inactive", "replaced"}
        if effectiveness not in valid_eff:
            return json.dumps({"success": False, "error": f"Invalid effectiveness. Must be one of {sorted(valid_eff)}"})
        if status not in valid_status:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] + [0]) + 1)

        workaround_id = generate_id(workarounds)
        ts = "2025-09-02T23:59:59"

        new_workaround = {
            "workaround_id": workaround_id,
            "incident_id": incident_id,
            "implemented_by_id": implemented_by_id,
            "effectiveness": effectiveness,
            "status": status,
            "implemented_at": implemented_at or ts,
            "created_at": ts,
        }

        workarounds[workaround_id] = new_workaround
        return json.dumps({"workaround_id": workaround_id, "success": True})

    @staticmethod
    def edit_root_cause_analysis_invoke(
        data: Dict[str, Any],
        rca_id: str,
        incident_id: str = None,
        analysis_method: str = None,   # five_whys|fishbone|timeline_analysis|fault_tree
        conducted_by_id: str = None,
        completed_at: str = None,
        status: str = None             # in_progress|completed|approved
    ) -> str:
        try:
            # Helper kept inside edit_root_cause_analysis_invoke per requirement
            def is_iso(ts: str) -> bool:
                try:
                    datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    return True
                except Exception:
                    return False

            rcas = data.get("root_cause_analysis", {})
            if rca_id not in rcas:
                return json.dumps({"success": False, "error": f"RCA {rca_id} not found"})

            valid_methods = {"five_whys","fishbone","timeline_analysis","fault_tree"}
            valid_status = {"in_progress","completed","approved"}

            if analysis_method and analysis_method not in valid_methods:
                return json.dumps({"success": False, "error": f"Invalid analysis_method. Must be one of {sorted(valid_methods)}"})
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
            if completed_at is not None and not is_iso(completed_at):
                return json.dumps({"success": False, "error": "completed_at must be ISO timestamp"})

            r = rcas[rca_id]
            if incident_id is not None: r["incident_id"] = incident_id
            if analysis_method is not None: r["analysis_method"] = analysis_method
            if conducted_by_id is not None: r["conducted_by_id"] = conducted_by_id
            if completed_at is not None: r["completed_at"] = completed_at
            if status is not None: r["status"] = status

            return json.dumps(r)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def edit_communication_invoke(
        data: Dict[str, Any],
        communication_id: str,
        incident_id: str = None,
        sender_id: str = None,
        recipient_id: str = None,
        recipient_type: str = None,     # client|internal_team|executive|vendor|regulatory
        communication_type: str = None, # email|sms|phone_call|status_page|portal_update
        sent_at: str = None,
        delivery_status: str = None     # sent|delivered|failed|pending
    ) -> str:
        try:
            # Helper inside edit_communication_invoke per requirement
            def is_iso(ts: str) -> bool:
                try:
                    datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    return True
                except Exception:
                    return False

            comms = data.get("communications", {})
            if communication_id not in comms:
                return json.dumps({"success": False, "error": f"Communication {communication_id} not found"})

            valid_recipient = {"client","internal_team","executive","vendor","regulatory"}
            valid_comm_type = {"email","sms","phone_call","status_page","portal_update"}
            valid_delivery = {"sent","delivered","failed","pending"}

            if recipient_type and recipient_type not in valid_recipient:
                return json.dumps({"success": False, "error": f"Invalid recipient_type. Must be one of {sorted(valid_recipient)}"})
            if communication_type and communication_type not in valid_comm_type:
                return json.dumps({"success": False, "error": f"Invalid communication_type. Must be one of {sorted(valid_comm_type)}"})
            if delivery_status and delivery_status not in valid_delivery:
                return json.dumps({"success": False, "error": f"Invalid delivery_status. Must be one of {sorted(valid_delivery)}"})
            if sent_at is not None and not is_iso(sent_at):
                return json.dumps({"success": False, "error": "sent_at must be ISO timestamp"})

            c = comms[communication_id]
            if incident_id is not None: c["incident_id"] = incident_id
            if sender_id is not None: c["sender_id"] = sender_id
            if recipient_id is not None: c["recipient_id"] = recipient_id
            if recipient_type is not None: c["recipient_type"] = recipient_type
            if communication_type is not None: c["communication_type"] = communication_type
            if sent_at is not None: c["sent_at"] = sent_at
            if delivery_status is not None: c["delivery_status"] = delivery_status

            # No updated_at per original behavior
            return json.dumps(c)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def query_change_requests_invoke(
        data: Dict[str, Any],
        change_id: str = None,
        incident_id: str = None,
        requested_by_id: str = None,
        change_type: str = None,
        risk_level: str = None,
        status: str = None,
        scheduled_start_from: str = None,
        scheduled_end_to: str = None
    ) -> str:
        try:
            # Helper kept inside query_change_requests_invoke per requirement
            def parse_iso(ts: Optional[str]) -> Optional[datetime]:
                if not ts:
                    return None
                ts_local = ts.replace("Z", "+00:00")
                return datetime.fromisoformat(ts_local)

            changes: Dict[str, Any] = data.get("change_requests", {})
            results: List[Dict[str, Any]] = []

            start_from_dt = parse_iso(scheduled_start_from) if scheduled_start_from else None
            end_to_dt = parse_iso(scheduled_end_to) if scheduled_end_to else None

            for cr in changes.values():
                if change_id and cr.get("change_id") != change_id:
                    continue
                if incident_id and cr.get("incident_id") != incident_id:
                    continue
                if requested_by_id and cr.get("requested_by_id") != requested_by_id:
                    continue
                if change_type and cr.get("change_type") != change_type:
                    continue
                if risk_level and cr.get("risk_level") != risk_level:
                    continue
                if status and cr.get("status") != status:
                    continue

                # time bounds
                if start_from_dt:
                    cr_start = cr.get("scheduled_start")
                    if not cr_start:
                        continue
                    try:
                        if parse_iso(cr_start) < start_from_dt:
                            continue
                    except Exception:
                        continue

                if end_to_dt:
                    cr_end = cr.get("scheduled_end")
                    if not cr_end:
                        continue
                    try:
                        if parse_iso(cr_end) > end_to_dt:
                            continue
                    except Exception:
                        continue

                results.append(cr)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def record_incident_update_record_invoke(
        data: Dict[str, Any],
        incident_id: str,
        updated_by_id: str,
        update_type: str,           # status_change|severity_change|assignment|workaround|resolution|communication
        field_name: str,            # e.g., status, severity, assigned_manager_id, note, etc.
        new_value: Optional[str] = None,
        old_value: Optional[str] = None
    ) -> str:
        # Enum checks only (per instructions)
        valid_update_types = {"status_change","severity_change","assignment","workaround","resolution","communication"}
        if update_type not in valid_update_types:
            return json.dumps({"success": False, "error": f"Invalid update_type. Must be one of {sorted(valid_update_types)}"})

        allowed_fields = {
            "status","severity","assigned_manager_id","component_id","category",
            "impact","urgency","resolved_at","closed_at","note","workaround"
        }
        if field_name not in allowed_fields:
            return json.dumps({"success": False, "error": f"Invalid field_name. Must be one of {sorted(allowed_fields)}"})

        updates = data.setdefault("incident_updates", {})

        # generate_id must be within record_incident_update_record_invoke
        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] + [0]) + 1)

        update_id = generate_id(updates)
        timestamp = "2025-09-02T23:59:59"  # fixed timestamp for create APIs

        updates[update_id] = {
            "update_id": update_id,
            "incident_id": incident_id,
            "updated_by_id": updated_by_id,
            "update_type": update_type,
            "field_name": field_name,
            "old_value": None if old_value is None else str(old_value),
            "new_value": None if new_value is None else str(new_value),
            "created_at": timestamp
        }

        return json.dumps({"success": True, "update_id": update_id})

    @staticmethod
    def query_workarounds_invoke(
        data: Dict[str, Any],
        workaround_id: str = None,
        incident_id: str = None,
        implemented_by_id: str = None,
        effectiveness: str = None,
        status: str = None,
        implemented_since: str = None
    ) -> str:
        try:
            workarounds: Dict[str, Any] = data.get("workarounds", {})
            results: List[Dict[str, Any]] = []

            # Local ISO parser -> always return UTC-aware datetime
            def parse_iso_utc(ts: Optional[str]) -> Optional[datetime]:
                if not ts:
                    return None
                s = ts.strip()
                if s.endswith("Z"):
                    s = s[:-1] + "+00:00"
                dt = datetime.fromisoformat(s)
                if dt.tzinfo is None:
                    return dt.replace(tzinfo=timezone.utc)
                return dt.astimezone(timezone.utc)

            since_dt = parse_iso_utc(implemented_since) if implemented_since else None

            for w in workarounds.values():
                if workaround_id and w.get("workaround_id") != workaround_id:
                    continue
                if incident_id and w.get("incident_id") != incident_id:
                    continue
                if implemented_by_id and w.get("implemented_by_id") != implemented_by_id:
                    continue
                if effectiveness and w.get("effectiveness") != effectiveness:
                    continue
                if status and w.get("status") != status:
                    continue

                if since_dt:
                    ts = w.get("implemented_at")
                    if not ts:
                        continue
                    try:
                        dt = parse_iso_utc(ts)
                        # inclusive lower bound: keep only dt >= since_dt
                        if dt < since_dt:
                            continue
                    except Exception:
                        continue

                results.append(w)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def query_post_incident_reviews_invoke(
        data: Dict[str, Any],
        pir_id: str = None,
        incident_id: str = None,
        facilitator_id: str = None,
        status: str = None,            # scheduled|completed|cancelled
        scheduled_from: str = None,    # ISO
        scheduled_to: str = None       # ISO
    ) -> str:
        try:
            # Helper inside query_post_incident_reviews_invoke per requirement
            def parse_iso(ts: Optional[str]) -> Optional[datetime]:
                if not ts:
                    return None
                ts_local = ts.replace("Z", "+00:00")
                return datetime.fromisoformat(ts_local)

            pirs: Dict[str, Any] = data.get("post_incident_reviews", {})
            results: List[Dict[str, Any]] = []

            from_dt = parse_iso(scheduled_from) if scheduled_from else None
            to_dt = parse_iso(scheduled_to) if scheduled_to else None

            for p in pirs.values():
                if pir_id and p.get("pir_id") != pir_id:
                    continue
                if incident_id and p.get("incident_id") != incident_id:
                    continue
                if facilitator_id and p.get("facilitator_id") != facilitator_id:
                    continue
                if status and p.get("status") != status:
                    continue

                if from_dt or to_dt:
                    sched = p.get("scheduled_date")
                    if not sched:
                        continue
                    try:
                        sched_dt = parse_iso(sched)
                        if sched_dt is None:
                            continue
                    except Exception:
                        continue
                    if from_dt and sched_dt < from_dt:
                        continue
                    if to_dt and sched_dt > to_dt:
                        continue

                results.append(p)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def record_post_incident_review_invoke(
        data: Dict[str, Any],
        incident_id: str,
        scheduled_date: str,   # ISO timestamp
        facilitator_id: str,
        status: str = "scheduled"
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            pirs = data.setdefault("post_incident_reviews", {})
            valid_status = {"scheduled","completed","cancelled"}
            if status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            pir_id = generate_id(pirs)
            timestamp = "2025-09-02T23:59:59"

            new_pir = {
                "pir_id": pir_id,
                "incident_id": incident_id,
                "scheduled_date": scheduled_date,
                "facilitator_id": facilitator_id,
                "timeline_accuracy_rating": None,
                "communication_effectiveness_rating": None,
                "technical_response_rating": None,
                "status": status,
                "created_at": timestamp
            }

            pirs[pir_id] = new_pir
            return json.dumps({"pir_id": pir_id, "status": status, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def create_incident_invoke(
        data: Dict[str, Any],
        title: str,
        category: str,
        impact: str,
        client_id: str,
        reporter_id: str,
        detected_at: str,              # required
        component_id: str = None,
        severity: str = None,
        p1_outage_no_workaround: bool = None,
        p1_wide_enterprise_or_5plus_customers: bool = None,
        p1_regulatory_safety_financial: bool = None,
        p1_high_priority_customer_or_recurrent: bool = None,
        p2_major_degradation_with_workaround: bool = None,
        p2_multi_dept_sites_or_critical_functions: bool = None,
        p2_risk_high_priority_sla_breach: bool = None,
        p3_localized_or_non_critical: bool = None,
        p3_moderate_deg_minimal_workaround: bool = None,
        urgency: str = None,
        assigned_manager_id: str = None
    ) -> str:
        # Local helper to avoid referencing the class name
        def compute_severity(
            severity_in: Optional[str],
            p1_a: Optional[bool], p1_b: Optional[bool], p1_c: Optional[bool], p1_d: Optional[bool],
            p2_a: Optional[bool], p2_b: Optional[bool], p2_c: Optional[bool],
            p3_a: Optional[bool], p3_b: Optional[bool]
        ) -> str:
            valid = {"P1","P2","P3","P4"}
            if severity_in:
                return severity_in if severity_in in valid else "__INVALID__"
            if any([p1_a, p1_b, p1_c, p1_d]): return "P1"
            if any([p2_a, p2_b, p2_c]):       return "P2"
            if any([p3_a, p3_b]):             return "P3"
            return "P4"

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            incidents = data.setdefault("incidents", {})

            # Validate impact & urgency
            valid_levels = {"critical","high","medium","low"}
            if impact not in valid_levels:
                return json.dumps({"success": False, "error": f"Invalid impact. Must be one of {sorted(valid_levels)}"})
            if urgency and urgency not in valid_levels:
                return json.dumps({"success": False, "error": f"Invalid urgency. Must be one of {sorted(valid_levels)}"})

            # Validate detected_at (non-empty string; caller ensures ISO format)
            if not detected_at or not isinstance(detected_at, str) or not detected_at.strip():
                return json.dumps({"success": False, "error": "detected_at is required and must be a non-empty ISO timestamp string"})

            # Compute severity if not provided
            sev = compute_severity(
                severity,
                p1_outage_no_workaround,
                p1_wide_enterprise_or_5plus_customers,
                p1_regulatory_safety_financial,
                p1_high_priority_customer_or_recurrent,
                p2_major_degradation_with_workaround,
                p2_multi_dept_sites_or_critical_functions,
                p2_risk_high_priority_sla_breach,
                p3_localized_or_non_critical,
                p3_moderate_deg_minimal_workaround
            )
            if sev == "__INVALID__":
                return json.dumps({"success": False, "error": "Invalid severity. Must be one of ['P1','P2','P3','P4']"})

            ts = "2025-09-02T23:59:59"
            incident_id = generate_id(incidents)

            new_incident = {
                "incident_id": incident_id,
                "title": title,
                "reporter_id": reporter_id,
                "assigned_manager_id": assigned_manager_id,
                "client_id": client_id,
                "component_id": component_id,
                "severity": sev,
                "status": "open",               # SOP: always start as open
                "impact": impact,
                "urgency": urgency if urgency else impact,
                "category": category,
                "detected_at": detected_at,
                "resolved_at": None,
                "closed_at": None,
                "rto_breach": False,
                "sla_breach": False,
                "is_recurring": False,
                "downtime_minutes": None,
                "created_at": ts,
                "updated_at": ts
            }

            incidents[incident_id] = new_incident
            return json.dumps({"incident_id": incident_id, "severity": sev, "status": "open", "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def query_root_cause_analyses_invoke(
        data: Dict[str, Any],
        rca_id: str = None,
        incident_id: str = None,
        conducted_by_id: str = None,
        analysis_method: str = None,
        status: str = None
    ) -> str:
        try:
            rcas: Dict[str, Any] = data.get("root_cause_analysis", {}) or data.get("root_cause_analyses", {}) or data.get("root_cause_analysis_records", {})
            # Normalize: prefer a single dict key
            if not rcas:
                rcas = data.get("root_cause_analysis", {})
            results: List[Dict[str, Any]] = []

            for r in rcas.values():
                if rca_id and r.get("rca_id") != rca_id:
                    continue
                if incident_id and r.get("incident_id") != incident_id:
                    continue
                if conducted_by_id and r.get("conducted_by_id") != conducted_by_id:
                    continue
                if analysis_method and r.get("analysis_method") != analysis_method:
                    continue
                if status and r.get("status") != status:
                    continue
                results.append(r)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def query_communications_invoke(
        data: Dict[str, Any],
        communication_id: str = None,
        incident_id: str = None,
        sender_id: str = None,
        recipient_id: str = None,
        recipient_type: str = None,
        communication_type: str = None,
        delivery_status: str = None,
        sent_since: str = None
    ) -> str:
        try:
            # Helper kept inside query_communications_invoke per requirement
            def parse_iso(ts: Optional[str]) -> Optional[datetime]:
                if not ts:
                    return None
                ts_local = ts.replace("Z", "+00:00")
                return datetime.fromisoformat(ts_local)

            comms: Dict[str, Any] = data.get("communications", {})
            results: List[Dict[str, Any]] = []

            since_dt = parse_iso(sent_since) if sent_since else None

            for c in comms.values():
                if communication_id and c.get("communication_id") != communication_id:
                    continue
                if incident_id and c.get("incident_id") != incident_id:
                    continue
                if sender_id and c.get("sender_id") != sender_id:
                    continue
                if recipient_id and c.get("recipient_id") != recipient_id:
                    continue
                if recipient_type and c.get("recipient_type") != recipient_type:
                    continue
                if communication_type and c.get("communication_type") != communication_type:
                    continue
                if delivery_status and c.get("delivery_status") != delivery_status:
                    continue

                if since_dt:
                    sent_at = c.get("sent_at")
                    if not sent_at:
                        continue
                    try:
                        sent_dt = parse_iso(sent_at)
                        if sent_dt is None or sent_dt < since_dt:
                            continue
                    except Exception:
                        continue

                results.append(c)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def query_incidents_invoke(
        data: Dict[str, Any],
        incident_id: str = None,
        client_id: str = None,
        reporter_id: str = None,
        assigned_manager_id: str = None,
        component_id: str = None,
        status: str = None,
        severity: str = None,
        category: str = None,
        impact: str = None,
        urgency: str = None,
        rto_breach: Optional[bool] = None,
        sla_breach: Optional[bool] = None,
        is_recurring: Optional[bool] = None,
        title_contains: str = None,
        detected_since: str = None,
        detected_until: str = None,
        resolved_since: str = None,
        resolved_until: str = None,
        closed_since: str = None,
        closed_until: str = None,
        downtime_minutes_min: Optional[int] = None,
        downtime_minutes_max: Optional[int] = None
    ) -> str:
        try:
            incidents = data.get("incidents", {})
            results = []

            # Local ISO8601 parser (handles trailing 'Z')
            def parse_iso(ts: Optional[str]) -> Optional[datetime]:
                if not ts:
                    return None
                s = ts.strip().replace("Z", "+00:00")
                return datetime.fromisoformat(s)

            # Pre-parse time bounds
            ds = parse_iso(detected_since)
            du = parse_iso(detected_until)
            rs = parse_iso(resolved_since)
            ru = parse_iso(resolved_until)
            cs = parse_iso(closed_since)
            cu = parse_iso(closed_until)

            def within_range(value_ts: Optional[str],
                             start: Optional[datetime],
                             end: Optional[datetime]) -> bool:
                if start is None and end is None:
                    return True
                if not value_ts:
                    return False
                try:
                    dt = parse_iso(value_ts)
                except Exception:
                    return False
                if start and dt < start:
                    return False
                if end and dt > end:
                    return False
                return True

            for inc in incidents.values():
                if incident_id and inc.get("incident_id") != incident_id:
                    continue
                if client_id and inc.get("client_id") != client_id:
                    continue
                if reporter_id and inc.get("reporter_id") != reporter_id:
                    continue
                if assigned_manager_id and inc.get("assigned_manager_id") != assigned_manager_id:
                    continue
                if component_id and inc.get("component_id") != component_id:
                    continue
                if status and inc.get("status") != status:
                    continue
                if severity and inc.get("severity") != severity:
                    continue
                if category and inc.get("category") != category:
                    continue
                if impact and inc.get("impact") != impact:
                    continue
                if urgency and inc.get("urgency") != urgency:
                    continue
                if rto_breach is not None and bool(inc.get("rto_breach")) != rto_breach:
                    continue
                if sla_breach is not None and bool(inc.get("sla_breach")) != sla_breach:
                    continue
                if is_recurring is not None and bool(inc.get("is_recurring")) != is_recurring:
                    continue
                if title_contains and title_contains.lower() not in (inc.get("title", "").lower()):
                    continue

                # Time filters (inclusive bounds)
                if not within_range(inc.get("detected_at"), ds, du):
                    continue
                if not within_range(inc.get("resolved_at"), rs, ru):
                    continue
                if not within_range(inc.get("closed_at"), cs, cu):
                    continue

                # Numeric ranges
                dm = inc.get("downtime_minutes")
                if downtime_minutes_min is not None and (dm is None or dm < downtime_minutes_min):
                    continue
                if downtime_minutes_max is not None and (dm is None or dm > downtime_minutes_max):
                    continue

                results.append(inc)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

