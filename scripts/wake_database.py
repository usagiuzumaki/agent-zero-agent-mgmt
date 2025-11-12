#!/usr/bin/env python3
"""
Wake up the Neon PostgreSQL database
"""
import os
import sys
import time
from urllib.parse import urlparse
import pg8000.native

def wake_database():
    """Wake up the sleeping Neon database"""
    try:
        # Get database URL from environment
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in environment variables")
            return False
        
        # Parse the database URL
        url = urlparse(database_url)
        
        # Extract connection parameters
        host = url.hostname
        port = url.port or 5432
        database = url.path[1:]  # Remove leading '/'
        user = url.username
        password = url.password
        
        print("🔄 Attempting to wake up the Neon database...")
        print(f"   Host: {host}")
        print(f"   Database: {database}")
        print(f"   User: {user}")
        
        # Try to connect with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Connect using pg8000
                conn = pg8000.native.Connection(
                    host=host,
                    port=port,
                    database=database,
                    user=user,
                    password=password,
                    ssl_context=True
                )
                
                # Run a simple query to wake the database
                result = conn.run("SELECT 1")
                print(f"✅ Database is now awake! Query result: {result}")
                
                # Check if our User table exists
                tables = conn.run("""
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public'
                """)
                print(f"📊 Found {len(tables)} tables in the database")
                if tables:
                    print("   Tables:", [t[0] for t in tables])
                
                conn.close()
                return True
                
            except Exception as e:
                print(f"   Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    print(f"   Waiting 2 seconds before retry...")
                    time.sleep(2)
        
        print("❌ Failed to wake database after all retries")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = wake_database()
    sys.exit(0 if success else 1)