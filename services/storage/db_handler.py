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
            instance = model(**kwargs)
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except Exception as e:
            self.db.rollback()
            raise e
