import hashlib
import json
from pathlib import Path
from core.mt5.symbol_dumper import dump_symbols_via_mt5_auto

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_symbol_cache_filename(data_path: str):
    h = hashlib.sha1(data_path.encode()).hexdigest()[:8]
    return CACHE_DIR / f"symbols_{h}.json"


def load_symbols(data_path: str, force_refresh=False):
    data_path = Path(data_path)
    cache_file = get_symbol_cache_filename(str(data_path))

    if not force_refresh and cache_file.exists():
        try:
            return json.loads(cache_file.read_text())
        except Exception as e:
            print(f"⚠️ Failed to load symbol cache: {e}")

    symbols_file = data_path / "MQL5" / "Files" / "symbols.txt"
    if not symbols_file.exists():
        print(f"❌ No symbols.txt found at {symbols_file}")

        # Auto-run symbol dumper
        try:
            with open("settings.json") as f:
                mt5 = json.load(f)
            terminal_path = mt5["terminal_path"]
            data_path_str = mt5["data_path"]

            if dump_symbols_via_mt5_auto(terminal_path, data_path_str):
                return load_symbols(data_path, force_refresh=True)
        except Exception as e:
            print(f"⚠️ Auto-dump failed: {e}")

        return []

    symbols = [
        line.strip() for line in symbols_file.read_text().splitlines() if line.strip()
    ]
    cache_file.write_text(json.dumps(symbols, indent=2))
    return symbols
