from abc import ABC, abstractmethod
import requests
from typing import List, Dict

from requests import Response


class VacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self) -> list[dict]:
        """Метод для получения вакансий по поисковому запросу"""
        pass


class HeadHunterAPI(VacancyAPI):

    LIST_ID = [
        11669695,
        2066667,
        1911403,
        4685961,
        197566,
        2300703,
        1189354,
        45124,
        9498120,
        2393,
        4437201,
    ]

    def __init__(self) -> None:
        """Метод для инициализации экземпляра класса"""
        self.__params: dict = {"text": "", "page": 0, "per_page": 100, "employer_id": 0, "area": 113}
        self.__vacancies: list = []

    def get_vacancies(self) -> list[dict]:
        """Метод для получения вакансий по поисковому запросу"""

        for i in self.LIST_ID:
            self.__params["employer_id"] = i

            response: Response = requests.get("https://api.hh.ru/vacancies",
                                    headers={"User-Agent": "HH-User-Agent"},
                                    params=self.__params)
            if response.status_code == 200:
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)

        return self.__vacancies