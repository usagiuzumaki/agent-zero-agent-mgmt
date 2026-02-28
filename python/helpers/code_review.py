import sys
from python.helpers.print_style import PrintStyle

def run_checks():
    PrintStyle().info("Running production readiness checks...")

    checks = [
        ("Config Validator", "python/helpers/config_validator.py"),
        ("Readiness Check", "python/helpers/ready_check.py"),
        ("Structured Logging", "python/helpers/logger.py"),
        ("Safe Mode", "python/helpers/safe_mode.py"),
        ("Agent Registry", "python/helpers/agent_registry.py"),
        ("CI Workflow", ".github/workflows/ci.yml"),
        ("Makefile", "Makefile"),
        ("Architecture Doc", "docs/ARCHITECTURE.md"),
        ("Reality Map", "docs/REALITY_MAP.md")
    ]

    all_ok = True
    for name, path in checks:
        if os.path.exists(path):
            PrintStyle().success(f"✓ {name} exists at {path}")
        else:
            PrintStyle().error(f"✗ {name} missing at {path}")
            all_ok = False

    return all_ok

if __name__ == "__main__":
    import os
    if run_checks():
        PrintStyle().success("All production readiness files are present.")
    else:
        sys.exit(1)
