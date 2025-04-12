# File: dev/tools/check_connection.py

from sqlalchemy import text
from database.session import get_engine


def test_db_connection():
    engine = get_engine()
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful:", result.scalar())
    except Exception as e:
        print("❌ Database connection failed:", e)


if __name__ == "__main__":
    test_db_connection()
