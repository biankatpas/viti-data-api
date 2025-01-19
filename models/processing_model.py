from sqlalchemy import Column, Integer, String, BigInteger, UniqueConstraint

from .base import Base


class Processing(Base):
    """
    Represents the processing data table in the database.

    Attributes:
        id (int): The primary key for the table. Auto-incremented.
        year (int): The year associated with the processing data.
        variety (str): The variety of the processed product (e.g., type of grape or derivative).
        quantity (BigInteger, optional): The quantity of the processed product.
        classification (str): The classification of the processed product (e.g., type or category).

    Constraints:
        UniqueConstraint: Ensures that each combination of 'year', 'variety', and 'classification'
                          is unique within the table.

    Table:
        - Name: "processing"
    """

    __tablename__ = "processing"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    variety = Column(String, nullable=False)
    quantity = Column(BigInteger, nullable=True)
    classification = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("year", "variety", "classification", name="uq_processing_year_variety_classification"),
    )