# Birthday Reminder

Утилита для Windows, которая показывает системное уведомление, если сегодня у кого-то из списка день рождения. По клику на уведомление открывается ссылка на соцсеть — можно сразу поздравить.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-336791)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)

## Особенности

- Хранение данных в PostgreSQL через SQLAlchemy
- Загрузка списка людей из текстового файла
- Системные уведомления Windows (win11toast) с кликабельной ссылкой
- Возраст вычисляется автоматически из даты рождения
- Настройки подключения к БД через `.env` файл

## Стек

- **Python 3.10+**
- **SQLAlchemy** — ORM для работы с PostgreSQL
- **psycopg2** — драйвер PostgreSQL
- **win11toast** — Windows-уведомления
- **python-dotenv** — загрузка переменных окружения

## Структура проекта

```
birthday-reminder/
├── main.py            # Точка входа
├── db.py              # Работа с базой данных (CRUD)
├── models.py          # SQLAlchemy-модель Person
├── config.py          # Конфигурация (загрузка .env)
├── input.txt          # Пример данных (имя, дата, ссылка)
├── requirements.txt   # Зависимости
├── .env.example       # Шаблон переменных окружения
└── README.md
```

## Установка и запуск

1. Клонировать репозиторий:

```bash
git clone https://github.com/makel0ve/birthday-reminder.git
cd birthday-reminder
```

2. Установить зависимости:

```bash
pip install -r requirements.txt
```

3. Создать файл `.env` на основе шаблона и указать свои данные:

```bash
cp .env.example .env
```

4. Заполнить `input.txt` данными в формате:

```
Имя ДД.ММ.ГГГГ ссылка_на_соцсеть
```

5. Запустить:

```bash
python main.py
```

## Формат данных

Каждая строка в `input.txt` содержит три поля через пробел:

```
Иван 15.03.1995 https://t.me/example_ivan
Мария 06.04.2000 https://vk.com/example_maria
```

При запуске программа проверяет, есть ли в базе люди с сегодняшним днём рождения, и показывает уведомление для каждого из них.