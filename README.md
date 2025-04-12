Great — let’s modernize your `README.md` to reflect the full power of OptiBatch as it stands now.

---

## ✅ Key Enhancements to Add

1. **"Continue Previous Job"** logic with `job_config.json`
2. **Job folder cleanup + XML auto-routing**
3. **Run skipping if XML already exists**
4. ✅ Clarify real folder names: `.cache/`, `generated/`, `reports/`
5. ✅ Mention `job_config.json` and `current_config.json` clearly

---

## ✍️ Updated `README.md`

```markdown
# 🧠 Optibatch

**Optibatch** is a Python-based GUI tool that automates MT5 strategy optimizations using `.ini` Tester configuration files. It supports batch processing, multi-symbol backtests, and job management — all from an intuitive GUI.

---

## ✨ Features

- ✅ Friendly Tkinter GUI to configure MT5 strategy optimization jobs
- 📂 Load existing `.ini` files to auto-populate settings
- 🧠 Resume previous jobs using `job_config.json`
- 🗃️ Automatically skips symbols with already-exported `.xml` reports
- 🗃️ `job_config.json` and `.ini` files saved inside each job folder
- 🗓️ Built-in date pickers for optimization ranges
- 📈 Supports multi-symbol jobs and discrete monthly splitting
- 🚀 Auto-launches MT5 with proper config
- 🧹 Automatically moves exported `.xml` to the correct job/symbol folder
- 🛠 Supports dry-run mode and safe caching
- 🧪 Supports `.htm`, `.csv`, and `.xml` reporting (via context menu export)

---

## 🗂️ Project Structure (Simplified)

```bash
.
├── main_app.py                 # Tkinter GUI entry point
├── README.md
├── .cache/                     # Active working config files
│   ├── current_config.json
│   └── current_config.ini
├── generated/                  # Saved job folders (1 per run)
│   └── <timestamp>_<EA>/      # Includes job_config.json, .ini, and results
│       ├── job_config.json
│       ├── <symbol>/
│           ├── .ini files
│           └── .xml results
├── reports/                    # Temporary XML export staging area
├── settings.json               # MT5 terminal config (required)
│
├── core/                       # Core logic (job runner, optimizer, state)
├── ui/                         # Tkinter GUI widgets and layout
├── report_util/                # XML saving, pathing, file movement
└── tests/                      # Pytest unit tests
```

---

## 🚀 How to Run

```bash
# Activate your venv
.venv/Scripts/activate

# Launch the GUI
python main_app.py
```

---

## 🔁 Continue a Previous Job

1. Click **"⏭️ Continue Previous"**
2. Select a `generated/<job_folder>` that contains `job_config.json`
3. Optibatch will:
   - Use the job's existing `.ini` files
   - Skip symbols with already-exported `.xml` results
   - Export only what's missing

---

## 🧪 Testing

```bash
pytest
```

---

## 🛠 Requirements

- Python 3.11+
- MT5 installed and configured in `settings.json`
- Dependencies: `psutil`, `pyautogui`, `pytest`, `mypy`, etc.

---

## 📌 Notes

- `.xml` reports are saved to `reports/` first, then moved to the job folder
- Jobs are organized into folders like `generated/20250411_163229_IndyTSL`
- INI files are saved in UTF-16 (as required by MT5)
- All paths are dynamically constructed using `pathlib`

---

## 🧠 Roadmap

- [ ] CLI mode for batch job scripting
- [ ] Visual dashboard for result tracking
- [ ] Advanced retry/resume logic
- [ ] Cloud execution or agent support

---

## 👤 Author

Built by **512jay** for Dharmesh and others automating MT5 strategies.
```

---
