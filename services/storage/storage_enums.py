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

ColumnKeyMapping =
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
{
    "Produto": "product",
    "Quantidade (L.)": "quantity",
    "Quantidade (Kg)": "quantity",
    "Valor": "value",
    "Valor (US$)": "value",
    "País": "country",
    "Países": "country",
    "Cultivar": "variety",
}
