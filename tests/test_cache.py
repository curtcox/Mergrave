"""Tests for cache-aware execution helpers."""

from __future__ import annotations

from mergrave import cached_execution


def test_cached_execution_returns_cached_result_without_work() -> None:
    """An exact cache hit skips both tool usage and recursion."""

    cache: dict[str, str] = {"normalized": "cached result"}

    tool_calls = 0
    recursion_calls = 0

    def invoke_tool() -> str:
        nonlocal tool_calls
        tool_calls += 1
        return "tool output"

    def run_recursive() -> str:
        nonlocal recursion_calls
        recursion_calls += 1
        return "final result"

    def executor() -> str:
        invoke_tool()
        return run_recursive()

    result = cached_execution("normalized", cache, executor)

    assert result == "cached result"
    assert tool_calls == 0
    assert recursion_calls == 0


def test_cached_execution_runs_executor_once_on_cache_miss() -> None:
    """A single uncached request triggers exactly one executor invocation."""

    cache: dict[str, str] = {}

    executor_calls = 0

    def executor() -> str:
        nonlocal executor_calls
        executor_calls += 1
        return "fresh result"

    result = cached_execution("normalized", cache, executor)

    assert result == "fresh result"
    assert executor_calls == 1
    # Subsequent calls should reuse the cached value without rerunning the executor.
    second_result = cached_execution("normalized", cache, executor)

    assert second_result == "fresh result"
    assert executor_calls == 1
