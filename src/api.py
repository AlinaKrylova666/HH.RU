from abc import ABC, abstractmethod
import requests
from typing import List, Dict


class VacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict]:
        """Метод для получения вакансий по поисковому запросу"""
        pass


class HeadHunterAPI(VacancyAPI):
    def __init__(self):
        self._base_url = "https://api.hh.ru/vacancies"

    def _connect(self) -> None:
        """Приватный метод для проверки подключения к API"""
        response = requests.get(self._base_url)
        if response.status_code != 200:
            raise ConnectionError("Не удалось подключиться к API hh.ru")

    def get_vacancies(self, search_query: str) -> List[Dict]:
        """Получение вакансий с hh.ru по поисковому запросу"""
        self._connect()
        params = {
            'text': search_query,
            'area': 113,  # 113 - Россия
            'per_page': 10
        }
        response = requests.get(self._base_url, params=params)
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            return []

