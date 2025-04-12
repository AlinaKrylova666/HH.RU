from typing import Optional

class Vacancy:
    __slots__ = ('title', 'url', 'salary', 'description')

    def __init__(self, title: str, url: str, salary: Optional[str], description: str):
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    def __lt__(self, other: 'Vacancy') -> bool:
        return self._get_salary_value() < other._get_salary_value()

    def __eq__(self, other: 'Vacancy') -> bool:
        return self._get_salary_value() == other._get_salary_value()

    def _validate_salary(self, salary: Optional[str]) -> str:
        if salary and salary.isdigit():
            return salary
        return "Зарплата не указана"

    def _get_salary_value(self) -> int:
        try:
            return int(self.salary.replace(' ', ''))
        except ValueError:
            return 0

    @staticmethod
    def cast_to_object_list(vacancies_json: list) -> list:
        return [
            Vacancy(
                item['name'],
                item['alternate_url'],
                item.get('salary', {}).get('from') or "Зарплата не указана",
                item.get('snippet', {}).get('requirement', 'Описание не указано')
            )
            for item in vacancies_json
        ]