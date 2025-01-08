from sqlalchemy import Column, Integer, String, BigInteger, UniqueConstraint

from .base import Base


class Import(Base):
    __tablename__ = "import"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    quantity = Column(BigInteger, nullable=True)
    value = Column(BigInteger, nullable=True)

    __table_args__ = (
        UniqueConstraint("year", "country", name="uq_import_year_country"),
    )