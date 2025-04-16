# backend/db
from database.session import get_session as _get_session


def get_session():
    return _get_session()
