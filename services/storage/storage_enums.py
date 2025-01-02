from enum import Enum
from models import (
    Production,
    Processing,
    Commercialization,
    Import,
    Export,
)


class PageModelMapping(Enum):
    PRODUCTION = Production
    PROCESSING = Processing
    COMMERCIALIZATION = Commercialization
    IMPORT = Import
    EXPORT = Export

ColumnKeyMapping = {
    "Produto": "product",
    "Quantidade (L.)": "quantity",
    "Valor": "value",
    "País": "country",
}
