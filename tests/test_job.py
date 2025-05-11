import json
from unittest.mock import mock_open, patch

import pytest

from src.job import Vacancy, VacancyManager


@pytest.fixture
def sample_vacancies():
    return [
        {
            "id": "1",
            "name": "Python Developer",
            "url": "http://example.com/vacancy1",
            "salary": {"from": 1000, "to": 1500},
            "company": "Company A",
            "area": "Area A",
        },
        {
            "id": "2",
            "name": "Java Developer",
            "url": "http://example.com/vacancy2",
            "salary": {"from": 1200, "to": 1600},
            "company": "Company B",
            "area": "Area B",
        },
    ]


def test_load_vacancies(sample_vacancies):
    with mock_open(read_data=json.dumps(sample_vacancies)) as m:
        manager = VacancyManager("../data/vacancies.json")
        manager.load_vacancies()

        assert len(manager.vacancies) == 2
        assert manager.vacancies[0].name == "Python Developer"
        assert manager.vacancies[1].name == "Java Developer"


def test_save_vacancies(sample_vacancies):
    manager = VacancyManager("../data/vacancies.json")
    manager.vacancies = [Vacancy(**vacancy) for vacancy in sample_vacancies]

    with patch("builtins.open", mock_open()) as m:
        manager.save_vacancies()
        m.assert_called_once_with("../data/vacancies.json", "w", encoding="utf-8")
        handle = m()
        handle.write.assert_called_once_with(json.dumps(sample_vacancies, ensure_ascii=False, indent=4))


def test_filter_vacancies(sample_vacancies):
    manager = VacancyManager()
    manager.vacancies = [Vacancy(**vacancy) for vacancy in sample_vacancies]

    filtered = manager.filter_vacancies("Python")
    assert len(filtered) == 1
    assert filtered[0].name == "Python Developer"

    filtered = manager.filter_vacancies("Developer")
    assert len(filtered) == 2


def test_delete_vacancy(sample_vacancies):
    manager = VacancyManager()
    manager.vacancies = [Vacancy(**vacancy) for vacancy in sample_vacancies]

    manager.delete_vacancy("1")
    assert len(manager.vacancies) == 1
    assert manager.vacancies[0].name == "Java Developer"


if __name__ == "__main__":
    pytest.main()
