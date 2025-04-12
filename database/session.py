# File: database/session.py
# Purpose: Manage SQLAlchemy engine and session creation for OptiBatch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# You can use an environment variable for production vs dev
DB_URL = os.getenv("DATABASE_URL", "")

_engine = create_engine(DB_URL, echo=False, future=True)
_SessionLocal = sessionmaker(
    bind=_engine, autoflush=False, autocommit=False, future=True
)


def get_engine():
    return _engine


@contextmanager
def get_session(engine=None):
    engine = engine or _engine
    session = _SessionLocal(bind=engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
