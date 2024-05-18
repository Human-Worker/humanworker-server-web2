from app.common.database import get_session


def get_db():
    return next(get_session())
