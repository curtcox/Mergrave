"""Mergrave placeholder library."""

from collections.abc import Callable, MutableMapping
from typing import TypeVar

_ResultT = TypeVar("_ResultT")


def echo(value: str) -> str:
    """Return the input value unchanged.

    This placeholder demonstrates a trivial pure function that can be tested
    with both example-based and property-based testing strategies.
    """

    return value


def recursion_with_limits(
    depth_limit: int,
    budget_limit: int,
    work: Callable[[int], bool],
    fallback: str = "limit reached",
    *,
    direct_result: str | None = None,
) -> tuple[str, int]:
    """Recursively execute ``work`` while respecting the provided limits.

    The ``work`` callable receives the number of completed steps and should
    return ``True`` when another recursive step is required. Whenever either
    limit is exhausted the function stops recursing and returns ``fallback``
    together with the amount of work completed. If ``work`` indicates
    completion before the limits are reached, the function returns
    ``("completed", steps)``. When ``direct_result`` is provided, the helper
    skips recursion entirely and returns ``(direct_result, 0)`` without
    invoking ``work``.
    """

    if depth_limit < 0 or budget_limit < 0:
        msg = "depth_limit and budget_limit must be non-negative"
        raise ValueError(msg)

    if direct_result is not None:
        return direct_result, 0
    def _recurse(
        depth_remaining: int, budget_remaining: int, steps: int
    ) -> tuple[str, int]:
        if depth_remaining <= 0 or budget_remaining <= 0:
            return fallback, steps

        if not work(steps):
            return "completed", steps

        return _recurse(depth_remaining - 1, budget_remaining - 1, steps + 1)

    return _recurse(depth_limit, budget_limit, 0)


def cached_execution(
    cache_key: str,
    cache: MutableMapping[str, _ResultT],
    executor: Callable[[], _ResultT],
) -> _ResultT:
    """Return a cached result when available without running the executor.

    The helper inspects ``cache`` for ``cache_key``. When a hit is found the
    cached value is returned immediately and the ``executor`` is never invoked.
    Otherwise ``executor`` runs and its result is stored under ``cache_key`` for
    future lookups before being returned.
    """

    try:
        return cache[cache_key]
    except KeyError:
        result = executor()
        cache[cache_key] = result
        return result

