from sqlalchemy import Column, Integer, String, BigInteger, UniqueConstraint

from .base import Base


class Import(Base):
    """
    Represents the import data table.

    Attributes:
        id (int): Primary key for the table.
        year (int): The year associated with the import data.
        country (str): The origin country for the imported goods.
        quantity (int, optional): The quantity of goods imported.
        value (int, optional): The monetary value of the imported goods.

    Constraints:
        - UniqueConstraint: Ensures that the combination of 'year' and 'country' is unique.
    """

    __tablename__ = "import"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    quantity = Column(BigInteger, nullable=True)
    value = Column(BigInteger, nullable=True)

    __table_args__ = (
        UniqueConstraint("year", "country", name="uq_import_year_country"),
    )