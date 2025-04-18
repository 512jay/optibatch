# JedgeBot Project Structure

```
JedgeBot/
│   ├── .cache
│   │   ├── app_state.json
│   │   ├── current_config.ini
│   │   ├── current_config.json
│   ├── .optibatch
│   │   ├── optibatch.db.20250416_223323.bak
│   ├── Makefile
│   ├── README.md
│   ├── README.txt
│   ├── __init__.py
│   ├── backend
│   │   ├── db.py
│   │   ├── main.py
│   │   ├── routers
│   │   │   ├── runs_db_connected.py
│   │   │   ├── stats_db_connected.py
│   ├── bootstrap.sh
│   ├── cache
│   │   ├── symbols_241f1d24.json
│   │   ├── symbols_6fee9933.json
│   ├── check_controller.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── automation.py
│   │   ├── enums.py
│   │   ├── ini_generator.py
│   │   ├── input_parser.py
│   │   ├── job_context.py
│   │   ├── job_ini_writer.py
│   │   ├── job_runner.py
│   │   ├── jobs_utils
│   │   │   ├── __init__.py
│   │   │   ├── forward_utils.py
│   │   │   ├── runner.py
│   │   │   ├── settings.py
│   │   ├── loader.py
│   │   ├── logging
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   ├── main_runner.py
│   │   ├── mt5
│   │   │   ├── __init__.py
│   │   │   ├── exporter.bak.py
│   │   │   ├── report_exporter.py
│   │   │   ├── scanner.py
│   │   │   ├── symbol_dumper.py
│   │   │   ├── symbol_loader.py
│   │   │   ├── tester_log_monitor.py
│   │   ├── process.py
│   │   ├── run_utils.py
│   │   ├── session.py
│   │   ├── state.py
│   │   ├── types.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── io.py
│   │   ├── validation.py
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
│   │   ├── optibatch_config.schema.json
│   │   ├── optimization mapping
│   │   │   ├── All symbols selected in MarketWatch.ini
│   │   │   ├── Disabled.ini
│   │   │   ├── Fast genetic based algorithm.ini
│   │   │   ├── Slow complete algorithm.ini
│   ├── database
│   │   ├── __init__.py
│   │   ├── export
│   │   │   ├── ini_writer.py
│   │   ├── ingest
│   │   │   ├── ingest_job.py
│   │   ├── init_db.py
│   │   ├── models.py
│   │   ├── session.py
│   ├── dev
│   │   ├── New shortcut.lnk
│   │   ├── check_db_writer.py
│   │   ├── check_ingest.py
│   │   ├── commands
│   │   ├── tools
│   │   │   ├── check_connection.py
│   │   │   ├── dev_ingest.py
│   │   │   ├── query.py
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
│   ├── generated
│   │   ├── 20250415_114231_IndyTSL_v2_0
│   │   │   ├── EURUSD
│   │   │   ├── GBPUSD
│   │   │   ├── current_config.ini
│   │   │   ├── job_config.json
│   │   ├── 20250415_114648_IndyTSL_v2
│   │   │   ├── EURUSD
│   │   │   ├── GBPUSD
│   │   │   ├── current_config.ini
│   │   │   ├── job_config.json
│   │   ├── 20250415_114938_IndyTSL_v2
│   │   │   ├── EURUSD
│   │   │   │   ├── EURUSD.20200401_20200430.ini
│   │   │   │   ├── EURUSD.20200501_20200531.ini
│   │   │   │   ├── EURUSD.20200601_20200630.ini
│   │   │   │   ├── EURUSD.20200701_20200731.ini
│   │   │   │   ├── EURUSD.20200801_20200831.ini
│   │   │   │   ├── EURUSD.20200901_20200930.ini
│   │   │   │   ├── EURUSD.20201001_20201031.ini
│   │   │   │   ├── EURUSD.20201101_20201130.ini
│   │   │   │   ├── EURUSD.20201201_20201231.ini
│   │   │   │   ├── EURUSD.20210101_20210131.ini
│   │   │   │   ├── EURUSD.20210201_20210228.ini
│   │   │   │   ├── EURUSD.20210301_20210331.ini
│   │   │   │   ├── EURUSD.20210401_20210430.ini
│   │   │   │   ├── EURUSD.20210501_20210531.ini
│   │   │   │   ├── EURUSD.20210601_20210630.ini
│   │   │   │   ├── EURUSD.20210701_20210731.ini
│   │   │   │   ├── EURUSD.20210801_20210831.ini
│   │   │   │   ├── EURUSD.20210901_20210930.ini
│   │   │   │   ├── EURUSD.20211001_20211031.ini
│   │   │   │   ├── EURUSD.20211101_20211130.ini
│   │   │   │   ├── EURUSD.20211201_20211231.ini
│   │   │   │   ├── EURUSD.20220101_20220131.ini
│   │   │   │   ├── EURUSD.20220201_20220228.ini
│   │   │   │   ├── EURUSD.20220301_20220331.ini
│   │   │   │   ├── EURUSD.20220401_20220430.ini
│   │   │   │   ├── EURUSD.20220501_20220531.ini
│   │   │   │   ├── EURUSD.20220601_20220630.ini
│   │   │   │   ├── EURUSD.20220701_20220731.ini
│   │   │   │   ├── EURUSD.20220801_20220831.ini
│   │   │   │   ├── EURUSD.20220901_20220930.ini
│   │   │   │   ├── EURUSD.20221001_20221031.ini
│   │   │   │   ├── EURUSD.20221101_20221130.ini
│   │   │   │   ├── EURUSD.20221201_20221231.ini
│   │   │   │   ├── EURUSD.20230101_20230131.ini
│   │   │   │   ├── EURUSD.20230201_20230228.ini
│   │   │   │   ├── EURUSD.20230301_20230331.ini
│   │   │   │   ├── EURUSD.20230401_20230430.ini
│   │   │   │   ├── EURUSD.20230501_20230531.ini
│   │   │   │   ├── EURUSD.20230601_20230630.ini
│   │   │   │   ├── EURUSD.20230701_20230731.ini
│   │   │   │   ├── EURUSD.20230801_20230831.ini
│   │   │   │   ├── EURUSD.20230901_20230930.ini
│   │   │   │   ├── EURUSD.20231001_20231031.ini
│   │   │   │   ├── EURUSD.20231101_20231130.ini
│   │   │   │   ├── EURUSD.20231201_20231231.ini
│   │   │   │   ├── EURUSD.20240101_20240131.ini
│   │   │   │   ├── EURUSD.20240201_20240229.ini
│   │   │   │   ├── EURUSD.20240301_20240331.ini
│   │   │   │   ├── EURUSD.20240401_20240430.ini
│   │   │   │   ├── EURUSD.20240501_20240531.ini
│   │   │   │   ├── EURUSD.20240601_20240630.ini
│   │   │   │   ├── EURUSD.20240701_20240731.ini
│   │   │   │   ├── EURUSD.20240801_20240831.ini
│   │   │   │   ├── EURUSD.20240901_20240930.ini
│   │   │   │   ├── EURUSD.20241001_20241031.ini
│   │   │   │   ├── EURUSD.20241101_20241130.ini
│   │   │   │   ├── EURUSD.20241201_20241231.ini
│   │   │   │   ├── EURUSD.20250101_20250131.ini
│   │   │   │   ├── EURUSD.20250201_20250228.ini
│   │   │   │   ├── EURUSD.20250301_20250331.ini
│   │   │   ├── GBPUSD
│   │   │   │   ├── GBPUSD.20200401_20200430.ini
│   │   │   │   ├── GBPUSD.20200501_20200531.ini
│   │   │   │   ├── GBPUSD.20200601_20200630.ini
│   │   │   │   ├── GBPUSD.20200701_20200731.ini
│   │   │   │   ├── GBPUSD.20200801_20200831.ini
│   │   │   │   ├── GBPUSD.20200901_20200930.ini
│   │   │   │   ├── GBPUSD.20201001_20201031.ini
│   │   │   │   ├── GBPUSD.20201101_20201130.ini
│   │   │   │   ├── GBPUSD.20201201_20201231.ini
│   │   │   │   ├── GBPUSD.20210101_20210131.ini
│   │   │   │   ├── GBPUSD.20210201_20210228.ini
│   │   │   │   ├── GBPUSD.20210301_20210331.ini
│   │   │   │   ├── GBPUSD.20210401_20210430.ini
│   │   │   │   ├── GBPUSD.20210501_20210531.ini
│   │   │   │   ├── GBPUSD.20210601_20210630.ini
│   │   │   │   ├── GBPUSD.20210701_20210731.ini
│   │   │   │   ├── GBPUSD.20210801_20210831.ini
│   │   │   │   ├── GBPUSD.20210901_20210930.ini
│   │   │   │   ├── GBPUSD.20211001_20211031.ini
│   │   │   │   ├── GBPUSD.20211101_20211130.ini
│   │   │   │   ├── GBPUSD.20211201_20211231.ini
│   │   │   │   ├── GBPUSD.20220101_20220131.ini
│   │   │   │   ├── GBPUSD.20220201_20220228.ini
│   │   │   │   ├── GBPUSD.20220301_20220331.ini
│   │   │   │   ├── GBPUSD.20220401_20220430.ini
│   │   │   │   ├── GBPUSD.20220501_20220531.ini
│   │   │   │   ├── GBPUSD.20220601_20220630.ini
│   │   │   │   ├── GBPUSD.20220701_20220731.ini
│   │   │   │   ├── GBPUSD.20220801_20220831.ini
│   │   │   │   ├── GBPUSD.20220901_20220930.ini
│   │   │   │   ├── GBPUSD.20221001_20221031.ini
│   │   │   │   ├── GBPUSD.20221101_20221130.ini
│   │   │   │   ├── GBPUSD.20221201_20221231.ini
│   │   │   │   ├── GBPUSD.20230101_20230131.ini
│   │   │   │   ├── GBPUSD.20230201_20230228.ini
│   │   │   │   ├── GBPUSD.20230301_20230331.ini
│   │   │   │   ├── GBPUSD.20230401_20230430.ini
│   │   │   │   ├── GBPUSD.20230501_20230531.ini
│   │   │   │   ├── GBPUSD.20230601_20230630.ini
│   │   │   │   ├── GBPUSD.20230701_20230731.ini
│   │   │   │   ├── GBPUSD.20230801_20230831.ini
│   │   │   │   ├── GBPUSD.20230901_20230930.ini
│   │   │   │   ├── GBPUSD.20231001_20231031.ini
│   │   │   │   ├── GBPUSD.20231101_20231130.ini
│   │   │   │   ├── GBPUSD.20231201_20231231.ini
│   │   │   │   ├── GBPUSD.20240101_20240131.ini
│   │   │   │   ├── GBPUSD.20240201_20240229.ini
│   │   │   │   ├── GBPUSD.20240301_20240331.ini
│   │   │   │   ├── GBPUSD.20240401_20240430.ini
│   │   │   │   ├── GBPUSD.20240501_20240531.ini
│   │   │   │   ├── GBPUSD.20240601_20240630.ini
│   │   │   │   ├── GBPUSD.20240701_20240731.ini
│   │   │   │   ├── GBPUSD.20240801_20240831.ini
│   │   │   │   ├── GBPUSD.20240901_20240930.ini
│   │   │   │   ├── GBPUSD.20241001_20241031.ini
│   │   │   │   ├── GBPUSD.20241101_20241130.ini
│   │   │   │   ├── GBPUSD.20241201_20241231.ini
│   │   │   │   ├── GBPUSD.20250101_20250131.ini
│   │   │   │   ├── GBPUSD.20250201_20250228.ini
│   │   │   │   ├── GBPUSD.20250301_20250331.ini
│   │   │   ├── current_config.ini
│   │   │   ├── job_config.json
│   │   ├── 20250415_115419_IndyTSL_v2
│   │   │   ├── EURUSD
│   │   │   │   ├── EURUSD.20200401_20200430.ini
│   │   │   │   ├── EURUSD.20200401_20200430.xml
│   │   │   │   ├── EURUSD.20200501_20200531.ini
│   │   │   │   ├── EURUSD.20200501_20200531.xml
│   │   │   │   ├── EURUSD.20200601_20200630.ini
│   │   │   │   ├── EURUSD.20200601_20200630.xml
│   │   │   │   ├── EURUSD.20200701_20200731.ini
│   │   │   │   ├── EURUSD.20200701_20200731.xml
│   │   │   │   ├── EURUSD.20200801_20200831.ini
│   │   │   │   ├── EURUSD.20200801_20200831.xml
│   │   │   │   ├── EURUSD.20200901_20200930.ini
│   │   │   │   ├── EURUSD.20200901_20200930.xml
│   │   │   │   ├── EURUSD.20201001_20201031.ini
│   │   │   │   ├── EURUSD.20201001_20201031.xml
│   │   │   │   ├── EURUSD.20201101_20201130.ini
│   │   │   │   ├── EURUSD.20201101_20201130.xml
│   │   │   │   ├── EURUSD.20201201_20201231.ini
│   │   │   │   ├── EURUSD.20201201_20201231.xml
│   │   │   │   ├── EURUSD.20210101_20210131.ini
│   │   │   │   ├── EURUSD.20210101_20210131.xml
│   │   │   │   ├── EURUSD.20210201_20210228.ini
│   │   │   │   ├── EURUSD.20210201_20210228.xml
│   │   │   │   ├── EURUSD.20210301_20210331.ini
│   │   │   │   ├── EURUSD.20210301_20210331.xml
│   │   │   │   ├── EURUSD.20210401_20210430.ini
│   │   │   │   ├── EURUSD.20210401_20210430.xml
│   │   │   │   ├── EURUSD.20210501_20210531.ini
│   │   │   │   ├── EURUSD.20210501_20210531.xml
│   │   │   │   ├── EURUSD.20210601_20210630.ini
│   │   │   │   ├── EURUSD.20210601_20210630.xml
│   │   │   │   ├── EURUSD.20210701_20210731.ini
│   │   │   │   ├── EURUSD.20210701_20210731.xml
│   │   │   │   ├── EURUSD.20210801_20210831.ini
│   │   │   │   ├── EURUSD.20210801_20210831.xml
│   │   │   │   ├── EURUSD.20210901_20210930.ini
│   │   │   │   ├── EURUSD.20210901_20210930.xml
│   │   │   │   ├── EURUSD.20211001_20211031.ini
│   │   │   │   ├── EURUSD.20211001_20211031.xml
│   │   │   │   ├── EURUSD.20211101_20211130.ini
│   │   │   │   ├── EURUSD.20211101_20211130.xml
│   │   │   │   ├── EURUSD.20211201_20211231.ini
│   │   │   │   ├── EURUSD.20211201_20211231.xml
│   │   │   │   ├── EURUSD.20220101_20220131.ini
│   │   │   │   ├── EURUSD.20220101_20220131.xml
│   │   │   │   ├── EURUSD.20220201_20220228.ini
│   │   │   │   ├── EURUSD.20220201_20220228.xml
│   │   │   │   ├── EURUSD.20220301_20220331.ini
│   │   │   │   ├── EURUSD.20220301_20220331.xml
│   │   │   │   ├── EURUSD.20220401_20220430.ini
│   │   │   │   ├── EURUSD.20220401_20220430.xml
│   │   │   │   ├── EURUSD.20220501_20220531.ini
│   │   │   │   ├── EURUSD.20220501_20220531.xml
│   │   │   │   ├── EURUSD.20220601_20220630.ini
│   │   │   │   ├── EURUSD.20220601_20220630.xml
│   │   │   │   ├── EURUSD.20220701_20220731.ini
│   │   │   │   ├── EURUSD.20220701_20220731.xml
│   │   │   │   ├── EURUSD.20220801_20220831.ini
│   │   │   │   ├── EURUSD.20220801_20220831.xml
│   │   │   │   ├── EURUSD.20220901_20220930.ini
│   │   │   │   ├── EURUSD.20220901_20220930.xml
│   │   │   │   ├── EURUSD.20221001_20221031.ini
│   │   │   │   ├── EURUSD.20221001_20221031.xml
│   │   │   │   ├── EURUSD.20221101_20221130.ini
│   │   │   │   ├── EURUSD.20221101_20221130.xml
│   │   │   │   ├── EURUSD.20221201_20221231.ini
│   │   │   │   ├── EURUSD.20221201_20221231.xml
│   │   │   │   ├── EURUSD.20230101_20230131.ini
│   │   │   │   ├── EURUSD.20230101_20230131.xml
│   │   │   │   ├── EURUSD.20230201_20230228.ini
│   │   │   │   ├── EURUSD.20230201_20230228.xml
│   │   │   │   ├── EURUSD.20230301_20230331.ini
│   │   │   │   ├── EURUSD.20230301_20230331.xml
│   │   │   │   ├── EURUSD.20230401_20230430.ini
│   │   │   │   ├── EURUSD.20230401_20230430.xml
│   │   │   │   ├── EURUSD.20230501_20230531.ini
│   │   │   │   ├── EURUSD.20230501_20230531.xml
│   │   │   │   ├── EURUSD.20230601_20230630.ini
│   │   │   │   ├── EURUSD.20230601_20230630.xml
│   │   │   │   ├── EURUSD.20230701_20230731.ini
│   │   │   │   ├── EURUSD.20230701_20230731.xml
│   │   │   │   ├── EURUSD.20230801_20230831.ini
│   │   │   │   ├── EURUSD.20230801_20230831.xml
│   │   │   │   ├── EURUSD.20230901_20230930.ini
│   │   │   │   ├── EURUSD.20230901_20230930.xml
│   │   │   │   ├── EURUSD.20231001_20231031.ini
│   │   │   │   ├── EURUSD.20231001_20231031.xml
│   │   │   │   ├── EURUSD.20231101_20231130.ini
│   │   │   │   ├── EURUSD.20231101_20231130.xml
│   │   │   │   ├── EURUSD.20231201_20231231.ini
│   │   │   │   ├── EURUSD.20231201_20231231.xml
│   │   │   │   ├── EURUSD.20240101_20240131.ini
│   │   │   │   ├── EURUSD.20240101_20240131.xml
│   │   │   │   ├── EURUSD.20240201_20240229.ini
│   │   │   │   ├── EURUSD.20240201_20240229.xml
│   │   │   │   ├── EURUSD.20240301_20240331.ini
│   │   │   │   ├── EURUSD.20240301_20240331.xml
│   │   │   │   ├── EURUSD.20240401_20240430.ini
│   │   │   │   ├── EURUSD.20240401_20240430.xml
│   │   │   │   ├── EURUSD.20240501_20240531.ini
│   │   │   │   ├── EURUSD.20240501_20240531.xml
│   │   │   │   ├── EURUSD.20240601_20240630.ini
│   │   │   │   ├── EURUSD.20240601_20240630.xml
│   │   │   │   ├── EURUSD.20240701_20240731.ini
│   │   │   │   ├── EURUSD.20240701_20240731.xml
│   │   │   │   ├── EURUSD.20240801_20240831.ini
│   │   │   │   ├── EURUSD.20240801_20240831.xml
│   │   │   │   ├── EURUSD.20240901_20240930.ini
│   │   │   │   ├── EURUSD.20240901_20240930.xml
│   │   │   │   ├── EURUSD.20241001_20241031.ini
│   │   │   │   ├── EURUSD.20241001_20241031.xml
│   │   │   │   ├── EURUSD.20241101_20241130.ini
│   │   │   │   ├── EURUSD.20241101_20241130.xml
│   │   │   │   ├── EURUSD.20241201_20241231.ini
│   │   │   │   ├── EURUSD.20241201_20241231.xml
│   │   │   │   ├── EURUSD.20250101_20250131.ini
│   │   │   │   ├── EURUSD.20250101_20250131.xml
│   │   │   │   ├── EURUSD.20250201_20250228.ini
│   │   │   │   ├── EURUSD.20250201_20250228.xml
│   │   │   │   ├── EURUSD.20250301_20250331.ini
│   │   │   │   ├── EURUSD.20250301_20250331.xml
│   │   │   ├── GBPUSD
│   │   │   │   ├── GBPUSD.20200401_20200430.ini
│   │   │   │   ├── GBPUSD.20200401_20200430.xml
│   │   │   │   ├── GBPUSD.20200501_20200531.ini
│   │   │   │   ├── GBPUSD.20200501_20200531.xml
│   │   │   │   ├── GBPUSD.20200601_20200630.ini
│   │   │   │   ├── GBPUSD.20200601_20200630.xml
│   │   │   │   ├── GBPUSD.20200701_20200731.ini
│   │   │   │   ├── GBPUSD.20200701_20200731.xml
│   │   │   │   ├── GBPUSD.20200801_20200831.ini
│   │   │   │   ├── GBPUSD.20200801_20200831.xml
│   │   │   │   ├── GBPUSD.20200901_20200930.ini
│   │   │   │   ├── GBPUSD.20200901_20200930.xml
│   │   │   │   ├── GBPUSD.20201001_20201031.ini
│   │   │   │   ├── GBPUSD.20201001_20201031.xml
│   │   │   │   ├── GBPUSD.20201101_20201130.ini
│   │   │   │   ├── GBPUSD.20201101_20201130.xml
│   │   │   │   ├── GBPUSD.20201201_20201231.ini
│   │   │   │   ├── GBPUSD.20201201_20201231.xml
│   │   │   │   ├── GBPUSD.20210101_20210131.ini
│   │   │   │   ├── GBPUSD.20210101_20210131.xml
│   │   │   │   ├── GBPUSD.20210201_20210228.ini
│   │   │   │   ├── GBPUSD.20210201_20210228.xml
│   │   │   │   ├── GBPUSD.20210301_20210331.ini
│   │   │   │   ├── GBPUSD.20210301_20210331.xml
│   │   │   │   ├── GBPUSD.20210401_20210430.ini
│   │   │   │   ├── GBPUSD.20210401_20210430.xml
│   │   │   │   ├── GBPUSD.20210501_20210531.ini
│   │   │   │   ├── GBPUSD.20210501_20210531.xml
│   │   │   │   ├── GBPUSD.20210601_20210630.ini
│   │   │   │   ├── GBPUSD.20210601_20210630.xml
│   │   │   │   ├── GBPUSD.20210701_20210731.ini
│   │   │   │   ├── GBPUSD.20210701_20210731.xml
│   │   │   │   ├── GBPUSD.20210801_20210831.ini
│   │   │   │   ├── GBPUSD.20210801_20210831.xml
│   │   │   │   ├── GBPUSD.20210901_20210930.ini
│   │   │   │   ├── GBPUSD.20210901_20210930.xml
│   │   │   │   ├── GBPUSD.20211001_20211031.ini
│   │   │   │   ├── GBPUSD.20211001_20211031.xml
│   │   │   │   ├── GBPUSD.20211101_20211130.ini
│   │   │   │   ├── GBPUSD.20211101_20211130.xml
│   │   │   │   ├── GBPUSD.20211201_20211231.ini
│   │   │   │   ├── GBPUSD.20211201_20211231.xml
│   │   │   │   ├── GBPUSD.20220101_20220131.ini
│   │   │   │   ├── GBPUSD.20220101_20220131.xml
│   │   │   │   ├── GBPUSD.20220201_20220228.ini
│   │   │   │   ├── GBPUSD.20220201_20220228.xml
│   │   │   │   ├── GBPUSD.20220301_20220331.ini
│   │   │   │   ├── GBPUSD.20220301_20220331.xml
│   │   │   │   ├── GBPUSD.20220401_20220430.ini
│   │   │   │   ├── GBPUSD.20220401_20220430.xml
│   │   │   │   ├── GBPUSD.20220501_20220531.ini
│   │   │   │   ├── GBPUSD.20220501_20220531.xml
│   │   │   │   ├── GBPUSD.20220601_20220630.ini
│   │   │   │   ├── GBPUSD.20220601_20220630.xml
│   │   │   │   ├── GBPUSD.20220701_20220731.ini
│   │   │   │   ├── GBPUSD.20220701_20220731.xml
│   │   │   │   ├── GBPUSD.20220801_20220831.ini
│   │   │   │   ├── GBPUSD.20220801_20220831.xml
│   │   │   │   ├── GBPUSD.20220901_20220930.ini
│   │   │   │   ├── GBPUSD.20220901_20220930.xml
│   │   │   │   ├── GBPUSD.20221001_20221031.ini
│   │   │   │   ├── GBPUSD.20221001_20221031.xml
│   │   │   │   ├── GBPUSD.20221101_20221130.ini
│   │   │   │   ├── GBPUSD.20221101_20221130.xml
│   │   │   │   ├── GBPUSD.20221201_20221231.ini
│   │   │   │   ├── GBPUSD.20221201_20221231.xml
│   │   │   │   ├── GBPUSD.20230101_20230131.ini
│   │   │   │   ├── GBPUSD.20230101_20230131.xml
│   │   │   │   ├── GBPUSD.20230201_20230228.ini
│   │   │   │   ├── GBPUSD.20230201_20230228.xml
│   │   │   │   ├── GBPUSD.20230301_20230331.ini
│   │   │   │   ├── GBPUSD.20230301_20230331.xml
│   │   │   │   ├── GBPUSD.20230401_20230430.ini
│   │   │   │   ├── GBPUSD.20230401_20230430.xml
│   │   │   │   ├── GBPUSD.20230501_20230531.ini
│   │   │   │   ├── GBPUSD.20230501_20230531.xml
│   │   │   │   ├── GBPUSD.20230601_20230630.ini
│   │   │   │   ├── GBPUSD.20230601_20230630.xml
│   │   │   │   ├── GBPUSD.20230701_20230731.ini
│   │   │   │   ├── GBPUSD.20230701_20230731.xml
│   │   │   │   ├── GBPUSD.20230801_20230831.ini
│   │   │   │   ├── GBPUSD.20230801_20230831.xml
│   │   │   │   ├── GBPUSD.20230901_20230930.ini
│   │   │   │   ├── GBPUSD.20230901_20230930.xml
│   │   │   │   ├── GBPUSD.20231001_20231031.ini
│   │   │   │   ├── GBPUSD.20231001_20231031.xml
│   │   │   │   ├── GBPUSD.20231101_20231130.ini
│   │   │   │   ├── GBPUSD.20231101_20231130.xml
│   │   │   │   ├── GBPUSD.20231201_20231231.ini
│   │   │   │   ├── GBPUSD.20231201_20231231.xml
│   │   │   │   ├── GBPUSD.20240101_20240131.ini
│   │   │   │   ├── GBPUSD.20240101_20240131.xml
│   │   │   │   ├── GBPUSD.20240201_20240229.ini
│   │   │   │   ├── GBPUSD.20240201_20240229.xml
│   │   │   │   ├── GBPUSD.20240301_20240331.ini
│   │   │   │   ├── GBPUSD.20240301_20240331.xml
│   │   │   │   ├── GBPUSD.20240401_20240430.ini
│   │   │   │   ├── GBPUSD.20240401_20240430.xml
│   │   │   │   ├── GBPUSD.20240501_20240531.ini
│   │   │   │   ├── GBPUSD.20240501_20240531.xml
│   │   │   │   ├── GBPUSD.20240601_20240630.ini
│   │   │   │   ├── GBPUSD.20240601_20240630.xml
│   │   │   │   ├── GBPUSD.20240701_20240731.ini
│   │   │   │   ├── GBPUSD.20240701_20240731.xml
│   │   │   │   ├── GBPUSD.20240801_20240831.ini
│   │   │   │   ├── GBPUSD.20240801_20240831.xml
│   │   │   │   ├── GBPUSD.20240901_20240930.ini
│   │   │   │   ├── GBPUSD.20240901_20240930.xml
│   │   │   │   ├── GBPUSD.20241001_20241031.ini
│   │   │   │   ├── GBPUSD.20241001_20241031.xml
│   │   │   │   ├── GBPUSD.20241101_20241130.ini
│   │   │   │   ├── GBPUSD.20241101_20241130.xml
│   │   │   │   ├── GBPUSD.20241201_20241231.ini
│   │   │   │   ├── GBPUSD.20241201_20241231.xml
│   │   │   │   ├── GBPUSD.20250101_20250131.ini
│   │   │   │   ├── GBPUSD.20250101_20250131.xml
│   │   │   │   ├── GBPUSD.20250201_20250228.ini
│   │   │   │   ├── GBPUSD.20250201_20250228.xml
│   │   │   │   ├── GBPUSD.20250301_20250331.ini
│   │   │   │   ├── GBPUSD.20250301_20250331.xml
│   │   │   ├── current_config.ini
│   │   │   ├── job_config.json
│   │   ├── 20250415_175518_IndyTSL_v2
│   │   │   ├── EURUSD
│   │   │   │   ├── EURUSD.20200401_20200430.ini
│   │   │   │   ├── EURUSD.20200401_20200430.xml
│   │   │   │   ├── EURUSD.20200501_20200531.ini
│   │   │   │   ├── EURUSD.20200501_20200531.xml
│   │   │   │   ├── EURUSD.20200601_20200630.ini
│   │   │   │   ├── EURUSD.20200701_20200731.ini
│   │   │   │   ├── EURUSD.20200801_20200831.ini
│   │   │   │   ├── EURUSD.20200901_20200930.ini
│   │   │   │   ├── EURUSD.20201001_20201031.ini
│   │   │   │   ├── EURUSD.20201101_20201130.ini
│   │   │   │   ├── EURUSD.20201201_20201231.ini
│   │   │   │   ├── EURUSD.20210101_20210131.ini
│   │   │   │   ├── EURUSD.20210201_20210228.ini
│   │   │   │   ├── EURUSD.20210301_20210331.ini
│   │   │   │   ├── EURUSD.20210401_20210430.ini
│   │   │   │   ├── EURUSD.20210501_20210531.ini
│   │   │   │   ├── EURUSD.20210601_20210630.ini
│   │   │   │   ├── EURUSD.20210701_20210731.ini
│   │   │   │   ├── EURUSD.20210801_20210831.ini
│   │   │   │   ├── EURUSD.20210901_20210930.ini
│   │   │   │   ├── EURUSD.20211001_20211031.ini
│   │   │   │   ├── EURUSD.20211101_20211130.ini
│   │   │   │   ├── EURUSD.20211201_20211231.ini
│   │   │   │   ├── EURUSD.20220101_20220131.ini
│   │   │   │   ├── EURUSD.20220201_20220228.ini
│   │   │   │   ├── EURUSD.20220301_20220331.ini
│   │   │   │   ├── EURUSD.20220401_20220430.ini
│   │   │   │   ├── EURUSD.20220501_20220531.ini
│   │   │   │   ├── EURUSD.20220601_20220630.ini
│   │   │   │   ├── EURUSD.20220701_20220731.ini
│   │   │   │   ├── EURUSD.20220801_20220831.ini
│   │   │   │   ├── EURUSD.20220901_20220930.ini
│   │   │   │   ├── EURUSD.20221001_20221031.ini
│   │   │   │   ├── EURUSD.20221101_20221130.ini
│   │   │   │   ├── EURUSD.20221201_20221231.ini
│   │   │   │   ├── EURUSD.20230101_20230131.ini
│   │   │   │   ├── EURUSD.20230201_20230228.ini
│   │   │   │   ├── EURUSD.20230301_20230331.ini
│   │   │   │   ├── EURUSD.20230401_20230430.ini
│   │   │   │   ├── EURUSD.20230501_20230531.ini
│   │   │   │   ├── EURUSD.20230601_20230630.ini
│   │   │   │   ├── EURUSD.20230701_20230731.ini
│   │   │   │   ├── EURUSD.20230801_20230831.ini
│   │   │   │   ├── EURUSD.20230901_20230930.ini
│   │   │   │   ├── EURUSD.20231001_20231031.ini
│   │   │   │   ├── EURUSD.20231101_20231130.ini
│   │   │   │   ├── EURUSD.20231201_20231231.ini
│   │   │   │   ├── EURUSD.20240101_20240131.ini
│   │   │   │   ├── EURUSD.20240201_20240229.ini
│   │   │   │   ├── EURUSD.20240301_20240331.ini
│   │   │   │   ├── EURUSD.20240401_20240430.ini
│   │   │   │   ├── EURUSD.20240501_20240531.ini
│   │   │   │   ├── EURUSD.20240601_20240630.ini
│   │   │   │   ├── EURUSD.20240701_20240731.ini
│   │   │   │   ├── EURUSD.20240801_20240831.ini
│   │   │   │   ├── EURUSD.20240901_20240930.ini
│   │   │   │   ├── EURUSD.20241001_20241031.ini
│   │   │   │   ├── EURUSD.20241101_20241130.ini
│   │   │   │   ├── EURUSD.20241201_20241231.ini
│   │   │   │   ├── EURUSD.20250101_20250131.ini
│   │   │   │   ├── EURUSD.20250201_20250228.ini
│   │   │   │   ├── EURUSD.20250301_20250331.ini
│   │   │   ├── GBPUSD
│   │   │   │   ├── GBPUSD.20200401_20200430.ini
│   │   │   │   ├── GBPUSD.20200501_20200531.ini
│   │   │   │   ├── GBPUSD.20200601_20200630.ini
│   │   │   │   ├── GBPUSD.20200701_20200731.ini
│   │   │   │   ├── GBPUSD.20200801_20200831.ini
│   │   │   │   ├── GBPUSD.20200901_20200930.ini
│   │   │   │   ├── GBPUSD.20201001_20201031.ini
│   │   │   │   ├── GBPUSD.20201101_20201130.ini
│   │   │   │   ├── GBPUSD.20201201_20201231.ini
│   │   │   │   ├── GBPUSD.20210101_20210131.ini
│   │   │   │   ├── GBPUSD.20210201_20210228.ini
│   │   │   │   ├── GBPUSD.20210301_20210331.ini
│   │   │   │   ├── GBPUSD.20210401_20210430.ini
│   │   │   │   ├── GBPUSD.20210501_20210531.ini
│   │   │   │   ├── GBPUSD.20210601_20210630.ini
│   │   │   │   ├── GBPUSD.20210701_20210731.ini
│   │   │   │   ├── GBPUSD.20210801_20210831.ini
│   │   │   │   ├── GBPUSD.20210901_20210930.ini
│   │   │   │   ├── GBPUSD.20211001_20211031.ini
│   │   │   │   ├── GBPUSD.20211101_20211130.ini
│   │   │   │   ├── GBPUSD.20211201_20211231.ini
│   │   │   │   ├── GBPUSD.20220101_20220131.ini
│   │   │   │   ├── GBPUSD.20220201_20220228.ini
│   │   │   │   ├── GBPUSD.20220301_20220331.ini
│   │   │   │   ├── GBPUSD.20220401_20220430.ini
│   │   │   │   ├── GBPUSD.20220501_20220531.ini
│   │   │   │   ├── GBPUSD.20220601_20220630.ini
│   │   │   │   ├── GBPUSD.20220701_20220731.ini
│   │   │   │   ├── GBPUSD.20220801_20220831.ini
│   │   │   │   ├── GBPUSD.20220901_20220930.ini
│   │   │   │   ├── GBPUSD.20221001_20221031.ini
│   │   │   │   ├── GBPUSD.20221101_20221130.ini
│   │   │   │   ├── GBPUSD.20221201_20221231.ini
│   │   │   │   ├── GBPUSD.20230101_20230131.ini
│   │   │   │   ├── GBPUSD.20230201_20230228.ini
│   │   │   │   ├── GBPUSD.20230301_20230331.ini
│   │   │   │   ├── GBPUSD.20230401_20230430.ini
│   │   │   │   ├── GBPUSD.20230501_20230531.ini
│   │   │   │   ├── GBPUSD.20230601_20230630.ini
│   │   │   │   ├── GBPUSD.20230701_20230731.ini
│   │   │   │   ├── GBPUSD.20230801_20230831.ini
│   │   │   │   ├── GBPUSD.20230901_20230930.ini
│   │   │   │   ├── GBPUSD.20231001_20231031.ini
│   │   │   │   ├── GBPUSD.20231101_20231130.ini
│   │   │   │   ├── GBPUSD.20231201_20231231.ini
│   │   │   │   ├── GBPUSD.20240101_20240131.ini
│   │   │   │   ├── GBPUSD.20240201_20240229.ini
│   │   │   │   ├── GBPUSD.20240301_20240331.ini
│   │   │   │   ├── GBPUSD.20240401_20240430.ini
│   │   │   │   ├── GBPUSD.20240501_20240531.ini
│   │   │   │   ├── GBPUSD.20240601_20240630.ini
│   │   │   │   ├── GBPUSD.20240701_20240731.ini
│   │   │   │   ├── GBPUSD.20240801_20240831.ini
│   │   │   │   ├── GBPUSD.20240901_20240930.ini
│   │   │   │   ├── GBPUSD.20241001_20241031.ini
│   │   │   │   ├── GBPUSD.20241101_20241130.ini
│   │   │   │   ├── GBPUSD.20241201_20241231.ini
│   │   │   │   ├── GBPUSD.20250101_20250131.ini
│   │   │   │   ├── GBPUSD.20250201_20250228.ini
│   │   │   │   ├── GBPUSD.20250301_20250331.ini
│   │   │   ├── current_config.ini
│   │   │   ├── job_config.json
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
│   ├── logs
│   ├── main_app.py
│   ├── main_app.spec
│   ├── mt5
│   │   ├── __init__.py
│   │   ├── controller.py
│   ├── optibatch.bat
│   ├── pyproject.toml
│   ├── pytest.ini
│   ├── report_util
│   │   ├── job_summary.py
│   │   ├── reporter.py
│   ├── reports
│   ├── requirements.txt
│   ├── retype_dryrun_20250416_223317.json
│   ├── retype_params_json.py
│   ├── robot.ico
│   ├── robot.png
│   ├── run_dashboard.py
│   ├── settings.py
│   ├── streamlit_view
│   │   ├── charts.py
│   │   ├── filters.py
│   │   ├── ini_export_controls.py
│   │   ├── layout.py
│   │   ├── load_data.py
│   │   ├── main.py
│   │   ├── summary.py
│   │   ├── tables.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── backend
│   │   │   ├── routers
│   │   │   │   ├── test_runs_extended.py
│   │   │   ├── test_api.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── tools
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_log_utils.py
│   │   ├── example.ini
│   │   ├── ini_utils
│   │   ├── test_dummy.py
│   │   ├── ui
│   │   │   ├── __init__.py
│   │   │   ├── test_updaters.py
│   ├── trash
│   │   ├── actions
│   │   │   ├── ini_buttons.py
│   │   ├── config.py
│   │   ├── date_picker.py
│   │   ├── input_hints.py
│   │   ├── registry.py
│   │   ├── writer.py
│   ├── ui
│   │   ├── __init__.py
│   │   ├── config_loader.py
│   │   ├── database_menu.py
│   │   ├── edit_inputs_popup.py
│   │   ├── ini_loader.py
│   │   ├── input_editor.py
│   │   ├── mt5_menu.py
│   │   ├── mt5_scanner_ui.py
│   │   ├── symbol_picker.py
│   │   ├── symbols.txt
│   │   ├── updaters.py
│   │   ├── widgets
│   │   │   ├── button_row.py
│   │   │   ├── date_fields.py
│   │   │   ├── ea_inputs.py
│   │   │   ├── header_fields.py
│   │   │   ├── optimized_preview.py
│   │   │   ├── options_menu.py
│   │   │   ├── strategy_config.py
│   ├── windows
│   │   ├── controller.py
│   ├── x_generate_structure.py
│   ├── x_generate_whole_project.py
```
