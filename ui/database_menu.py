# File: ui/database_menu.py

import tkinter as tk
from tkinter import Menu, messagebox, simpledialog, filedialog, scrolledtext, Toplevel
import subprocess
import threading


def build_database_menu(root: tk.Tk) -> Menu:
    """Creates a 'Database' top-level menu with common DB operations."""
    menu = Menu(root, tearoff=0)

    def run_db_command(title: str, command: list[str]) -> None:
        if not messagebox.askyesno(
            "Confirm", f"Are you sure you want to run: {title}?"
        ):
            return

        output_window = Toplevel(root)
        output_window.title(f"{title} Output")
        output_window.geometry("600x300")

        log_area = scrolledtext.ScrolledText(output_window, wrap="word", state="normal")
        log_area.pack(expand=True, fill="both")
        log_area.insert("end", f"Running: {' '.join(command)}\n\n")

        def task():
            try:
                process = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
                )
                for line in process.stdout:
                    log_area.insert("end", line)
                    log_area.see("end")
                process.wait()
                if process.returncode == 0:
                    messagebox.showinfo("Success", f"{title} completed successfully.")
                else:
                    messagebox.showerror(
                        "Failure", f"{title} failed. Return code: {process.returncode}"
                    )
            except Exception as e:
                log_area.insert("end", f"\nERROR: {e}")
                messagebox.showerror("Error", f"{title} failed:\n{e}")

        threading.Thread(target=task, daemon=True).start()

    def create_database():
        pw = simpledialog.askstring(
            "DB Password", "Enter password for postgres user:", show="*"
        )
        if not pw:
            return
        run_db_command(
            "Create Database",
            ["psql", "-U", "postgres", "-c", "CREATE DATABASE optibatch;"],
        )

    def initialize_tables():
        pw = simpledialog.askstring(
            "DB Password", "Enter password for postgres user:", show="*"
        )
        if not pw:
            return
        run_db_command("Initialize Tables", ["python", "-m", "database.init_db"])

    def ingest_folder():
        folder = filedialog.askdirectory(title="Select Folder to Ingest")
        if not folder:
            return
        run_db_command(
            "Manual Ingest", ["python", "-m", "database.ingest.ingest_job", folder]
        )

    menu.add_command(label="Create Database", command=create_database)
    menu.add_command(label="Initialize Tables", command=initialize_tables)
    menu.add_command(label="Manual Ingest Folder", command=ingest_folder)
    return menu
