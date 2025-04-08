# JedgeBot Project Structure

```
JedgeBot/
│   ├── Makefile
│   ├── README.md
│   ├── __init__.py
│   ├── bootstrap.sh
│   ├── cache
│   │   ├── symbols_6fee9933.json
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── jobs_utils
│   │   │   ├── __init__.py
│   │   │   ├── forward_utils.py
│   │   │   ├── generator.py
│   │   │   ├── runner.py
│   │   │   ├── settings.py
│   │   │   ├── validator.py
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
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── io.py
│   ├── docs
│   │   ├── _current_project_structure.md
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
│   │   ├── job_20250405_001
│   │   │   ├── IndyTSL.EURUSD.H1.20250101_20250402.001.ini
│   │   ├── job_20250405_001.json
│   │   ├── job_20250405_002.json
│   │   ├── job_20250405_003.json
│   │   ├── job_20250405_004.json
│   │   ├── job_20250405_005.json
│   │   ├── job_20250405_006.json
│   │   ├── job_20250405_007.json
│   │   ├── job_20250405_008.json
│   │   ├── job_20250405_009
│   │   │   ├── IndyTSL.CHFJPY.H1.20250101_20250402.001.ini
│   │   ├── job_20250405_009.json
│   │   ├── job_20250405_010
│   │   │   ├── IndyTSL.EURUSD.H1.20250102_20250402.001.ini
│   │   ├── job_20250405_010.json
│   │   ├── job_20250405_011
│   │   │   ├── IndyTSL.AUDCAD.H1.20250102_20250402.001.ini
│   │   │   ├── IndyTSL.AUDJPY.H1.20250102_20250402.002.ini
│   │   │   ├── IndyTSL.EURCHF.H1.20250102_20250402.003.ini
│   │   ├── job_20250405_011.json
│   │   ├── job_20250405_012.json
│   │   ├── job_20250405_013.json
│   │   ├── job_20250405_014
│   │   │   ├── IndyTSL.EURUSD.H1.20250101_20250403.001.ini
│   │   ├── job_20250405_014.json
│   │   ├── job_20250405_015
│   │   │   ├── IndyTSL.EURAUD.H1.20250101_20250403.001.ini
│   │   │   ├── IndyTSL.EURCAD.H1.20250101_20250403.002.ini
│   │   │   ├── IndyTSL.EURCHF.H1.20250101_20250403.003.ini
│   │   │   ├── IndyTSL.EURGBP.H1.20250101_20250403.004.ini
│   │   │   ├── IndyTSL.EURJPY.H1.20250101_20250403.005.ini
│   │   ├── job_20250405_015.json
│   │   ├── job_20250405_016
│   │   │   ├── IndyTSL.AUDUSD.H1.20250101_20250404.001.ini
│   │   │   ├── IndyTSL.EURGBP.H1.20250101_20250404.002.ini
│   │   │   ├── IndyTSL.EURUSD.H1.20250101_20250404.003.ini
│   │   ├── job_20250405_016.json
│   │   ├── job_20250405_017
│   │   │   ├── IndyTSL.EURCAD.H1.20250101_20250404.001.ini
│   │   │   ├── IndyTSL.EURCHF.H1.20250101_20250404.002.ini
│   │   ├── job_20250405_017.json
│   │   ├── job_20250405_018
│   │   │   ├── IndyTSL.CADCHF.H1.20250101_20250302.004.ini
│   │   │   ├── IndyTSL.EURCHF.H1.20250101_20250302.001.ini
│   │   │   ├── IndyTSL.EURGBP.H1.20250101_20250302.002.ini
│   │   │   ├── IndyTSL.EURJPY.H1.20250101_20250302.003.ini
│   │   ├── job_20250405_018.json
│   │   ├── job_20250405_019
│   │   │   ├── IndyTSL.CADCHF.H1.20250101_20250202.004.ini
│   │   │   ├── IndyTSL.EURCHF.H1.20250101_20250202.001.ini
│   │   │   ├── IndyTSL.EURGBP.H1.20250101_20250202.002.ini
│   │   │   ├── IndyTSL.EURJPY.H1.20250101_20250202.003.ini
│   │   ├── job_20250405_019.json
│   │   ├── job_20250405_020
│   │   │   ├── IndyTSL.CADJPY.H1.20250101_20250202.001.ini
│   │   │   ├── IndyTSL.CHFJPY.H1.20250101_20250202.002.ini
│   │   │   ├── IndyTSL.EURNOK.H1.20250101_20250202.003.ini
│   │   │   ├── IndyTSL.EURNZD.H1.20250101_20250202.004.ini
│   │   ├── job_20250405_020.json
│   │   ├── job_20250405_021
│   │   │   ├── IndyTSL.AUDJPY.H1.20250101_20250305.001.ini
│   │   │   ├── IndyTSL.EURCHF.H1.20250101_20250305.002.ini
│   │   ├── job_20250405_021.json
│   │   ├── job_20250405_022
│   │   │   ├── IndyTSL.EURCAD.H1.20250201_20250402.001.ini
│   │   │   ├── IndyTSL.EURCHF.H1.20250201_20250402.002.ini
│   │   │   ├── IndyTSL.EURGBP.H1.20250201_20250402.003.ini
│   │   │   ├── IndyTSL.EURJPY.H1.20250201_20250402.004.ini
│   │   ├── job_20250405_022.json
│   │   ├── job_20250405_023
│   │   │   ├── IndyTSL.CADCHF.H1.20250201_20250402.001.ini
│   │   │   ├── IndyTSL.CADJPY.H1.20250201_20250402.002.ini
│   │   │   ├── IndyTSL.CHFJPY.H1.20250201_20250402.003.ini
│   │   ├── job_20250405_023.json
│   │   ├── job_20250405_024
│   │   │   ├── IndyTSL.CADCHF.H1.20250101_20250402.002.ini
│   │   │   ├── IndyTSL.CADJPY.H1.20250101_20250402.003.ini
│   │   │   ├── IndyTSL.CHFJPY.H1.20250101_20250402.004.ini
│   │   │   ├── IndyTSL.EURJPY.H1.20250101_20250402.001.ini
│   │   │   ├── IndyTSL.EURNOK.H1.20250101_20250402.005.ini
│   │   ├── job_20250405_024.json
│   │   ├── job_20250405_025
│   │   │   ├── IndyTSL.CADCHF.H1.20241201_20250402.005.ini
│   │   │   ├── IndyTSL.EURCAD.H1.20241201_20250402.001.ini
│   │   │   ├── IndyTSL.EURCHF.H1.20241201_20250402.002.ini
│   │   │   ├── IndyTSL.EURGBP.H1.20241201_20250402.003.ini
│   │   │   ├── IndyTSL.EURJPY.H1.20241201_20250402.004.ini
│   │   │   ├── IndyTSL.EURUSD.H1.20241201_20250402.007.ini
│   │   │   ├── IndyTSL.GBPCAD.H1.20241201_20250402.006.ini
│   │   ├── job_20250405_025.json
│   │   ├── job_20250405_026
│   │   │   ├── IndyTSL.CADCHF.H1.20241101_20250402.003.ini
│   │   │   ├── IndyTSL.CADJPY.H1.20241101_20250402.004.ini
│   │   │   ├── IndyTSL.EURGBP.H1.20241101_20250402.001.ini
│   │   │   ├── IndyTSL.EURJPY.H1.20241101_20250402.002.ini
│   │   ├── job_20250405_026.json
│   │   ├── job_20250405_027
│   │   │   ├── IndyTSL.EURUSD.H1.20250101_20250402.001.ini
│   │   ├── job_20250405_027.json
│   │   ├── job_20250405_028
│   │   │   ├── IndyTSL.EURUSD.H1.20250101_20250402.001.ini
│   │   ├── job_20250405_028.json
│   │   ├── job_20250405_029
│   │   │   ├── IndyTSL.EURUSD.H1.20250101_20250402.001.ini
│   │   ├── job_20250405_029.json
│   │   ├── job_20250406_001
│   │   │   ├── IndyTSL.AUDCAD.H1.20200101_20250402.001.ini
│   │   │   ├── IndyTSL.AUDCHF.H1.20200101_20250402.002.ini
│   │   │   ├── IndyTSL.AUDJPY.H1.20200101_20250402.004.ini
│   │   │   ├── IndyTSL.AUDNZD.H1.20200101_20250402.003.ini
│   │   │   ├── IndyTSL.AUDUSD.H1.20200101_20250402.005.ini
│   │   │   ├── IndyTSL.Australia 200.H1.20200101_20250402.030.ini
│   │   │   ├── IndyTSL.CADCHF.H1.20200101_20250402.011.ini
│   │   │   ├── IndyTSL.CADJPY.H1.20200101_20250402.012.ini
│   │   │   ├── IndyTSL.CHFJPY.H1.20200101_20250402.013.ini
│   │   │   ├── IndyTSL.China 50.H1.20200101_20250402.031.ini
│   │   │   ├── IndyTSL.China H Shares.H1.20200101_20250402.032.ini
│   │   │   ├── IndyTSL.EURAUD.H1.20200101_20250402.006.ini
│   │   │   ├── IndyTSL.EURCAD.H1.20200101_20250402.007.ini
│   │   │   ├── IndyTSL.EURCHF.H1.20200101_20250402.008.ini
│   │   │   ├── IndyTSL.EURGBP.H1.20200101_20250402.009.ini
│   │   │   ├── IndyTSL.EURJPY.H1.20200101_20250402.010.ini
│   │   │   ├── IndyTSL.EURNZD.H1.20200101_20250402.014.ini
│   │   │   ├── IndyTSL.EURUSD.H1.20200101_20250402.016.ini
│   │   │   ├── IndyTSL.Europe 50.H1.20200101_20250402.033.ini
│   │   │   ├── IndyTSL.France 40.H1.20200101_20250402.034.ini
│   │   │   ├── IndyTSL.GBPAUD.H1.20200101_20250402.017.ini
│   │   │   ├── IndyTSL.GBPCAD.H1.20200101_20250402.015.ini
│   │   │   ├── IndyTSL.GBPCHF.H1.20200101_20250402.018.ini
│   │   │   ├── IndyTSL.GBPJPY.H1.20200101_20250402.019.ini
│   │   │   ├── IndyTSL.GBPUSD.H1.20200101_20250402.020.ini
│   │   │   ├── IndyTSL.GDX.US.H1.20200101_20250402.026.ini
│   │   │   ├── IndyTSL.GLD.US.H1.20200101_20250402.027.ini
│   │   │   ├── IndyTSL.Germany 40.H1.20200101_20250402.035.ini
│   │   │   ├── IndyTSL.Hong Kong 50.H1.20200101_20250402.036.ini
│   │   │   ├── IndyTSL.Japan 225.H1.20200101_20250402.037.ini
│   │   │   ├── IndyTSL.NZDCAD.H1.20200101_20250402.021.ini
│   │   │   ├── IndyTSL.NZDJPY.H1.20200101_20250402.022.ini
│   │   │   ├── IndyTSL.NZDUSD.H1.20200101_20250402.023.ini
│   │   │   ├── IndyTSL.Netherlands 25.H1.20200101_20250402.038.ini
│   │   │   ├── IndyTSL.Singapore 20.H1.20200101_20250402.039.ini
│   │   │   ├── IndyTSL.Swiss 20.H1.20200101_20250402.040.ini
│   │   │   ├── IndyTSL.Taiwan Index.H1.20200101_20250402.041.ini
│   │   │   ├── IndyTSL.UK 100.H1.20200101_20250402.042.ini
│   │   │   ├── IndyTSL.UK Brent Oil.H1.20200101_20250402.028.ini
│   │   │   ├── IndyTSL.US Mid Cap 400.H1.20200101_20250402.043.ini
│   │   │   ├── IndyTSL.US Oil.H1.20200101_20250402.029.ini
│   │   │   ├── IndyTSL.US SP 500.H1.20200101_20250402.044.ini
│   │   │   ├── IndyTSL.US Small Cap 2000.H1.20200101_20250402.045.ini
│   │   │   ├── IndyTSL.US Tech 100.H1.20200101_20250402.046.ini
│   │   │   ├── IndyTSL.USDCAD.H1.20200101_20250402.024.ini
│   │   │   ├── IndyTSL.USDCHF.H1.20200101_20250402.025.ini
│   │   │   ├── IndyTSL.Wall Street 30.H1.20200101_20250402.047.ini
│   │   ├── job_20250406_001.json
│   │   ├── job_20250406_002
│   │   │   ├── IndyTSL.AUDUSD.H1.20200101_20250402.001.ini
│   │   │   ├── IndyTSL.EURAUD.H1.20200101_20250402.002.ini
│   │   │   ├── IndyTSL.EURCAD.H1.20200101_20250402.003.ini
│   │   │   ├── IndyTSL.EURCHF.H1.20200101_20250402.004.ini
│   │   │   ├── IndyTSL.EURGBP.H1.20200101_20250402.005.ini
│   │   │   ├── IndyTSL.EURJPY.H1.20200101_20250402.006.ini
│   │   ├── job_20250406_002.json
│   │   ├── job_20250407_001
│   │   │   ├── IndyTSL.NZDCHF.H1.20250101_20250402.001.ini
│   │   ├── job_20250407_001.json
│   │   ├── job_20250407_002
│   │   │   ├── IndyTSL.CADCHF.H1.20250101_20250402.001.ini
│   │   ├── job_20250407_002.json
│   │   ├── job_20250407_003
│   │   │   ├── IndyTSL.CADCHF.H1.20250101_20250407.001.ini
│   │   ├── job_20250407_003.json
│   │   ├── job_20250407_004
│   │   │   ├── IndyTSL.BTCETH.H1.20250101_20250407.001.ini
│   │   ├── job_20250407_004.json
│   │   ├── job_20250407_005
│   │   │   ├── IndyTSL.ETHUSD.H1.20250101_20250407.001.ini
│   │   ├── job_20250407_005.json
│   │   ├── job_20250407_006
│   │   │   ├── IndyTSL.EURAUD.H1.20250101_20250407.001.ini
│   │   │   ├── IndyTSL.EURCAD.H1.20250101_20250407.002.ini
│   │   │   ├── IndyTSL.EURNZD.H1.20250101_20250407.003.ini
│   │   │   ├── IndyTSL.EURUSD.H1.20250101_20250407.004.ini
│   │   ├── job_20250407_006.json
│   │   ├── job_20250407_007
│   │   │   ├── IndyTSL.AUDCAD.H1.20241101_20250402.001.ini
│   │   │   ├── IndyTSL.AUDCHF.H1.20241101_20250402.002.ini
│   │   │   ├── IndyTSL.AUDJPY.H1.20241101_20250402.004.ini
│   │   │   ├── IndyTSL.AUDNZD.H1.20241101_20250402.003.ini
│   │   ├── job_20250407_007.json
│   │   ├── job_20250407_008
│   │   │   ├── IndyTSL.EURAUD.H1.20241101_20250402.001.ini
│   │   │   ├── IndyTSL.EURCAD.H1.20241101_20250402.002.ini
│   │   │   ├── IndyTSL.EURCHF.H1.20241101_20250402.003.ini
│   │   ├── job_20250407_008.json
│   │   ├── job_20250407_009
│   │   │   ├── IndyTSL.NZDCHF.H1.20241101_20250402.003.ini
│   │   │   ├── IndyTSL.USDCNH.H1.20241101_20250402.002.ini
│   │   │   ├── IndyTSL.XAGUSD.H1.20241101_20250402.001.ini
│   │   ├── job_20250407_009.json
│   │   ├── job_20250407_010
│   │   │   ├── IndyTSL.EURUSD.H1.20241001_20250402.001.ini
│   │   ├── job_20250407_010.json
│   │   ├── job_20250407_011
│   │   │   ├── IndyTSL.EURUSD.H1.20240901_20250402.001.ini
│   │   ├── job_20250407_011.json
│   │   ├── job_20250407_012
│   │   │   ├── IndyTSL.EURUSD.H1.20240801_20250402.001.ini
│   │   ├── job_20250407_012.json
│   │   ├── job_20250407_013
│   │   │   ├── IndyTSL.EURUSD.H1.20240701_20250402.001.ini
│   │   ├── job_20250407_013.json
│   │   ├── job_20250407_014
│   │   │   ├── IndyTSL.EURUSD.H1.20240702_20250402.001.ini
│   │   ├── job_20250407_014.json
│   │   ├── job_20250407_015
│   │   │   ├── IndyTSL.EURUSD.H1.20240601_20250402.001.ini
│   │   ├── job_20250407_015.json
│   │   ├── job_20250407_016
│   │   │   ├── IndyTSL.EURUSD.H1.20240501_20250402.001.ini
│   │   ├── job_20250407_016.json
│   │   ├── job_20250407_017
│   │   │   ├── IndyTSL.EURUSD.H1.20240401_20250402.001.ini
│   │   ├── job_20250407_017.json
│   │   ├── job_20250407_018
│   │   │   ├── IndyTSL.XAGUSD.H1.20200101_20250402.001.ini
│   │   │   ├── IndyTSL.XAUUSD.H1.20200101_20250402.002.ini
│   │   │   ├── IndyTSL.XPDUSD.H1.20200101_20250402.003.ini
│   │   │   ├── IndyTSL.XPTUSD.H1.20200101_20250402.004.ini
│   │   ├── job_20250407_018.json
│   │   ├── job_20250407_019
│   │   │   ├── IndyTSL.USDCAD.H1.20200101_20250402.001.ini
│   │   ├── job_20250407_019.json
│   │   ├── job_20250407_020
│   │   │   ├── IndyTSL.CADCHF.H1.20250101_20250402.001.ini
│   │   ├── job_20250407_020.json
│   │   ├── job_20250407_021
│   │   │   ├── IndyTSL.CHFJPY.H1.20250101_20250402.001.ini
│   │   │   ├── IndyTSL.EURNZD.H1.20250101_20250402.002.ini
│   │   ├── job_20250407_021.json
│   │   ├── job_20250407_022
│   │   │   ├── IndyTSL.AUDCAD.H1.20250101_20250402.001.ini
│   │   │   ├── IndyTSL.AUDCHF.H1.20250101_20250402.002.ini
│   │   │   ├── IndyTSL.AUDJPY.H1.20250101_20250402.004.ini
│   │   │   ├── IndyTSL.AUDNZD.H1.20250101_20250402.003.ini
│   │   │   ├── IndyTSL.AUDUSD.H1.20250101_20250402.005.ini
│   │   │   ├── IndyTSL.CADCHF.H1.20250101_20250402.011.ini
│   │   │   ├── IndyTSL.CADJPY.H1.20250101_20250402.012.ini
│   │   │   ├── IndyTSL.CHFJPY.H1.20250101_20250402.013.ini
│   │   │   ├── IndyTSL.EURAUD.H1.20250101_20250402.006.ini
│   │   │   ├── IndyTSL.EURCAD.H1.20250101_20250402.007.ini
│   │   │   ├── IndyTSL.EURCHF.H1.20250101_20250402.008.ini
│   │   │   ├── IndyTSL.EURGBP.H1.20250101_20250402.009.ini
│   │   │   ├── IndyTSL.EURJPY.H1.20250101_20250402.010.ini
│   │   ├── job_20250407_022.json
│   │   ├── job_20250407_023
│   │   │   ├── IndyTSL.EURUSD.H1.20220101_20250402.001.ini
│   │   ├── job_20250407_023.json
│   │   ├── job_20250407_024
│   │   │   ├── IndyTSL.ETCUSD.H1.20250101_20250402.001.ini
│   │   ├── job_20250407_024.json
│   │   ├── job_20250407_025
│   │   │   ├── IndyTSL.AAPL.H1.20250101_20250402.001.ini
│   │   ├── job_20250407_025.json
│   │   ├── job_20250407_026
│   │   │   ├── IndyTSL.SGDJPY.H1.20250101_20250402.001.ini
│   │   ├── job_20250407_026.json
│   │   ├── job_20250407_027
│   │   │   ├── IndyTSL.USDHKD.H1.20250101_20250402.001.ini
│   │   ├── job_20250407_027.json
│   │   ├── job_20250407_028
│   │   │   ├── IndyTSL.USDPLN.H1.20250101_20250402.001.ini
│   │   ├── job_20250407_028.json
│   │   ├── job_20250407_029
│   │   │   ├── IndyTSL.USDMXN.H1.20250101_20250402.001.ini
│   │   ├── job_20250407_029.json
│   ├── logs
│   ├── main_app.py
│   ├── main_app.spec
│   ├── pyproject.toml
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── settings.json
│   ├── starter.ini
│   ├── state
│   │   ├── __init__.py
│   │   ├── app_state.py
│   │   ├── report_click.json
│   ├── state.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── tools
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_log_utils.py
│   │   ├── ini_utils
│   │   │   ├── __init__.py
│   │   │   ├── test_ini_loader.py
│   │   ├── test_dummy.py
│   ├── titles.py
│   ├── ui
│   │   ├── __init__.py
│   │   ├── date_picker.py
│   │   ├── input_editor.py
│   │   ├── mt5_scanner_ui.py
│   │   ├── symbol_picker.py
│   ├── visualize_mt5.py
│   ├── x_generate_structure.py
```
