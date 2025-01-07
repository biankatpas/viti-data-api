import logging
import pandas as pd

from enum import Enum

from services.scraper import Scraper, ScraperPages, ScraperParsers
from services.storage import ColumnKeyMapping

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def perform_scrape(year, page):
    try:
        page_to_scrape = ScraperPages[page.upper()]
    except KeyError:
        raise ValueError(f"Invalid page: {page_to_scrape}. Must be one of {list(ScraperPages)}.")

    scraped_data = scrape_data(year, page_to_scrape)
    scraped_data = translate_columns(scraped_data, ColumnKeyMapping)

    return scraped_data

def scrape_data(year, page):
    """
    Scrape data for the given year and page (ScraperPages).
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
        mapping (dict): Dictionary mapping original column names to new names.

    Returns:
        pd.DataFrame: DataFrame with translated column names.
    """

    filtered_mapping = {key: value for key, value in mapping.items() if key in df.columns}
    return df.rename(columns=filtered_mapping)