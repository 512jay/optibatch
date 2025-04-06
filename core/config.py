
import json
from pathlib import Path

CONFIG_PATH = Path("settings.json")


class Config:
    def __init__(self):
        self.data = {}
        self._load()

    def _load(self):
        if CONFIG_PATH.exists():
            with CONFIG_PATH.open("r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save(self):
        with CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.set(key, value)


# Global config instance
config = Config()
