from .scraper_enums import ScraperPages
from .parsers import (
    ProductionParser, ProcessingParser, CommercializationParser, ImportParser, ExportParser,
)


class ScraperParsers:
    """
    A registry and factory class for retrieving parser instances based on scraper pages.

    Attributes:
        _parsers (dict): A mapping between ScraperPages and their corresponding parser classes.

    Methods:
        get_parser(parser_name: ScraperPages) -> BaseParser:
            Retrieves an instance of the parser corresponding to the provided scraper page.

    Usage:
        # Example usage
        parser = ScraperParsers.get_parser(ScraperPages.PRODUCTION)
        data = parser.parse(html_content)
    """

    _parsers = {
        ScraperPages.PRODUCTION: ProductionParser,
        ScraperPages.PROCESSING: ProcessingParser,
        ScraperPages.COMMERCIALIZATION: CommercializationParser,
        ScraperPages.IMPORT: ImportParser,
        ScraperPages.EXPORT: ExportParser,
    }

    @staticmethod
    def get_parser(parser_name):
        """
        Retrieves an instance of the parser corresponding to the provided scraper page.

        Args:
            parser_name (ScraperPages): The scraper page for which a parser is requested.

        Returns:
            BaseParser: An instance of the parser class corresponding to the scraper page.

        Raises:
            ValueError: If no parser is found for the given scraper page.

        Example:
            parser = ScraperParsers.get_parser(ScraperPages.PRODUCTION)
            data = parser.parse(html_content)
        """
        
        parser_class = ScraperParsers._parsers.get(parser_name)
        if not parser_class:
            raise ValueError(f"No parser found for {parser_name}")
        return parser_class()
