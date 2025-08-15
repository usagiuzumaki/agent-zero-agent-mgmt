# Problem
Analyze screenplay structure and dialogue distribution.

# Solution
1. If the file is stored elsewhere, change directory to it.
2. Run the analyzer with the screenplay path:

```bash
bash /a0/instruments/default/script_analyzer/script_analyzer.sh <path>
```

3. Replace `<path>` with your script file.
4. The command prints JSON with scene count, character list, and dialogue line tallies.
