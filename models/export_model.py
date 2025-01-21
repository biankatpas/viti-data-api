from sqlalchemy import Column, Integer, String, BigInteger

from .base import Base


class Export(Base):
    """
    Represents the export data table in the database.

    Attributes:
        id (int): The primary key for the table. Auto-incremented.
        year (int): The year associated with the export data.
        country (str): The destination country for the exported goods.
        quantity (BigInteger, optional): The quantity of goods exported.
        value (BigInteger, optional): The monetary value of the exported goods.
        classification (str): The classification of the exported goods (e.g., type of product).

    Constraints:
        UniqueConstraint: Ensures that each combination of 'year', 'country', and 'classification'
                          is unique within the table.

    Table:
        - Name: "export"
    """

    __tablename__ = "export"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    quantity = Column(BigInteger, nullable=True)
    value = Column(BigInteger, nullable=True)
    classification = Column(String, nullable=False)
