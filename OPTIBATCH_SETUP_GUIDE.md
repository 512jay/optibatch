
# 🖱️ OptiBatch Post-Install Setup Guide

Once OptiBatch is installed and running, you'll need to configure your environment for reliable PyAutoGUI automation with MetaTrader 5 (MT5). This includes click position calibration, window geometry setup, and generating the `symbols.txt` file for your market.

---

## 🪟 1. Configure MT5 Window Geometry

OptiBatch relies on consistent MT5 layout and window positioning. Here's how to set it up:

### ✅ Steps:
1. Launch **MetaTrader 5**
2. Open the **Strategy Tester** (press `Ctrl+R`)
3. Drag the MT5 window to your **secondary screen** (or desired monitor)
4. Resize it to show:
   - Strategy tester panel
   - Symbol and expert advisor drop-downs
   - Run button and chart
5. In OptiBatch, use the UI option to **"Set Window Position"**
   - This records `x`, `y`, `width`, and `height` into `.cache/app_state.json`
   - Used for `move_and_resize_window(...)`

---

## 🖱️ 2. Record Mouse Click Position

OptiBatch uses a specific screen coordinate to open the MT5 Strategy Tester context menu and export the XML report.

### ✅ Steps:
1. Open OptiBatch UI
2. Navigate to the **Settings → Record Click Position**
3. A countdown will begin — hover your mouse over the **“Results” context menu** in MT5
4. Click once (or let the countdown finish)
5. The recorded `x, y` will be saved into `.cache/app_state.json` as:
   ```json
   "click_position": [x, y],
   "click_offset": [dx, dy]
   ```

---

## 📁 3. Generate `symbols.txt` Inside MT5 (Required Once)

OptiBatch needs a list of symbols to test. You can generate this from inside MetaTrader 5 by running a short script.

### ✅ Steps:

1. Open **MetaEditor**
2. Go to **File → New → Script**
3. Name the script `WriteSymbolsList` and click *Next → Finish*
4. Replace all code in the editor with:

```mql5
//+------------------------------------------------------------------+
//| Write all available symbols to symbols.txt                       |
//+------------------------------------------------------------------+
void OnStart()
  {
   int total = SymbolsTotal(false);
   string path = "symbols.txt";
   int handle = FileOpen(path, FILE_WRITE|FILE_TXT);
   if(handle != INVALID_HANDLE)
     {
      for(int i = 0; i < total; i++)
         FileWrite(handle, SymbolName(i, false));
      FileClose(handle);
      Print("✅ symbols.txt written to MQL5\\Files");
     }
   else
     {
      Print("❌ Failed to open file for writing");
     }
  }
```

5. Press **F7** to compile
6. Go back to MetaTrader 5
7. Run the script from the **Navigator → Scripts** panel

📍 Output file:
```
C:\Users\<your-user>\AppData\Roaming\MetaQuotes\Terminal\<HASH>\MQL5\Files\symbols.txt
```

OptiBatch will auto-detect this path using your `tester_log_path`.

---

## 🔁 4. Test a Dry Run

Before running a full job:
1. Select a valid `.ini` configuration
2. Choose a small symbol subset (e.g., 1–2 pairs)
3. Enable "Dry Run" mode to verify window moves and file generation without running real backtests

---

## 🧪 5. Common Configuration Keys (`.cache/app_state.json`)

| Key | Description |
|-----|-------------|
| `install_path` | MT5 install path (optional if `terminal_path` is used) |
| `terminal_path` | Full path to `terminal64.exe` |
| `tester_log_path` | Used to find `symbols.txt` |
| `click_position` | Absolute position for XML export click |
| `click_offset` | Relative offset for “Save as XML” |
| `window_geometry` | MT5 window screen size/position |

---

## 🧼 6. Optional Cleanup

To reset settings:
```bash
del .cache\app_state.json
```

Or delete only individual values through the OptiBatch UI if available.

---

## 💡 Tips

- Avoid screen scaling (set Windows to 100%) for consistent PyAutoGUI behavior
- Set `.xml` files to open with **Notepad** to simplify closing the viewer window
- OptiBatch can auto-close Notepad using `taskkill` or `pygetwindow`
- Keep the RDP window open if running on a VPS — PyAutoGUI requires a visible display

---

## 🙋 Need Help?

Check logs in:
```
C:\Users\<user>\AppData\Roaming\MetaQuotes\Terminal\<hash>\Tester\logs
```
