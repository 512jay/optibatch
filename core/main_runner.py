# File: optibatch/core/main_runner.py

from pathlib import Path
import json
from loguru import logger
from core.logging.logger import start_run_logger, stop_run_logger
from core.run_utils import create_run_folder, copy_core_files_to_run, launch_mt5_with_ini, wait_for_mt5_to_finish
from core.ini_writer import generate_ini_files
from core.state import registry


mt5_path = Path(registry.get("install_path", "C:/MT5/terminal64.exe"))

def run_optimizations(config_path: Path) -> None:
    logger.info("Run Optimizations triggered.")
    config_json = Path(config_path).read_text(encoding="utf-8")
    config = json.loads(config_json)

    # Extract EA name from path (handle Windows-style backslashes)
    ea_name = config["tester"]["Expert"].split("\\")[-1].split(".")[0]
    run_folder = create_run_folder(ea_name)

    # Save job name to registry for resume support
    job_name = run_folder.name
    registry.set("last_job_name", job_name)
    registry.save()

    sink_id = start_run_logger(run_folder)
    logger.info(f"Started new optimization run: {job_name}")

    try:
        ini_src = Path(".cache/current_config.ini")
        json_src = Path(".cache/current_config.json")
        copy_core_files_to_run(run_folder, ini_src, json_src)

        dry_run = registry.get("dry_run")
        logger.info(f"Dry run mode: {'ON' if dry_run else 'OFF'}")

        # Generate INI files for each symbol (with or without month splitting)
        ini_count = generate_ini_files(config, run_folder, dry_run=dry_run)
        logger.success(f"Generated {ini_count} INI files.")



        if not dry_run:
            from core.automation import optimize_with_mt5
            from core.run_utils import get_mt5_data_path

            mt5_path = Path(registry.get("install_path", "C:/MT5/terminal64.exe"))
            log_path = get_mt5_data_path(mt5_path)

            if not log_path:
                logger.error("Could not locate MT5 tester/logs folder.")
                return

            for symbol_folder in run_folder.iterdir():
                if not symbol_folder.is_dir():
                    continue
                for ini_file in sorted(symbol_folder.glob("*.ini")):
                    optimize_with_mt5(
                        ini_file=ini_file,
                        mt5_path=mt5_path,
                        log_path=log_path,
                        timeout=300
                    )

            logger.info("Launching MT5 and starting real optimizations...")
            for symbol_folder in run_folder.iterdir():
                if not symbol_folder.is_dir():
                    continue
                for ini_file in symbol_folder.glob("*.ini"):
                    logger.info(f"Launching MT5 with: {ini_file.name}")
                    launch_mt5_with_ini(ini_file, mt5_path)

                    success = wait_for_mt5_to_finish(tester_log_dir, time.time())
                    if success:
                        logger.success(f"Optimization completed for: {ini_file.name}")
                    else:
                        logger.error(f"Timeout or failure for: {ini_file.name}")
    except Exception as e:
        logger.exception(f"Unexpected error during run: {e}")
    finally:
        stop_run_logger(sink_id)
        logger.info(f"Optimization run complete: {job_name}")
