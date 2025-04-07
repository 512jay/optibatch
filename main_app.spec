# File: main_app.spec

from PyInstaller.utils.hooks import collect_submodules
from pathlib import Path
import json

# Project root directory
project_root = Path(".").resolve()

# Additional non-code files (like settings.json)
data_files = [
    (str(project_root / "settings.json"), "settings.json"),
]

# Add your app entry script
a = Analysis(
    ['main_app.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=data_files,
    hiddenimports=collect_submodules("core") + collect_submodules("state"),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# This block builds a console (terminal) version, so logs are visible
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='OptibatchApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # <- ✅ Shows log output in terminal window
    icon=None,
)

