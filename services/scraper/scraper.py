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
    """
    A class for scraping data from web pages with retry and parsing functionality.

    Attributes:
        year (int): The year for which data is being scraped.
        page (ScraperPages): The page enum indicating which data to scrape.
        url (str): The constructed URL for scraping based on the year and page.

    Methods:
        fetch_data(retries=3, backoff_factor=2) -> str:
            Fetches the HTML content from the URL with retry logic.

        parse_data(html: str) -> pd.DataFrame:
            Parses the fetched HTML content using the appropriate parser.

        scrape() -> pd.DataFrame:
            Fetches and parses the data, returning it as a pandas DataFrame.
    """

    def __init__(self, year, page: ScraperPages):
        """
        Initializes the Scraper with the specified year and page.

        Args:
            year (int): The year for which data is being scraped.
            page (ScraperPages): The page enum indicating which data to scrape.
        """

        self.year = year
        self.page = page
        self.url = f"{BASE_URL}?ano={year}&opcao={page.value}"

    def fetch_data(self, retries=3, backoff_factor=2):
        """
        Fetch the page data with retry logic.

        Args:
            retries (int): Number of retry attempts. Defaults to 3.
            backoff_factor (int): Backoff multiplier for retry delays. Defaults to 2.

        Returns:
            str: HTML content of the page if successful.

        Raises:
            RequestException: If all retry attempts fail.

        Logs:
            - Info: On each fetch attempt.
            - Warning: For failed attempts with retry.
            - Error: If all retry attempts fail.
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
        """
        Parses the fetched HTML content using the appropriate parser.

        Args:
            html (str): The HTML content to parse.

        Returns:
            pd.DataFrame: A DataFrame containing the parsed data.

        Raises:
            ValueError: If no parser is implemented for the specified page.

        Logs:
            - Error: If no parser is found for the specified page.
        """

        parser = ScraperParsers.get_parser(self.page)

        if parser:
            return parser.parse(html)
        else:
            logger.error(f"Parser for {self.page} not implemented")
            return None

    def scrape(self):
        """
        Perform scraping by fetching and parsing data.

        Returns:
            pd.DataFrame: A DataFrame containing the scraped and parsed data, or None if scraping fails.

        Logs:
            - Info: Logs the scraping process.
        """
        
        html = self.fetch_data()
        if html:
            return self.parse_data(html)
        return None
