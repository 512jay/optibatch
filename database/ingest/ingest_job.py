# File: ingestion/ingest_job.py
# Purpose: Ingest MT5 optimization XML + config into PostgreSQL
# Notes: This script parses job_config.json and multiple XMLs, populating structured runs

import re
import json
import hashlib
from pathlib import Path
from datetime import datetime, date
from calendar import monthrange
from xml.etree import ElementTree as ET
from typing import Any, Optional, List, Dict, Union, Tuple
from sqlalchemy.orm import Session
from database.models import Job, Run
from database.session import get_engine, get_session
from loguru import logger
import re
from datetime import datetime
from typing import Any

def coerce_tester_value(key: str, val: str) -> Any:
    val = val.strip()

    int_keys = {
        "deposit",
        "leverage",
        "model",
        "profitinpips",
        "optimization",
        "optimizationcriterion",
        "executionmode",
        "forwardmode",
    }

    date_keys = {"fromdate", "todate"}

    try:
        if key.lower() in int_keys:
            return int(val)
        if key.lower() in date_keys:
            return datetime.strptime(val, "%Y.%m.%d").date()
    except Exception:
        pass

    return val  # fallback to string


def parse_input_types_from_json(path: Path) -> dict[str, type]:
    with open(path, encoding="utf-8-sig") as f:
        config = json.load(f)
    inputs = config.get("inputs", {})

    def infer_type(val: Any) -> type:
        try:
            if isinstance(val, bool):
                return bool
            elif isinstance(val, int):
                return int
            elif isinstance(val, float):
                return float
            elif isinstance(val, str):
                # Try to guess from string
                if val.lower() in {"true", "false"}:
                    return bool
                elif "." in val:
                    float(val)
                    return float
                else:
                    int(val)
                    return int
        except Exception:
            pass
        return str

    return {
        k: infer_type(v.get("default", v.get("value", ""))) for k, v in inputs.items()
    }


def parse_input_types_from_ini(ini_path: Path) -> dict[str, type]:
    """
    Returns a dict mapping each input name to its best-guessed type based on the ini values.
    """
    from configparser import ConfigParser

    config = ConfigParser(strict=False, delimiters=("=",))
    config.optionxform = str  # preserve case
    config.read(ini_path, encoding="utf-8")

    input_types: dict[str, type] = {}

    if "TesterInputs" not in config:
        return input_types

    for key, val in config["TesterInputs"].items():
        if key.startswith(";"):
            continue  # skip headers or comments

        try:
            first_val = val.split("||")[0].strip().lower()

            if first_val in {"true", "false"}:
                input_types[key] = bool
            elif first_val == "":
                input_types[key] = str
            elif "." in first_val:
                float(first_val)  # validate
                input_types[key] = float
            else:
                int(first_val)  # validate
                input_types[key] = int
        except Exception:
            input_types[key] = str  # fallback

    return input_types


def extract_strategy_version(expert_path: str) -> str | None:
    """
    Extracts the strategy version from an expert filename.
    Supports formats like:
    - IndyTSL_v2.ex5
    - IndyTSL_v1_3_0.ex5
    - IndyTSL_v2.1.4.ex5
    """
    match = re.search(r"_v(\d+(?:[_\.]\d+)*)", expert_path)
    if match:
        # Normalize underscores to dots for consistent version formatting
        return match.group(1).replace("_", ".")
    return None


def generate_result_hash(
    symbol: str,
    modeling_mode: str,
    start_date: date,
    end_date: date,
    inputs: dict[str, Any],
    strategy_version: str,
    summary: dict[str, float],
) -> str:
    key = {
        "symbol": symbol,
        "modeling_mode": modeling_mode,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "inputs": dict(sorted(inputs.items())),
        "strategy_version": strategy_version,
        "summary": summary,  # optional, but useful for deduping results
    }
    encoded = json.dumps(key, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(encoded.encode()).hexdigest()


def extract_job_metadata(config_path: Path) -> dict:
    with config_path.open("r", encoding="utf-8") as f:
        job_config = json.load(f)

    tester = job_config["tester"]
    expert_path = tester.get("Expert", "")
    strategy_version = extract_strategy_version(expert_path)
    if not strategy_version:
        logger.warning(f"Could not extract version from {expert_path}")

    raw_inputs = job_config.get("inputs", {})

    def safe(x: str | None) -> str:
        return "" if x is None or str(x).lower() == "none" else str(x)

    full_inputs = {}
    for key, param in raw_inputs.items():
        if isinstance(param, dict) and all(
            k in param for k in ["default", "start", "step", "end"]
        ):
            formatted = f"{safe(param['default'])}||{safe(param['default'])}||{safe(param['start'])}||{safe(param['end'])}||{'Y' if param.get('optimize', False) else 'N'}"
        else:
            val = param.get("value") if isinstance(param, dict) else param
            formatted = f"{safe(val)}||{safe(val)}||{safe(val)}||{safe(val)}||N"
        full_inputs[key] = formatted

    return {
        "expert_name": Path(tester["Expert"]).stem,
        "strategy_version": strategy_version,
        "expert_path": tester["Expert"],
        "model": str(tester.get("Model", "0")),
        "period": str(tester.get("Period", "")),  # ✅ add this
        "optimization_mode": str(tester.get("Optimization", "")),  # ✅ add this
        "optimization_criterion": str(tester.get("OptimizationCriterion", "")),
        "deposit": float(tester["Deposit"]),
        "currency": tester["Currency"],
        "leverage": int(tester["Leverage"]),
        "tester_inputs": full_inputs,
    }


def extract_symbol_and_dates_from_xml(xml_path: Path) -> Tuple[str, date, date, str]:
    """Parse <Title> from DocumentProperties to extract symbol and date range."""
    tree = ET.parse(xml_path)
    ns = {"o": "urn:schemas-microsoft-com:office:office"}
    title = tree.findtext(".//o:Title", namespaces=ns)
    if not title:
        raise ValueError(f"⚠️ No <Title> in {xml_path.name}")

    try:
        parts = title.strip().split()
        symbol = parts[1].split(",")[0]
        date_range = parts[-1]  # e.g. 2023.03.01-2023.03.31
        start_str, end_str = date_range.split("-")
        start = datetime.strptime(start_str, "%Y.%m.%d").date()
        end = datetime.strptime(end_str, "%Y.%m.%d").date()
        run_month = f"{start.year}-{start.month:02}"
        return symbol, start, end, run_month
    except Exception as e:
        raise ValueError(f"⚠️ Could not parse Title in {xml_path.name}: {e}")


def is_discrete_month(start: date, end: date) -> bool:
    """Returns True if the start and end dates span exactly one calendar month."""
    return (
        start.day == 1
        and start.year == end.year
        and start.month == end.month
        and end.day == monthrange(start.year, start.month)[1]
    )


def extract_runs_from_xml(xml_path: Path) -> list[dict]:
    """Extract all optimization runs from a given XML file."""
    tree = ET.parse(xml_path)
    ns = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}

    header_row = tree.find(".//ss:Table/ss:Row", namespaces=ns)
    if header_row is None:
        logger.warning(f"No header row found in {xml_path.name}")
        return []

    headers = [
        cell.findtext("ss:Data", default="", namespaces=ns)
        for cell in header_row.findall("ss:Cell", namespaces=ns)
    ]
    data_rows = tree.findall(".//ss:Table/ss:Row", namespaces=ns)[1:]  # skip header
    results = []

    for i, row in enumerate(data_rows):
        cells = [
            cell.findtext("ss:Data", default="", namespaces=ns)
            for cell in row.findall("ss:Cell", namespaces=ns)
        ]
        if not cells:
            continue
        record = dict(zip(headers, cells))
        record["pass_number"] = str(i)
        results.append(record)

    logger.info(f"✅ Parsed {len(results)} passes from {xml_path.name}")
    return results


def ingest_job_folder(folder: Path, config_path: Path | None = None) -> int:
    """
    Ingest all XML result files in a job folder (generated/YYYYMMDD_HHMMSS_NAME).

    Automatically creates the Job record and commits all runs.
    """
    engine = get_engine()
    config_path = config_path or (folder / "job_config.json")
    job_id = folder.name
    total_runs = 0

    with get_session(engine) as session:
        # Create Job record if missing
        from database.models import Job

        job_meta = extract_job_metadata(config_path)
        job = Job(
            id=job_id, job_name=job_id, created_at=datetime.utcnow(), **job_meta
        )

        runs_to_add: list[Run] = []

        for xml_file in folder.rglob("*.xml"):
            added = ingest_single_xml(
                xml_file,
                config_path,
                session=session,
                job_id=job_id,
                preloaded_job=job,           # we'll add this param next
                collect_only=True            # new param
            )
            if added:
                runs_to_add.extend(added)
                logger.info(f"📥 Parsed {len(added)} runs from {xml_file.name}")

        if runs_to_add:
            session.add(job)
            for run in runs_to_add:
                session.add(run)
            session.commit()
            logger.success(f"✅ Ingested {len(runs_to_add)} runs from job: {job_id}")
        else:
            logger.warning(f"⚠️ Skipping job '{job_id}' — all runs were duplicates or empty.")
            return 0

        session.commit()

    logger.success(f"✅ Ingested {total_runs} runs from job: {job_id}")
    return total_runs


def ingest_single_xml(
    xml_path: Path,
    config_path: Path,
    session: Session | None = None,
    job_id: str = "",
    preloaded_job: Job | None = None,
    collect_only: bool = False,
) -> list[Run] | int:

    """
    Ingest a single MT5 XML result file and commit all runs to the database.

    - If no session is passed, creates one automatically.
    - Calculates derived metrics: expected_payoff, recovery_factor, custom_score
    """
    added_runs: list[Run] = []
    owns_session = session is None
    engine = get_engine() if owns_session else None
    session = session or get_session(engine).__enter__()

    try:
        job_meta = extract_job_metadata(config_path)
        symbol, start_date, end_date, run_month = extract_symbol_and_dates_from_xml(
            xml_path
        )
        raw_runs = extract_runs_from_xml(xml_path)
        skipped_zero_trades = 0
        total = 0

        for record in raw_runs:
            trades = int(record.get("Trades", 0))
            if trades == 0:
                skipped_zero_trades += 1
                continue


            if config_path.name.endswith(".json"):
                input_type_map = parse_input_types_from_json(config_path)
            else:
                input_type_map = parse_input_types_from_ini(config_path)


            inputs = {}
            for k, v in record.items():
                if not k.startswith("input_"):
                    continue
                val = v.strip()
                expected_type = input_type_map.get(k, str)
                try:
                    if expected_type == bool:
                        inputs[k] = val.lower() == "true"
                    elif expected_type == float:
                        inputs[k] = float(val)
                    elif expected_type == int:
                        inputs[k] = int(float(val))  # allow "2.0" style ints
                    else:
                        inputs[k] = val
                except Exception:
                    inputs[k] = val

            profit = float(record.get("Profit", 0))
            drawdown_str = record.get("Equity DD %", "0").replace("%", "").strip()
            drawdown = float(drawdown_str) if drawdown_str else 0.0
            sharpe_ratio = float(record.get("Sharpe Ratio", 0))
            profit_factor = float(record.get("Profit Factor", 0))
            recovery_factor = float(record.get("Recovery Factor", 0))
            expected_payoff = float(record.get("Expected Payoff", 0))
            result = float(record.get("Result", 0))
            custom_score = profit - (drawdown * 2)

            run = Run(
                job_id=job_id,
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                run_month=run_month,
                is_full_month=is_discrete_month(start_date, end_date),
                pass_number=int(record["pass_number"]),
                result=result,
                profit=profit,
                drawdown=drawdown,
                sharpe_ratio=sharpe_ratio,
                trades=trades,
                expected_payoff=expected_payoff,
                recovery_factor=recovery_factor,
                profit_factor=profit_factor,
                custom_score=custom_score,
                params_json=inputs,
                result_hash = generate_result_hash(
                    symbol=symbol,
                    modeling_mode=job_meta["model"],
                    start_date=start_date,
                    end_date=end_date,
                    inputs=inputs,
                    strategy_version=job_meta["strategy_version"],
                    summary={"profit": profit, "drawdown": drawdown, "trades": trades}
                ),

                created_at=datetime.utcnow(),
            )

            if session.query(Run).filter_by(result_hash=run.result_hash).first():
                logger.info(f"🛑 Duplicate run skipped: {run.result_hash}")
                continue

            if collect_only:
                run.job = preloaded_job
                added_runs.append(run)
            else:
                session.add(run)

            total += 1

        if owns_session:
            if skipped_zero_trades:
                logger.info(f"📭 Skipped {skipped_zero_trades} runs with 0 trades in {xml_path.name}")
            session.commit()
            logger.info(f"💾 Committed {total} runs from {xml_path.name}")
    finally:
        if owns_session:
            session.close()

    if collect_only:
        return added_runs
    else:
        return total
