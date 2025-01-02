import logging

from services.scraper import Scraper, ScraperPages, ScraperParsers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def perform_scrape(year, page):
    try:
        page_to_scrape = ScraperPages[page.upper()]
    except KeyError:
        raise ValueError(f"Invalid page: {page_to_scrape}. Must be one of {list(ScraperPages)}.")

    scraped_data = scrape_data(year, page_to_scrape)
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