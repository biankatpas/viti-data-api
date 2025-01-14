import pandas as pd

from bs4 import BeautifulSoup


class BaseParser:
    """
    A base class for parsing HTML tables using BeautifulSoup and pandas.

    Attributes:
        class_name (str): The CSS class name of the table to parse. Defaults to "tb_base tb_dados".

    Methods:
        parse(html: str) -> pd.DataFrame:
            Parses the HTML to extract a table with the specified class name and converts it into a pandas DataFrame.
    """

    def __init__(self, class_name="tb_base tb_dados"):
        """
        Initializes the BaseParser with a specific table class name.

        Args:
            class_name (str): The CSS class name of the table to parse. Defaults to "tb_base tb_dados".
        """

        self.class_name = class_name

    def parse(self, html):
        """
        Parses the HTML to extract a table with the specified class name.

        Args:
            html (str): The HTML content as a string.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the table data.

        Raises:
            ValueError: If no table with the specified class name is found in the HTML.

        Example:
            html_content = '''
            <table class="tb_base tb_dados">
                <tr><th>Column1</th><th>Column2</th></tr>
                <tr><td>Value1</td><td>Value2</td></tr>
            </table>
            '''
            parser = BaseParser()
            df = parser.parse(html_content)
            print(df)
        """

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find("table", class_=self.class_name)

        if not table:
            raise ValueError(f"Table with class '{self.class_name}' not found.")

        df = pd.read_html(str(table))[0]

        return df
