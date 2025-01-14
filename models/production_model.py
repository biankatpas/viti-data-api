from sqlalchemy import Column, Integer, String, BigInteger, UniqueConstraint

from .base import Base


class Production(Base):
    """
    Represents the production data table.

    Attributes:
        id (int): Primary key for the table.
        year (int): The year associated with the production data.
        product (str): The name of the product being produced.
        quantity (int, optional): The quantity of the product produced.

    Constraints:
        - UniqueConstraint: Ensures that the combination of 'year' and 'product' is unique.
    """
    
    __tablename__ = "production"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(BigInteger, nullable=True)

    __table_args__ = (
        UniqueConstraint("year", "product", name="uq_production_year_product"),
    )
