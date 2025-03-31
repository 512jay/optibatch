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
source env/bin/activate  # Windows: .\env\Scripts\activate
pip install -r requirements.txt
```

Or use the provided bootstrap script:

```bash
./bootstrap.sh
```

---

## 🧪 Run Tests

```bash
pytest
```

---

## 📌 Roadmap

- [x] Initial CLI scaffold
- [ ] Add INI file builder
- [ ] MT5 launcher with log monitor
- [ ] Report parser and organizer
- [ ] GUI with Tkinter (optional)
- [ ] Integration with Fordis Ludus

---

## 🤝 Contributing

Pull requests welcome! For major changes, open an issue first.

---

## 📄 License

MIT License. See [`LICENSE`](LICENSE) file.
