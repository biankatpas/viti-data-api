from sqlalchemy import Column, Integer, String, BigInteger, UniqueConstraint

from .base import Base


class Export(Base):
    """
    Represents the export data table.

    Attributes:
        id (int): Primary key for the table.
        year (int): The year associated with the export data.
        country (str): The destination country for the exported goods.
        quantity (int, optional): The quantity of goods exported.
        value (int, optional): The monetary value of the exported goods.

    Constraints:
        - UniqueConstraint: Ensures that the combination of 'year' and 'country' is unique.
    """

    __tablename__ = "export"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    quantity = Column(BigInteger, nullable=True)
    value = Column(BigInteger, nullable=True)

    __table_args__ = (
        UniqueConstraint("year", "country", name="uq_export_year_country"),
    )