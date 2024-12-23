import pandas as pd

from bs4 import BeautifulSoup


def parse_commercialization(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")
    df = pd.read_html(str(table))[0]

    return df
