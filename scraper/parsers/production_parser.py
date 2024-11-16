import pandas as pd

from bs4 import BeautifulSoup

from scraper.parser_factory import ParserFactory
from scraper.enums import ScraperOption


def parse_production(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")
    df = pd.read_html(str(table))[0]

    return df

ParserFactory.register_parser(ScraperOption.PRODUCTION, parse_production)
