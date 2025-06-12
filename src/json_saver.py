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
    def __init__(self, filename: str = 'vacancies.json'):
        self._filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.get_vacancies()
        if vacancy.to_dict() not in vacancies:
            vacancies.append(vacancy.to_dict())
            self._save_vacancies(vacancies)

    def delete_vacancy(self, vacancy: Dict) -> None:
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v['url'] != vacancy['url']]
        self._save_vacancies(vacancies)

    def get_vacancies(self) -> List[Dict]:
        if os.path.exists(self._filename):
            try:
                with open(self._filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                return []
        return []

    def _save_vacancies(self, vacancies: List[Dict]) -> None:
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=4)