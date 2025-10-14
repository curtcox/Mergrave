# Unit

- Returns a cached result without invoking any tools or recursion when an exact cache hit exists.
- Skips all AI/tool work when a prior “no AI needed” decision is recorded for the same normalized input.
- When a tool response contains executable code with a “run” directive, executes it and returns the program output.
- Strips or masks inputs tagged as IP before any model or tool invocation.
- Maps internal results into the user-requested schema (e.g., JSON, Markdown) including required fields and formatting.
- On runtime error from executed code, records the error, retries only if retryable, and surfaces a structured failure otherwise.
- Invokes a fact-check tool on extractable claims and downgrades or replaces unsupported claims per policy.
- When given a tool-spec artifact, registers the new tool and successfully invokes it in a subsequent recursive step.
- Emits a structured trace containing decisions, tool calls, depths, scores, and errors sufficient to replay the plan offline.
- Cache hit: identical normalized input returns the cached result with zero AI/tool calls or recursion.
- Base case termination: when the request can be satisfied directly, the function returns without recursion or tool use.
- Single AI call success: a request requiring exactly one AI call executes once and returns the expected result.
- Error propagation: errors from AI calls, tools, or executed code are caught, wrapped with context, and propagated up the recursion stack.
- Tool selection: given unambiguous intent and an available toolset, the correct tool is chosen deterministically.
- Context transformation: inputs are normalized/optimized before the AI call while preserving semantics.
- Code generation and execution: generated code is sandboxed, executed, and its outputs (stdout/stderr/exit) feed the next step.
- Output reformatting: AI/tool outputs are converted to the requested schema/format before returning or recursing.
- Fact-check integration: extractable claims are verified and unsupported claims are downgraded or replaced per policy.
- Tool creation during execution: when no suitable tool exists, a new tool is registered and successfully invoked in the same run.
- Structured trace emission: each run produces a replayable trace of decisions, tool calls, depths, scores, and errors.

# Property
- For any DAG of tool dependencies, invokes tools in a topologically valid order without cycles.
- At every recursion depth, outputs containing prohibited knowledge are redacted or blocked before returning upward.
- Constructed prompt/context never exceeds the configured token budget.
- Input normalization is idempotent and monotonic with respect to whitespace, casing, and punctuation rules.
- If the quality score is below threshold, a recursive improvement pass is triggered; otherwise it returns immediately.
- Decomposition produces subproblems whose combined scope covers the original request with bounded redundancy.
- Given unambiguous intent, the tool selector chooses the correct tool with precision 1.0 on provided fixtures.
- Tool invocations include only the minimal required arguments and exclude PII unless explicitly authorized.
- Retry logic attempts retryable failures at most N times with exponential backoff and never retries non-retryable errors.
- Across multiple candidate responses, returns the one with the highest composite score according to the configured objective.
- Cache keys are deterministic and invariant to commutative parameter ordering for the same semantic request.
- Recursion always terminates by honoring depth_limit or budget_limit and returns a graceful fallback when limits are hit.
- Cumulative cost (tokens × calls) never exceeds the configured budget, and near-budget the planner prunes lower-value branches first.
- Forbidden context guard (input): requests containing IP/forbidden content are rejected before any AI/tool invocation.
- Maximum recursion depth: exceeding the configured depth yields a graceful, structured termination rather than unbounded recursion.
- Topological sequencing: for multi-step plans, tools are invoked in dependency-respecting order without cycles.
- Circular dependency detection: mutually dependent subtasks are identified and halted without entering infinite recursion.
- Normalization idempotence: applying normalization twice yields the same result as applying it once.
- Forbidden content guard (output): any prohibited knowledge in outputs is redacted or blocked prior to return.
- Quality threshold: results below the minimum quality trigger an improvement pass; acceptable results return immediately.
- Retry policy: retryable failures backoff and retry up to N times, and non-retryable errors are never retried.
- Recursive decomposition: complex tasks decompose into subproblems that collectively cover the original goal with bounded overlap.
- Multi-attempt best selection: among multiple candidate solutions, the highest composite-scoring result is returned.
- Parallel execution optimization: independent subtasks run concurrently when enabled and their results are deterministically merged.
- Token/cost budgeting: context never exceeds token limits and cumulative cost respects budget, pruning low-value branches near limits.
- Cache key determinism: semantically equivalent requests yield identical cache keys despite parameter ordering or superficial differences.




