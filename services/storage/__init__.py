from .storage_enums import PageModelMapping
from .storage_enums import ColumnKeyMapping
from services.storage.db_handler import DBHandler

# Create a global instance of DBHandler
db_handler = DBHandler()

# Dependency function
def get_db():
    """
    Dependency function to provide a SQLAlchemy session.
    """
    db = db_handler.SessionLocal()
    try:
        yield db
    finally:
        db.close()
