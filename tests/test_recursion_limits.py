"""Tests for recursion guard helper behavior."""

from __future__ import annotations

from itertools import product

import pytest

from mergrave import recursion_with_limits


@pytest.mark.parametrize("depth_limit, budget_limit", list(product(range(0, 6), repeat=2)))
def test_recursion_honors_limits(depth_limit: int, budget_limit: int) -> None:
    """Recursion terminates with a fallback whenever limits are exhausted."""

    calls = 0

    def work(step: int) -> bool:
        nonlocal calls
        calls += 1
        return True

    result, steps = recursion_with_limits(depth_limit, budget_limit, work)

    assert result == "limit reached"
    assert steps == min(depth_limit, budget_limit)
    assert calls == steps
    assert steps <= depth_limit
    assert steps <= budget_limit


@pytest.mark.parametrize(
    "depth_limit, budget_limit, target_steps",
    [
        (1, 1, 0),
        (3, 5, 2),
        (10, 10, 7),
        (50, 10, 5),
        (10, 50, 8),
    ],
)
def test_recursion_returns_completion_when_work_finishes(
    depth_limit: int, budget_limit: int, target_steps: int
) -> None:
    """The helper returns a completion result when ``work`` signals done."""

    calls = 0

    def work(step: int) -> bool:
        nonlocal calls
        calls += 1
        return step < target_steps

    result, steps = recursion_with_limits(depth_limit, budget_limit, work)

    assert result == "completed"
    assert steps == target_steps
    assert calls == steps + 1  # Final call that returned False.
    assert steps <= depth_limit
    assert steps <= budget_limit


@pytest.mark.parametrize(
    "depth_limit, budget_limit",
    [(-1, 0), (0, -1), (-5, -5)],
)
def test_recursion_rejects_negative_limits(depth_limit: int, budget_limit: int) -> None:
    """Negative limits are rejected with a ``ValueError``."""

    with pytest.raises(ValueError):
        recursion_with_limits(depth_limit, budget_limit, lambda _: False)
