import json
import os
from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, **criteria) -> list:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy) -> None:
        pass


class JSONVacancyStorage(AbstractStorage):
    def __init__(self, filename="./data/vacancies.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        data = self._load()
        data.append(vacancy.__dict__)
        self._save(data)

    def get_vacancies(self, **criteria):
        data = self._load()
        result = []
        for item in data:
            match = True
            if "min_salary" in criteria and item.get("salary", 0) < criteria["min_salary"]:
                match = False
            if "keyword" in criteria and criteria["keyword"].lower() not in item.get("description", "").lower():
                match = False
            if match:
                result.append(item)
        return result

    def delete_vacancy(self, vacancy):
        data = self._load()
        updated = [v for v in data if v["title"] != vacancy.title or v["url"] != vacancy.url]
        self._save(updated)
