from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Commercialization(Base):
    __tablename__ = "commercialization"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=True)
