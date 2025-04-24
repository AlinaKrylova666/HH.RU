def filter_vacancies(vacancies, keywords):
    """Фильтрует вакансии по ключевым словам в описании."""
    return [vacancy for vacancy in vacancies if any(keyword.lower() in vacancy.description.lower() for keyword in keywords)]

def get_vacancies_by_salary(vacancies, salary_range):
    try:
        min_salary, max_salary = map(int, salary_range.split('-'))
    except ValueError:
        print("Ошибка: Диапазон зарплат должен быть в формате 'min-max'.")
        return []  # Возвращаем пустой список, если формат некорректен

    return [
        vacancy for vacancy in vacancies
        if vacancy._get_salary_value() >= min_salary and vacancy._get_salary_value() <= max_salary
    ]

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