# Bolt's Journal

## 2025-01-28 - [Optimizing Dynamic Python Filter]
**Learning:** `eval()` in Python is significantly slower when parsing the same string repeatedly in a loop. Compiling the string into a code object once using `compile()` reduced execution time by ~50x (from 23s to 0.4s for 10k items).
**Action:** When filtering large datasets using dynamic string conditions, always compile the condition once outside the loop.
