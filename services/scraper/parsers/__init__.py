from scraper.enums import ScraperOption
from scraper.parser_factory import ParserFactory

from .production_parser import parse_production
from .processing_parser import parse_processing
from .commercialization_parser import parse_commercialization
from .import_parser import parse_import
from .export_parser import parse_export


ParserFactory.register_parser(ScraperOption.PRODUCTION, parse_production)
ParserFactory.register_parser(ScraperOption.PROCESSING, parse_processing)
ParserFactory.register_parser(ScraperOption.COMMERCIALIZATION, parse_commercialization)
ParserFactory.register_parser(ScraperOption.IMPORT, parse_import)
ParserFactory.register_parser(ScraperOption.EXPORT, parse_export)
