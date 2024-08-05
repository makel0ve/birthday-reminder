from datetime import datetime

from sqlalchemy import create_engine, extract
from sqlalchemy.orm import Session
import psycopg2

from models import Person, Base


def create_database():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin", host="127.0.0.1")
    cursor = conn.cursor()
    conn.autocommit = True
    sql = "CREATE DATABASE birthday_reminder_db"
    try:
        cursor.execute(sql)
        cursor.close()
        conn.close()
    except:
        return
 
    
def calculate_age(birthday):
    now = datetime.now().date()
    birthday_date = datetime.strptime(birthday, "%d.%m.%Y")
    age = now.year - birthday_date.year - ((now.month, now.day) < (birthday_date.month, birthday_date.day))
    if birthday_date.month == 2 and birthday_date.day == 29:
        try:
            leap_year_birthday = birthday_date.replace(year=now.year)
        except ValueError:
            leap_year_birthday = birthday_date.replace(year=now.year, day=28)

        if now < leap_year_birthday:
            age -= 1
    return age
    

def create(session, data):
    with session as db:
        age = calculate_age(data[1])
        birthday_date = datetime.strptime(data[1], "%d.%m.%Y").date()

        p = Person(name=data[0], 
                birthday=birthday_date, 
                age=age, 
                social_media=data[2])
        
        try:
            db.add(p)
            db.commit()
        except:
            return
    
    
def read(session):
    with session as db:
        now = datetime.now()
        people = db.query(Person).filter(extract('month', Person.birthday) == now.month, 
                                         extract('day', Person.birthday) == now.day).all()
        
        return people
   
   
def update(session, value):
    with session as db:
        person = db.query(Person).filter(Person.social_media == value).first()
        if person:
            print(f"Введите данные для обновления записи человека\n{person.name} \
                  {person.birthday} \
                  {person.age} \
                  {person.social_media}")
            print("Имя")
            person.name = input()
            print("День рождения в формате ДД.ММ.ГГГГ")
            birthday_date = input()
            person.birthday = birthday_date
            person.age = calculate_age(birthday_date)
            print("Социальная сеть")
            person.social_media = input()

            db.commit()
            
            
def delete(session, value):
    with session as db:
        person = db.query(Person).filter(Person.social_media == value).first()
        if person:
            print(f"Вы уверены, что хотите удалить запись {person.name} {person.birthday} {person.age} {person.social_media} из базы данных (Y/N)?")
            if input() == "Y":
                db.delete(person)
                db.commit()
                print("Запись была удалена")
            else:
                print("Запись не была удалена")
                

def connect_db():
    engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/birthday_reminder_db")
    session = Session(autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    
    return session