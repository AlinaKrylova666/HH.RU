import os

from src.api import HeadHunterAPI
from src.db_manage import DBManage
from src.utils import filter_vacancies, sort_vacancies, get_vacancies_by_salary, get_top_vacancies, print_vacancies
from src.vacancy import Vacancy
from src.json_saver import JSONSaver
from dotenv import load_dotenv

load_dotenv()

json_saver = JSONSaver()
hh_api = HeadHunterAPI()
manage_database = DBManage(
    os.getenv("DB_USER_NAME"),
    os.getenv("DB_USER_PSW"),
    os.getenv("DB_DATABASE"),
    os.getenv("DB_HOST")
)


def user_interaction():
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат (например, 100000-150000): ")

    hh_vacancies = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)

if __name__ == "__main__":
    user_interaction()
