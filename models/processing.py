from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Processing(Base):
    __tablename__ = "processing"

    id = Column(Integer, primary_key=True, autoincrement=True)
    variety = Column(String, nullable=False)
    quantity = Column(Integer, nullable=True)
