from typing import Optional

import f


class Vacancy:
    __slots__ = ('title', 'url', 'salary', 'description')

    def __init__(self, title: str, url: str, salary: Optional[str], description: str):
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'salary': self.salary,
            'description': self.description
        }

    def __lt__(self, other: 'Vacancy') -> bool:
        return self.salary < other.salary

    def __eq__(self, other: 'Vacancy') -> bool:
        return self.salary == other.salary

    def _validate_salary(self, salary: str | int) -> int:
        if isinstance(salary, str):
            return salary.isdigit()
        elif isinstance(salary, int):
            return salary
        return 0

    def _get_salary_value(self) -> int:
        try:
            return int(self.salary.replace(' ', ''))
        except ValueError:
            return 0

    @staticmethod
    def cast_to_object_list(vacancies_json: list) -> list:
        list_vacancies = []
        for item in vacancies_json:
            name = f.ichain(item, 'name') or 'Нет названия'
            alternate_url = f.ichain(item, 'alternate_url') or 'Нет url'
            salary = f.ichain(item, 'salary', 'from') or 0
            requirement = f.ichain(item,'snippet', 'requirement') or 'Нет описания'
            list_vacancies.append(Vacancy(name, alternate_url, salary, requirement))
        return list_vacancies