Absolutely — here's a clean, mypy-friendly `README.md` for OptiBatch setup that another developer could use to get started on a new machine.

---  

```markdown
# 🧪 OptiBatch

OptiBatch is an automation tool for running, managing, and analyzing MetaTrader 5 (MT5) strategy optimizations using `.ini` configuration files. It uses Python, PyAutoGUI, and MT5 to automate backtesting and store results into a SQLite database for later analysis.

---

## ⚙️ Requirements

- Windows 10 or 11 (with display access for MT5)
- Python 3.11+ (check version with `python --version`)
- MetaTrader 5 (installed and configured)
- Git
- Pip 

---

## 📦 Install & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/optibatch.git
cd optibatch
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate       # On Windows
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 🖥️ MetaTrader 5 Setup

1. Install MT5 from your broker or [MetaTrader's official site](https://www.metatrader5.com).
2. Launch MT5 at least once.
3. Ensure:
   - Language is set to **English**
   - The desired EA (`.ex5` file) is compiled and placed in:
     ```
     C:\Users\<YourName>\AppData\Roaming\MetaQuotes\Terminal\<HASH>\MQL5\Experts\Shared Projects\<EA Folder>
     ```

4. Determine the terminal hash by checking:
   ```
   %APPDATA%\MetaQuotes\Terminal
   ```

---

## 🔧 Configuration

### Environment Variables

Set this before running the app:

```bash
set OPTIVIEW_DB_PATH=C:\Path\To\optibatch_results.db
```

Alternatively, create a `.env` file:

```env
OPTIVIEW_DB_PATH=C:\Path\To\optibatch_results.db
```

---

## 🚀 Running OptiBatch

Start the main UI:

```bash
python main_app.py
```

From there, you can:
- Load `.ini` configurations
- Select symbols from `symbols.txt`
- Run backtests
- Ingest results into the database

---

## 🗂️ Project Structure

```
optibatch/
├── core/               # Main automation logic
├── database/           # SQLite interaction and ingestion
├── ui/                 # Tkinter UI elements
├── reports/            # Saved MT5 XML outputs
├── generated/          # Job outputs, including INI + XML
├── .cache/             # Per-user runtime state (ignored in Git)
├── requirements.txt    # Dependency list
└── main_app.py         # App entry point
```

---

## 🧼 Good to Know

- `.cache/` is local state and should **not** be committed.
- You can re-run partial months like April and delete/reingest as needed.
- Cursor position is restored after automation (or will be soon).
- OptiBatch uses `pyautogui` to control MT5 – keep the screen unlocked and RDP open.
- Default XML viewer should be **Notepad** for easy automation cleanup.

---

## 🧪 Optional: Dev Notes

- All Python code should be **mypy compliant**
- Use `utf-16` for all `.xml` read/write
- Avoid `except Exception:` — always catch specific exceptions

---

## 🔍 Troubleshooting

- **MT5 doesn't launch properly?**
  - Check your EA path
  - Make sure `terminal64.exe` is specified correctly

- **XML file doesn’t close?**
  - Set default app for `.xml` to Notepad
  - OptiBatch can auto-close Notepad

- **Backtests not starting?**
  - Check `.ini` for valid symbol, timeframe, EA path

---

## 🙋 Support

None, lol.