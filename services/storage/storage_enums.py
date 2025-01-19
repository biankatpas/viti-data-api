from enum import Enum
from models import (
    Production,
    Processing,
    Commercialization,
    Import,
    Export,
)


class PageModelMapping(Enum):
    """
    Maps scraper pages to their corresponding SQLAlchemy models.

    Members:
        PRODUCTION (Production): Maps to the Production model.
        PROCESSING (Processing): Maps to the Processing model.
        COMMERCIALIZATION (Commercialization): Maps to the Commercialization model.
        IMPORT (Import): Maps to the Import model.
        EXPORT (Export): Maps to the Export model.
    """

    PRODUCTION = Production
    PROCESSING = Processing
    COMMERCIALIZATION = Commercialization
    IMPORT = Import
    EXPORT = Export

ColumnKeyMapping = {
    """
    Maps column names from scraped HTML tables to database field names.

    Key (str): The column name as it appears in the scraped HTML.
    Value (str): The corresponding field name in the database model.

    Example:
        "Produto": "product" - Maps the column "Produto" to the database field "product".

    Supported Keys:
        - "Produto": Maps to "product".
        - "Quantidade (L.)": Maps to "quantity".
        - "Quantidade (Kg)": Maps to "quantity".
        - "Valor": Maps to "value".
        - "Valor (US$)": Maps to "value".
        - "País": Maps to "country".
        - "Países": Maps to "country".
        - "Cultivar": Maps to "variety".
    """

    "Produto": "product",
    "Quantidade (L.)": "quantity",
    "Quantidade (Kg)": "quantity",
    "Valor": "value",
    "Valor (US$)": "value",
    "País": "country",
    "Países": "country",
    "Cultivar": "variety",
}

SuboptionKeyMapping = {
    """
    Maps suboption identifiers to their corresponding classifications.

    This dictionary is used to associate suboptions (e.g., "subopt_01") with human-readable
    classifications for specific pages (e.g., "Import", "Export", "Processing").

    Structure:
        - Keys: Names of models (e.g., "Import", "Export", "Processing").
        - Values: Nested dictionaries where:
            - Keys: Suboption identifiers (e.g., "subopt_01").
            - Values: Human-readable classifications (e.g., "Vinhos de mesa").

    Usage:
        Retrieve the classification for a specific suboption:
            classification = SuboptionKeyMapping["Import"]["subopt_01"]
            print(classification)  # Output: "Vinhos de mesa"

    """

    "Import": {
        "subopt_01": "Vinhos de mesa",
        "subopt_02": "Espumantes",
        "subopt_03": "Uvas frescas",
        "subopt_04": "Uvas passas",
        "subopt_05": "Suco de uva",
    },
    "Export": {
        "subopt_01": "Vinhos de mesa",
        "subopt_02": "Espumantes",
        "subopt_03": "Uvas frescas",
        "subopt_04": "Suco de uva",
    },
    "Processing": {
        "subopt_01": "Viniferas",
        "subopt_02": "Americanas e hibridas",
        "subopt_03": "Uvas de mesa",
        "subopt_04": "Sem classificacao",
    }
}
