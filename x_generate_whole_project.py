# File: x_generate_whole_project.py

import fnmatch
import os
import subprocess
import argparse
from typing import List, Tuple

excluded_files = {
    "x_generate_whole_project.py",
    "x_generate_structure.py",
    "./x_generate_whole_project.py",
    "./x_generate_structure.py"
}


def load_gitignore() -> List[str]:
    gitignore_path = ".gitignore"
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

def is_ignored(path: str, ignore_patterns: List[str], ignored_dirs: List[str]) -> bool:
    return (
        any(fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(os.path.basename(path), pat) for pat in ignore_patterns)
        or any(ignored_dir in path for ignored_dir in ignored_dirs)
    )

def is_package_metadata_file(path: str) -> bool:
    """Returns True if the file is a known dependency/lockfile or contains [package] markers."""
    basename = os.path.basename(path).lower()
    if basename in {"poetry.lock", "requirements.txt", "pyproject.toml", "pdm.lock", "pdm.toml"}:
        return True

    if basename.endswith(".toml") or basename.endswith(".cfg"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                head = f.read(512)
                return "[package" in head or "[tool.poetry]" in head or "[project]" in head
        except Exception:
            return False
    return False

def has_python_files(path: str) -> bool:
    try:
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isfile(full_path) and entry.endswith(".py"):
                return True
            if os.path.isdir(full_path):
                for sub in os.listdir(full_path):
                    if sub.endswith(".py"):
                        return True
    except Exception:
        pass
    return False

def generate_summary_structure(root_dir: str, ignore_patterns: List[str], ignored_dirs: List[str]) -> List[str]:
    structure: List[str] = []
    include_dot_dirs = {".streamlit"}

    for entry in sorted(os.listdir(root_dir)):
        full_path = os.path.join(root_dir, entry)

        if is_ignored(full_path, ignore_patterns, ignored_dirs):
            continue

        if entry.startswith(".") and entry not in include_dot_dirs:
            continue

        if os.path.isdir(full_path) and (has_python_files(full_path) or entry in include_dot_dirs):
            structure.append(f"├── {entry}/")
            for sub in sorted(os.listdir(full_path)):
                sub_path = os.path.join(full_path, sub)
                if os.path.isdir(sub_path):
                    structure.append(f"│   ├── {sub}/")
                    for subsub in sorted(os.listdir(sub_path)):
                        if subsub.endswith(".py"):
                            structure.append(f"│   │   └── {subsub}")
                elif sub.endswith(".py") or entry in include_dot_dirs:
                    structure.append(f"│   └── {sub}")
        elif os.path.isfile(full_path) and entry.endswith(".py") and entry not in excluded_files:
            structure.append(f"├── {entry}")

    return structure

def generate_full_structure(
    root_dir: str,
    ignore_patterns: List[str],
    ignored_dirs: List[str],
    prefix: str = ""
) -> Tuple[List[str], List[str]]:
    structure: List[str] = []
    file_dumps: List[str] = []

    try:
        entries = sorted(os.listdir(root_dir))
    except PermissionError:
        return structure, file_dumps

    for entry in entries:
        full_path = os.path.join(root_dir, entry)
        rel_path = os.path.relpath(full_path, ".")

        if is_ignored(full_path, ignore_patterns, ignored_dirs):
            continue
        if os.path.basename(full_path) in excluded_files or rel_path.replace("\\", "/") in excluded_files:
            continue
        if is_package_metadata_file(full_path):
            continue

        structure.append(f"{prefix}├── {entry}")

        if os.path.isdir(full_path):
            substructure, subfiles = generate_full_structure(
                full_path, ignore_patterns, ignored_dirs, prefix + "│   "
            )
            structure.extend(substructure)
            file_dumps.extend(subfiles)
        elif os.path.isfile(full_path):
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                file_dumps.append(f"\n--- {rel_path} ---\n```python\n{content}\n```")
            except Exception as e:
                print(f"⚠️ Skipped unreadable file: {rel_path} — {e}")

    return structure, file_dumps

def save_to_markdown(structure: List[str], files: List[str], full: bool = False) -> None:
    docs_folder = "docs"
    md_file_path = os.path.join(docs_folder, "_current_project_structure.md")

    if not os.path.exists(docs_folder):
        os.makedirs(docs_folder)

    with open(md_file_path, "w", encoding="utf-8") as f:
        project_name = os.path.basename(os.path.abspath("."))
        f.write("# Project Structure\n\n")
        f.write("```\n")
        f.write(f"{project_name}/\n")
        f.write("\n".join(structure))
        f.write("\n```\n")
        if full and files:
            f.write("\n\n# File Contents\n")
            f.write("\n".join(files))

    print(f"✅ Saved to {md_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate project structure and optionally file contents.")
    parser.add_argument("--full", action="store_true", help="Include full tree and file contents")
    args = parser.parse_args()

    ignored_dirs = [
        ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache",
        ".tox", ".idea", ".vscode", ".git", "node_modules", "dist",
        "build", ".egg-info", "site-packages", ".cache", "env", ".env"
    ]

    ignore_patterns = load_gitignore()

    if args.full:
        print("🔍 Generating full project structure with file contents...")
        structure, file_dumps = generate_full_structure(".", ignore_patterns, ignored_dirs)
        save_to_markdown(structure, file_dumps, full=True)
    else:
        print("🔍 Generating top-level summary with first-level contents...")
        structure = generate_summary_structure(".", ignore_patterns, ignored_dirs)
        save_to_markdown(structure, files=[], full=False)

    print("✅ Done!")
