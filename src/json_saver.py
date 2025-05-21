import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict

from src.vacancy import Vacancy


class FileSaver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Dict) -> None:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Dict) -> None:
        pass

    @abstractmethod
    def get_vacancies(self) -> List[Dict]:
        pass

class JSONSaver(FileSaver):
    def __init__(self):
        """Initialize an empty list to store vacancies."""
        self.vacancies = []

    def add_vacancy(self, vacancy: dict) -> None:
        """
        Add a vacancy to the list if it is not already present.

        :param vacancy: A dictionary with vacancy details.
        """
        if vacancy not in self.vacancies:
            self.vacancies.append(vacancy)

    def delete_vacancy(self, vacancy: Dict) -> None:
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v['url'] != vacancy['url']]
        self._save_vacancies(vacancies)

    def get_vacancies(self):
        if not os.path.exists(self._filename):
            return []
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print("Ошибка: Некорректный или пустой JSON-файл. Возвращаем пустой список.")
            return []

    def _save_vacancies(self, vacancies: List[Dict]) -> None:
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=4)


        """Class to save and manage job vacancies in JSON format."""
