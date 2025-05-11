import json
from abc import ABC, abstractmethod

import requests


class AbstractVacancy(ABC):
    @abstractmethod
    def display(self):
        pass


class Vacancy(AbstractVacancy):
    def __init__(self, id, name, url, salary, company, area):
        self.id = id
        self.name = name
        self.url = url
        self.salary = salary
        self.company = company
        self.area = area

    def display(self):
        return f"{self.name} - {self.company} - {self.url}"


class VacancyManager:
    def __init__(self, filename="../data/vacancies.json"):
        self.filename = filename
        self.vacancies = self.load_vacancies()

    def load_vacancies(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Vacancy(**vacancy) for vacancy in data]
        except FileNotFoundError:
            return []

    def save_vacancies(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([vacancy.__dict__ for vacancy in self.vacancies], file, ensure_ascii=False, indent=4)

    def fetch_vacancies(self, keyword):
        url = f"https://api.hh.ru/vacancies?text={keyword}&area=113"  # area=113 - это Россия
        response = requests.get(url)
        if response.status_code == 200:
            for item in response.json().get("items", []):
                vacancy = Vacancy(
                    id=item["id"],
                    name=item["name"],
                    url=item["alternate_url"],
                    salary=item["salary"],
                    company=item["employer"]["name"],
                    area=item["area"]["name"],
                )
                self.vacancies.append(vacancy)
            self.save_vacancies()
        else:
            print(f"Ошибка при получении данных: {response.status_code}")

    def filter_vacancies(self, keyword):
        return [vacancy for vacancy in self.vacancies if keyword.lower() in vacancy.name.lower()]

    def delete_vacancy(self, vacancy_id):
        self.vacancies = [vacancy for vacancy in self.vacancies if vacancy.id != vacancy_id]
        self.save_vacancies()

    def display_vacancies(self):
        if not self.vacancies:
            print("Нет доступных вакансий.")
            return
        for vacancy in self.vacancies:
            print(vacancy.display())


class JobVacancyApp:
    def __init__(self):
        self.manager = VacancyManager()

    def run(self):
        while True:
            print("\n1. Получить вакансии")
            print("2. Показать все вакансии")
            print("3. Фильтровать вакансии")
            print("4. Удалить вакансию")
            print("5. Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                keyword = input("Введите ключевое слово для поиска: ")
                self.manager.fetch_vacancies(keyword)
            elif choice == "2":
                self.manager.display_vacancies()
            elif choice == "3":
                keyword = input("Введите ключевое слово для фильтрации: ")
                filtered_vacancies = self.manager.filter_vacancies(keyword)
                if filtered_vacancies:
                    for vacancy in filtered_vacancies:
                        print(vacancy.display())
                else:
                    print("Нет вакансий, соответствующих критериям фильтрации.")
            elif choice == "4":
                vacancy_id = input("Введите ID вакансии для удаления: ")
                self.manager.delete_vacancy(vacancy_id)
            elif choice == "5":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    app = JobVacancyApp()
    app.run()
