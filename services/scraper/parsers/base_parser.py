import pandas as pd

from bs4 import BeautifulSoup


class BaseParser:
    def __init__(self, class_name="tb_base tb_dados"):
        self.class_name = class_name

    def parse(self, html):
        """Common parsing logic."""
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find("table", class_=self.class_name)
        if not table:
            raise ValueError(f"Table with class '{self.class_name}' not found.")
        df = pd.read_html(str(table))[0]
        return df
