"""Tests for recursion guard helper behavior."""

from __future__ import annotations

import importlib.util
from itertools import product

import pytest

from mergrave import RecursiveExecutionError, recursion_with_limits

skip_hypothesis = pytest.mark.skip(reason="hypothesis is required for property tests")

if importlib.util.find_spec("hypothesis") is not None:
    from hypothesis import assume, given
    from hypothesis import strategies as st

    @pytest.mark.property
    @given(
        depth_limit=st.integers(min_value=0, max_value=50),
        budget_limit=st.integers(min_value=0, max_value=50),
        fallback=st.text(max_size=5),
    )
    def test_property_recursion_honors_limits(
        depth_limit: int, budget_limit: int, fallback: str
    ) -> None:
        """Recursion respects limits and returns the provided fallback when hit."""

        calls = 0

        def work(step: int) -> bool:
            nonlocal calls
            calls += 1
            return True

        result, steps = recursion_with_limits(
            depth_limit, budget_limit, work, fallback
        )

        assert result == fallback
        assert steps == min(depth_limit, budget_limit)
        assert calls == steps
        assert steps <= depth_limit
        assert steps <= budget_limit

    @pytest.mark.property
    @given(
        depth_limit=st.integers(min_value=1, max_value=50),
        budget_limit=st.integers(min_value=1, max_value=50),
        target_steps=st.integers(min_value=0, max_value=50),
    )
    def test_property_recursion_returns_completion_when_work_finishes(
        depth_limit: int, budget_limit: int, target_steps: int
    ) -> None:
        """The helper returns completion when ``work`` stops before limits."""

        assume(target_steps < min(depth_limit, budget_limit))

        calls = 0

        def work(step: int) -> bool:
            nonlocal calls
            calls += 1
            return step < target_steps

        result, steps = recursion_with_limits(depth_limit, budget_limit, work)

        assert result == "completed"
        assert steps == target_steps
        assert calls == steps + 1
        assert steps < depth_limit
        assert steps < budget_limit
else:

    @pytest.mark.property
    @skip_hypothesis
    def test_property_recursion_honors_limits() -> None:
        """Placeholder when hypothesis is unavailable."""

    @pytest.mark.property
    @skip_hypothesis
    def test_property_recursion_returns_completion_when_work_finishes() -> None:
        """Placeholder when hypothesis is unavailable."""


@pytest.mark.parametrize(
    "depth_limit, budget_limit",
    list(product(range(0, 6), repeat=2)),
)
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


def test_recursion_returns_direct_result_without_recursing() -> None:
    """A direct answer short-circuits recursion and avoids tool usage."""

    calls = 0

    def work(step: int) -> bool:  # pragma: no cover - should not run
        nonlocal calls
        calls += 1
        return True

    result, steps = recursion_with_limits(
        depth_limit=5,
        budget_limit=5,
        work=work,
        fallback="unused",
        direct_result="cached",
    )

    assert result == "cached"
    assert steps == 0
    assert calls == 0


@pytest.mark.parametrize(
    "depth_limit, budget_limit",
    [(-1, 0), (0, -1), (-5, -5)],
)
def test_recursion_rejects_negative_limits(depth_limit: int, budget_limit: int) -> None:
    """Negative limits are rejected with a ``ValueError``."""

    with pytest.raises(ValueError):
        recursion_with_limits(depth_limit, budget_limit, lambda _: False)


def test_recursion_wraps_errors_with_context() -> None:
    """Errors are wrapped with recursion context as they propagate."""

    def work(step: int) -> bool:
        if step == 1:
            raise RuntimeError("tool failure")
        return True

    with pytest.raises(RecursiveExecutionError) as excinfo:
        recursion_with_limits(depth_limit=3, budget_limit=3, work=work)

    outer_error = excinfo.value
    assert outer_error.step == 0
    assert outer_error.depth_remaining == 3
    assert outer_error.budget_remaining == 3
    assert outer_error.original_exception is outer_error.__cause__
    assert "step 0" in str(outer_error)
    assert "depth_remaining=3" in str(outer_error)
    assert "budget_remaining=3" in str(outer_error)

    inner_error = outer_error.__cause__
    assert isinstance(inner_error, RecursiveExecutionError)
    assert inner_error.step == 1
    assert inner_error.depth_remaining == 2
    assert inner_error.budget_remaining == 2
    assert inner_error.original_exception is inner_error.__cause__
    assert isinstance(inner_error.__cause__, RuntimeError)
    assert str(inner_error.__cause__) == "tool failure"
