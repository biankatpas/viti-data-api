from sqlalchemy import Column, Integer, String, BigInteger, UniqueConstraint

from .base import Base


class Processing(Base):
    """
    Represents the processing data table.

    Attributes:
        id (int): Primary key for the table.
        year (int): The year associated with the processing data.
        variety (str): The variety of the processed product.
        quantity (int, optional): The quantity of the processed product.

    Constraints:
        - UniqueConstraint: Ensures that the combination of 'year' and 'variety' is unique.
    """
    
    __tablename__ = "processing"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    variety = Column(String, nullable=False)
    quantity = Column(BigInteger, nullable=True)

    __table_args__ = (
        UniqueConstraint("year", "variety", name="uq_processing_year_variety"),
    )