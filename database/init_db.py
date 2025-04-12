# File: database/init_db.py

from database.session import get_engine
from database.models import Base

if __name__ == "__main__":
    engine = get_engine()
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Done.")
