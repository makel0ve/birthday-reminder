from win11toast import toast

import db


def main():
    db.create_database()
    session = db.connect_db()

    db.load_from_file(session, "input.txt")

    birthdays = db.get_todays_birthdays(session)

    for person in birthdays:
        toast(
            f"Сегодня день рождения у {person.name} ({person.age} лет)",
            "Нажми и поздравь с днем рождения!",
            on_click=person.social_media,
        )


if __name__ == "__main__":
    main()