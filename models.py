from sqlalchemy import Integer, String, Date, Column, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "Люди"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    birthday = Column(Date)
    age = Column(Integer)
    social_media = Column(String)
    
    __table_args__ = (UniqueConstraint("name", "birthday", "social_media", name="uniq_idx_1"), )