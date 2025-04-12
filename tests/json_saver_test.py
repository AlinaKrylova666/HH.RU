import unittest
import os
import json
from src.json_saver import JSONSaver

class TestJSONSaver(unittest.TestCase):
    def setUp(self):
        self.filename = 'test_vacancies.json'
        self.saver = JSONSaver(self.filename)
        self.vacancy = {
            'name': 'Python Developer',
            'url': 'https://hh.ru/vacancy/123',
            'salary': '100000-150000',
            'description': 'Python, Django'
        }

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_add_vacancy(self):
        self.saver.add_vacancy(self.vacancy)
        vacancies = self.saver.get_vacancies()
        self.assertIn(self.vacancy, vacancies)

    def test_delete_vacancy(self):
        self.saver.add_vacancy(self.vacancy)
        self.saver.delete_vacancy(self.vacancy)
        vacancies = self.saver.get_vacancies()
        self.assertNotIn(self.vacancy, vacancies)

    def test_get_vacancies_empty(self):
        vacancies = self.saver.get_vacancies()
        self.assertEqual(vacancies, [])

if __name__ == '__main__':
    unittest.main()