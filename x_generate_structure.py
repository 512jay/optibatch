import fnmatch
import os
import sys


def load_gitignore():
    """Loads patterns from .gitignore and returns them as a list of ignored patterns."""
    gitignore_path = ".gitignore"
    ignore_patterns = []

    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):  # Ignore comments and empty lines
                    ignore_patterns.append(line)

    return ignore_patterns


def is_ignored(path, ignore_patterns, ignored_dirs):
    """Checks if a given file or directory should be ignored based on .gitignore and predefined rules."""
    if any(
        fnmatch.fnmatch(path, pattern)
        or fnmatch.fnmatch(os.path.basename(path), pattern)
        for pattern in ignore_patterns
    ):
        return True
    if any(
        ignored_dir in path for ignored_dir in ignored_dirs
    ):  # Check ignored directories
        return True
    return False


def generate_structure(root_dir, ignore_patterns, ignored_dirs, prefix=""):
    """Recursively lists the directory structure while respecting .gitignore and ignoring unnecessary files."""
    structure = []
    try:
        entries = sorted(os.listdir(root_dir))  # Sort for consistent output
    except PermissionError:
        return structure

    for entry in entries:
        full_path = os.path.join(root_dir, entry)

        # Skip ignored files/directories
        if is_ignored(full_path, ignore_patterns, ignored_dirs):
            continue

        structure.append(f"{prefix}├── {entry}")

        if os.path.isdir(full_path):  # If it's a directory, recurse
            structure.extend(
                generate_structure(
                    full_path, ignore_patterns, ignored_dirs, prefix + "│   "
                )
            )

    return structure


def save_structure_to_markdown(structure):
    """Saves the project structure to a markdown file inside the 'docs/' folder."""
    docs_folder = "docs"
    md_file_path = os.path.join(docs_folder, "_current_project_structure.md")

    if not os.path.exists(docs_folder):
        os.makedirs(docs_folder)  # Ensure docs folder exists

    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write("# JedgeBot Project Structure\n\n")
        f.write("```\n")
        f.write("\n".join(structure))
        f.write("\n```\n")

    print(f"✅ Project structure saved to {md_file_path}")


if __name__ == "__main__":
    ignored_dirs = [
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".tox",
        ".idea",
        ".vscode",
        ".git",
        "node_modules",
        "dist",
        "build",
        ".egg-info",
    ]  # Explicitly ignored directories

    print("Generating Project Structure...")
    ignore_patterns = load_gitignore()
    structure = ["JedgeBot/"] + generate_structure(
        ".", ignore_patterns, ignored_dirs, prefix="│   "
    )

    save_structure_to_markdown(structure)
    print(
        "✅ Done! Check `docs/_current_project_structure.md` for the updated project structure."
    )
