from datetime import date

from sqlalchemy import Integer, String, Date, Column, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    social_media = Column(String)

    __table_args__ = (
        UniqueConstraint("name", "birthday", "social_media", name="uq_person"),
    )

    @property
    def age(self) -> int:
        """Вычисляет текущий возраст на основе даты рождения."""

        today = date.today()
        
        return today.year - self.birthday.year - (
            (today.month, today.day) < (self.birthday.month, self.birthday.day)
        )

    def __repr__(self) -> str:
        return f"<Person(name='{self.name}', birthday='{self.birthday}')>"