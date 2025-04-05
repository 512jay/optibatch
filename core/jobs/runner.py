# File: core/jobs/runner.py
from tkinter import filedialog, messagebox
from pathlib import Path
import json
import subprocess

from state.app_state import AppState
from core.jobs.settings import load_settings
from core.tools.ini_utils import generate_ini_files_from_job


def resume_job(job_path: Path, terminal_path: Path):
    """
    Launch MT5 in config-driven batch mode using .ini files created from the job file.
    """
    ini_files = generate_ini_files_from_job(job_path)
    for ini in ini_files:
        subprocess.run([str(terminal_path), f"/config:{ini}"])


def pick_and_resume_job():
    file_path = filedialog.askopenfilename(
        filetypes=[("Job Config", "*.json")],
        initialdir="jobs",
        title="Select a Job File",
    )
    if not file_path:
        return

    settings = load_settings()
    terminal_path = Path(settings.get("terminal_path", ""))

    if terminal_path.exists():
        resume_job(Path(file_path), terminal_path)
    else:
        messagebox.showerror("Error", "Terminal path not found.")
