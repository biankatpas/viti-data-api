import requests

from .config import BASE_URL
from .enums import ScraperOption
from .parser_factory import ParserFactory


class Scraper:
    def __init__(self, year, option: ScraperOption):
        self.year = year
        self.option = option
        self.url = f"{BASE_URL}?ano={year}&opcao={option.value}"

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error accessing the page: {self.url}")
            return None

    def parse_data(self, html):
        parser = ParserFactory.get_parser(self.option)

        if parser:
            return parser(html)
        else:
            print(f"Parser for {self.option} not implemented")
            return None

    def scrape(self):
        html = self.fetch_data()
        if html:
            return self.parse_data(html)
        return None
