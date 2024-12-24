import logging
import requests

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

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"Error accessing the page: {self.url}")
            return None

    def parse_data(self, html):
        parser = ScraperParsers.get_parser(self.page)

        if parser:
            return parser.parse(html)
        else:
            logger.error(f"Parser for {self.page} not implemented")
            return None

    def scrape(self):
        html = self.fetch_data()
        if html:
            return self.parse_data(html)
        return None
