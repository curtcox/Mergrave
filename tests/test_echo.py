"""Tests for the ``echo`` helper."""

import string

import pytest

from mergrave import echo


def test_echo_returns_input() -> None:
    sample = "Mergrave"
    assert echo(sample) == sample


@pytest.mark.parametrize(
    "value",
    [
        "", "123", "test", "with spaces", string.ascii_letters, string.punctuation,
    ],
)
def test_echo_parametrized(value: str) -> None:
    assert echo(value) == value


def test_echo_handles_all_printable_characters() -> None:
    text = string.printable
    assert echo(text) == text
