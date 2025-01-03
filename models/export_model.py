from sqlalchemy import Column, Integer, String, Numeric, BigInteger

from .base import Base


class Export(Base):
    __tablename__ = "export"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    quantity = Column(BigInteger, nullable=True)
    value = Column(Numeric(10, 2), nullable=True)
