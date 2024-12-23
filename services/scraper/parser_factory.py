from .enums import ScraperOption


class ParserFactory:
    _parsers = {}

    @classmethod
    def register_parser(cls, option: ScraperOption, parser_func):
        cls._parsers[option] = parser_func

    @classmethod
    def get_parser(cls, option: ScraperOption):
        return cls._parsers.get(option, None)
