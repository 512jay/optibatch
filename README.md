# 🧠 Optibach

**Optibach** is a Python-based GUI tool that simplifies the automation of MT5 strategy optimization using `.ini` Tester configuration files. It enables users to configure, generate, and run backtests and optimizations — with support for multi-symbol strategies and batch management.

---

## ✨ Features

- ✅ Easy GUI to configure strategies, symbols, and timeframes
- 📂 Load existing `.ini` files and auto-populate fields
- 🖁️ Resume previously saved jobs
- 🗕️ Built-in date pickers and dropdowns for optimization options
- 🧪 Generate and save `.ini` files for each symbol in a job
- 🚀 Run optimizations directly in MT5 with auto-launch
- 🧹 Organizes jobs by date and label
- 🗞️ Export results to CSV/HTML

---

## 🗂️ Project Structure

```bash
.
├── main_app.py              # Tkinter GUI entry point
├── README.md
├── settings.json            # MT5 terminal config
├── cache/                   # Temporary or cached files (e.g., symbol dumps)
├── jobs/                    # Generated jobs and associated .ini files
├── exports/                 # Exported backtest results (CSV, HTML)
│
├── core/
│   ├── jobs/                # Job lifecycle: validation, generation, running
│   │   ├── generator.py
│   │   ├── runner.py
│   │   └── validator.py
│   ├── mt5/                 # MT5 interaction logic
│   │   ├── mt5_process.py
│   │   ├── symbol_dumper.py
│   │   └── symbol_loader.py
│
├── ini_utilities/           # INI loading, writing, formatting
│   ├── ini_loader.py
│   ├── ini_writer.py
│   └── ini_utils.py
│
├── helpers/                 # Shared logic and enums
│   ├── enums.py
│   └── path_utils.py
│
├── state/                   # App-wide state tracking
│   └── app_state.py
│
├── ui/                      # GUI components and widgets
│   ├── date_picker.py
│   ├── input_editor.py
│   └── symbol_picker.py
│
└── tests/                   # Pytest-based unit tests
    └── ini_utilities/
        ├── test_ini_loader.py
        └── ...
```

---

## 🚀 Running the App

```bash
# Activate your virtual environment
.venv/Scripts/activate

# Launch the GUI
python main_app.py
```

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🛠 Requirements

- Python 3.11+
- MT5 installed (path configured in `settings.json`)
- `psutil`, `tkinter`, `pytest`, `mypy`, etc.

---

## 📌 Related Files

- `settings.json`: Stores paths to MT5 terminal and data directories
- `.gitignore`: Excludes `/cache/`, `.opt` files, and MT5 logs

---

## 📌 Notes

- Job configs (`job_*.json`) are saved to `jobs/` with a timestamp and index
- Generated `.ini` files are UTF-16 encoded and follow MT5 formatting
- Each job folder may contain multiple `.ini` files (one per symbol)

---

## 🧠 Future Plans

- [ ] CLI version for power users
- [ ] Job queue with scheduling
- [ ] Result visualization
- [ ] Upload jobs to cloud for distributed testing

---

## 👤 Author

Developed by **512jay** for Dharmesh and other algo strategy users.

