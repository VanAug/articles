# scripts/setup_db.py
import sys
import os

# Add the project root to sys.path so lib/ can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.db.connection import CONN, CURSOR


def setup_database():
    with open("lib/db/schema.sql") as file:
        CURSOR.executescript(file.read())
    CONN.commit()
    print("✅ Database setup complete.")

def load_schema():
    with open("lib/db/schema.sql") as file:
        sql_script = file.read()
        CURSOR.executescript(sql_script)
        CONN.commit()

if __name__ == "__main__":
    load_schema()

