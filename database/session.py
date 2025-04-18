# File: database/session.py

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from settings import DATABASE_URL

from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
from loguru import logger

from database.models import Base
from datetime import datetime
from typing import Generator
from sqlalchemy.orm import Session

# Create the engine and session factory
_engine = create_engine(DATABASE_URL, echo=False, future=True)
_SessionLocal = sessionmaker(
    bind=_engine, autoflush=False, autocommit=False, future=True
)


def get_engine():
    return _engine


@contextmanager
def get_session(engine=None, **kwargs) -> Generator[Session, None, None]:
    engine = engine or _engine
    session = _SessionLocal(bind=engine, **kwargs)
    try:
        yield session
        session.commit()
    except SQLAlchemyError as db_err:
        logger.error(f"💥 SQLAlchemy error during session: {db_err}")
        session.rollback()
        raise
    except Exception as err:
        logger.error(f"❌ Unexpected error during session: {err}")
        session.rollback()
        raise
    finally:
        session.close()


def _should_create_sqlite_schema() -> bool:
    if not DATABASE_URL.startswith("sqlite:///"):
        return False

    db_path = Path(DATABASE_URL.removeprefix("sqlite:///"))
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Case 1: File doesn't exist
    if not db_path.exists():
        return True

    # Case 2: File exists but tables are missing
    inspector = inspect(_engine)
    tables = inspector.get_table_names()
    required_tables = {"jobs", "runs"}
    return not required_tables.issubset(set(tables))


if _should_create_sqlite_schema():
    from database.models import Job, Run  # Import models to register them

    Base.metadata.create_all(bind=_engine)
    logger.info("✅ SQLite schema created.")
