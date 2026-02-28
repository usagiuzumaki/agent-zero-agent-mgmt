import os
from python.helpers.print_style import PrintStyle

def check_db():
    """
    Checks if the primary database is reachable.
    """
    # Using the lazy initialization pattern common in the app
    try:
        from auth_models import db
        # Attempt a simple query
        db.session.execute("SELECT 1")
        return True, "Database reachable"
    except Exception as e:
        return False, f"Database error: {str(e)}"

def check_config():
    """
    Checks if critical config is valid.
    """
    from python.helpers.config_validator import REQUIRED_VARS
    missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
    if missing:
        return False, f"Missing config: {', '.join(missing)}"
    return True, "Config valid"

def perform_ready_check():
    """
    Runs all readiness checks.
    """
    results = {}

    db_ok, db_msg = check_db()
    results["database"] = {"status": "ok" if db_ok else "error", "message": db_msg}

    cfg_ok, cfg_msg = check_config()
    results["config"] = {"status": "ok" if cfg_ok else "error", "message": cfg_msg}

    overall_ok = db_ok and cfg_ok
    return overall_ok, results
