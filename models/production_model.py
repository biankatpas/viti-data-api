from sqlalchemy import Column, Integer, String

from .base import Base


class Production(Base):
    __tablename__ = "production"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=True)
