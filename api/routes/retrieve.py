"""
This module provides functions for retrieving data from the database
and utility functions for processing query parameters.

Functions:
    get_imports(db: Session, years: list = None) -> list:
        Retrieve import data for the given years or all data if no years are specified.

    get_exports(db: Session, years: list = None) -> list:
        Retrieve export data for the given years or all data if no years are specified.

    get_production(db: Session, years: list = None) -> list:
        Retrieve production data for the given years or all data if no years are specified.

    get_commercialization(db: Session, years: list = None) -> list:
        Retrieve commercialization data for the given years or all data if no years are specified.

    get_processing(db: Session, years: list = None) -> list:
        Retrieve processing data for the given years or all data if no years are specified.

    get_years_as_list(years: str) -> list[int]:
        Convert a comma-separated string of years into a list of integers.
"""

from sqlalchemy.orm import Session

from services.storage import db_handler
from models import Import, Export, Production, Commercialization, Processing


def get_imports(db: Session, years: list = None):
    """
    Retrieve import data for the given years or all data if no years are specified.

    Args:
        db (Session): SQLAlchemy session instance.
        years (list, optional): List of years to filter by. Defaults to None.

    Returns:
        list: List of import data rows.
    """

    return db_handler.retrieve(db, Import, years)


def get_exports(db: Session, years: list = None):
    """
    Retrieve export data for the given years or all data if no years are specified.

    Args:
        db (Session): SQLAlchemy session instance.
        years (list, optional): List of years to filter by. Defaults to None.

    Returns:
        list: List of export data rows.
    """

    return db_handler.retrieve(db, Export, years)


def get_production(db: Session, years: list = None):
    """
    Retrieve production data for the given years or all data if no years are specified.

    Args:
        db (Session): SQLAlchemy session instance.
        years (list, optional): List of years to filter by. Defaults to None.

    Returns:
        list: List of production data rows.
    """

    return db_handler.retrieve(db, Production, years)


def get_commercialization(db: Session, years: list = None):
    """
    Retrieve commercialization data for the given years or all data if no years are specified.

    Args:
        db (Session): SQLAlchemy session instance.
        years (list, optional): List of years to filter by. Defaults to None.

    Returns:
        list: List of commercialization data rows.
    """

    return db_handler.retrieve(db, Commercialization, years)


def get_processing(db: Session, years: list = None):
    """
    Retrieve processing data for the given years or all data if no years are specified.

    Args:
        db (Session): SQLAlchemy session instance.
        years (list, optional): List of years to filter by. Defaults to None.

    Returns:
        list: List of processing data rows.
    """

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
