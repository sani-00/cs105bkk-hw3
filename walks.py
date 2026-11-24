"""HW3 · walks.py: read the step counter's CSV file and keep only the good rows. Practises
Session 7 (reading a CSV file, cleaning data) and Session 9 (a generator and a decorator)."""

import csv
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Walk:
    """Provided: one walk from the log, cleaned. `steps` is a whole number, 0 or more."""

    date: str
    steps: int
    place: str


def parse_walk(row: dict[str, str]) -> Walk:
    """Turn one row of the CSV file into a Walk, or raise ValueError if the row is bad."""
    raise NotImplementedError("core: clean one row into a Walk, or raise ValueError for a bad row")


def none_on_error(func: Callable) -> Callable:
    """A decorator: the wrapped function returns None instead of raising ValueError."""
    raise NotImplementedError("core: wrap func so that a ValueError becomes None")


def read_rows(path: Path) -> Iterator[dict[str, str]]:
    """Yield the rows of a CSV file one at a time, each as a dict of text."""
    raise NotImplementedError("core: open the CSV file and yield its rows one at a time")


def good_walks(rows: Iterable[dict[str, str]]) -> Iterator[Walk]:
    """Yield a Walk for every good row, one at a time, and skip the bad rows."""
    raise NotImplementedError("core: yield a Walk for each good row and skip the bad ones")
