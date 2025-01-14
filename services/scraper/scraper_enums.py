from enum import Enum


class ScraperPages(Enum):
    """
    Represents the available pages for scraping data.

    Members:
        PRODUCTION (str): Corresponds to the "opt_02" page for production data.
        PROCESSING (str): Corresponds to the "opt_03" page for processing data.
        COMMERCIALIZATION (str): Corresponds to the "opt_04" page for commercialization data.
        IMPORT (str): Corresponds to the "opt_05" page for import data.
        EXPORT (str): Corresponds to the "opt_06" page for export data.
    """

    PRODUCTION = "opt_02"
    PROCESSING = "opt_03"
    COMMERCIALIZATION = "opt_04"
    IMPORT = "opt_05"
    EXPORT = "opt_06"
