from .base_parser import BaseParser


class ProductionParser(BaseParser):
    """
    A parser for extracting production data from HTML tables.

    Inherits from:
        BaseParser: Provides the common parsing logic for HTML tables.

    Attributes:
        class_name (str): The CSS class name of the table to parse. Inherits the default value "tb_base tb_dados" from BaseParser.

    Methods:
        parse(html: str) -> pd.DataFrame:
            Parses the HTML to extract a table with the specified class name and converts it into a pandas DataFrame.
    """

    def __init__(self):
        """
        Initializes the ProductionParser with the default table class name.

        Inherits:
            BaseParser.__init__: Uses the default class name "tb_base tb_dados".
        """
        super().__init__()
