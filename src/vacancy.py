class Vacancy:
    def __init__(self, title, url, salary, description):
        self.title = title or "Название не указано"
        self.url = url or "Ссылка отсутствует"
        self.salary = self._validate_salary(salary)
        self.description = description or "Описание не указано"

    def _validate_salary(self, salary):
        if isinstance(salary, (int, float)):
            return salary
        try:
            return int(salary)
        except:
            return 0

    def __str__(self):
        return f"{self.title} | {self.salary} ₽ | {self.url}"

    def __lt__(self, other):
        return self.salary < other.salary

    @classmethod
    def from_hh_dict(cls, data: dict):
        return cls(
            title=data.get("name"),
            url=data.get("alternate_url"),
            salary=(data.get("salary") or {}).get("from"),
            description=(data.get("snippet") or {}).get("requirement", "Нет описания"),
        )
