import time
import logging
import requests

from requests.exceptions import RequestException

from config import BASE_URL

from .scraper_enums import ScraperPages
from .scraper_parsers import ScraperParsers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self, year, page: ScraperPages):
        self.year = year
        self.page = page
        self.url = f"{BASE_URL}?ano={year}&opcao={page.value}"

    def fetch_data(self, retries=3, backoff_factor=2):
        """
        Fetch the page data with retry logic.

        Args:
            retries (int): Number of retry attempts.
            backoff_factor (int): Backoff multiplier for retry delays.

        Returns:
            str: HTML content of the page if successful, None otherwise.
        """
        for attempt in range(retries):
            try:
                logger.info(f"Fetching data from {self.url} (Attempt {attempt + 1})")
                response = requests.get(self.url, timeout=10)
                response.raise_for_status()  # Raise HTTPError for bad responses
                return response.text
            except RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))
                else:
                    logger.error(f"All retry attempts failed for {self.url}")
                    raise e

    def parse_data(self, html):
        parser = ScraperParsers.get_parser(self.page)

        if parser:
            return parser.parse(html)
        else:
            logger.error(f"Parser for {self.page} not implemented")
            return None

    def scrape(self):
        """
        Perform scraping by fetching and parsing data.
        """
        html = self.fetch_data()
        if html:
            return self.parse_data(html)
        return None
