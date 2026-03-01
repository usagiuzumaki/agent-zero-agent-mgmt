import os
import sys
from flask import Flask

# Add project root to sys.path
sys.path.append(os.getcwd())

from auth_models import init_db, db
from python.helpers.aria_models import *

def main():
    app = Flask(__name__)

    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Initialize DB
    if init_db(app):
        with app.app_context():
            print("Creating Aria specific tables...")
            db.create_all()
            print("Successfully initialized Aria database tables.")
    else:
        print("Failed to initialize database connection.")

if __name__ == "__main__":
    main()
