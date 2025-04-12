import unittest
from src.vacancy import Vacancy
from src.utils import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies

class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.vacancies = [
            Vacancy("Python Developer", "https://hh.ru/vacancy/1", "100000", "Python, Django"),
            Vacancy("Java Developer", "https://hh.ru/vacancy/2", "150000", "Java, Spring"),
            Vacancy("Frontend Developer", "https://hh.ru/vacancy/3", "120000", "JavaScript, React")
        ]

    def test_filter_vacancies(self):
        result = filter_vacancies(self.vacancies, ["Python"])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Python Developer")

    def test_get_vacancies_by_salary(self):
        result = get_vacancies_by_salary(self.vacancies, "100000-130000")
        self.assertEqual(len(result), 2)

    def test_sort_vacancies(self):
        result = sort_vacancies(self.vacancies)
        self.assertEqual(result[0].title, "Java Developer")

    def test_get_top_vacancies(self):
        result = get_top_vacancies(self.vacancies, 2)
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()