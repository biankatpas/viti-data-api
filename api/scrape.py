import logging

import services.scraper.parsers

from services.scraper.enums import ScraperOption
from services.scraper import Scraper
from services.scraper.parser_factory import ParserFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def perform_scrape(year):
    scraped_data = scrape_all_data(year)
    return scraped_data

def scrape_all_data(year):
    scraped_data = {}

    for option in ScraperOption:
        parser = ParserFactory.get_parser(option)
        if parser is None:
            logger.warning(f"No parser registered for {option.name}. Skipping...")
            continue

        scraper = Scraper(year=year, option=option)
        try:
            data = scraper.scrape()
        except Exception as e:
            logger.error(f"Error scraping data for {option.name}: {e}")
            data = None

        if data is None:
            logger.warning(f"No data found for {option.name}.")

        scraped_data[option.name] = data

    logger.info(scraped_data)
    return scraped_data
