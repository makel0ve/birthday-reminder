from win11toast import toast

import db


def main():
    db.create_database()
    session = db.connect_db()
    f = open("input.txt", "r", encoding="utf-8")
    for line in f:
        db.create(session, line.strip().split())
        
    # print("Введите социальную сеть человека, запись которого хотите обновить.")
    # db.update(session, input().strip().replace('"', ''))
    
    # print("Введите социальную сеть человека, запись которого хотите удалить.")
    # db.delete(session, input().strip().replace('"', ''))
        
    people = db.read(session)
    if people != []:
        for p in people:
            toast(f'Сегодня день рождения у {p.name}', 'Нажми и поздравь с днем рождения!', on_click=f"{p.social_media}")
    

if __name__ == "__main__":
    main()