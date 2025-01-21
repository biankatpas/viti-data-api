import logging

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from config import DATABASE_URL
from models import Base

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DBHandler:
    """
    A handler class for managing database operations, including initialization,
    data storage, retrieval, and sanitization.

    Attributes:
        engine (sqlalchemy.engine.Engine): SQLAlchemy engine instance.
        SessionLocal (sqlalchemy.orm.sessionmaker): Factory for creating database sessions.

    Methods:
        init_db():
            Initializes the database by creating all tables.

        store(db: Session, model, **kwargs):
            Stores data into the database, creating or updating records.

        retrieve(db: Session, model, years: list = None) -> list:
            Retrieves rows from the database, optionally filtered by a list of years.

        sanitize_data(data: dict) -> dict:
            Sanitizes data before storing it into the database.
    """

    def __init__(self):
        """
        Initializes the DBHandler by setting up the database engine and session factory.
        """

        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self):
        """
        Initializes the database by creating all tables defined in the SQLAlchemy models.

        Logs:
            - Info: When database initialization starts and completes.
        """

        logger.info("Initializing database...")
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database initialized.")

    def store(self, db: Session, model, **kwargs):
        """
        Stores data into the database with an update-or-create approach.

        Args:
            db (Session): SQLAlchemy session instance.
            model (Base): SQLAlchemy model class representing the target table.
            kwargs: Column-value mappings for the model.

        Returns:
            The created or updated model instance.

        Raises:
            Exception: If an error occurs during the database transaction.
        """

        try:
            # Sanitize the data before processing
            sanitized_data = self.sanitize_data(kwargs)

            # Build dynamic filters based on model columns
            filters = {key: value for key, value in sanitized_data.items() if key in model.__table__.columns.keys()}

            # Check for an existing instance
            instance = db.query(model).filter_by(**filters).first()

            if instance:
                # Update existing record
                for key, value in sanitized_data.items():
                    if key in model.__table__.columns.keys():
                        setattr(instance, key, value)
            else:
                # Create a new record
                instance = model(**sanitized_data)
                db.add(instance)

            # Commit the transaction
            db.commit()
            db.refresh(instance)

            return instance
        except Exception as e:
            db.rollback()
            raise Exception(f"Error storing data: {e}")

    def retrieve(self, db: Session, model, years: list = None) -> list:
        """
        Retrieves rows from a given table, optionally filtering by years.

        Args:
            db (Session): SQLAlchemy session instance.
            model (Base): SQLAlchemy model class representing the target table.
            years (list, optional): List of years to filter by. Defaults to None,
                                    which retrieves all rows.

        Returns:
            list: List of rows matching the criteria.

        Raises:
            Exception: If an error occurs during the query.

        Logs:
            - Error: If an exception is raised during the query.
        """

        try:
            if years:
                return db.query(model).filter(model.year.in_(years)).all()
            return db.query(model).all()
        except Exception as e:
            logger.error(f"Error retrieving data from {model.__tablename__}: {e}")
            raise e

    def sanitize_data(self, data: dict) -> dict:
        """
        Sanitizes data before storing it in the database.

        Args:
            data (dict): The raw data to sanitize.

        Returns:
            dict: Sanitized data ready for database insertion.

        Sanitization Logic:
            - Converts `quantity` from a string with thousand separators to an integer.
            - Converts `value` from a string with thousand separators to an integer.
            - Replaces `"-"` with None for `quantity` and `value`.

        Example:
            Input:
                {"quantity": "1.234", "value": "567.890"}
            Output:
                {"quantity": 1234, "value": 567890}
        """

        sanitized_data = data.copy()

        # Sanitize the `quantity` field
        if "quantity" in sanitized_data and isinstance(sanitized_data["quantity"], str):
            sanitized_data["quantity"] = int(sanitized_data["quantity"].replace(".", "")) if sanitized_data["quantity"] != "-" else None
        # Sanitize the `value` field
        if "value" in sanitized_data and isinstance(sanitized_data["value"], str):
            sanitized_data["value"] = int(sanitized_data["value"].replace(".", "")) if sanitized_data["value"] != "-" else None

        return sanitized_data
