"""Property-based tests for recursion guard helpers."""

from __future__ import annotations

from hypothesis import given, strategies as st

from mergrave import recursion_with_limits


@given(
    depth_limit=st.integers(min_value=0, max_value=100),
    budget_limit=st.integers(min_value=0, max_value=100),
)
def test_recursion_honors_limits(depth_limit: int, budget_limit: int) -> None:
    """Recursion terminates with a fallback whenever limits are exhausted."""

    calls = 0

    def work(step: int) -> bool:  # pragma: no cover - executed via property testing
        nonlocal calls
        calls += 1
        return True

    result, steps = recursion_with_limits(depth_limit, budget_limit, work)

    assert result == "limit reached"
    assert steps == min(depth_limit, budget_limit)
    assert calls == steps
    assert steps <= depth_limit
    assert steps <= budget_limit
