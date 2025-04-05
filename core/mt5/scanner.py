from pathlib import Path
import re


def get_broker_name(data_path: Path) -> str:
    # Try config/terminal.ini (older method)
    config_file = data_path / "config" / "terminal.ini"
    if config_file.exists():
        try:
            with config_file.open(encoding="utf-16") as f:
                for line in f:
                    if line.strip().lower().startswith("broker="):
                        return line.strip().split("=")[-1]
        except Exception:
            pass

    # Try latest valid session log files for "authorized on <broker>"
    logs_dir = data_path / "logs"
    if logs_dir.exists() and logs_dir.is_dir():
        log_files = sorted(
            [f for f in logs_dir.glob("*.log") if f.name[:8].isdigit()],
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )
        for log_file in log_files:
            try:
                with log_file.open(encoding="utf-16") as f:
                    for line in f:
                        match = re.search(r"authorized on ([^\s]+)", line)
                        if match:
                            return match.group(1)
            except Exception:
                continue

    return "(Unknown Broker)"


def scan_mt5_from_origin(base_path: Path):
    found = []
    for folder in base_path.iterdir():
        if not folder.is_dir():
            continue
        origin_file = folder / "origin.txt"
        if origin_file.exists():
            try:
                origin_path = Path(origin_file.read_text(encoding="utf-16").strip())
                terminal_exe = origin_path / "terminal64.exe"
                if terminal_exe.exists():
                    found.append(
                        {
                            "terminal_path": str(terminal_exe),
                            "data_path": str(folder.resolve()),
                            "broker_name": get_broker_name(folder),
                        }
                    )
            except Exception as e:
                print(f"⚠️ Failed to read {origin_file}: {e}")
    return found
