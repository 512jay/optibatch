# File: tools/export_min_vol_symbols.py
# Purpose: Export all MT5 symbols where min volume is 0.01 to a CSV file or stdout

import csv
import argparse
from pathlib import Path
import MetaTrader5 as mt5  # type: ignore


def export_min_vol_symbols(output_path: Path = Path("min_vol_0.01_symbols.csv")) -> int:
    """Connects to MetaTrader5 terminal and exports all symbols where min volume is 0.01.

    Args:
        output_path (Path): Path to save the CSV file. Defaults to current dir.

    Returns:
        int: Number of symbols written.
    """
    # Initialize MT5 connection
    if not mt5.initialize():
        print(f"❌ MT5 initialization failed: {mt5.last_error()}")
        return 0

    try:
        all_symbols = mt5.symbols_get()
        if not all_symbols:
            print("⚠️ No symbols found.")
            return 0

        filtered = [s for s in all_symbols if s.volume_min == 0.01]

        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["symbol", "volume_min", "volume_step", "description"])
            for sym in filtered:
                writer.writerow(
                    [sym.name, sym.volume_min, sym.volume_step, sym.description]
                )

        print(f"✅ Saved {len(filtered)} symbols to {output_path}")
        return len(filtered)

    finally:
        mt5.shutdown()


def list_min_vol_symbols() -> int:
    """Prints all symbols with min volume = 0.01 to stdout.

    Returns:
        int: Number of symbols printed.
    """
    if not mt5.initialize():
        print(f"❌ MT5 initialization failed: {mt5.last_error()}")
        return 0

    try:
        all_symbols = mt5.symbols_get()
        if not all_symbols:
            print("⚠️ No symbols found.")
            return 0

        filtered = [s.name for s in all_symbols if s.volume_min == 0.01]
        for name in sorted(filtered):
            print(name)

        return len(filtered)
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Export or list MT5 symbols with min vol = 0.01"
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="Only list matching symbols, do not write CSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("min_vol_0.01_symbols.csv"),
        help="Path to save CSV file",
    )
    args = parser.parse_args()

    if args.list_only:
        count = list_min_vol_symbols()
        print(f"\n✅ Listed {count} symbols with volume_min = 0.01")
    else:
        export_min_vol_symbols(output_path=args.output)
