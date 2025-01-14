from sqlalchemy import Column, Integer, String, BigInteger, UniqueConstraint

from .base import Base


class Commercialization(Base):
    """
    Represents the commercialization data table.

    Attributes:
        id (int): Primary key for the table.
        year (int): The year associated with the commercialization data.
        product (str): The product name.
        quantity (int, optional): The quantity of the product sold.

    Constraints:
        - UniqueConstraint: Ensures that the combination of 'year' and 'product' is unique.
    """

    __tablename__ = "commercialization"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(BigInteger, nullable=True)

    __table_args__ = (
        UniqueConstraint("year", "product", name="uq_commercialization_year_product"),
    )
