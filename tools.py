from typing import Any, Dict
import json
import uuid

class Tools:
    @staticmethod
    def count_team_members_invoke(data: Dict[str, Any], team_id: str) -> str:
        team_members = data.get("team_members", {})

        count = sum(
            1 for record in team_members.values()
            if record.get("team_id") == team_id and record.get("left_at") is None
        )

        return json.dumps({
            "team_id": team_id,
            "active_member_count": count
        })

    @staticmethod
    def get_user_profile_invoke(data: Dict[str, Any], user_id: str) -> str:
        users = data.get("users", {})
        if user_id not in users:
            raise ValueError("User not found")
        user = users[user_id]
        return json.dumps({
            "user_id": user_id,
            "role": user.get("role"),
            "locale": user.get("locale"),
            "email": user.get("email"),
            "timezone": user.get("timezone"),
            "status": user.get("status")
        })

    @staticmethod
    def list_organization_departments_invoke(
        data: Dict[str, Any],
        department_id: str = None,
        organization_id: str = None,
        manager_user_id: str = None,
        name: str = None
    ) -> str:
        departments = data.get("org_departments", {})

        def matches(dept_id, dept):
            if department_id and dept_id != department_id:
                return False
            if organization_id and dept.get("organization_id") != organization_id:
                return False
            if manager_user_id and dept.get("manager_user_id") != manager_user_id:
                return False
            if name and name.lower() not in dept.get("name", "").lower():
                return False
            return True

        results = [
            {**dept, "department_id": dept_id}
            for dept_id, dept in departments.items()
            if matches(dept_id, dept)
        ]

        return json.dumps(results)

    @staticmethod
    def get_worker_profile_invoke(
        data: Dict[str, Any],
        worker_id: str = None,
        user_id: str = None,
        organization_id: str = None
    ) -> str:
        workers = data.get("workers", {})

        # Case 1: Direct lookup by worker_id
        if worker_id:
            if worker_id not in workers:
                raise ValueError("Worker not found for the given worker_id")
            worker = workers[worker_id]
            if user_id and worker.get("user_id") != user_id:
                raise ValueError("Provided user_id does not match the given worker_id")
            return json.dumps({
                "worker_id": worker_id,
                "user_id": worker.get("user_id"),
                "worker_type": worker.get("worker_type"),
                "status": worker.get("status"),
                "organization_id": worker.get("organization_id")
            })

        # Case 2: Composite key — user_id + organization_id
        if user_id and organization_id:
            for wid, w in workers.items():
                if w.get("user_id") == user_id and w.get("organization_id") == organization_id:
                    return json.dumps({
                        "worker_id": wid,
                        "user_id": w.get("user_id"),
                        "worker_type": w.get("worker_type"),
                        "status": w.get("status"),
                        "organization_id": w.get("organization_id")
                    })
            raise ValueError("Worker not found for the given user_id and organization_id")

        raise ValueError("You must provide either worker_id or both user_id and organization_id")

    @staticmethod
    def submit_reimbursement_receipt_invoke(data: Dict[str, Any], reimbursement_id: str, **kwargs) -> str:
        reimbursements = data.setdefault("reimbursements", {})

        # If reimbursement does not exist, create a new record
        if reimbursement_id not in reimbursements:
            reimbursements[reimbursement_id] = {}

        # Filter out document_id — do not store it
        filtered_kwargs = {k: v for k, v in kwargs.items() if k != "document_id"}

        # Update the reimbursement with the remaining fields
        reimbursements[reimbursement_id].update(filtered_kwargs)

        return json.dumps({
            "reimbursement_id": reimbursement_id,
            **reimbursements[reimbursement_id]
        })

    @staticmethod
    def remove_team_member_invoke(
        data: Dict[str, Any],
        team_member_id: str = None,
        worker_id: str = None,
        team_id: str = None
    ) -> str:
        team_members = data.get("team_members", {})

        target_id = None

        # Case 1: Direct match via team_member_id
        if team_member_id:
            if team_member_id not in team_members:
                return json.dumps({
                    "status": "error",
                    "message": "Team member ID not found",
                    "team_member_id": team_member_id
                })
            record = team_members[team_member_id]

            # Cross-validation if worker_id or team_id is provided
            if worker_id and record.get("worker_id") != worker_id:
                return json.dumps({
                    "status": "error",
                    "message": "worker_id does not match the team_member_id",
                    "team_member_id": team_member_id
                })
            if team_id and record.get("team_id") != team_id:
                return json.dumps({
                    "status": "error",
                    "message": "team_id does not match the team_member_id",
                    "team_member_id": team_member_id
                })

            target_id = team_member_id

        # Case 2: Match by worker_id + team_id
        elif worker_id and team_id:
            for tid, record in team_members.items():
                if record.get("worker_id") == worker_id and record.get("team_id") == team_id:
                    target_id = tid
                    break
            if not target_id:
                return json.dumps({
                    "status": "error",
                    "message": "No team member found for given worker_id and team_id",
                    "worker_id": worker_id,
                    "team_id": team_id
                })
        else:
            return json.dumps({
                "status": "error",
                "message": "You must provide either team_member_id or both worker_id and team_id"
            })

        removed = team_members.pop(target_id)
        return json.dumps({
            "status": "removed",
            "team_member_id": target_id,
            **removed
        })

    @staticmethod
    def create_worker_invoke(
        data: Dict[str, Any],
        user_id: str,
        worker_type: str,
        status: str,
        organization_id: str
    ) -> str:
        workers = data.setdefault("workers", {})

        # Optional validations
        if "users" in data and user_id not in data["users"]:
            raise ValueError("User ID does not exist")
        if "organizations" in data and organization_id not in data["organizations"]:
            raise ValueError("Organization ID does not exist")

        worker_id = str(uuid.uuid4())
        workers[worker_id] = {
            "user_id": user_id,
            "worker_type": worker_type,
            "status": status,
            "organization_id": organization_id
        }

        return json.dumps({"worker_id": worker_id})

    @staticmethod
    def get_time_entry_worker_invoke(
        data: Dict[str, Any],
        worker_id: str,
        description: str = None,
        time_entry_id: str = None
    ) -> str:
        time_entries = data.get("time_entries", {})

        def matches(entry_id, entry):
            if time_entry_id and entry_id != time_entry_id:
                return False
            if entry.get("worker_id") != worker_id:
                return False
            if description and description.lower() not in entry.get("description", "").lower():
                return False
            return True

        results = [
            {**entry, "time_entry_id": entry_id}
            for entry_id, entry in time_entries.items()
            if matches(entry_id, entry)
        ]

        return json.dumps(results)

    @staticmethod
    def deactivate_user_invoke(data: Dict[str, Any], user_id: str) -> str:
        users = data.get("users", {})
        if user_id not in users:
            raise ValueError("User not found")

        users[user_id]["status"] = "inactive"
        return json.dumps({"user_id": user_id, "status": "inactive"})

    @staticmethod
    def allocate_time_entry_invoke(data: Dict[str, Any], worker_id: str, hours: float, task: str) -> str:
        if hours <= 0 or hours > 24:
            raise ValueError("Invalid hours range")

        workers = data.get("workers", {})
        if worker_id not in workers:
            raise ValueError("Worker not found")

        time_entries = data.setdefault("time_entries", {})
        entry_id = str(uuid.uuid4())
        time_entries[entry_id] = {
            "worker_id": worker_id,
            "duration_hours": round(hours, 2),
            "project_code": "AUTO",
            "description": task,
            "status": "submitted",
            "date": "2025-07-01",
            "start_time": "2025-07-01T09:00:00Z",
            "end_time": "2025-07-01T17:00:00Z",
            "user_id": workers[worker_id]["user_id"]
        }
        return json.dumps({"time_entry_id": entry_id})

    @staticmethod
    def assign_worker_to_team_invoke(
        data: Dict[str, Any],
        user_id: str,
        worker_id: str,
        team_id: str,
        role: str,
        joined_at: str
    ) -> str:
        team_members = data.setdefault("team_members", {})

        # Optional validations
        if "users" in data and user_id not in data["users"]:
            raise ValueError("User ID not found")
        if "workers" in data and worker_id not in data["workers"]:
            raise ValueError("Worker ID not found")
        if "teams" in data and team_id not in data["teams"]:
            raise ValueError("Team ID not found")

        team_member_id = str(uuid.uuid4())

        new_record = {
            "user_id": user_id,
            "worker_id": worker_id,
            "team_id": team_id,
            "role": role,
            "joined_at": joined_at,
            "left_at": None
        }

        team_members[team_member_id] = new_record

        return json.dumps({
            "team_member_id": team_member_id,
            **new_record
        })

    @staticmethod
    def get_worker_financial_summary_invoke(data: Dict[str, Any], worker_id: str) -> str:
        payroll_items = data.get("payroll_items", {})
        reimbursements = data.get("reimbursements", {})

        total_payroll = sum(item.get("amount", 0) for item in payroll_items.values() if item.get("worker_id") == worker_id)
        total_reimb = sum(item.get("amount", 0) for item in reimbursements.values() if item.get("worker_id") == worker_id)

        return json.dumps({
            "worker_id": worker_id,
            "total_payroll_amount": round(total_payroll, 2),
            "total_reimbursements_amount": round(total_reimb, 2)
        })

    @staticmethod
    def list_organization_teams_invoke(
        data: Dict[str, Any],
        team_id: str = None,
        organization_id: str = None,
        name: str = None,
        description: str = None
    ) -> str:
        teams = data.get("org_teams", {})

        def matches(tid, team):
            if team_id and tid != team_id:
                return False
            if organization_id and team.get("organization_id") != organization_id:
                return False
            if name and name.lower() not in team.get("name", "").lower():
                return False
            if description and description.lower() not in team.get("description", "").lower():
                return False
            return True

        results = [
            {**team, "team_id": tid}
            for tid, team in teams.items()
            if matches(tid, team)
        ]

        return json.dumps(results)

    @staticmethod
    def create_user_profile_invoke(data: Dict[str, Any], name: str, email: str, role: str, timezone: str) -> str:
        users = data.setdefault("users", {})
        if any(u.get("email") == email for u in users.values()):
            raise ValueError("Email already exists")

        user_id = str(uuid.uuid4())
        first_name, *last = name.split()
        users[user_id] = {
            "first_name": first_name,
            "last_name": " ".join(last) if last else "",
            "email": email,
            "role": role,
            "timezone": timezone,
            "locale": "en-US",
            "password_hash": "not_set",
            "status": "active"
        }
        return json.dumps({"user_id": user_id})

    @staticmethod
    def assign_worker_to_org_invoke(data: Dict[str, Any], worker_id: str, new_organization_id: str) -> str:
        workers = data.get("workers", {})
        organizations = data.get("organizations", {})

        if worker_id not in workers:
            raise ValueError(f"Worker '{worker_id}' not found.")

        if new_organization_id not in organizations:
            raise ValueError(f"Organization '{new_organization_id}' not found.")

        workers[worker_id]["organization_id"] = new_organization_id
        workers[worker_id]["updated_at"] = "2025-07-01T09:25:07.660396Z"

        return json.dumps(workers[worker_id])

    @staticmethod
    def list_open_reimbursements_invoke(
        data: Dict[str, Any],
        user_id: str = None,
        worker_id: str = None,
        currency: str = None,
        organization_id: str = None,
        contract_id: str = None,
        submit_date: str = None,
        approve_date: str = None,
        min_amount: float = None,
        max_amount: float = None
    ) -> str:
        reimbursements = data.get("reimbursements", {})
        workers = data.get("workers", {})

        # Resolve user_id if only worker_id is provided
        if not user_id and worker_id:
            if worker_id not in workers:
                return "Error: Worker not found"
            user_id = workers[worker_id].get("user_id")

        def matches(r):
            if r.get("status") != "submitted":
                return False
            if user_id and r.get("user_id") != user_id:
                return False
            if currency and r.get("currency") != currency:
                return False
            if organization_id and r.get("organization_id") != organization_id:
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

        results = [r for r in reimbursements.values() if matches(r)]
        return json.dumps(results)

    @staticmethod
    def update_virtual_card_limit_invoke(data: Dict[str, Any], card_id: str, new_limit: float) -> str:
        cards = data.get("virtual_cards", {})
        card = cards.get(card_id)

        if not card:
            raise ValueError("Card not found")
        if card.get("status") in ["revoked", "expired", "blocked"]:
            raise ValueError("Card cannot be modified in current status")
        if new_limit <= 0 or new_limit > 100000:
            raise ValueError("Limit must be between 1 and 100000")

        card["limit"] = round(new_limit, 2)
        return json.dumps({"card_id": card_id, "new_limit": new_limit})

    @staticmethod
    def list_organizations_invoke(
        data: Dict[str, Any],
        user_id: str = None,
        worker_id: str = None,
        name: str = None,
        country: str = None,
        timezone: str = None,
        address_line1: str = None,
        address_city: str = None,
        address_zip: str = None
    ) -> str:
        workers = data.get("workers", {})
        organizations = data.get("organizations", {})

        # Resolve user_id if worker_id is given
        if worker_id:
            if worker_id not in workers:
                raise ValueError("Worker not found for the given worker_id")
            resolved_user_id = workers[worker_id].get("user_id")
            if user_id and user_id != resolved_user_id:
                raise ValueError("Provided user_id does not match worker_id")
            user_id = resolved_user_id

        # If user_id is present, limit org_ids to those associated with the user
        org_ids = None
        if user_id:
            org_ids = {
                w["organization_id"]
                for w in workers.values()
                if w.get("user_id") == user_id
            }

        def match(org):
            if name and name.lower() not in org.get("name", "").lower():
                return False
            if country and org.get("country") != country:
                return False
            if timezone and org.get("timezone") != timezone:
                return False
            address = org.get("address", {})
            if address_line1 and address.get("line1") != address_line1:
                return False
            if address_city and address.get("city") != address_city:
                return False
            if address_zip and address.get("zip") != address_zip:
                return False
            return True

        # Apply filters
        matched_orgs = [
            org for oid, org in organizations.items()
            if (org_ids is None or oid in org_ids) and match(org)
        ]

        return json.dumps(matched_orgs)

    @staticmethod
    def view_virtual_card_usage_invoke(data: Dict[str, Any], virtual_card_id: str = None, user_id: str = None) -> str:
        cards = data.get("virtual_cards", {})

        # Resolve virtual_card_id if only user_id is given
        if not virtual_card_id:
            if not user_id:
                raise ValueError("Either virtual_card_id or user_id must be provided")
            for cid, card in cards.items():
                if card.get("user_id") == user_id:
                    virtual_card_id = cid
                    break
            if not virtual_card_id:
                raise ValueError("No virtual card found for the given user_id")

        card = cards.get(virtual_card_id)
        if not card:
            raise ValueError("Virtual card not found")

        # Validate if both are provided
        if user_id and card.get("user_id") != user_id:
            raise ValueError("Provided user_id does not match the virtual_card_id")

        # Simulated usage: 60% of the limit used
        usage = float(card.get("limit", 0)) * 0.6
        return json.dumps({
            "card_id": virtual_card_id,
            "user_id": card.get("user_id"),
            "provider_id": card.get("provider_id"),
            "limit": card.get("limit"),
            "currency": card.get("currency"),
            "status": card.get("status"),
            "used": round(usage, 2),
            "available": round(float(card.get("limit", 0)) - usage, 2)
        })

