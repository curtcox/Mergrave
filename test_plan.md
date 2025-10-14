# To Do

## Unit

- Skips all AI/tool work when a prior “no AI needed” decision is recorded for the same normalized input.
- When a tool response contains executable code with a “run” directive, executes it and returns the program output.
- Strips or masks inputs tagged as IP before any model or tool invocation.
- Maps internal results into the user-requested schema (e.g., JSON, Markdown) including required fields and formatting.
- On runtime error from executed code, records the error, retries only if retryable, and surfaces a structured failure otherwise.
- Invokes a fact-check tool on extractable claims and downgrades or replaces unsupported claims per policy.
- When given a tool-spec artifact, registers the new tool and successfully invokes it in a subsequent recursive step.
- Emits a structured trace containing decisions, tool calls, depths, scores, and errors sufficient to replay the plan offline.
- Cache hit: identical normalized input returns the cached result with zero AI/tool calls or recursion.
- Single AI call success: a request requiring exactly one AI call executes once and returns the expected result.
- Error propagation: errors from AI calls, tools, or executed code are caught, wrapped with context, and propagated up the recursion stack.
- Tool selection: given unambiguous intent and an available toolset, the correct tool is chosen deterministically.
- Context transformation: inputs are normalized/optimized before the AI call while preserving semantics.
- Code generation and execution: generated code is sandboxed, executed, and its outputs (stdout/stderr/exit) feed the next step.
- Output reformatting: AI/tool outputs are converted to the requested schema/format before returning or recursing.
- Fact-check integration: extractable claims are verified and unsupported claims are downgraded or replaced per policy.
- Tool creation during execution: when no suitable tool exists, a new tool is registered and successfully invoked in the same run.
- Structured trace emission: each run produces a replayable trace of decisions, tool calls, depths, scores, and errors.

## Property
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

## Integration

- End-to-end cache hit: with the request pre-seeded in cache, the function returns the cached answer without invoking any tools or recursion and emits a minimal trace showing only a cache read.
- “No AI needed” short-circuit: with a prior decision artifact stored for the normalized input, the function skips tool calls and recursion and returns the previously approved final output.
- Code-gen→exec path: a tool returns runnable code with a “run” directive, the function executes it in the sandbox, captures stdout/stderr, and returns the program output in the requested schema.
- Multi-tool pipeline: the function performs input transformation, generation, formatting, and post-processing across at least three tools in the correct order and returns the composed result.
- IP guard on ingress: inputs tagged as restricted IP are masked before any tool/model call at every recursion depth, and the trace proves no raw IP leaves the guard.
- Forbidden knowledge on egress: a tool emits disallowed content, the function redacts/blocks it, triggers a safe-rewrite pass, and returns a compliant substitute.
- Fact-check loop: extracted claims are sent to a fact-checker, failing claims cause a recursive revision, and the final answer cites only verified claims with downgraded confidence noted where applicable.
- Quality-gate improvement: an initial draft scores below threshold, the function triggers one improvement recursion and returns the improved version once the score exceeds the threshold.
- Decompose→solve→merge: the function splits the request into subproblems, solves them (some in parallel branches), and merges results into a coherent final answer that covers all subgoals.
- Token-budget orchestration: given a tight context limit, the function prunes low-value context, compresses history, and completes the run without exceeding the budget.
- Tool selection under cost: with multiple viable tools, the function selects the cheapest toolchain that still meets quality constraints per configured objective, as evidenced by the trace.
- Transient failure with retry: a tool fails with a retryable error once, the function applies exponential backoff and succeeds on the next attempt, logging both attempts.
- Non-retryable failure surface: a tool returns a hard error, the function does not retry, produces a structured failure payload, and includes actionable remediation in the output.
- New-tool bootstrap: given a tool-spec artifact, the function registers the tool during the run and successfully invokes it in a subsequent recursive step to complete the task.
- Best-of-N candidate selection: the function generates multiple candidates via different tool plans, scores them with a judge, and returns the highest-scoring candidate with ranking metadata.
- Code-exec repair loop: generated code fails at runtime, the function captures logs, performs an error-aware fix-and-rerun recursion, and returns the successful run’s output.
- Depth and budget limits: with adversarial inputs that encourage infinite improvement, the function terminates at depth_limit or budget_limit and returns the best partial answer plus a summary of remaining gaps.
- Subgraph caching: during a composite task, repeated identical subrequests are served from the run-local cache while other branches continue to use tools, reducing total calls as shown in the trace.
- Output reformatting: upstream tools return heterogeneous structures, and the function emits the final answer in the exact user-requested schema (e.g., JSON with required fields and order).
- Safety at all depths: a prohibited string inserted by a deep tool call is detected and removed before it can propagate to siblings or the final output, with a trace entry at the offending depth.
- Research→synthesis: with a “research existing solutions” goal, the function uses the research tool, deduplicates overlapping findings, and synthesizes a unified, non-plagiarized response with attribution.

# Done

## Unit
- Base case termination: when the request can be satisfied directly, the function returns without recursion or tool use.
- Returns a cached result without invoking any tools or recursion when an exact cache hit exists.

## Property
- Recursion always terminates by honoring depth_limit or budget_limit and returns a graceful fallback when limits are hit.

## Integration


