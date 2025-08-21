from datetime import datetime
from typing import Any, Dict
from typing import Any, Dict, Optional
import calendar
import json
import re

class Tools:
    @staticmethod
    def get_address_invoke(data: Dict[str, Any],
               address_id: str = None,
               house_number: str = None,
               building_name: str = None,
               street: str = None,
               city_name: str = None,
               state: str = None) -> str:
        """
        Retrieve addresses matching any combination of the provided fields.
        Returns a JSON array of matching address objects (including address_id).
        """
        addresses = data.get("addresses", {})
        results = []

        def norm(val: Any) -> str:
            return str(val).strip().lower()

        for addr in addresses.values():
            # Filter by each provided field
            if address_id and str(addr.get("address_id")) != address_id:
                continue
            if house_number and norm(addr.get("house_number")) != norm(house_number):
                continue
            if building_name and norm(addr.get("building_name")) != norm(building_name):
                continue
            if street and norm(addr.get("street")) != norm(street):
                continue
            if city_name and norm(addr.get("city_name")) != norm(city_name):
                continue
            if state and norm(addr.get("state")) != norm(state):
                continue

            # Build the result object
            results.append({
                "address_id": addr.get("address_id"),
                "house_number": addr.get("house_number"),
                "building_name": addr.get("building_name"),
                "street": addr.get("street"),
                "city_name": addr.get("city_name"),
                "state": addr.get("state"),
                "created_at": addr.get("created_at"),
                "updated_at": addr.get("updated_at"),
            })

        return json.dumps(results)

    @staticmethod
    def add_command_invoke(data: Dict[str, Any],
               device_type: str,
               routine_id: str,
               device_id: str,
               device_status: str,
               bulb_brightness_level: str = None,
               bulb_color: str = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T00:00:00"

        # Add to device_commands
        device_commands = data.setdefault("device_commands", {})
        dcid = generate_id(device_commands)
        device_commands[dcid] = {
            "device_command_id": dcid,
            "routine_id": routine_id,
            "device_id": device_id,
            "status": device_status,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        # If it's a bulb and both fields are provided, add to bulb_commands
        if device_type == "bulb" and bulb_brightness_level and bulb_color:
            bulb_commands = data.setdefault("bulb_commands", {})
            bcid = generate_id(bulb_commands)
            bulb_commands[bcid] = {
                "bulb_command_id": bcid,
                "routine_id": routine_id,
                "device_id": device_id,
                "brightness_level": bulb_brightness_level,
                "color": bulb_color,
                "created_at": timestamp,
                "updated_at": timestamp
            }

        return json.dumps({"success": True})

    @staticmethod
    def create_emergency_alert_invoke(data: Dict[str, Any],
               home_id: str,
               device_id: str,
               alert_type: str,
               severity_level: str,
               triggered_at: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] or [0]) + 1)

        alerts = data.setdefault("emergency_alerts", {})
        alert_id = generate_id(alerts)

        alert_record = {
            "home_id": home_id,
            "device_id": device_id,
            "alert_type": alert_type,
            "severity_level": severity_level,
            "triggered_at": triggered_at,
            "acknowledged_at": None,
            "acknowledged_by_user": None,
            "resolved_at": None,
            "resolved_by_user": None,
            "created_at": triggered_at
        }

        alerts[alert_id] = alert_record

        return json.dumps({"alert_id": alert_id, "success": True})

    @staticmethod
    def get_home_info_invoke(data: Dict[str, Any],
               home_id: str = None,
               owner_id: str = None,
               address_id: str = None) -> str:
        """Fetch homes filtered by home_id, owner_id, or address_id; include num_residents and num_rooms_occupied."""
        homes = data.get("homes", {})
        users = data.get("users", {})
        rooms = data.get("rooms", {})
        results = []

        for h in homes.values():
            if home_id and h.get("home_id") != home_id:
                continue
            if owner_id and h.get("owner_id") != owner_id:
                continue
            if address_id and h.get("address_id") != address_id:
                continue

            num_residents = sum(
                1 for u in users.values()
                if u.get("primary_address_id") == h.get("address_id")
            )

            num_rooms_occupied = sum(
                1 for r in rooms.values()
                if r.get("home_id") == h.get("home_id") and r.get("status") == "occupied"
            )

            results.append({
                "home_id":             h.get("home_id"),
                "owner_id":            h.get("owner_id"),
                "address_id":          h.get("address_id"),
                "home_type":           h.get("home_type"),
                "num_residents":       num_residents,
                "num_rooms_occupied":  num_rooms_occupied
            })

        return json.dumps(results)

    @staticmethod
    def update_home_info_invoke(data: Dict[str, Any],
               home_id: str,
               owner_id: str = None,
               address_id: str = None,
               home_type: str = None) -> str:
        
        homes = data.get("homes", {})
        home = homes.get(str(home_id))
        if not home:
            raise ValueError(f"Home with ID {home_id} not found")

        timestamp = "2025-10-01T00:00:00"
        if owner_id is not None:
            home["owner_id"] = owner_id
        if address_id is not None:
            home["address_id"] = address_id
        if home_type is not None:
            home["home_type"] = home_type

        home["updated_at"] = timestamp
        return json.dumps(home)

    @staticmethod
    def create_routine_invoke(data: Dict[str, Any],
               user_id: int,
               home_id: int,
               action_time: str,
               start_action_date: str,
               action_interval: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] or [0]) + 1)

        routines = data.setdefault("automated_routines", {})
        routine_id = generate_id(routines)
        timestamp = "2025-10-01T00:00:00"

        new_routine = {
            "routine_id": routine_id,
            "user_id": str(user_id),
            "home_id": str(home_id),
            "action_time": action_time,
            "start_action_date": start_action_date,
            "action_interval": action_interval,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        routines[routine_id] = new_routine

        return json.dumps({
            "routine_id": routine_id,
            "success": True
        })

    @staticmethod
    def update_device_info_invoke(data: Dict[str, Any],
               device_id: str,
               room_id: Optional[str] = None,
               installed_on: Optional[str] = None,
               insurance_expiry_date: Optional[str] = None,
               home_id: Optional[str] = None,
               status: Optional[str] = None,
               width_ft: Optional[float] = None,
               length_ft: Optional[float] = None,
               price: Optional[float] = None,
               scheduled_maintainance_date: Optional[str] = None,
               last_maintainance_date: Optional[str] = None,
               daily_rated_power_consumption_kWh: Optional[float] = None,
               brightness_level: Optional[str] = None,
               color: Optional[str] = None) -> str:
        """Update a device by ID. If bulb, update smart_bulbs if applicable and include brightness/color in output."""

        devices = data.get("devices", {})
        smart_bulbs = data.get("smart_bulbs", {})
        timestamp = "2025-10-01T00:00:00"

        device = devices.get(device_id)
        if not device:
            return json.dumps({"error": f"Device ID {device_id} not found"})

        # Update general device fields
        if room_id is not None:
            device["room_id"] = room_id
        if installed_on is not None:
            device["installed_on"] = installed_on
        if insurance_expiry_date is not None:
            device["insurance_expiry_date"] = insurance_expiry_date
        if home_id is not None:
            device["home_id"] = home_id
        if status is not None:
            device["status"] = status
        if width_ft is not None:
            device["width_ft"] = width_ft
        if length_ft is not None:
            device["length_ft"] = length_ft
        if price is not None:
            device["price"] = price
        if scheduled_maintainance_date is not None:
            device["scheduled_maintainance_date"] = scheduled_maintainance_date
        if last_maintainance_date is not None:
            device["last_maintainance_date"] = last_maintainance_date
        if daily_rated_power_consumption_kWh is not None:
            device["daily_rated_power_consumption_kWh"] = daily_rated_power_consumption_kWh

        device["updated_at"] = timestamp

        # Prepare return data
        result = dict(device)

        # If bulb, update and include smart_bulb info
        if device.get("device_type") == "bulb":
            bulb = smart_bulbs.get(device_id)
            if bulb:
                if brightness_level is not None:
                    bulb["brightness_level"] = brightness_level
                if color is not None:
                    bulb["color"] = color
                bulb["updated_at"] = timestamp

                result["brightness_level"] = bulb.get("brightness_level")
                result["color"] = bulb.get("color")

        return json.dumps(result)

    @staticmethod
    def get_energy_tariffs_info_invoke(data: Dict[str, Any],
               home_id: str) -> str:
        tariffs = data.get("energy_tariffs", {})
        results = [t for t in tariffs.values() if t.get("home_id") == home_id]
        return json.dumps(results)

    @staticmethod
    def list_children_invoke(data: Dict[str, Any],
               parent_id: str) -> str:
        users = data.get("users", {})
        results = [u for u in users.values() if u.get("parent_id") == parent_id]
        return json.dumps(results)

    @staticmethod
    def get_user_info_invoke(data: Dict[str, Any],
               user_id: str = None,
               phone_number: str = None,
               email: str = None) -> str:
        """
        Retrieve user records matching optional filters: user_id, phone_number, or email.
        Phone numbers are compared by digits only (ignoring formatting characters) and support suffix matching.
        Email comparisons are case-insensitive.
        """
        users = data.get("users", {})
        results = []

        def normalize_phone(p) -> str:
            if p is None:
                return ""
            return re.sub(r"\D", "", str(p))

        target_phone = normalize_phone(phone_number)
        target_email = email.lower() if email is not None else None

        for user in users.values():
            # Filter by user_id
            if user_id is not None and user.get("user_id") != user_id:
                continue

            # Filter by phone_number (normalize digits, allow suffix match)
            if target_phone:
                user_phone = normalize_phone(user.get("phone_number"))
                if not user_phone.endswith(target_phone):
                    continue

            # Filter by email (case-insensitive)
            if target_email:
                user_email = user.get("email", "").lower()
                if user_email != target_email:
                    continue

            results.append(user)

        return json.dumps(results)

    @staticmethod
    def get_historical_energy_consumption_by_device_invoke(
        data: Dict[str, Any],
        device_id: Optional[str] = None,
        date: Optional[str] = None,
        month: Optional[int] = None
    ) -> str:
        records = data.get("historical_energy_consumption", {})

        if not device_id:
            return json.dumps({"total_power_used_kWh": 0.0})

        # Filter records by device_id (as string)
        filtered = [
            r for r in records.values()
            if str(r.get("device_id")) == device_id
        ]

        if date:
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
                year = dt.year
                month = dt.month
                day = dt.day

                # Select either the 1st or 15th of the month
                target_day = 1 if day <= 14 else 15
                target_date = f"{year:04d}-{month:02d}-{target_day:02d}"

                match = next((r for r in filtered if r["date"] == target_date), None)
                return json.dumps({"total_power_used_kWh": match["power_used_kWh"] if match else 0.0})
            except Exception:
                return json.dumps({"total_power_used_kWh": 0.0})

        elif month:
            try:
                # Use current year (2025) for all calculations
                year = 2025
                total_days = calendar.monthrange(year, month)[1]
                first_val = None
                fifteenth_val = None

                for r in filtered:
                    try:
                        r_date = datetime.strptime(r["date"], "%Y-%m-%d")
                        if r_date.month == month and r_date.year == year:
                            if r_date.day == 1:
                                first_val = r["power_used_kWh"]
                            elif r_date.day == 15:
                                fifteenth_val = r["power_used_kWh"]
                    except Exception:
                        continue

                if first_val is not None and fifteenth_val is not None:
                    approx = first_val * 14 + fifteenth_val * (total_days - 14)
                elif first_val is not None:
                    approx = first_val * total_days
                elif fifteenth_val is not None:
                    approx = fifteenth_val * total_days
                else:
                    approx = 0.0

                return json.dumps({"total_power_used_kWh": round(approx, 2)})
            except Exception:
                return json.dumps({"total_power_used_kWh": 0.0})

        return json.dumps({"total_power_used_kWh": 0.0})

    @staticmethod
    def get_emergency_alerts_invoke(
        data: Dict[str, Any],
        home_id: Optional[str] = None,
        device_id: Optional[str] = None,
        alert_type: Optional[str] = None,
        severity_level: Optional[str] = None,
        resolved_by_user: Optional[str] = None,
        acknowledged_by_user: Optional[str] = None
    ) -> str:
        alerts = data.get("emergency_alerts", {})
        results = []

        for alert in alerts.values():
            if home_id is not None and str(alert.get("home_id")) != home_id:
                continue
            if device_id is not None and str(alert.get("device_id")) != device_id:
                continue
            if alert_type is not None and alert.get("alert_type") != alert_type:
                continue
            if severity_level is not None and alert.get("severity_level") != severity_level:
                continue
            if resolved_by_user is not None and str(alert.get("resolved_by_user")) != resolved_by_user:
                continue
            if acknowledged_by_user is not None and str(alert.get("acknowledged_by_user")) != acknowledged_by_user:
                continue

            results.append(alert)

        return json.dumps(results)

    @staticmethod
    def add_device_invoke(data: Dict[str, Any],
               device_type: str,
               room_id: str,
               home_id: str,
               width_ft: float,
               length_ft: float,
               price: float,
               daily_rated_power_consumption_kWh: float,
               brightness_level: str = None,
               color: str = None,
               insurance_expiry_date: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            return max([int(k) for k in table.keys()], default=0) + 1

        timestamp = "2025-10-01T00:00:00"
        devices = data.setdefault("devices", {})
        smart_bulbs = data.setdefault("smart_bulbs", {})

        device_id = generate_id(devices)

        # Build device entry
        new_device = {
            "device_id": str(device_id),
            "device_type": device_type,
            "room_id": room_id,
            "installed_on": timestamp,
            "insurance_expiry_date": insurance_expiry_date or "2026-10-01",
            "home_id": home_id,
            "status": "off",
            "width_ft": width_ft,
            "length_ft": length_ft,
            "price": price,
            "scheduled_maintainance_date": None,
            "last_maintainance_date": timestamp,
            "daily_rated_power_consumption_kWh": daily_rated_power_consumption_kWh,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        devices[str(device_id)] = new_device

        # Add to smart_bulbs if device is a bulb
        if device_type == "bulb":
            smart_bulbs[str(device_id)] = {
                "device_id": str(device_id),
                "brightness_level": brightness_level,
                "color": color,
                "created_at": timestamp,
                "updated_at": timestamp
            }

        return json.dumps({"device_id": str(device_id), "success": True})

    @staticmethod
    def update_user_info_invoke(data: Dict[str, Any],
               user_id: str,
               first_name: Optional[str] = None,
               last_name: Optional[str] = None,
               phone_number: Optional[str] = None,
               role: Optional[str] = None,
               email: Optional[str] = None,
               primary_address_id: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        user = users.get(user_id)

        if not user:
            raise ValueError(f"User with ID {user_id} not found.")

        # Update fields if provided
        if first_name is not None:
            user["first_name"] = first_name
        if last_name is not None:
            user["last_name"] = last_name
        if phone_number is not None:
            user["phone_number"] = phone_number
        if role is not None:
            user["role"] = role
        if email is not None:
            user["email"] = email
        if primary_address_id is not None:
            user["primary_address_id"] = primary_address_id

        # Always update the timestamp
        user["updated_at"] = "2025-10-01T00:00:00"

        return json.dumps(user)

    @staticmethod
    def get_rooms_info_invoke(data: Dict[str, Any],
               room_id: str = None,
               home_id: str = None) -> str:
        rooms = data.get("rooms", {})
        results = []

        for r in rooms.values():
            if room_id and r.get("room_id") != room_id:
                continue
            if home_id and r.get("home_id") != home_id:
                continue

            results.append({
                "room_id":       r.get("room_id"),
                "home_id":       r.get("home_id"),
                "room_type":     r.get("room_type"),
                "room_owner_id": r.get("room_owner_id"),
                "status":        r.get("status"),
                "width_ft":      r.get("width_ft"),
                "length_ft":     r.get("length_ft")
            })

        return json.dumps(results)

    @staticmethod
    def get_devices_info_invoke(data: Dict[str, Any],
               device_id: str = None,
               room_id: str = None,
               device_type: str = None,
               status: str = None) -> str:
        devices = data.get("devices", {})
        smart_bulbs = data.get("smart_bulbs", {})
        results = []

        for d in devices.values():
            if device_id and str(d.get("device_id")) != device_id:
                continue
            if room_id and d.get("room_id") != room_id:
                continue
            if device_type and d.get("device_type") != device_type:
                continue
            if status and d.get("status") != status:
                continue

            device_info = {
                "device_id": d.get("device_id"),
                "device_type": d.get("device_type"),
                "room_id": d.get("room_id"),
                "installed_on": d.get("installed_on"),
                "insurance_expiry_date": d.get("insurance_expiry_date"),
                "home_id": d.get("home_id"),
                "status": d.get("status"),
                "width_ft": d.get("width_ft"),
                "length_ft": d.get("length_ft"),
                "price": d.get("price"),
                "scheduled_maintainance_date": d.get("scheduled_maintainance_date"),
                "last_maintainance_date": d.get("last_maintainance_date"),
                "daily_rated_power_consumption_kWh": d.get("daily_rated_power_consumption_kWh")
            }

            if d.get("device_type") == "bulb":
                bulb_info = smart_bulbs.get(str(d.get("device_id")), {})
                device_info["brightness_level"] = bulb_info.get("brightness_level")
                device_info["color"] = bulb_info.get("color")

            results.append(device_info)

        return json.dumps(results)

    @staticmethod
    def create_address_invoke(data: Dict[str, Any],
               house_number: str,
               building_name: str,
               street: str,
               city_name: str,
               state: str) -> str:
        
        addresses = data.setdefault("addresses", {})

        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] or [0]) + 1)

        address_id = generate_id(addresses)
        timestamp = "2025-10-01T00:00:00"

        new_address = {
            "address_id": address_id,
            "house_number": house_number,
            "building_name": building_name,
            "street": street,
            "city_name": city_name,
            "state": state,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        addresses[address_id] = new_address
        return json.dumps({"address_id": address_id, "success": True})

    @staticmethod
    def get_commands_invoke(data: Dict[str, Any],
               routine_id: str = None,
               device_id: str = None) -> str:
        results = []
        
        # Define table configurations
        tables = [
            ("device_commands", "on_off_command", "device_command_id", {"status": "status"}),
            ("bulb_commands", "bulb_command", "bulb_command_id", {"brightness_level": "brightness_level", "color": "color"}),
            ("thermostat_commands", "thermostat_command", "thermostat_command_id", {"current_temperature": "current_temperature"})
        ]
        
        for table_name, command_type, id_field, specific_fields in tables:
            commands = data.get(table_name, {})
            
            for cmd in commands.values():
                # Apply filters based on the three cases
                if routine_id and device_id:
                    # Case 3: Both parameters given
                    if str(cmd.get("routine_id")) != routine_id or str(cmd.get("device_id")) != device_id:
                        continue
                elif routine_id:
                    # Case 1: Only routine_id given
                    if str(cmd.get("routine_id")) != routine_id:
                        continue
                elif device_id:
                    # Case 2: Only device_id given
                    if str(cmd.get("device_id")) != device_id:
                        continue
                else:
                    # Case 4: No parameters - skip all
                    continue
                
                # Build command info
                command_info = {
                    "command_type": command_type,
                    "command_id": cmd.get(id_field),
                    "routine_id": cmd.get("routine_id"),
                    "device_id": cmd.get("device_id"),
                    "created_at": cmd.get("created_at"),
                    "updated_at": cmd.get("updated_at")
                }
                
                # Add table-specific fields
                command_info.update({k: cmd.get(v) for k, v in specific_fields.items()})
                results.append(command_info)
        
        return json.dumps(results)

    @staticmethod
    def update_room_info_invoke(data: Dict[str, Any],
               room_id: str,
               room_owner_id: str = None,
               status: str = None) -> str:
        
        rooms = data.get("rooms", {})
        room = rooms.get(str(room_id))
        if not room:
            raise ValueError(f"Room with ID {room_id} not found")

        timestamp = "2025-10-01T00:00:00"

        # Handle status change to vacant → clear owner
        if status == "vacant":
            room["status"] = "vacant"
            room["room_owner_id"] = None

        # Handle assigning owner to vacant room → auto-occupy
        elif room_owner_id is not None:
            room["room_owner_id"] = room_owner_id
            if room.get("status") == "vacant" and status is None:
                room["status"] = "occupied"

        # Update status if provided and not handled already
        if status is not None and status != "vacant":
            room["status"] = status

        room["updated_at"] = timestamp
        return json.dumps(room)

    @staticmethod
    def add_feedback_invoke(data: Dict[str, Any],
               user_id: str,
               device_id: str,
               rating: int) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T00:00:00"
        feedbacks = data.setdefault("user_feedbacks", {})
        feedback_id = generate_id(feedbacks)

        feedbacks[feedback_id] = {
            "user_feedback_id": feedback_id,
            "user_id": user_id,
            "device_id": device_id,
            "rating": rating,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        return json.dumps({"user_feedback_id": feedback_id, "success": True})

    @staticmethod
    def get_routines_invoke(data: Dict[str, Any],
               routine_id: str = None,
               user_id: str = None,
               home_id: str = None,
               action_time: str = None,
               action_interval: str = None,
               start_action_date: str = None) -> str:
        routines = data.get("automated_routines", {})
        results = []

        for r in routines.values():
            if routine_id and r.get("routine_id") != routine_id:
                continue
            if user_id and r.get("user_id") != user_id:
                continue
            if home_id and r.get("home_id") != home_id:
                continue
            if action_time and r.get("action_time") != action_time:
                continue
            if action_interval and r.get("action_interval") != action_interval:
                continue
            if start_action_date and r.get("start_action_date") != start_action_date:
                continue
            results.append(r)

        return json.dumps(results)

    @staticmethod
    def acknowledge_or_resolve_alert_invoke(data: Dict[str, Any],
               alert_id: str,
               acknowledged_at: str = None,
               acknowledged_by_user: str = None,
               resolved_at: str = None,
               resolved_by_user: str = None) -> str:
        
        alerts = data.get("emergency_alerts", {})
        alert = alerts.get(alert_id)

        if not alert:
            raise ValueError(f"Alert with ID {alert_id} not found.")

        default_time = "2025-10-01T00:00:00"

        # Handle acknowledgment
        if acknowledged_by_user is not None:
            alert["acknowledged_by_user"] = acknowledged_by_user
            alert["acknowledged_at"] = acknowledged_at or default_time

        # Handle resolution
        if resolved_by_user is not None:
            alert["resolved_by_user"] = resolved_by_user
            alert["resolved_at"] = resolved_at or default_time

        return json.dumps(alert)

