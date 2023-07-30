from app.db.db import db


def db_manager(function):
    async def wrapper(*args):
        with db:
            return await function(*args)

    return wrapper


def db_manager_sync(function):
    def wrapper(*args, **kwargs):
        with db:
            result = function(*args, **kwargs)
        return result

    return wrapper
