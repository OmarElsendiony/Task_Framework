from typing import Any, Dict
from typing import Any, Dict, List
import json
import uuid

class Tools:
    @staticmethod
    def upload_document_invoke(
        data: Dict[str, Any],
        user_id: str,
        worker_id: str,
        title: str,
        file_type: str,
        status: str = "pending"
    ) -> str:
        # Validate presence of user and worker (if needed)
        users = data.get("users", {})
        workers = data.get("workers", {})
        if user_id not in users:
            raise ValueError("User ID not found")
        if worker_id not in workers:
            raise ValueError("Worker ID not found")

        documents = data.setdefault("documents", {})
        document_id = str(uuid.uuid4())

        documents[document_id] = {
            "user_id": user_id,
            "worker_id": worker_id,
            "title": title,
            "file_type": file_type,
            "status": status
        }

        return json.dumps({
            "document_id": document_id,
            "user_id": user_id,
            "worker_id": worker_id,
            "title": title,
            "file_type": file_type,
            "status": status
        })

    @staticmethod
    def update_document_status_invoke(data: Dict[str, Any], document_id: str, new_status: str) -> str:
        documents = data.get("documents", {})
        if document_id not in documents:
            raise ValueError("Document not found")

        doc = documents[document_id]
        if doc.get("status") in ["archived", "deleted"]:
            raise ValueError("Document cannot be updated in its current state")

        doc["status"] = new_status
        return json.dumps({"document_id": document_id, "new_status": new_status})

    @staticmethod
    def block_suspicious_payment_invoke(data: Dict[str, Any], payment_id: str) -> str:
        payments = data.get("payments", {})
        if payment_id not in payments:
            raise ValueError("Payment not found")

        payment = payments[payment_id]
        if payment.get("status") == "failed":
            raise ValueError("Payment already marked as failed and cannot be reprocessed")

        payment["status"] = "blocked"
        return json.dumps({"payment_id": payment_id, "status": "blocked"})

    @staticmethod
    def extend_contract_period_invoke(data: Dict[str, Any], contract_id: str, new_end_date: str) -> str:
        contracts = data.get("contracts", {})
        if contract_id not in contracts:
            raise ValueError("Contract not found")

        contract = contracts[contract_id]
        if new_end_date <= contract.get("start_date"):
            raise ValueError("End date must be after start date")

        contract["end_date"] = new_end_date
        return json.dumps(contract)

    @staticmethod
    def create_payment_invoke(
        data: Dict[str, Any],
        user_id: str,
        invoice_id: str,
        amount: float,
        currency: str
    ) -> str:
        payments = data.setdefault("payments", {})
        payment_id = str(uuid.uuid4())

        payments[payment_id] = {
            "user_id": user_id,
            "invoice_id": invoice_id,
            "amount": round(amount, 2),
            "status": "pending",
            "currency": currency,
            "processed_at": None
        }

        return json.dumps({
            "payment_id": payment_id,
            **payments[payment_id]
        })

    @staticmethod
    def block_virtual_card_invoke(data: Dict[str, Any], card_id: str) -> str:
        cards = data.get("virtual_cards", {})
        if card_id not in cards:
            raise ValueError("Card not found")

        card = cards[card_id]
        if card.get("status") in ["revoked", "expired", "blocked"]:
            raise ValueError("Card cannot be blocked in current status")

        card["status"] = "blocked"
        return json.dumps({"card_id": card_id, "status": "blocked"})

    @staticmethod
    def fetch_time_summary_by_team_invoke(
        data: Dict[str, Any],
        team_id: str,
        start_date: str = None,
        end_date: str = None,
        worker_type: str = None,
        time_entry_ids: List[str] = None,
        status: str = None,
        project_code: str = None
    ) -> str:
        team_members = data.get("team_members", {})
        time_entries = data.get("time_entries", {})
        workers = data.get("workers", {})

        # Step 1: Find valid worker_ids in the team
        member_worker_ids = {
            m["worker_id"]
            for m in team_members.values()
            if m["team_id"] == team_id
        }

        # Step 2: Apply worker_type filter if specified
        if worker_type:
            member_worker_ids = {
                wid for wid in member_worker_ids
                if workers.get(wid, {}).get("worker_type") == worker_type
            }

        summary = {}
        filtered_entries = []

        def in_range(date_str: str) -> bool:
            if not date_str:
                return False
            if start_date and date_str < start_date:
                return False
            if end_date and date_str > end_date:
                return False
            return True

        for entry_id, entry in time_entries.items():
            if time_entry_ids and entry_id not in time_entry_ids:
                continue
            if entry["worker_id"] not in member_worker_ids:
                continue
            if status and entry.get("status") != status:
                continue
            if project_code and entry.get("project_code") != project_code:
                continue
            if (start_date or end_date) and not in_range(entry.get("date")):
                continue

            duration = entry.get("duration_hours", 0)
            entry_date = entry.get("date")
            summary[entry_date] = summary.get(entry_date, 0) + duration
            filtered_entries.append({"time_entry_id": entry_id, **entry})

        return json.dumps({
            "team_id": team_id,
            "summary_by_date": summary,
            "entries": filtered_entries
        })

    @staticmethod
    def get_payments_invoke(
        data: Dict[str, Any],
        payment_id: str = None,
        user_id: str = None,
        invoice_id: str = None,
        status: str = None,
        currency: str = None,
        processed_at: str = None,
        min_amount: float = None,
        max_amount: float = None
    ) -> str:
        payments = data.get("payments", {})

        def matches(pid, payment):
            if payment_id and pid != payment_id:
                return False
            if user_id and payment.get("user_id") != user_id:
                return False
            if invoice_id and payment.get("invoice_id") != invoice_id:
                return False
            if status and payment.get("status") != status:
                return False
            if currency and payment.get("currency") != currency:
                return False
            if processed_at and payment.get("processed_at") != processed_at:
                return False
            if min_amount is not None and payment.get("amount", 0) < min_amount:
                return False
            if max_amount is not None and payment.get("amount", 0) > max_amount:
                return False
            return True

        results = [
            {**payment, "payment_id": pid}
            for pid, payment in payments.items()
            if matches(pid, payment)
        ]
        return json.dumps(results)

    @staticmethod
    def retrieve_worker_contracts_with_organization_invoke(data: Dict[str, Any], worker_id: str, org_id: str) -> str:
        contracts = data.get("contracts", {})
        result = [
            c for c in contracts.values()
            if c.get("worker_id") == worker_id and c.get("organization_id") == org_id
        ]
        return json.dumps(result)

    @staticmethod
    def get_contracts_invoke(
        data: Dict[str, Any],
        contract_id: str = None,
        user_id: str = None,
        worker_id: str = None,
        status: str = None,
        currency: str = None,
        organization_id: str = None,
        rate_type: str = None,
        document_id: str = None,
        min_rate: float = None,
        max_rate: float = None,
        start_date_from: str = None,
        start_date_to: str = None,
        end_date_from: str = None,
        end_date_to: str = None
    ) -> str:
        contracts = data.get("contracts", {})

        def matches(cid, c):
            if contract_id and cid != contract_id:
                return False
            if user_id and c.get("user_id") != user_id:
                return False
            if worker_id and c.get("worker_id") != worker_id:
                return False
            if status and c.get("status") != status:
                return False
            if currency and c.get("currency") != currency:
                return False
            if organization_id and c.get("organization_id") != organization_id:
                return False
            if rate_type and c.get("rate_type") != rate_type:
                return False
            if document_id and c.get("document_id") != document_id:
                return False
            if min_rate is not None and c.get("rate", 0) < min_rate:
                return False
            if max_rate is not None and c.get("rate", 0) > max_rate:
                return False
            if start_date_from and c.get("start_date") < start_date_from:
                return False
            if start_date_to and c.get("start_date") > start_date_to:
                return False
            if end_date_from and c.get("end_date") < end_date_from:
                return False
            if end_date_to and c.get("end_date") > end_date_to:
                return False
            return True

        result = [
            {**c, "contract_id": cid}
            for cid, c in contracts.items()
            if matches(cid, c)
        ]
        return json.dumps(result)

    @staticmethod
    def get_pending_reimbursements_invoke(
        data: Dict[str, Any],
        organization_id: str,
        user_id: str = None,
        worker_id: str = None,
        currency: str = None,
        contract_id: str = None,
        submit_date: str = None,
        approve_date: str = None,
        min_amount: float = None,
        max_amount: float = None
    ) -> str:
        reimbursements = data.get("reimbursements", {})

        def matches(r):
            if r.get("status") != "submitted":
                return False
            if r.get("organization_id") != organization_id:
                return False
            if user_id and r.get("user_id") != user_id:
                return False
            if worker_id and r.get("worker_id") != worker_id:
                return False
            if currency and r.get("currency") != currency:
                return False
            if contract_id and r.get("contract_id") != contract_id:
                return False
            if submit_date and r.get("submit_date") != submit_date:
                return False
            if approve_date and r.get("approve_date") != approve_date:
                return False
            if min_amount is not None and r.get("amount", 0) < min_amount:
                return False
            if max_amount is not None and r.get("amount", 0) > max_amount:
                return False
            return True

        result = [r for r in reimbursements.values() if matches(r)]
        return json.dumps(result)

    @staticmethod
    def find_user_invoke(
        data: Dict[str, Any],
        user_id: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        role: str = None,
        status: str = None,
        locale: str = None,
        timezone: str = None
    ) -> str:
        users = data.get("users", {})
        workers = data.get("workers", {})
        results = []

        for uid, user in users.items():
            if user_id and uid != user_id:
                continue
            if email and user.get("email") != email:
                continue
            if first_name and user.get("first_name") != first_name:
                continue
            if last_name and user.get("last_name") != last_name:
                continue
            if role and user.get("role") != role:
                continue
            if status and user.get("status") != status:
                continue
            if locale and user.get("locale") != locale:
                continue
            if timezone and user.get("timezone") != timezone:
                continue

            user_workers = [
                {"worker_id": wid, **w}
                for wid, w in workers.items()
                if w.get("user_id") == uid
            ]
            results.append({"user_id": uid, **user, "workers": user_workers})

        return json.dumps(results)

    @staticmethod
    def create_new_contract_invoke(data: Dict[str, Any], worker_id: str, terms: Dict[str, Any]) -> str:
        contracts = data.setdefault("contracts", {})
        contract_id = str(uuid.uuid4())

        required_fields = ["start_date", "end_date", "rate", "rate_type", "currency"]
        for f in required_fields:
            if f not in terms:
                raise ValueError(f"Missing field in terms: {f}")
        if terms["end_date"] <= terms["start_date"]:
            raise ValueError("End date must be after start date")

        workers = data.get("workers", {})
        if worker_id not in workers:
            raise ValueError("Worker not found")

        user_id = workers[worker_id]["user_id"]
        org_id = workers[worker_id]["organization_id"]

        contracts[contract_id] = {
            "worker_id": worker_id,
            "organization_id": org_id,
            "user_id": user_id,
            "start_date": terms["start_date"],
            "end_date": terms["end_date"],
            "rate": terms["rate"],
            "rate_type": terms["rate_type"],
            "currency": terms["currency"],
            "status": "draft",
            "document_id": None
        }
        return json.dumps({"contract_id": contract_id})

    @staticmethod
    def get_payroll_run_details_invoke(data: Dict[str, Any], payroll_run_id: str) -> str:
        runs = data.get("payroll_runs", {})
        if payroll_run_id not in runs:
            raise ValueError("Payroll run not found")

        if runs[payroll_run_id]["status"] != "confirmed":
            raise ValueError("Payroll run is not in a confirmed state")

        items = [
            item for item in data.get("payroll_items", {}).values()
            if item.get("run_id") == payroll_run_id
        ]
        return json.dumps({
            "payroll_run_id": payroll_run_id,
            "items": items
        })

    @staticmethod
    def start_new_engagement_invoke(
        data: Dict[str, Any],
        name: str,
        organization_id: str,
        status: str = "active",
        worker_type: str = "employee",
        time_entry: Dict[str, Any] = None
    ) -> str:
        users = data.get("users", {})
        orgs = data.get("organizations", {})
        if organization_id not in orgs:
            raise ValueError("Organization not found")

        # Resolve user_id from full name
        matched_user_id = None
        for uid, u in users.items():
            full_name = f"{u.get('first_name', '').strip()} {u.get('last_name', '').strip()}".strip()
            if full_name.lower() == name.strip().lower():
                matched_user_id = uid
                break

        if not matched_user_id:
            raise ValueError("No user found with the given name")

        workers = data.setdefault("workers", {})
        if any(w["user_id"] == matched_user_id and w["organization_id"] == organization_id for w in workers.values()):
            raise ValueError("This user already has a worker in the given organization")

        # Create worker
        worker_id = str(uuid.uuid4())
        workers[worker_id] = {
            "user_id": matched_user_id,
            "organization_id": organization_id,
            "status": status,
            "worker_type": worker_type
        }

        response = {
            "worker_id": worker_id,
            **workers[worker_id]
        }

        # Optionally create time entry
        if time_entry:
            entries = data.setdefault("time_entries", {})
            time_entry_id = str(uuid.uuid4())
            entries[time_entry_id] = {
                "user_id": matched_user_id,
                "worker_id": worker_id,
                "status": time_entry.get("status", "draft"),
                "description": time_entry.get("description", ""),
                "project_code": time_entry.get("project_code"),
                "duration_hours": time_entry.get("duration_hours"),
                "start_time": time_entry.get("start_time"),
                "end_time": time_entry.get("end_time"),
                "date": time_entry.get("date")
            }
            response["time_entry"] = {"time_entry_id": time_entry_id, **entries[time_entry_id]}

        return json.dumps(response)

    @staticmethod
    def approve_overtime_entry_invoke(data: Dict[str, Any], time_entry_id: str) -> str:
        entries = data.get("time_entries", {})
        if time_entry_id not in entries:
            raise ValueError("Time entry not found")

        entry = entries[time_entry_id]
        if entry.get("status") not in ["submitted", "draft"]:
            raise ValueError("Only draft or submitted entries can be approved")

        entry["status"] = "approved"
        return json.dumps(entry)

    @staticmethod
    def get_documents_invoke(
        data: Dict[str, Any],
        document_id: str = None,
        user_id: str = None,
        worker_id: str = None,
        title: str = None,
        file_type: str = None,
        status: str = None
    ) -> str:
        documents = data.get("documents", {})

        def matches(doc_id, doc):
            if document_id and doc_id != document_id:
                return False
            if user_id and doc.get("user_id") != user_id:
                return False
            if worker_id and doc.get("worker_id") != worker_id:
                return False
            if title and title.lower() not in doc.get("title", "").lower():
                return False
            if file_type and doc.get("file_type") != file_type:
                return False
            if status and doc.get("status") != status:
                return False
            return True

        result = [
            {**doc, "document_id": doc_id}
            for doc_id, doc in documents.items()
            if matches(doc_id, doc)
        ]
        return json.dumps(result)

    @staticmethod
    def check_user_virtual_cards_invoke(
        data: Dict[str, Any],
        user_id: str,
        limit: float = None,
        provider_id: str = None
    ) -> str:
        cards = data.get("virtual_cards", {})

        result = [
            card for card in cards.values()
            if card.get("user_id") == user_id
            and (limit is None or card.get("limit") == round(limit, 2))
            and (provider_id is None or card.get("provider_id") == provider_id)
        ]
        return json.dumps(result)

