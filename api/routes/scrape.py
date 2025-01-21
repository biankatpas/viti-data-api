"""
This module handles scraping data from external sources and preparing it for storage or processing.

Functions:
    perform_scrape(year: int, page: str) -> dict:
        Perform a scrape for a specific year and page, translating column names and organizing data by suboptions.

    scrape_data(year: int, page: ScraperPages) -> dict:
        Perform the actual scraping for a given year and page, including handling suboptions if applicable.

    translate_columns(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        Translate column names in a DataFrame based on a dictionary mapping.

    process_and_store_data(scraped_data: pd.DataFrame, db: Session, model: Base, year: int, suboption: str = None) -> str:
        Process and store the scraped data into the database, optionally handling suboptions.
"""

import logging
import pandas as pd

from enum import Enum

from services.scraper import Scraper, ScraperPages, ScraperParsers
from services.storage import db_handler, ColumnKeyMapping, SuboptionKeyMapping

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def perform_scrape(year, page):
    """
    Perform a scrape for a specific year and page, translating column names.

    Args:
        year (int): The year for which data should be scraped.
        page (str): The page to scrape, corresponding to one of the ScraperPages.

    Returns:
        dict: A dictionary where keys are suboptions (or "default") and values are translated DataFrames.

    Raises:
        ValueError: If the specified page is not valid.
    """

    try:
        scraped_data = scrape_data(year, page)

        translated_data = {
            suboption: translate_columns(data, ColumnKeyMapping)
            for suboption, data in scraped_data.items() if not data.empty
        }

        return translated_data

    except KeyError:
        raise ValueError(f"Invalid page: {page}. Must be one of {list(ScraperPages)}.")

def scrape_data(year, page):
    """
    Perform the actual scraping for a given year and page.

    This function handles suboptions when available and organizes the scraped data
    into a dictionary, with suboptions as keys and the respective DataFrames as values.

    Args:
        year (int): The year for which data should be scraped.
        page (ScraperPages): The page to scrape, represented as a ScraperPages enum value.

    Returns:
        dict: A dictionary with suboptions as keys and DataFrames as values. If no suboptions exist,
        the key "default" will hold the DataFrame.

    Logs:
        - An error message if scraping fails.
    """

    results = {}
    suboptions = page.value["suboptions"]

    try:
        if suboptions:
            for suboption in suboptions:
                scraper = Scraper(year, page, suboption=suboption)
                data = scraper.scrape()
                results[suboption] = data
        else:
            scraper = Scraper(year, page)
            results["default"] = scraper.scrape()

    except Exception as e:
        logger.error(f"Error scraping data for {page}: {e}")

    return results

def translate_columns(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """
    Translate column names of a DataFrame using a dictionary mapping.

    Args:
        df (pd.DataFrame): The DataFrame to translate.
        mapping (dict): A dictionary mapping original column names to new column names.

    Returns:
        pd.DataFrame: A DataFrame with translated column names.

    Example:
        Input DataFrame:
            Produto  Quantidade
            A        100
            B        200

        Mapping:
            {"Produto": "product", "Quantidade": "quantity"}

        Translated DataFrame:
            product   quantity
            A         100
            B         200

    Raises:
        KeyError: If any column in the mapping does not exist in the DataFrame.
    """


    try:
        df.columns = df.columns.str.strip().str.lower()

        normalized_mapping = {key.strip().lower(): value for key, value in mapping.items()}

        filtered_mapping = {key: value for key, value in normalized_mapping.items() if key in df.columns}

        return df.rename(columns=filtered_mapping)

    except Exception:
        return None

def process_and_store_data(scraped_data, db, model, year, suboption=None):
    """
    Process and store data from the scraped DataFrame into the database.

    This function iterates through the rows of the scraped DataFrame, processes each row,
    and stores it in the database. If a suboption is provided, the classification field is
    added to the row data using SuboptionKeyMapping.

    Args:
        scraped_data (pd.DataFrame): The DataFrame containing scraped data.
        db (Session): Database session.
        model (Base): SQLAlchemy model class to store the data.
        year (int): Year of the data being processed.
        suboption (str, optional): Suboption name, if applicable. Defaults to None.

    Returns:
        str: Status message indicating success or no data found.

    Example:
        For a given suboption, the function adds a "classification" field to each row based
        on SuboptionKeyMapping and then stores the row in the database.
    """

    if scraped_data.empty:
        return "No data found."

    try:
        for _, row in scraped_data.iterrows():
            row_data = {
                **row.to_dict(),
                "year": year,
            }
            if suboption:
                classification = SuboptionKeyMapping.get(model.__name__, {}).get(suboption, "")
                row_data["classification"] = classification
            db_handler.store(
                db=db,
                model=model,
                **row_data
            )
    except Exception as e:
        logger.error(f"Error storing data: {e}")

    return "Data stored successfully."
