# File: database/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from settings import DATABASE_URL

_engine = create_engine(DATABASE_URL, echo=False, future=True)
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
