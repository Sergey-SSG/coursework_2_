from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.storage import JSONVacancyStorage


def main():
    api = HeadHunterAPI()
    storage = JSONVacancyStorage()

    while True:
        print("\nВыберите действие:")
        print("1. Найти вакансии")
        print("2. Показать топ N по зарплате")
        print("3. Поиск по ключевому слову в описании")
        print("4. Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            keyword = input("Введите поисковый запрос: ")
            items = api.get_vacancies(keyword, per_page=10)
            for item in items:
                vac = Vacancy.from_hh_dict(item)
                storage.add_vacancy(vac)
                print(f"Добавлена: {vac}")

        elif choice == "2":
            n = int(input("Сколько вакансий показать? "))
            data = storage.get_vacancies()
            objects = [Vacancy(**d) for d in data]
            for v in sorted(objects, reverse=True)[:n]:
                print(v)

        elif choice == "3":
            keyword = input("Ключевое слово: ")
            data = storage.get_vacancies(keyword=keyword)
            for v in data:
                print(Vacancy(**v))

        elif choice == "4":
            print("До свидания!")
            break

        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()