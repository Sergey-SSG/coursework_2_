from abc import ABC, abstractmethod

import requests


class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword: str, page: int = 0, per_page: int = 20) -> list:
        pass


class HeadHunterAPI(JobAPI):
    BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, keyword: str, page: int = 0, per_page: int = 20) -> list:
        try:
            response = requests.get(self.BASE_URL, params={"text": keyword, "page": page, "per_page": per_page})
            response.raise_for_status()
            return response.json().get("items", [])
        except requests.RequestException as e:
            print(f"Ошибка при запросе к hh.ru: {e}")
            return []
