from sqlalchemy import Column, Integer, String, BigInteger, UniqueConstraint

from .base import Base


class Import(Base):
    """
    Represents the import data table in the database.

    Attributes:
        id (int): The primary key for the table. Auto-incremented.
        year (int): The year associated with the import data.
        country (str): The origin country for the imported goods.
        quantity (BigInteger, optional): The quantity of goods imported.
        value (BigInteger, optional): The monetary value of the imported goods.
        classification (str): The classification of the imported goods (e.g., type of product).

    Constraints:
        UniqueConstraint: Ensures that each combination of 'year', 'country', and 'classification'
                          is unique within the table.

    Table:
        - Name: "import"
    """

    __tablename__ = "import"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    quantity = Column(BigInteger, nullable=True)
    value = Column(BigInteger, nullable=True)
    classification = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("year", "country", "classification", name="uq_import_year_country_classification"),
    )