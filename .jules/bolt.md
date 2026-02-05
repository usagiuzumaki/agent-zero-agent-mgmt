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

## 2025-05-21 - [Optimizing DirtyJson Parser]
**Learning:** String concatenation in a loop (O(N^2)) and character-by-character processing in Python are extremely slow for large strings. Replacing a character-loop with `str.find()` and slicing (O(1) loop overhead) reduced execution time by ~300x (3.5s -> 0.01s) for parsing large multiline strings.
**Action:** When parsing strings, avoid iterating by character if possible. Use built-in string methods like `find`, `index`, and slicing which are implemented in C and highly optimized.

## 2025-10-27 - [Re-compiling Compiled Regex Patterns]
**Learning:** `re.compile(compiled_pattern_object)` is significantly slower (~18x slower in benchmarks) than `re.compile(string_or_bytes_pattern)`. This is because `re.compile(string)` hits an optimized internal cache, whereas `re.compile(object)` performs type checking and overhead without the same caching benefit.
**Action:** When writing helper functions that accept regex patterns (which might be pre-compiled), check `isinstance(p, re.Pattern)` first. If it's already compiled, use it directly; otherwise, compile it. Do not blindly call `re.compile(p)` on everything.
