from enum import Enum


class ScraperPages(Enum):
    """
    Represents the available pages for scraping data from the website.

    Each member of this enumeration corresponds to a specific page on the website,
    with an associated `option` identifier and, if applicable, a list of `suboptions`.

    Members:
        PRODUCTION (dict): Corresponds to the "opt_02" page for production data.
            - option: "opt_02"
            - suboptions: None (no suboptions available for this page).

        PROCESSING (dict): Corresponds to the "opt_03" page for processing data.
            - option: "opt_03"
            - suboptions: ["subopt_01", "subopt_02", "subopt_03", "subopt_04"]

        COMMERCIALIZATION (dict): Corresponds to the "opt_04" page for commercialization data.
            - option: "opt_04"
            - suboptions: None (no suboptions available for this page).

        IMPORT (dict): Corresponds to the "opt_05" page for import data.
            - option: "opt_05"
            - suboptions: ["subopt_01", "subopt_02", "subopt_03", "subopt_04", "subopt_05"]

        EXPORT (dict): Corresponds to the "opt_06" page for export data.
            - option: "opt_06"
            - suboptions: ["subopt_01", "subopt_02", "subopt_03", "subopt_04"]

    Attributes:
        option (str): The option identifier for the page (used in the URL).
        suboptions (list or None): A list of suboptions available for the page, or None if no suboptions exist.

    Example:
        Accessing the option and suboptions for a page:
            ScraperPages.PRODUCTION.value["option"]  # Returns "opt_02"
            ScraperPages.PROCESSING.value["suboptions"]  # Returns ["subopt_01", "subopt_02", "subopt_03", "subopt_04"]
    """

    PRODUCTION = {"option": "opt_02", "suboptions": None}
    PROCESSING = {"option": "opt_03", "suboptions": ["subopt_01", "subopt_02", "subopt_03", "subopt_04"]}
    COMMERCIALIZATION = {"option": "opt_04", "suboptions": None}
    IMPORT = {"option": "opt_05", "suboptions": ["subopt_01", "subopt_02", "subopt_03", "subopt_04", "subopt_05"]}
    EXPORT = {"option": "opt_06", "suboptions": ["subopt_01", "subopt_02", "subopt_03", "subopt_04"]}
