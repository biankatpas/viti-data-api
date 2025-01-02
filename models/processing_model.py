from sqlalchemy import Column, Integer, String

from .base import Base


class Processing(Base):
    __tablename__ = "processing"

    id = Column(Integer, primary_key=True, autoincrement=True)
    variety = Column(String, nullable=False)
    quantity = Column(Integer, nullable=True)
