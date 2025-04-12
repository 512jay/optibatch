from pathlib import Path
from datetime import datetime


def write_job_readme(run_folder: Path, ea_name: str, symbol_folders: list[str]) -> None:
    readme_path = run_folder / "README.md"
    readme_path.write_text(
        f"""\
# 📝 Job Summary: {run_folder.name}

- **Expert Advisor**: {ea_name}
- **Created At**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Symbols**: {', '.join(symbol_folders)}

## Folder Contents

- `job_config.json` — Strategy config used for this run
- `current_config.ini` — Base .ini file from GUI
- `<symbol>/` folders — Contain .ini and .xml files per symbol

## Resume Tip

Use the Optibatch GUI → "⏭️ Continue Previous" to resume this job.
"""
    )
