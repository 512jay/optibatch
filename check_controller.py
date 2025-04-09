# mt5/test_controller.py

from pathlib import Path
import time
from mt5 import controller

# Define the path to your MT5 portable terminal
mt5_path = Path("C:/MT5/FOREX.com US")  # Adjust as needed

# Optional: path to an .ini file that defines strategy and backtest parameters
ini_file = Path(
    'C:/MT5/FOREX.com US/example.ini'
)  # You can use None to launch without a config

if __name__ == "__main__":
    # 1. Kill any existing MT5 instance launched from this folder
    print("🔪 Killing MT5 if running...")
    controller.kill_mt5(mt5_path)

    # 2. Launch MT5 in portable mode with an optional .ini config
    print("🚀 Launching MT5...")
    controller.launch_mt5()#(mt5_path, ini_file)

    # 3. Wait a few seconds to ensure MT5 has time to start
    print("⏳ Waiting for MT5 to initialize...")
    # Wait until the window actually appears
    print("🕵️ Waiting for MT5 window to appear...")
    hwnd = controller.wait_for_mt5_window(mt5_path)
    if hwnd:
        print("✅ MT5 window detected.")
        # Capture and restore as usual
        original_geom = controller.get_mt5_window_geometry(mt5_path)
        controller.restore_mt5_window_position(mt5_path, original_geom)
    else:
        print("❌ MT5 window did not appear in time.")

    # 4. Optionally capture the window's current position BEFORE anything moves it
    #    This allows you to restore it after MT5 possibly repositions itself
    print("📐 Capturing window position...")
    original_geom = controller.get_mt5_window_geometry(mt5_path)
    if original_geom:
        print(f"🧭 Saved window geometry: {original_geom}")
    else:
        print("⚠️ Could not get MT5 window geometry.")

    # 5. Check if MT5 is running from the expected folder
    print("🔍 Checking if MT5 is running...")
    if controller.is_mt5_running(mt5_path):
        print("✅ MT5 is running.")
    else:
        print("❌ MT5 is NOT running.")

    # 6. Attempt to bring the MT5 window to the front (if visible)
    print("🎯 Bringing MT5 window to front...")
    controller.focus_mt5(mt5_path)

    # 7. Restore window to the original position (if previously captured)
    print("📦 Restoring MT5 window position...")
    controller.restore_mt5_window_position(mt5_path, original_geom)
