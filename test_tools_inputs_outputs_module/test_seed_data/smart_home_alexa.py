import json, os, re, argparse, sys
from datetime import datetime, date

DATA_DIR = "envs/smart_home_alexa/data"

# helper to load a JSON file (dict mapping id->record expected)
def load_table(fname, data_dir=None):
    if data_dir is None:
        data_dir = DATA_DIR
    path = os.path.join(data_dir, fname)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Primary key mapping for quick pk set building
PK_TABLES = {
    "devices": ("devices.json", "device_id"),
    "users": ("users.json", "user_id"),
    "routines": ("routines.json", "routine_id"),
    "groups": ("groups.json", "group_id"),
    "skills": ("skills.json", "skill_id"),
    "voice_profiles": ("voice_profiles.json", "voice_profile_id"),
    "access_logs": ("access_logs.json", "log_id"),
    "backups": ("backups.json", "backup_id"),
}

def build_pk_sets(tables_dict):
    out = {}
    for logical, (fname, pk_field) in PK_TABLES.items():
        s = set()
        tbl = tables_dict.get(fname, {})
        for key, rec in tbl.items():
            pk_val = None
            if isinstance(rec, dict):
                pk_val = rec.get(pk_field)
            if pk_val is None:
                pk_val = key
            if pk_val is not None:
                s.add(str(pk_val))
        out[logical] = s
    return out

# ENUMS (subset per schema)
ENUMS = {
    "users.role": {"Admin","Household_Member","Guest"},
    "users.permission_level": {"full_access","restricted"},
    "users.account_status": {"active","suspended","expired"},
    "devices.device_type": {"light","lock","thermostat","camera","sensor","speaker","switch","plug","appliance","echo_device","hub"},
    "devices.connectivity_method": {"WiFi","Zigbee","Bluetooth","Matter"},
    "devices.connection_status": {"registered","online","offline","error"},
    "devices.device_status": {"registered","active","suspended","removed"},
    "devices.battery_status": {"normal","low","critical","charging"},
    "routines.routine_type": {"comfort","security","seasonal","awareness"},
    "routines.trigger_type": {"time","location","manual","sensor","voice"},
    "routines.schedule_recurrence": {"daily","weekdays","weekends","specific_dates","seasonal","once"},
    "routines.status": {"enabled","disabled"},
    "groups.group_type": {"location","functional"},
    "skills.enablement_status": {"enabled","disabled"},
    "voice_profiles.status": {"active","inactive"},
    "access_logs.action_type": {
        "device_add","device_remove","device_update","user_create","user_remove","user_update",
        "routine_create","routine_modify","routine_delete","routine_execute","group_create","group_update",
        "group_remove","skill_enable","skill_disable","privacy_settings_update","mfa_enable",
        "firmware_update","system_backup","system_restore","voice_profile_create","voice_profile_update","voice_profile_delete"
    },
    "access_logs.entity_type": {"device","user","routine","group","skill","voice_profile","backup","access_log"},
    "access_logs.outcome": {"success","failure"},
    "device_firmware_history.update_status": {"available","pending","in_progress","completed","failed","rolled_back"},
    "device_health_history.error_category": {"none","firmware_error","network_error","hardware_error","configuration_error","authentication_error","timeout_error","battery_error","sensor_error","communication_error","unknown_error"},
    "system_alerts.alert_type": {"security_alert","system_alert","device_failure","connectivity_issue","battery_low","firmware_available","temperature_threshold","unauthorized_access"},
    "system_alerts.priority": {"low","medium","high","critical"},
    "backups.backup_location_type": {"cloud","local"},
    "backups.status": {"in_progress","completed","failed"},
}

ISO_TS_FIELDS = re.compile(r".*_at$|.*_time$|.*_date$|timestamp|created_date|updated_date|scheduled_date|last_communication|training_date|enabled_date|generation_date")

TYPE_OVERRIDES = {
    # explicit numeric fields
    "devices.signal_strength": "int",
    "devices.battery_level": "int",
    "access_logs.log_id": "int",
    "backups.file_size": "int",
    "device_health_history.health_score": "float",
    "routine_execution_logs.execution_duration_ms": "int",
}

def is_timestamp(value):
    try:
        datetime.fromisoformat(value.replace("Z",""))
        return True
    except Exception:
        return False

def is_date(value):
    try:
        date.fromisoformat(value)
        return True
    except Exception:
        return False

errors = []

def check_enum(table_name, field, value, rec_id):
    key = f"{table_name}.{field}"
    if key in ENUMS and value is not None and value not in ENUMS[key]:
        errors.append(f"{table_name}:{rec_id} enum mismatch {field}='{value}' not in {sorted(ENUMS[key])}")

def fk_exists(set_name, value, table_name, rec_id, field, pk_sets):
    if value is None or value == "":
        return
    target = pk_sets.get(set_name, set())
    if str(value) not in target:
        errors.append(f"{table_name}:{rec_id} FK {field}='{value}' not found in {set_name}")

def expected_type_for(table_fname, field):
    tbl = table_fname.replace(".json","")
    key = f"{tbl}.{field}"
    if key in TYPE_OVERRIDES:
        return TYPE_OVERRIDES[key]
    if field.endswith("_date") and field not in ["generation_date"]:
        return "date"
    if field.endswith("_at") or field.endswith("_time") or field in ["timestamp","created_date","updated_date","last_communication","training_date","enabled_date","generation_date","scheduled_date","uploaded_at"]:
        return "timestamp"
    if field in ("signal_strength","battery_level","execution_duration_ms","file_size","log_id"):
        return "int"
    if field.endswith("_id") or field == "id" or field.endswith("_number") or "number" in field:
        return "str"
    if field.endswith("_name") or field.endswith("name") or field in ("title","description","message","email","file_name","file_url","model","manufacturer"):
        return "str"
    return None

def check_type(table_fname, rec_id, field, value):
    exp = expected_type_for(table_fname, field)
    if exp is None or value is None:
        return
    if exp == "int":
        if not isinstance(value, int):
            errors.append(f"{table_fname}:{rec_id} type mismatch {field} expected int got {type(value).__name__} ('{value}')")
    elif exp == "float":
        if not isinstance(value, (int,float)):
            errors.append(f"{table_fname}:{rec_id} type mismatch {field} expected float got {type(value).__name__} ('{value}')")
    elif exp == "timestamp":
        if not (isinstance(value,str) and is_timestamp(value)):
            errors.append(f"{table_fname}:{rec_id} invalid timestamp {field}='{value}'")
    elif exp == "date":
        if not (isinstance(value,str) and (is_date(value) or is_timestamp(value))):
            errors.append(f"{table_fname}:{rec_id} invalid date {field}='{value}'")
    elif exp == "str":
        if not isinstance(value,str):
            errors.append(f"{table_fname}:{rec_id} type mismatch {field} expected str got {type(value).__name__} ('{value}')")

def check_unique_field(table, field_name, tbl):
    seen = {}
    for rid, rec in tbl.items():
        v = rec.get(field_name)
        if v is None:
            continue
        if v in seen:
            errors.append(f"{table}:{rid} duplicate {field_name} value '{v}' (also in {seen[v]})")
        else:
            seen[v] = rid

def check_unique_pairs(table_file, pair_fields, tbl):
    seen = set()
    for rid, rec in tbl.items():
        key = tuple(rec.get(f) for f in pair_fields)
        if key in seen:
            errors.append(f"{table_file}:{rid} duplicate composite {pair_fields}={key}")
        else:
            seen.add(key)

def main(data_dir=None):
    global DATA_DIR, errors
    if data_dir:
        DATA_DIR = data_dir

    # Resolve DATA_DIR to absolute path so file existence checks work regardless of CWD.
    # If DATA_DIR is relative (e.g., "envs/..."), interpret it relative to the repo root:
    # repo root = two levels up from this script's directory.
    if not os.path.isabs(DATA_DIR):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        DATA_DIR = os.path.abspath(os.path.join(repo_root, DATA_DIR))

    # helpful debug print so you can confirm which directory is being checked
    print(f"Using data dir: {DATA_DIR}")

    # list of table files expected
    files = [
        "devices.json","users.json","routines.json","groups.json","skills.json","voice_profiles.json",
        "access_logs.json","backups.json",
        "user_device_permissions.json","user_group_permissions.json","skill_device_permissions.json","routine_devices.json",
        "device_health_history.json","device_firmware_history.json","routine_execution_logs.json","system_alerts.json"
    ]

    tables = {}
    for fn in files:
        try:
            tables[fn] = load_table(fn, DATA_DIR)
        except FileNotFoundError:
            tables[fn] = {}

    # --- added: target list, missing-file detection, and per-table counts ---
    TARGET_TABLES = [
        "access_logs.json","backups.json","device_firmware_history.json","device_health_history.json",
        "devices.json","groups.json","routine_devices.json","routine_execution_logs.json","routines.json",
        "skill_device_permissions.json","skills.json","system_alerts.json",
        "user_device_permissions.json","user_group_permissions.json","users.json","voice_profiles.json"
    ]

    missing_files = [fn for fn in TARGET_TABLES if not os.path.exists(os.path.join(DATA_DIR, fn))]
    if missing_files:
        print("Missing required data files in", DATA_DIR)
        for m in missing_files:
            print(" -", m)
        return 3

    print("Table record counts (requested tables):")
    for fn in TARGET_TABLES:
        tbl = tables.get(fn, {})
        print(f"  {fn}: {len(tbl)} record(s)")
    # --- end added section ---

    errors = []
    pk_sets = build_pk_sets(tables)

    # Basic enum & FK checks for core tables
    for rid, rec in tables["devices.json"].items():
        for f in ["device_type","connectivity_method","connection_status","device_status","battery_status"]:
            check_enum("devices", f, rec.get(f), rid)
        # unique/mac will be checked separately
        check_type("devices.json", rid, "signal_strength", rec.get("signal_strength"))
        check_type("devices.json", rid, "battery_level", rec.get("battery_level"))
        # group FK
        fk_exists("groups", rec.get("group_id"), "devices", rid, "group_id", pk_sets)

    for rid, rec in tables["users.json"].items():
        for f in ["role","permission_level","account_status"]:
            check_enum("users", f, rec.get(f), rid)
        # created_by FK
        fk_exists("users", rec.get("created_by_user_id"), "users", rid, "created_by_user_id", pk_sets)

    for rid, rec in tables["routines.json"].items():
        for f in ["routine_type","trigger_type","schedule_recurrence","status"]:
            if rec.get(f) is not None:
                check_enum("routines", f, rec.get(f), rid)
        fk_exists("users", rec.get("created_by_user_id"), "routines", rid, "created_by_user_id", pk_sets)
        check_type("routines.json", rid, "execution_count", rec.get("execution_count"))

    for rid, rec in tables["groups.json"].items():
        check_enum("groups", "group_type", rec.get("group_type"), rid)

    for rid, rec in tables["skills.json"].items():
        check_enum("skills", "enablement_status", rec.get("enablement_status"), rid)
        check_type("skills.json", rid, "ratings", rec.get("ratings"))

    for rid, rec in tables["voice_profiles.json"].items():
        check_enum("voice_profiles", "status", rec.get("status"), rid)
        fk_exists("users", rec.get("user_id"), "voice_profiles", rid, "user_id", pk_sets)

    for rid, rec in tables["access_logs.json"].items():
        for f in ["action_type","entity_type","outcome"]:
            if rec.get(f) is not None:
                check_enum("access_logs", f, rec.get(f), rid)
        fk_exists("users", rec.get("user_id"), "access_logs", rid, "user_id", pk_sets)
        check_type("access_logs.json", rid, "log_id", rec.get("log_id"))

    for rid, rec in tables["backups.json"].items():
        check_enum("backups", "backup_location_type", rec.get("backup_location_type"), rid)
        check_enum("backups", "status", rec.get("status"), rid)
        fk_exists("users", rec.get("created_by_user_id"), "backups", rid, "created_by_user_id", pk_sets)
        check_type("backups.json", rid, "file_size", rec.get("file_size"))

    # Relationship tables: composite uniqueness + FK checks
    rel_checks = [
        ("user_device_permissions.json", ("user_id","device_id")),
        ("user_group_permissions.json", ("user_id","group_id")),
        ("skill_device_permissions.json", ("skill_id","device_id")),
        ("routine_devices.json", ("routine_id","device_id"))
    ]
    for fname, pair in rel_checks:
        tbl = tables.get(fname, {})
        check_unique_pairs(fname, pair, tbl)
        for rid, rec in tbl.items():
            if fname == "user_device_permissions.json":
                fk_exists("users", rec.get("user_id"), fname, rid, "user_id", pk_sets)
                fk_exists("devices", rec.get("device_id"), fname, rid, "device_id", pk_sets)
            elif fname == "user_group_permissions.json":
                fk_exists("users", rec.get("user_id"), fname, rid, "user_id", pk_sets)
                fk_exists("groups", rec.get("group_id"), fname, rid, "group_id", pk_sets)
            elif fname == "skill_device_permissions.json":
                fk_exists("skills", rec.get("skill_id"), fname, rid, "skill_id", pk_sets)
                fk_exists("devices", rec.get("device_id"), fname, rid, "device_id", pk_sets)
            else:
                fk_exists("routines", rec.get("routine_id"), fname, rid, "routine_id", pk_sets)
                fk_exists("devices", rec.get("device_id"), fname, rid, "device_id", pk_sets)

    # Enhancement tables checks
    for rid, rec in tables["device_health_history.json"].items():
        check_enum("device_health_history", "error_category", rec.get("error_category"), rid)
        check_type("device_health_history.json", rid, "health_score", rec.get("health_score"))
        fk_exists("devices", rec.get("device_id"), "device_health_history", rid, "device_id", pk_sets)

    for rid, rec in tables["device_firmware_history.json"].items():
        check_enum("device_firmware_history", "update_status", rec.get("update_status"), rid)
        fk_exists("devices", rec.get("device_id"), "device_firmware_history", rid, "device_id", pk_sets)
        fk_exists("users", rec.get("update_initiated_by"), "device_firmware_history", rid, "update_initiated_by", pk_sets)

    for rid, rec in tables["routine_execution_logs.json"].items():
        check_enum("routine_execution_logs", "outcome", rec.get("outcome"), rid)
        fk_exists("routines", rec.get("routine_id"), "routine_execution_logs", rid, "routine_id", pk_sets)
        check_type("routine_execution_logs.json", rid, "execution_duration_ms", rec.get("execution_duration_ms"))

    for rid, rec in tables["system_alerts.json"].items():
        check_enum("system_alerts", "alert_type", rec.get("alert_type"), rid)
        check_enum("system_alerts", "priority", rec.get("priority"), rid)
        if rec.get("acknowledged_by_user_id"):
            fk_exists("users", rec.get("acknowledged_by_user_id"), "system_alerts", rid, "acknowledged_by_user_id", pk_sets)
        if rec.get("affected_device_id"):
            fk_exists("devices", rec.get("affected_device_id"), "system_alerts", rid, "affected_device_id", pk_sets)

    # Uniqueness checks for fields that must be unique
    check_unique_field("devices.json","mac_address", tables["devices.json"])
    check_unique_field("users.json","email", tables["users.json"])
    check_unique_field("routines.json","routine_name", tables["routines.json"])
    check_unique_field("groups.json","group_name", tables["groups.json"])
    check_unique_field("voice_profiles.json","profile_name", tables["voice_profiles.json"])

    # Generic field-type and timestamp validation across all tables
    for fname, data in tables.items():
        for rid, rec in data.items():
            if not isinstance(rec, dict):
                continue
            for field, value in rec.items():
                check_type(fname, rid, field, value)
                if value and isinstance(value, str):
                    if ISO_TS_FIELDS.match(field):
                        # date vs timestamp
                        if field.endswith("_date") and field not in ["generation_date"]:
                            if not (is_date(value) or is_timestamp(value)):
                                errors.append(f"{fname}:{rid} invalid date/timestamp {field}='{value}'")
                        else:
                            if not is_timestamp(value):
                                errors.append(f"{fname}:{rid} invalid timestamp {field}='{value}'")

    # Summary
    print("Smart Home Alexa data validation completed.")
    # Group identical error messages per table so repeated identical issues are shown once with counts/examples
    if errors:
        grouped = {}
        import re as _re
        _pat = _re.compile(r"^([^:]+):([^ ]+)\s*(.*)$")
        for full in errors:
            m = _pat.match(full)
            if m:
                table = m.group(1)
                rec_id = m.group(2)
                msg = m.group(3).strip()
            else:
                table = "unknown"
                rec_id = ""
                msg = full
            key = (table, msg)
            entry = grouped.get(key)
            if not entry:
                entry = {"count": 0, "examples": []}
                grouped[key] = entry
            entry["count"] += 1
            if rec_id and len(entry["examples"]) < 5:
                entry["examples"].append(rec_id)

        total_count = sum(v["count"] for v in grouped.values())
        print(f"Errors (grouped unique messages: {len(grouped)}, total occurrences: {total_count}):")
        shown = 0
        for (table, msg), info in sorted(grouped.items(), key=lambda kv: (-kv[1]["count"], kv[0])):
            shown += 1
            examples = ", ".join(info["examples"]) if info["examples"] else "(no example ids)"
            print(f" - [{table}] {msg} (occurrences: {info['count']}; examples: {examples})")
            if shown >= 200:
                break
        if len(grouped) > 200:
            print(f" ... {len(grouped)-200} more grouped messages")
        return 2
    else:
        print("No issues found.")
        return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate smart_home_alexa JSON data.")
    parser.add_argument("--data-dir", help="Path to data directory (defaults to value in file)", default=None)
    args = parser.parse_args()
    sys.exit(main(args.data_dir))
