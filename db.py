from datetime import datetime, date

from sqlalchemy import create_engine, extract, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, ProgrammingError

from models import Person, Base
from config import DATABASE_URL, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_database(db_name: str = "birthday_reminder_db") -> None:
    """Создаёт базу данных, если она ещё не существует."""

    maintenance_url = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
    )
    engine = create_engine(maintenance_url, isolation_level="AUTOCOMMIT")

    try:
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE {db_name}"))

    except ProgrammingError:
        pass

    finally:
        engine.dispose()


def connect_db() -> Session:
    """Создаёт подключение к БД и возвращает сессию."""

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    return Session(autoflush=False, bind=engine)


def load_from_file(session: Session, filepath: str) -> None:
    """
    Загружает данные о людях из текстового файла.

    Формат строки: Имя ДД.ММ.ГГГГ ссылка_на_соцсеть
    """

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()

            if len(parts) < 3:
                continue

            add_person(session, name=parts[0], birthday_str=parts[1], social_media=parts[2])


def add_person(session: Session, name: str, birthday_str: str, social_media: str) -> None:
    """Добавляет человека в БД. Пропускает дубликаты."""

    try:
        birthday_date = datetime.strptime(birthday_str, "%d.%m.%Y").date()

    except ValueError:
        print(f"Некорректная дата: {birthday_str}")

        return

    person = Person(name=name, birthday=birthday_date, social_media=social_media)

    try:
        session.add(person)
        session.commit()

    except IntegrityError:
        session.rollback()


def get_todays_birthdays(session: Session) -> list[Person]:
    """Возвращает список людей, у которых сегодня день рождения."""

    today = date.today()
    
    return (
        session.query(Person)
        .filter(
            extract("month", Person.birthday) == today.month,
            extract("day", Person.birthday) == today.day,
        )
        .all()
    )