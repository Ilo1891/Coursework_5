import psycopg2

from src.hh_company_vacancy_parser import HHVacancionParsing
from config import config


class DBModule:

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = psycopg2.connect(dbname=self.db_name, **config())

    def create_tables(self) -> None:
        """
        Метод создает две таблицы в базе данных 'hh_vacancies', Одна таблица называется 'employer', вторая 'vacancies'
        в 'employer' создаются две колонки: employer_id, employer_name. В 'vacancies' создаются шесть колонок:
        vacancy_id, company_id, vacancy_name, salary_from, salary_to и url.
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute('CREATE TABLE employer('
                               'employer_id int PRIMARY KEY,'
                               'employer_name varchar(150));'

                               'CREATE TABLE vacancies('
                               'vacancy_id int PRIMARY KEY,'
                               'company_id int REFERENCES employer(employer_id),'
                               'vacancy_name varchar(250) NOT NULL,'
                               'salary_from int,'
                               'salary_to int,'
                               'url varchar(250));')

    def full_tables(self, value) -> None:
        """
        Записываем компании и вакансии из сайта HH
        """
        head_hunter = HHVacancionParsing(value)
        employers = head_hunter.get_employers_sort()
        vacancies = head_hunter.filter_vacancyes()

        with self.conn:
            with self.conn.cursor() as cur:
                for employer in employers:
                    cur.execute("""
                                    INSERT INTO employer VALUES (%s, %s)
                                """, (employer["id"], employer["name"]))
                for vacancy in vacancies:
                    cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                                (vacancy["id"], vacancy["employer"], vacancy["name"], vacancy["salary_from"],
                                 vacancy["salary_to"], vacancy["url"],))


if __name__ == '__main__':
    hh = DBModule('python')