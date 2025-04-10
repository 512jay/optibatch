# core/tools/symbol_dumper.py

import subprocess
from pathlib import Path
import time
import shutil

from core.process import kill_mt5

DUMP_SCRIPT_NAME = "DumpSymbols.mq5"
COMPILED_NAME = "DumpSymbols.ex5"


def get_metaeditor_path(terminal_path: Path) -> Path:
    return terminal_path.parent / "metaeditor64.exe"


def write_dump_script(script_path: Path):
    content = """
void OnStart()
{
    int total = SymbolsTotal(false);
    int file = FileOpen("symbols.txt", FILE_WRITE | FILE_ANSI);
    if (file != INVALID_HANDLE)
    {
        for (int i = 0; i < total; i++)
        {
            string sym = SymbolName(i, false);
            FileWrite(file, sym);
        }
        FileClose(file);
    }
}
    """.strip()
    script_path.write_text(content, encoding="utf-8")


def compile_mq5(metaeditor_path: Path, script_path: Path):
    result = subprocess.run(
        [str(metaeditor_path), "/compile:", str(script_path), "/log:compile_log.txt"],
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError("❌ Compilation failed. Check compile_log.txt")

    # Wait a moment for file system to catch up
    time.sleep(1)

    # Move .ex5 to destination location
    compiled_output = script_path.with_suffix(".ex5")
    if compiled_output.exists():
        shutil.copy(compiled_output, script_path.parent / COMPILED_NAME)
        compiled_output.unlink()
    else:
        raise FileNotFoundError("❌ Compiled file not found.")


def run_mt5_script(terminal_path: Path, script_name: str, ini_path: Path):
    subprocess.Popen([str(terminal_path), f"/config:{ini_path}"])


def dump_symbols_via_mt5_auto(terminal_path_str: str, data_path_str: str) -> bool:
    terminal_path = Path(terminal_path_str)
    data_path = Path(data_path_str)
    metaeditor_path = get_metaeditor_path(terminal_path)

    scripts_dir = data_path / "MQL5" / "Scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)

    script_path = scripts_dir / DUMP_SCRIPT_NAME

    # Step 1: Create DumpSymbols.mq5
    write_dump_script(script_path)

    # Step 2: Compile it
    compile_mq5(metaeditor_path, script_path)

    # Step 3: Kill MT5 before launching script
    kill_mt5(str(terminal_path))

    # Step 4: Build .ini file
    ini_dir = Path("temp")
    ini_dir.mkdir(parents=True, exist_ok=True)
    ini_path = ini_dir / "dump_symbols.ini"

    ini_content = f"""
[Experts]
AllowAlgoTrading=true
EnableExperts=true
AllowDllImport=true
EnableAlerts=false

[Tester]
Expert={script_path.stem}
Symbol=EURUSD
Period=H1
Model=0
Optimization=0
FromDate=2024.01.01
ToDate=2025.01.01
    """.strip()
    ini_path.write_text(ini_content)

    # Step 5: Run MT5 silently
    run_mt5_script(terminal_path, script_path.stem, ini_path)

    # Step 6: Wait for output
    symbols_file = data_path / "MQL5" / "Files" / "symbols.txt"
    for _ in range(30):
        if symbols_file.exists():
            print("✅ symbols.txt dumped successfully.")
            return True
        time.sleep(1)

    print("❌ Failed to generate symbols.txt in time.")
    return False
