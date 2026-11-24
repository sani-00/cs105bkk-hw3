"""Part 10: your own tests for parse_walk. The README says what to write here.

We grade this file by running it against a correct walks.py, where every test must pass,
and against versions of walks.py with a bug planted in parse_walk, where your tests should fail.
"""

import pytest

from walks import Walk, parse_walk


@pytest.fixture
def good_row() -> dict[str, str]:
    """Provided: one good row, as csv.DictReader gives it. Each test gets its own new copy."""
    return {"date": "2026-11-16", "steps": "4200", "place": "Lumphini Park"}


def test_core_example_a_good_row_becomes_a_walk(good_row):
    """Provided: an example that uses the fixture. Write your own tests below it."""
    assert parse_walk(good_row) == Walk("2026-11-16", 4200, "Lumphini Park")


# Your tests go here.
