from typing import Optional, List

class Vacancy:
    slots = ('title', 'url', 'salary', 'description')

    def __str__(self) -> str:
        """
        Return a string representation of the vacancy.

        :return: A formatted string with vacancy details.
        """
        salary_info = self.salary if self.salary else "Не указана"
        return f"Вакансия: {self.title}\nURL: {self.url}\nЗарплата: {salary_info}\nОписание: {self.description}"

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
        salary_str = str(salary)  # Приведение к строке
        if salary_str.isdigit():
            return salary_str
        return "Зарплата не указана"

    def _get_salary_value(self) -> int:
        try:
            return int(self.salary.replace(' ', ''))
        except ValueError:
            return 0

    @staticmethod
    def cast_to_object_list(vacancies_json: List[dict]) -> List['Vacancy']:
        return [
            Vacancy(
                item['name'],
                item['alternate_url'],
                str((item.get('salary') or {}).get('from', "Зарплата не указана")),  # Приведение к строке
                item.get('snippet', {}).get('requirement', 'Описание не указано')
            )
            for item in vacancies_json
        ]

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
        }


    def __init__(self, title: str, url: str, salary: Optional[str], description: Optional[str]):
        """
        Initialize a vacancy with title, URL, salary, and description.

        :param title: The title of the vacancy.
        :param url: The URL of the vacancy.
        :param salary: The salary for the vacancy.
        :param description: The description of the vacancy.
        """
        self.title = title
        self.url = url
        self.salary = salary
        self.description = self._validate_description(description)

    def _validate_description(self, description: Optional[str]) -> str:
        """
        Validate the description, returning 'Не указано' if None.

        :param description: The description to validate.
        :return: Validated description.
        """
        return description if description is not None else "Не указано"
