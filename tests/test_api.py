from src.vacancy import Vacancy


def test_salary_validation():
    v = Vacancy("Test", "url", None, "desc")
    assert v.salary == 0

    v2 = Vacancy("Test", "url", "notanumber", "desc")
    assert v2.salary == 0

    v3 = Vacancy("Test", "url", 100000, "desc")
    assert v3.salary == 100000


def test_comparison():
    v1 = Vacancy("A", "url", 1000, "desc")
    v2 = Vacancy("B", "url", 2000, "desc")
    assert v2 > v1
    assert v1 < v2
