from abc import ABC, abstractmethod

import psycopg2

from src.vacancy import Vacancy


class ConnectDatabaseError(Exception):
    pass


class BaseDBManager(ABC):
    """Абстрактный метод для всех классов подключений к БД"""

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> list[tuple]: ...

    @abstractmethod
    def get_all_vacancies(self) -> list[tuple]: ...

    @abstractmethod
    def get_avg_salary(self) -> int: ...

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> list[tuple]: ...

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]: ...

    @abstractmethod
    def create_database(self) -> None: ...

    @abstractmethod
    def create_table(self) -> None: ...


class DBManager(BaseDBManager):
    def __init__(self, user, password, database, host, port=5432):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        self.conn = None

    def connect(self) -> None:
        """Соединение с БД"""
        try:
            self.conn = psycopg2.connect(
                user=self.user, password=self.password, database=self.database, host=self.host, port=self.port
            )
        except Exception as err:
            raise ConnectDatabaseError(f"Ошибка подключения к БД -> {err}")

    def create_database(self) -> None:
        """Создание базы данных"""
        temp_database = psycopg2.connect(
            dbname="template1", user=self.user, password=self.password, host=self.host, port=self.port
        )
        temp_database.set_session(autocommit=True)
        cursor = temp_database.cursor()
        cursor.execute(f"""
        SELECT 
            COUNT(*)
            WHERE NOT EXISTS 
            (
            SELECT FROM 
            pg_database 
            WHERE 
            datname = '{self.database}'
                   );
               """
                       )
        chk_database = cursor.fetchone()
        if chk_database:
            if chk_database[0] == 1:
                cursor.execute(f"CREATE DATABASE {self.database};")
        cursor.close()

    def create_table(self) -> None:
        """Создание таблиц"""
        cursor = self.conn.cursor()
        cursor.execute(
            f"""
               CREATE TABLE if not exists company
               (
               id int PRIMARY KEY,
               name text
               )
               """
        )

        cursor.execute(
            f"""
                       CREATE TABLE if not exists vacancy
                       (
                       id int PRIMARY KEY,
                       id_company int references company(id),
                       name text,
                       address text,
                       salary int,
                       description text
                       )
                       """
        )
        self.conn.commit()
        cursor.close()

    def insert(self, data: list[Vacancy]) -> None:
        """Метод вставки"""
        cursor = self.conn.cursor()
        for vacancy in data:
            cursor.execute(
                f"""
                    INSERT INTO company
                        (id, name) 
                    VALUES
                        (%s, %s)
                    ON CONFLICT (id)
                    DO NOTHING
                    """, (vacancy.company_id, vacancy.company_name)
            )
            cursor.execute(
                f"""
                    INSERT INTO vacancy
                        (id, id_company, name, address, salary, description) 
                   VALUES
                        (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id)
                        DO NOTHING
                   """, (vacancy.vacancy_id, vacancy.company_id, vacancy.title,
                         vacancy.url, vacancy.salary, vacancy.description)
            )
            self.conn.commit()

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """получает список всех компаний и количество вакансий у каждой компании."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT company.name, COUNT(*)
            FROM company
            JOIN vacancy on company.id = vacancy.id_company
            GROUP BY company.name
            """
        )
        result = cur.fetchall()
        cur.close()
        return result

    def get_all_vacancies(self) -> list[tuple]:
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT company.name,
                   vacancy.name,
                   salary,
                   address
            FROM company
            JOIN
                 vacancy on company.id = vacancy.id_company
            """
        )
        result = cur.fetchall()
        cur.close()
        return result

    def get_avg_salary(self) -> int:
        """получает среднюю зарплату по вакансиям"""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT (AVG(vacancy.salary)) / 2 as average_salary
            FROM vacancy
            WHERE salary > 0
            """
        )
        result = cur.fetchone()
        cur.close()
        return int(result[0])

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM vacancy
            WHERE salary > (SELECT (AVG(vacancy.salary)) / 2 as average_salary
                               FROM vacancy
                               WHERE salary > 0)
            """
        )
        result = cur.fetchall()
        cur.close()
        return result

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        cur = self.conn.cursor()
        cur.execute(
            f"""
                SELECT *
                FROM vacancy
                WHERE name iLIKE '%{keyword}%'
            """
        )

        result = cur.fetchall()
        cur.close()
        return result
