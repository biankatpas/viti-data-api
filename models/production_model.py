from sqlalchemy import Column, Integer, String

from .base import Base


class Production(Base):
    __tablename__ = "production"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=True)
