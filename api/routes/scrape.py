"""
This module handles scraping data from external sources and preparing it for storage or processing.

Functions:
    perform_scrape(year: int, page: str) -> pd.DataFrame:
        Perform a scrape for a specific year and page, then translate the column names.

    scrape_data(year: int, page: ScraperPages) -> pd.DataFrame:
        Perform the actual scraping for a given year and page.

    translate_columns(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        Translate column names in a DataFrame based on a dictionary mapping.
"""

import logging
import pandas as pd

from enum import Enum

from services.scraper import Scraper, ScraperPages, ScraperParsers
from services.storage import ColumnKeyMapping

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def perform_scrape(year, page):
    """
    Perform a scrape for a specific year and page, then translate the column names.

    Args:
        year (int): The year for which data should be scraped.
        page (str): The page to scrape, corresponding to one of the ScraperPages.

    Returns:
        pd.DataFrame: A DataFrame containing the scraped and translated data.

    Raises:
        ValueError: If the specified page is not valid.
    """

    try:
        page_to_scrape = ScraperPages[page.upper()]
    except KeyError:
        raise ValueError(f"Invalid page: {page_to_scrape}. Must be one of {list(ScraperPages)}.")

    scraped_data = scrape_data(year, page_to_scrape)
    scraped_data = translate_columns(scraped_data, ColumnKeyMapping)

    return scraped_data

def scrape_data(year, page):
    """
    Perform the actual scraping for a given year and page.

    Args:
        year (int): The year for which data should be scraped.
        page (Enum): The page to scrape, represented as a ScraperPages enum value.

    Returns:
        pd.DataFrame: A DataFrame containing the scraped data.

    Logs:
        An error message if scraping fails.

    Returns:
        pd.DataFrame: The scraped data or None if an error occurs.
    """

    scraper = Scraper(year=year, page=page)

    try:
        data = scraper.scrape()
    except Exception as e:
        logger.error(f"Error scraping data for {page}: {e}")
        data = None

    return data

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
    """

    filtered_mapping = {key: value for key, value in mapping.items() if key in df.columns}
    return df.rename(columns=filtered_mapping)