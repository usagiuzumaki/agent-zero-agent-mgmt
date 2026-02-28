import os
import sys
from python.helpers.print_style import PrintStyle

REQUIRED_VARS = [
    "SESSION_SECRET",
]

# Vars required for specific features
FEATURE_VARS = {
    "auth": ["GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "AUTH_BASE_URL"],
    "stripe": ["STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET"],
}

def validate_config():
    """
    Validates that the environment is correctly configured.
    Fails fast if critical variables are missing.
    """
    missing = []
    for var in REQUIRED_VARS:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        PrintStyle().error(f"FATAL: Missing required environment variables: {', '.join(missing)}")
        PrintStyle().error("Please check your .env file or environment settings.")
        sys.exit(1)

    # Check for feature-specific configs and warn if incomplete
    for feature, vars in FEATURE_VARS.items():
        feature_missing = [v for v in vars if not os.getenv(v)]
        if feature_missing and len(feature_missing) < len(vars):
            PrintStyle().warning(f"Incomplete {feature} configuration. Missing: {', '.join(feature_missing)}")
        elif feature_missing and len(feature_missing) == len(vars):
            PrintStyle().info(f"{feature.capitalize()} feature is disabled (no configuration found).")

    return True

if __name__ == "__main__":
    # Test validator
    validate_config()
