from .scraper_enums import ScraperPages
from .parsers import (
    ProductionParser, ProcessingParser, CommercializationParser, ImportParser, ExportParser,
)


class ScraperParsers:
    _parsers = {
        ScraperPages.PRODUCTION: ProductionParser,
        ScraperPages.PROCESSING: ProcessingParser,
        ScraperPages.COMMERCIALIZATION: CommercializationParser,
        ScraperPages.IMPORT: ImportParser,
        ScraperPages.EXPORT: ExportParser,
    }

    @staticmethod
    def get_parser(parser_name):
        parser_class = ScraperParsers._parsers.get(parser_name)
        if not parser_class:
            raise ValueError(f"No parser found for {parser_name}")
        return parser_class()
