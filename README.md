# OptiBatch

**OptiBatch** is a Python-based tool that automates strategy optimization runs in MetaTrader 5 (MT5).  
Designed for quant traders, analysts, and technical users who want to streamline batch optimizations.

---

## 🚀 Features

- Generate `.ini` config files for MT5 Strategy Tester
- Automatically launch and monitor optimization runs
- Organize `.htm` and `.csv` reports per symbol/timeframe
- Track progress via logs, detect optimization completion
- CLI-first, GUI/Tkinter planned
- Future SaaS integration via Fordis Ludus

---

## 🧰 Requirements

- MetaTrader 5 (installed and accessible)
- Python 3.10+
- Windows environment (Linux support planned)

---

## 📦 Install

```bash
git clone https://github.com/512jay/optibatch.git
cd optibatch
python -m venv env
source env/bin/activate  # Windows: .\\env\\Scripts\\activate
pip install -r requirements.txt
