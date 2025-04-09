from pathlib import Path

CACHE_DIR = Path(".cache")
CURRENT_INI = CACHE_DIR / "current_config.ini"


def cache_ini_file(src: Path) -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    content = src.read_text(encoding="utf-16")
    CURRENT_INI.write_text(content, encoding="utf-16")


def get_cached_ini_file() -> Path:
    return CURRENT_INI


def has_cached_ini() -> bool:
    return CURRENT_INI.exists()
