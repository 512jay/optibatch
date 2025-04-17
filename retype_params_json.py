# retype_params_json.py
"""
🛠 Retype Params JSON

Description:
    Updates the types of tester parameters and inputs in an existing OptiBatch SQLite database.
    Reads typing metadata from each job folder's job_config.json or current_config.ini (fallback).

Usage:
    python retype_params_json.py --db .optibatch/optibatch.db --job-root generated
    python retype_params_json.py --db .optibatch/optibatch.db --job-root generated --dry-run

Arguments:
    --db         Path to SQLite DB file (e.g., .optibatch/optibatch.db)
    --job-root   Path to folder containing job folders (e.g., generated)
    --dry-run    Optional; if set, will print what would change instead of modifying DB

Author:
    Regina's AI Assistant
"""

import argparse
import json
import os
import sqlite3
from typing import Any, Dict, Optional, Union, Callable
import configparser
import re
from datetime import datetime
from shutil import copy2

DBTester = Dict[str, Union[str, int, float, bool]]
DBInputs = Dict[str, Union[str, int, float, bool]]


def infer_type(value: str) -> Union[int, float, bool, str]:
    """Infer Python type from string."""
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def identity(x: str) -> str:
    return x


def parse_ini_file(path: str) -> Dict[str, Dict[str, Any]]:
    """Parse a .ini file and return a section-key-value dictionary."""
    config = configparser.ConfigParser(strict=False)
    config.optionxform = identity  # preserve case
    config.read(path, encoding="utf-8")
    return {s: dict(config.items(s)) for s in config.sections()}


def load_job_types(job_folder: str) -> Optional[Dict[str, Union[DBTester, DBInputs]]]:
    """Try to load job types from job_config.json, fallback to current_config.ini."""
    jc_path = os.path.join(job_folder, "job_config.json")
    ini_path = os.path.join(job_folder, "current_config.ini")

    if os.path.exists(jc_path):
        with open(jc_path, encoding="utf-8") as f:
            jc = json.load(f)
        tester: DBTester = {
            k: infer_type(str(v)) for k, v in jc.get("tester", {}).items()
        }
        inputs_json: DBInputs = {
            k: infer_type(str(v["default"]))
            for k, v in jc.get("inputs", {}).items()
            if k.lower() != "symbols"
        }
        return {"tester": tester, "inputs": inputs_json}

    if os.path.exists(ini_path):
        config = configparser.ConfigParser(strict=False)
        config.optionxform = identity
        config.read(ini_path, encoding="utf-8")
        tester = {k: infer_type(v) for k, v in config.items("Tester")}
        inputs_ini: DBInputs = {}
        pattern = re.compile(r"(?P<key>\w+?)\s*=\s*(?P<default>[^|]+)\|\|")
        for line in config.items("TesterInputs"):
            match = pattern.match(line[1])
            if match:
                k = match.group("key")
                v = match.group("default")
                inputs_ini[k] = infer_type(v)
        return {"tester": tester, "inputs": inputs_ini}

    return None


def update_db_types(db_path: str, job_root: str, dry_run: bool = False) -> None:
    """Apply retyping to job and run records already present in the database."""

    # 🔒 Auto-backup before mutation (only if not a dry run)
    if not dry_run:
        backup_path = f"{db_path}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
        copy2(db_path, backup_path)
        print(f"💾 Backup saved to: {backup_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    jobs = sorted(os.listdir(job_root))
    updated: Dict[str, Any] = {}
    missing = []

    for job_id in jobs:
        folder = os.path.join(job_root, job_id)
        if not os.path.isdir(folder):
            continue

        result = load_job_types(folder)
        if not result:
            print(f"⚠️  Missing INI or config for {job_id}")
            continue

        # Update job table (tester_inputs)
        cursor.execute("SELECT id FROM jobs WHERE id = ? LIMIT 1", (job_id,))
        job_row = cursor.fetchone()
        if not job_row:
            missing.append(job_id)
            continue

        if dry_run:
            updated[job_id] = {
                "tester_inputs": result["tester"],
                "params_json": result["inputs"],
            }
        else:
            cursor.execute(
                "UPDATE jobs SET tester_inputs = ? WHERE id = ?",
                (json.dumps(result["tester"], default=str), job_id),
            )

        # Update runs (params_json)
        cursor.execute("SELECT id FROM runs WHERE job_id = ?", (job_id,))
        for row in cursor.fetchall():
            run_id = row[0]
            if dry_run:
                continue  # already captured in above
            cursor.execute(
                "UPDATE runs SET params_json = ? WHERE id = ?",
                (json.dumps(result["inputs"], default=str), run_id),
            )

    if not dry_run:
        conn.commit()
    conn.close()

    print(f"🧠 Found {len(jobs)} job(s) in '{job_root}'")
    if missing:
        print("⚠️  Found", len(missing), "job folder(s) not in DB — skipping:")
        for m in missing:
            print("  -", m)

    if dry_run:
        print(f"\n🧪 Dry Run: {len(updated)} job(s) would be updated.")
        preview_path = f"retype_dryrun_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(preview_path, "w", encoding="utf-8") as f:
            json.dump(updated, f, indent=2, default=str)
        print(f"📝 Preview written to {preview_path}")
    else:
        print(
            f"✅ Re-typed {len(jobs)-len(missing)} job(s) with updated tester_inputs and run params."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Re-type tester_inputs and params_json in the database."
    )
    parser.add_argument("--db", required=True, help="Path to OptiBatch SQLite DB")
    parser.add_argument(
        "--job-root", required=True, help="Path to job folder root (e.g., generated)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only preview changes without modifying DB",
    )
    args = parser.parse_args()

    update_db_types(args.db, args.job_root, args.dry_run)
