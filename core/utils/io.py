# core/utils/io.py

import json
from configparser import ConfigParser
from pathlib import Path
from typing import Union


def read_utf16_file(path: Path) -> Union[dict, ConfigParser]:
    """
    Reads a UTF-16 encoded file and returns the parsed object.
    Supports .json (returns dict) and .ini (returns ConfigParser).
    """
    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    with path.open("r", encoding="utf-16") as f:
        if path.suffix.lower() == ".json":
            return json.load(f)
        elif path.suffix.lower() == ".ini":
            parser = ConfigParser()
            parser.read_file(f)
            return parser
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")



