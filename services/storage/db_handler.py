import logging

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from config import DATABASE_URL
from models import Base

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DBHandler:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self):
        """
        Initialize the database by creating all tables.
        """
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database initialized.")

    def store(self, db: Session, model, **kwargs):
        """
        Store data to the database.

        Args:
            model (Base): SQLAlchemy model class.
            kwargs: Column-value mappings for the model.

        Returns:
            The created model instance.
        """
        try:
            sanitized_data = self.sanitize_data(kwargs)

            instance = model(**sanitized_data)
            db.add(instance)
            db.commit()
            db.refresh(instance)
            return instance
        except Exception as e:
            db.rollback()
            raise e

    def sanitize_data(self, data: dict) -> dict:
            """
            Sanitize data before storing it in the database.

            Args:
                data (dict): Data to sanitize.

            Returns:
                dict: Sanitized data.
            """
            sanitized_data = data.copy()

            # Sanitize the `quantity` field
            if "quantity" in sanitized_data and isinstance(sanitized_data["quantity"], str):
                sanitized_data["quantity"] = int(sanitized_data["quantity"].replace(".", "")) if sanitized_data["quantity"] != "-" else None
            # Sanitize the `value` field
            if "value" in sanitized_data and isinstance(sanitized_data["value"], str):
                sanitized_data["value"] = int(sanitized_data["value"].replace(".", "")) if sanitized_data["value"] != "-" else None


            return sanitized_data