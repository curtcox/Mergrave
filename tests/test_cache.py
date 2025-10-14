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
