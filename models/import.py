from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Import(Base):
    __tablename__ = "import"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    quantity = Column(Integer, nullable=True)
    value = Column(Numeric(10, 2), nullable=True)
