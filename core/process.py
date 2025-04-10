import psutil
from pathlib import Path
# from trash.config import config
from core.state import registry

def kill_mt5(target_path: str = None) -> None:
    """
    Silently kills only the MT5 terminal64.exe process that matches the full path.

    Args:
        target_path (str): Full path to terminal64.exe from settings.json
    """
    if not target_path:
        target_path = registry.get("terminal_path")
        if not target_path:
            print("❌ No MT5 path provided and no terminal_path found in app_settings.json.")
            return
    else:
        target_path = str(Path(target_path).resolve()).lower()
    killed = 0

    for proc in psutil.process_iter(["pid", "name", "exe"]):
        try:
            exe_path = proc.info.get("exe")
            if (
                proc.info["name"]
                and "terminal64.exe" in proc.info["name"].lower()
                and exe_path
                and str(Path(exe_path).resolve()).lower() == target_path
            ):
                proc.kill()
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if killed:
        print(f"🔪 Killed {killed} MT5 process(es) at {target_path}")
    else:
        print(f"✅ No running MT5 instance found at {target_path}")
