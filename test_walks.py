from collections.abc import Iterator
from pathlib import Path

import pytest

from walks import Walk, good_walks, none_on_error, parse_walk, read_rows

WALKS_CSV = Path(__file__).parent / "walks.csv"


def test_core_parse_walk_cleans_a_good_row():
    row = {"date": "2026-11-16", "steps": " 3100 ", "place": " campus "}
    assert parse_walk(row) == Walk("2026-11-16", 3100, "campus")


def test_core_parse_walk_rejects_steps_that_are_not_a_number():
    with pytest.raises(ValueError):
        parse_walk({"date": "2026-11-18", "steps": "abc", "place": "campus"})


def test_core_parse_walk_rejects_negative_steps():
    with pytest.raises(ValueError):
        parse_walk({"date": "2026-11-19", "steps": "-300", "place": "campus"})


def test_core_parse_walk_rejects_a_row_with_no_date():
    with pytest.raises(ValueError):
        parse_walk({"date": "", "steps": "5000", "place": "campus"})


def test_core_none_on_error_keeps_a_normal_result():
    @none_on_error
    def half(number: int) -> int:
        return number // 2

    assert half(10) == 5


def test_core_none_on_error_turns_a_value_error_into_none():
    @none_on_error
    def to_int(text: str) -> int:
        return int(text)

    assert to_int("abc") is None


def test_core_read_rows_yields_each_row_as_a_dict(tmp_path):
    path = tmp_path / "walks.csv"
    path.write_text("date,steps,place\n2026-11-16,4200,Lumphini Park\n", encoding="utf-8")
    rows = read_rows(path)
    assert isinstance(rows, Iterator)
    assert list(rows) == [{"date": "2026-11-16", "steps": "4200", "place": "Lumphini Park"}]


def test_core_good_walks_skips_the_bad_rows():
    rows = [
        {"date": "2026-11-17", "steps": "", "place": "campus"},
        {"date": "2026-11-17", "steps": "6800", "place": "Chatuchak market"},
    ]
    walks = good_walks(rows)
    assert isinstance(walks, Iterator)
    assert list(walks) == [Walk("2026-11-17", 6800, "Chatuchak market")]


def test_core_good_walks_reads_the_log_file():
    walks = list(good_walks(read_rows(WALKS_CSV)))
    assert len(walks) == 9
    assert walks[0] == Walk("2026-11-16", 4200, "Lumphini Park")
