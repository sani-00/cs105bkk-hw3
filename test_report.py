import json

import pytest

from report import best_day, load_report, saved_safely, steps_per_day, write_report
from walks import Walk


def make_walks() -> list[Walk]:
    return [
        Walk("2026-11-17", 6800, "Chatuchak market"),
        Walk("2026-11-16", 4200, "Lumphini Park"),
        Walk("2026-11-17", 1500, "campus"),
    ]


def test_core_steps_per_day_adds_up_each_date():
    assert steps_per_day(make_walks()) == {"2026-11-16": 4200, "2026-11-17": 8300}


def test_core_steps_per_day_puts_the_dates_in_order():
    assert list(steps_per_day(make_walks())) == ["2026-11-16", "2026-11-17"]


def test_core_best_day_has_the_most_steps():
    assert best_day({"2026-11-16": 4200, "2026-11-17": 8300, "2026-11-18": 2500}) == "2026-11-17"


def test_core_best_day_of_no_days_raises():
    with pytest.raises(ValueError):
        best_day({})


def test_core_saved_safely_writes_the_file(tmp_path):
    path = tmp_path / "note.txt"
    with saved_safely(path) as file:
        file.write("hello")
    assert path.read_text(encoding="utf-8") == "hello"


def test_core_saved_safely_keeps_the_old_file_after_an_error(tmp_path):
    path = tmp_path / "note.txt"
    path.write_text("old", encoding="utf-8")
    with pytest.raises(OSError):
        with saved_safely(path) as file:
            file.write("new, but only half")
            raise OSError("the battery died")
    assert path.read_text(encoding="utf-8") == "old"


def test_core_write_report_saves_json_and_returns_it(tmp_path):
    path = tmp_path / "report.json"
    report = write_report(path, make_walks())
    assert report == {
        "total_steps": 12500,
        "best_day": "2026-11-17",
        "days": {"2026-11-16": 4200, "2026-11-17": 8300},
    }
    with open(path, "r", encoding="utf-8") as file:
        assert json.load(file) == report


def test_core_load_report_reads_what_write_report_saved(tmp_path):
    path = tmp_path / "report.json"
    report = write_report(path, make_walks())
    assert load_report(path) == report


def test_core_load_report_with_no_file_is_none(tmp_path):
    assert load_report(tmp_path / "report.json") is None
