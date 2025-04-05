import os
import time  # the module with time.time()
from datetime import time as dt_time
from pathlib import Path
from core.mt5.tester_log_monitor import (
    read_log_utf16,
    get_last_log_timestamp,
    log_contains,
    filter_log_by_keyword,
    get_latest_log,
)


SAMPLE_LOG = """\
NR\t0\t01:07:16.857\tTester\t"Shared Projects\\IndyTSL\\IndyTSL.ex5" 64 bit
OJ\t0\t01:07:17.393\tTester\tcomplete optimization started
OR\t0\t01:07:26.395\tTester\toptimization finished, total passes 25
"""
BAD_SAMPLE_LOG = """\
NR\t0\t01:07:16.857\tTester\t...
BAD\t0\tnotatime\tTester\tbroken line
OR\t0\t01:07:26.395\tTester\t...
"""

UTF16_ENCODING = "utf-16-le"


def test_get_latest_log(tmp_path):
    log1 = tmp_path / "log1.log"
    log2 = tmp_path / "log2.log"

    log1.write_text("old log", encoding="utf-16-le")
    log2.write_text("new log", encoding="utf-16-le")

    # Set custom modified times
    now = time.time()
    os.utime(log1, (now - 60, now - 60))
    os.utime(log2, (now, now))

    latest = get_latest_log(tmp_path)
    assert latest == log2


def test_read_log_utf16_with_invalid_time(tmp_path):
    log_file = write_sample_log(tmp_path, BAD_SAMPLE_LOG)
    result = read_log_utf16(log_file)
    assert len(result) == 2  # only two valid lines


def write_sample_log(path: Path, content: str) -> Path:
    log_path = path / "sample.log"
    with open(log_path, "w", encoding=UTF16_ENCODING) as f:
        f.write(content)
    return log_path


def test_read_log_utf16(tmp_path):
    log_file = write_sample_log(tmp_path, SAMPLE_LOG)
    result = read_log_utf16(log_file)
    assert len(result) == 3
    assert result[0][0] == dt_time(1, 7, 16)
    assert "Tester" in result[0][1]


def test_get_last_log_timestamp(tmp_path):
    log_file = write_sample_log(tmp_path, SAMPLE_LOG)
    last_time = get_last_log_timestamp(log_file)
    assert last_time == dt_time(1, 7, 26)


def test_log_contains(tmp_path):
    log_file = write_sample_log(tmp_path, SAMPLE_LOG)
    assert log_contains(log_file, "optimization finished")
    assert not log_contains(log_file, "unicorns and rainbows")


def test_filter_log_by_keyword(tmp_path):
    log_file = write_sample_log(tmp_path, SAMPLE_LOG)
    results = filter_log_by_keyword(log_file, "optimization")
    assert len(results) == 2
    assert all("optimization" in line for _, line in results)
