from sqlalchemy.orm import Session

from services.storage import db_handler
from models import Import, Export, Production, Commercialization, Processing


def get_imports(db: Session, years: list = None):
    return db_handler.retrieve(db, Import, years)


def get_exports(db: Session, years: list = None):
    return db_handler.retrieve(db, Export, years)


def get_production(db: Session, years: list = None):
    return db_handler.retrieve(db, Production, years)


def get_commercialization(db: Session, years: list = None):
    return db_handler.retrieve(db, Commercialization, years)


def get_processing(db: Session, years: list = None):
    return db_handler.retrieve(db, Processing, years)

def get_years_as_list(years: str) -> list[int]:
    """
    Convert a comma-separated string of years into a list of integers.

    Args:
        years (str): Comma-separated years (e.g., "2020,2021").

    Returns:
        list[int]: List of integers representing the years.
    """
    try:
        return [int(year) for year in years.split(",")] if years else None
    except ValueError:
        raise ValueError("Invalid format for years. Expected comma-separated integers.")
