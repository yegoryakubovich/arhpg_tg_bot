from app.db.db import db
from app.db.manager import db_manager_sync
from app.db.models import models


@db_manager_sync
def tables_create():
    db.create_tables(models=models)
