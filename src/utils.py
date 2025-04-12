def filter_vacancies(vacancies, keywords):
    """Фильтрует вакансии по ключевым словам в описании."""
    return [vacancy for vacancy in vacancies if any(keyword.lower() in vacancy.description.lower() for keyword in keywords)]

def get_vacancies_by_salary(vacancies, salary_range):
    """Возвращает вакансии, которые находятся в указанном диапазоне зарплат."""
    min_salary, max_salary = map(int, salary_range.split('-'))
    return [vacancy for vacancy in vacancies if min_salary <= vacancy._get_salary_value() <= max_salary]

def sort_vacancies(vacancies):
    """Сортирует вакансии по зарплате в порядке убывания."""
    return sorted(vacancies, reverse=True)

def get_top_vacancies(vacancies, top_n):
    """Возвращает топ N вакансий."""
    return vacancies[:top_n]

def print_vacancies(vacancies):
    """Выводит информацию о вакансиях."""
    for vacancy in vacancies:
        print(vacancy.__dict__)