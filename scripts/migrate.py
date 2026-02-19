#!/usr/bin/env python3
"""Database migration script for production deployment"""

import os
import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_migrations():
    """Run database migrations"""
    print("[MIGRATE] Starting database migrations...")
    
    try:
        # Import after path is set
        from python.api.auth.auth_models import db, User, OAuth
        from run_ui import webapp
        
        with webapp.app_context():
            # Create all tables if they don't exist
            db.create_all()
            print("[MIGRATE] ✓ Database tables created/verified")
            
            # Check connection
            result = db.session.execute(db.text("SELECT 1")).scalar()
            if result == 1:
                print("[MIGRATE] ✓ Database connection verified")
            
            # Count existing records
            user_count = User.query.count()
            print(f"[MIGRATE] Current users: {user_count}")
            
            print("[MIGRATE] ✓ Migrations completed successfully")
            return True
            
    except ImportError as e:
        print(f"[MIGRATE] ⚠ Auth models not available: {e}")
        print("[MIGRATE] Skipping database migrations (no auth configured)")
        return True
        
    except Exception as e:
        print(f"[MIGRATE] ✗ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)