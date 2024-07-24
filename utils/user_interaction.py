import psycopg2
from src.hh_company_vacancy_parser import HHVacancionParsing
from src.DB_module import DBModule
from config import config


def user_interaction(value, db_name) -> None:
    """
    Получаем данные от пользователя, записывает в базу даннных
    и сортирует.
    """
    HHVacancionParsing(value)
    module = DBModule(db_name)
    module.create_tables()
    module.full_tables(value)


def delete_database(database_name: str) -> None:
    """
    Удаление бызы данных
    """
    conn = psycopg2.connect(dbname='postgres', **config())
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE {database_name}')

    cur.close()
    conn.close()


def create_database(database_name: str) -> None:
    """
    Создание базы данных и таблиц для сохранения данных о каналах и видео
    """
    conn = psycopg2.connect(dbname='postgres', **config())
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()


if __name__ == '__main__':
    delete_database('python')