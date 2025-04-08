Perfect — let's take care of both!

---

### ✅ 1. **Bundle `symbols.txt` with PyInstaller**

To make sure `symbols.txt` is included in your `.exe` build:

#### ✅ Option 1: Add `--add-data` flag
```bash
pyinstaller --onefile --distpath dist --add-data "ui/symbols.txt;ui" main_app.py
```

> 📌 On Windows, the separator is `;` (e.g. `"source;destination"`), and `ui` is the destination folder inside the bundled app.

#### ✅ Option 2: Add to your `.spec` file (cleaner for multiple files)
In your `main_app.spec`, update the `datas` section like this:
```python
a = Analysis(
    ['main_app.py'],
    ...
    datas=[('ui/symbols.txt', 'ui')],
    ...
)
```

Then build with:
```bash
pyinstaller main_app.spec
```

---

### 📘 2. **Create `README.txt` for the app**

Here's a simple starting point for your `README.txt`:

---

#### 📘 `README.txt` — Optibatch Usage Guide

**Welcome to Optibatch!**  
This tool automates MT5 optimization runs and saves reports for later analysis.

---

### 🖥️ **How to Use the App**

1. **Select MT5 Install**
   - Click `🔍 Scan for MT5`.
   - Pick the desired install from the list.

2. **Set Report Click Point**
   - Click `🖱️ Set Report Click Point`.
   - Move your cursor to the top-left of the MT5 report menu.
   - Hit any key to save the coordinates.

3. **Load a Strategy File**
   - Click `📂 Load INI` to pick a `.ini` file containing strategy parameters.

4. **Pick Symbols**
   - Click `📈 Pick Symbols` to select the instruments to run.
   - Use the right panel to view your selected items.

5. **Edit Strategy Inputs**
   - Use the `🛠️ Edit Inputs` window to toggle which parameters are optimized.
   - Use the toggle button for each parameter to include/exclude it.

6. **Run Optimizations**
   - Click `▶️ Run Optimizations`.
   - MT5 will open, run the strategy, and close automatically.
   - XML reports will be saved to the `optibatch/exports/` folder.

7. **View Results**
   - Click `📊 Analyze Results` to launch a Streamlit dashboard.
   - Select a folder and browse reports visually.

---

### 📂 Files

- `ui/symbols.txt` — fallback list of symbols for symbol picker.
- `settings.json` — remembers your last used configuration.

---

### 🛠 Requirements

- MetaTrader 5 installed.
- Reports must be saved via MT5 right-click > "Save as report".

---

Would you like this saved into a `README.txt` and bundled as well?