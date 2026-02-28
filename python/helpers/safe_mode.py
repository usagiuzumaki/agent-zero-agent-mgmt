import os
from python.helpers.print_style import PrintStyle

def is_safe_mode():
    """
    Returns True if OPERATIONAL_SAFE_MODE is enabled.
    In safe mode, external side effects (like actual payments or social media posts) should be blocked or mocked.
    """
    return os.getenv("OPERATIONAL_SAFE_MODE", "false").lower() == "true"

def block_side_effect(feature_name):
    """
    Helper to check safe mode and raise/log if a side effect is attempted.
    """
    if is_safe_mode():
        PrintStyle().warning(f"[SAFE MODE] Blocked side effect for: {feature_name}")
        return True
    return False
