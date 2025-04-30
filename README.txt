OptiBatch - MT5 Optimization Automation Tool
============================================

Welcome to OptiBatch! This application automates strategy optimization in MetaTrader 5 (MT5)
by using Python, INI configuration files, and PyAutoGUI to launch and control MT5, save reports,
and ingest data into a database for later analysis.

------------------------------------------------------------
Basic Requirements:
------------------------------------------------------------
- Windows 10 or 11
- Python 3.11+
- MetaTrader 5 (installed)
- Git (to clone this repo)
- Pip (or virtualenv/Poetry for dependency management)

------------------------------------------------------------
Getting Started:
------------------------------------------------------------
1. Clone the repository:

   git clone https://github.com/your-org/optibatch.git
   cd optibatch

2. Set up a virtual environment:

   python -m venv .venv
   .venv\Scripts\activate

3. Install dependencies:

   pip install -r requirements.txt

4. Set environment variable:

   set OPTIVIEW_DB_PATH=C:\Path\To\optibatch_results.db

------------------------------------------------------------
Initial Setup Steps:
------------------------------------------------------------
- Configure MT5 window size/position via the UI (Set Window Position)
- Record the mouse click position (for saving XML exports)
- Generate the list of tradable symbols from within MT5 (see below)

------------------------------------------------------------
Generating symbols.txt in MT5:
------------------------------------------------------------
1. Open MetaEditor
2. Create a new script named WriteSymbolsList
3. Paste in the following code:

   void OnStart()
     {
      int total = SymbolsTotal(false);
      int handle = FileOpen("symbols.txt", FILE_WRITE|FILE_TXT);
      if(handle != INVALID_HANDLE)
        {
         for(int i = 0; i < total; i++)
            FileWrite(handle, SymbolName(i, false));
         FileClose(handle);
         Print("✅ symbols.txt written");
        }
     }

4. Compile and run it from within MetaTrader 5. The file will appear in:
   C:\Users\<YourUser>\AppData\Roaming\MetaQuotes\Terminal\<HASH>\MQL5\Files\symbols.txt

------------------------------------------------------------
Running OptiBatch:
------------------------------------------------------------
Run the UI:

   python main_app.py

From the UI, you can:
- Load INI files
- Select symbols
- Run optimizations
- Monitor MT5 log files
- Export and ingest XML results

------------------------------------------------------------
EXE Packaging:
------------------------------------------------------------
To generate a Windows executable from main_app.spec:

   pyinstaller main_app.spec

The output will be located in the /dist directory.

------------------------------------------------------------
Notes:
------------------------------------------------------------
- Avoid screen scaling (set Windows to 100%)
- Set default program for XML files to Notepad for easy automation
- .cache/ stores local runtime state and should not be committed to Git
- Always confirm the EA (.ex5) file exists and is in the expected MT5 directory

------------------------------------------------------------
Need Help?
------------------------------------------------------------
Check logs at:
   C:\Users\<YourUser>\AppData\Roaming\MetaQuotes\Terminal\<HASH>\Tester\logs

Contact the project maintainer for support.