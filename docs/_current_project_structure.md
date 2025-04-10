# JedgeBot Project Structure

```
JedgeBot/
│   ├── .cache
│   │   ├── current_config.ini
│   │   ├── current_config.json
│   ├── Makefile
│   ├── README.md
│   ├── README.txt
│   ├── __init__.py
│   ├── bootstrap.sh
│   ├── cache
│   │   ├── symbols_241f1d24.json
│   │   ├── symbols_6fee9933.json
│   ├── check_controller.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── enums.py
│   │   ├── ini_generator.py
│   │   ├── input_hints.py
│   │   ├── input_parser.py
│   │   ├── jobs_utils
│   │   │   ├── __init__.py
│   │   │   ├── forward_utils.py
│   │   │   ├── runner.py
│   │   │   ├── settings.py
│   │   ├── loader.py
│   │   ├── logging
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   ├── mt5
│   │   │   ├── __init__.py
│   │   │   ├── exporter.py
│   │   │   ├── process.py
│   │   │   ├── report_exporter.py
│   │   │   ├── scanner.py
│   │   │   ├── symbol_dumper.py
│   │   │   ├── symbol_loader.py
│   │   │   ├── tester_log_monitor.py
│   │   ├── registry.py
│   │   ├── session.py
│   │   ├── types.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── io.py
│   ├── data
│   │   ├── 1 min OHLC.ini
│   │   ├── 1min.ini
│   │   ├── basedonrealticks.ini
│   │   ├── chf.ini
│   │   ├── custom.ini
│   │   ├── everytick.ini
│   │   ├── forwardcustom.ini
│   │   ├── forwardhalf.ini
│   │   ├── lastmonth.ini
│   │   ├── lastyear.ini
│   │   ├── math calculations.ini
│   │   ├── mt5_registry.json
│   │   ├── open prices only.ini
│   │   ├── optimization mapping
│   │   │   ├── All symbols selected in MarketWatch.ini
│   │   │   ├── Disabled.ini
│   │   │   ├── Fast genetic based algorithm.ini
│   │   │   ├── Slow complete algorithm.ini
│   ├── docs
│   │   ├── _current_project_structure.md
│   ├── example.ini
│   ├── export_xml.py
│   ├── exports
│   │   ├── IndyTSL.AUDCAD.H1.20241101_20250402.001_main.xml
│   │   ├── IndyTSL.AUDCHF.H1.20241101_20250402.002_main.xml
│   │   ├── IndyTSL.AUDJPY.H1.20241101_20250402.004_main.xml
│   │   ├── IndyTSL.AUDNZD.H1.20241101_20250402.003_main.xml
│   │   ├── IndyTSL.CADCHF.H1.20250101_20250402.001.fwd.xml
│   │   ├── IndyTSL.CADCHF.H1.20250101_20250402.001.opt.xml
│   │   ├── IndyTSL.CHFJPY.H1.20250101_20250402.001.fwd.xml
│   │   ├── IndyTSL.CHFJPY.H1.20250101_20250402.001.opt.xml
│   │   ├── IndyTSL.ETHUSD.H1.20250101_20250407.001_main.xml
│   │   ├── IndyTSL.EURAUD.H1.20200101_20250402.002.xml
│   │   ├── IndyTSL.EURAUD.H1.20250101_20250407.001_main.xml
│   │   ├── IndyTSL.EURCAD.H1.20250101_20250407.002_main.xml
│   │   ├── IndyTSL.EURNZD.H1.20250101_20250402.002.fwd.xml
│   │   ├── IndyTSL.EURNZD.H1.20250101_20250402.002.opt.xml
│   │   ├── IndyTSL.EURNZD.H1.20250101_20250407.003_main.xml
│   │   ├── IndyTSL.EURUSD.H1.20220325_20250324.001.xml
│   │   ├── IndyTSL.EURUSD.H1.20240401_20250402.001.opt.xml
│   │   ├── IndyTSL.EURUSD.H1.20240501_20250402.001.fwd.xml
│   │   ├── IndyTSL.EURUSD.H1.20240501_20250402.001.opt.xml
│   │   ├── IndyTSL.EURUSD.H1.20250101_20250407.004_main.xml
│   │   ├── testers
│   ├── helpers
│   │   ├── __init__.py
│   │   ├── enums.py
│   │   ├── path_utils.py
│   ├── htmlcov
│   │   ├── class_index.html
│   │   ├── coverage_html_cb_497bf287.js
│   │   ├── favicon_32_cb_58284776.png
│   │   ├── function_index.html
│   │   ├── index.html
│   │   ├── keybd_closed_cb_ce680311.png
│   │   ├── status.json
│   │   ├── style_cb_718ce007.css
│   │   ├── z_57760688d1f824db___init___py.html
│   │   ├── z_df2a3875e135080e___init___py.html
│   │   ├── z_df2a3875e135080e_log_utils_py.html
│   ├── ini_utils
│   │   ├── __init__.py
│   │   ├── formatter.py
│   │   ├── loader.py
│   │   ├── writer.py
│   ├── jobs
│   │   ├── job_20250408_001.json
│   │   │   ├── job_20250408_001.json
│   │   │   │   ├── IndyTSL.EURAUD.H1.20250101_20250402.001.ini
│   │   │   │   ├── IndyTSL.EURCAD.H1.20250101_20250402.002.ini
│   │   │   │   ├── IndyTSL.EURCHF.H1.20250101_20250402.003.ini
│   │   │   ├── job_20250408_001.json.json
│   │   ├── job_20250408_002.json
│   │   │   ├── job_20250408_002.json
│   │   │   │   ├── IndyTSL.USDCNH.H1.20250101_20250402.001.ini
│   │   │   │   ├── IndyTSL.USDMXN.H1.20250101_20250402.002.ini
│   │   │   │   ├── IndyTSL.USDNOK.H1.20250101_20250402.003.ini
│   │   │   ├── job_20250408_002.json.json
│   │   ├── job_20250408_003.json
│   │   │   ├── job_20250408_003.json
│   │   │   │   ├── IndyTSL.CADCHF.H1.20250408_20250408.001.ini
│   │   │   │   ├── IndyTSL.CADJPY.H1.20250408_20250408.002.ini
│   │   │   │   ├── IndyTSL.CHFJPY.H1.20250408_20250408.003.ini
│   │   │   ├── job_20250408_003.json.json
│   │   ├── job_20250408_004.json
│   │   │   ├── job_20250408_004.json
│   │   │   │   ├── IndyTSL.XAGUSD.H1.20250101_20250402.001.ini
│   │   │   │   ├── IndyTSL.XAUUSD.H1.20250101_20250402.002.ini
│   │   │   │   ├── IndyTSL.XPDUSD.H1.20250101_20250402.003.ini
│   │   │   ├── job_20250408_004.json.json
│   │   ├── job_20250408_005.json
│   │   │   ├── job_20250408_005.json
│   │   │   │   ├── IndyTSL.AVAUSD.H1.20250101_20250402.001.ini
│   │   │   │   ├── IndyTSL.BATUSD.H1.20250101_20250402.002.ini
│   │   │   │   ├── IndyTSL.BCHUSD.H1.20250101_20250402.003.ini
│   │   │   ├── job_20250408_005.json.json
│   │   ├── job_20250408_006.json
│   │   │   ├── job_20250408_006.json
│   │   │   │   ├── IndyTSL.EURUSD.H1.20240408_20250408.001.ini
│   │   │   ├── job_20250408_006.json.json
│   │   ├── job_20250408_007.json
│   │   │   ├── job_20250408_007.json
│   │   │   │   ├── IndyTSL.EURUSD.H1.20250101_20250408.001.ini
│   │   │   ├── job_20250408_007.json.json
│   ├── logs
│   ├── main_app.py
│   ├── main_app.spec
│   ├── mt5
│   │   ├── __init__.py
│   │   ├── controller.py
│   ├── pyproject.toml
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── robot.ico
│   ├── robot.png
│   ├── settings.json
│   ├── tests
│   │   ├── __init__.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── tools
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_log_utils.py
│   │   ├── example.ini
│   │   ├── test_dummy.py
│   │   ├── ui
│   │   │   ├── __init__.py
│   │   │   ├── test_updaters.py
│   ├── titles.py
│   ├── trash
│   │   ├── date_picker.py
│   ├── ui
│   │   ├── __init__.py
│   │   ├── actions
│   │   │   ├── ini_buttons.py
│   │   ├── config_loader.py
│   │   ├── edit_inputs_popup.py
│   │   ├── ini_loader.py
│   │   ├── input_editor.py
│   │   ├── mt5_menu.py
│   │   ├── mt5_scanner_ui.py
│   │   ├── symbol_picker.py
│   │   ├── symbols.txt
│   │   ├── updaters.py
│   │   ├── widgets
│   │   │   ├── date_fields.py
│   │   │   ├── ea_inputs.py
│   │   │   ├── header_fields.py
│   │   │   ├── optimized_preview.py
│   │   │   ├── strategy_config.py
│   ├── visualize_mt5.py
│   ├── x_generate_structure.py
```
