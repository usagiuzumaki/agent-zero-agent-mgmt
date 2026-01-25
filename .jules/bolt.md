# Bolt's Journal

## 2025-01-28 - [Optimizing Dynamic Python Filter]
**Learning:** `eval()` in Python is significantly slower when parsing the same string repeatedly in a loop. Compiling the string into a code object once using `compile()` reduced execution time by ~50x (from 23s to 0.4s for 10k items).
**Action:** When filtering large datasets using dynamic string conditions, always compile the condition once outside the loop.

## 2025-02-12 - [Optimizing simple_eval in Loops]
**Learning:** The `simpleeval` library, like `eval()`, incurs significant overhead when parsing expression strings repeatedly. In `python/helpers/memory.py`, replacing per-item `simple_eval(condition)` with a pre-compiled code object (via `compile()`) and standard `eval()` yielded a massive ~200x speedup (10s -> 0.05s for 10k items).
**Action:** For hot loops involving dynamic expression evaluation, prefer pre-compilation. Note that `eval()` on compiled code requires careful scoping (using empty globals `{}` and specific locals) to maintain safety similar to `simple_eval`, though `simple_eval` offers stronger sandboxing by default. The trade-off was deemed acceptable here to match `vector_db.py` patterns.

## 2025-02-17 - [Eliminating Defensive DeepCopy in Logging]
**Learning:** `copy.deepcopy()` was used in the hot path of logging (`python/helpers/log.py`) solely to prevent mutation during truncation. By rewriting the truncation logic to be functional (returning new objects instead of mutating in-place), we eliminated the expensive deepcopy step, resulting in a ~2x speedup for logging complex structures.
**Action:** When working with data transformation where immutability is required, prefer creating new collections (copy-on-traverse) over `deepcopy` + in-place mutation.

## 2025-02-24 - [Pre-compiling Regex in Helper Functions]
**Learning:** Pre-compiling regex patterns in frequently called helper functions (like `replace_placeholders_dict` which is recursive) yields significant speedups (1.4x), whereas for simple operations on long strings (`remove_code_fences`) the gain is marginal (1.01x) but improves code cleanliness.
**Action:** Prioritize regex pre-compilation for recursive or tight-loop functions.

## 2025-03-01 - [Unicode-Aware Non-Alphanumeric Regex]
**Learning:** `[^a-zA-Z0-9]` is not a safe replacement for `not c.isalnum()` as it strips Unicode characters. The correct Regex equivalent is `[\W_]`, which matches all non-word characters and underscores, leaving Unicode letters and digits intact.
**Action:** Use `re.compile(r'[\W_]')` when optimizing alphanumeric filters to preserve internationalization support.
