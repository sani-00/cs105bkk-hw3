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
"""My own tests for parse_walk."""

import pytest

from walks import Walk, parse_walk


@pytest.fixture
def good_row() -> dict[str, str]:
    """One good example row."""
    return {
        "date": "2026-11-16",
        "steps": "4200",
        "place": "Lumphini Park",
    }


def test_good_row_becomes_a_walk(good_row):
    assert parse_walk(good_row) == Walk(
        "2026-11-16", 4200, "Lumphini Park"
    )


def test_date_and_place_are_stripped(good_row):
    good_row["date"] = " 2026-11-16 "
    good_row["place"] = " campus "

    assert parse_walk(good_row) == Walk(
        "2026-11-16", 4200, "campus"
    )


def test_zero_steps_is_valid(good_row):
    good_row["steps"] = "0"

    assert parse_walk(good_row).steps == 0


def test_spaces_around_steps_are_valid(good_row):
    good_row["steps"] = " 3100 "

    assert parse_walk(good_row).steps == 3100


@pytest.mark.parametrize(
    "field,value",
    [
        ("date", ""),
        ("date", "   "),
        ("steps", ""),
        ("steps", "abc"),
        ("steps", "12.5"),
        ("steps", "-1"),
        ("steps", "-300"),
    ],
)
def test_invalid_date_or_steps_raise_value_error(
    good_row, field, value
):
    good_row[field] = value

    with pytest.raises(ValueError):
        parse_walk(good_row)