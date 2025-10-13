import string

import pytest
from hypothesis import given
from hypothesis import strategies as st

from mergrave import echo


def test_echo_returns_input():
    sample = "Mergrave"
    assert echo(sample) == sample


@given(st.text(alphabet=string.printable))
def test_echo_property(text):
    assert echo(text) == text


@pytest.mark.parametrize("value", ["", "123", "test", "with spaces"])
def test_echo_parametrized(value):
    assert echo(value) == value

