import unittest
from unittest.mock import patch
from src.api import HeadHunterAPI

class TestHeadHunterAPI(unittest.TestCase):
    @patch('src.api.requests.get')
    def test_get_vacancies(self, mock_get):
        # Мок ответа от API
        mock_response = {
            'items': [
                {
                    'name': 'Python Developer',
                    'alternate_url': 'https://hh.ru/vacancy/123',
                    'salary': {'from': 100000, 'to': 150000},
                    'snippet': {'requirement': 'Python, Django'}
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies('Python')

        # Проверяем, что метод возвращает правильный формат данных
        self.assertIsInstance(vacancies, list)
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]['name'], 'Python Developer')

    @patch('src.api.requests.get')
    def test_api_connection_error(self, mock_get):
        # Мок ошибки подключения
        mock_get.return_value.status_code = 404

        api = HeadHunterAPI()

        with self.assertRaises(ConnectionError):
            api._connect()

if __name__ == '__main__':
    unittest.main()
