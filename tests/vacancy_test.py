import unittest
from src.vacancy import Vacancy

class TestVacancy(unittest.TestCase):
    def setUp(self):
        self.vacancy1 = Vacancy("Python Developer", "https://hh.ru/vacancy/1", "100000", "Python, Django")
        self.vacancy2 = Vacancy("Java Developer", "https://hh.ru/vacancy/2", "150000", "Java, Spring")
        self.vacancy3 = Vacancy("Frontend Developer", "https://hh.ru/vacancy/3", None, "JavaScript, React")

    def test_salary_validation(self):
        self.assertEqual(self.vacancy1.salary, "100000")
        self.assertEqual(self.vacancy3.salary, "Зарплата не указана")


    def test_comparison_operators(self):
        self.assertTrue(self.vacancy1 < self.vacancy2)
        self.assertFalse(self.vacancy1 == self.vacancy2)

    def test_cast_to_object_list(self):
        vacancies_json = [
            {
                'name': 'Python Developer',
                'alternate_url': 'https://hh.ru/vacancy/1',
                'salary': {'from': 100000},
                'snippet': {'requirement': 'Python, Django'}
            }
        ]
        vacancies = Vacancy.cast_to_object_list(vacancies_json)
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].title, "Python Developer")

if __name__ == '__main__':
    unittest.main()