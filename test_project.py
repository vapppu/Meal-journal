from io import StringIO
from project import Food, MEALS, day_string, printable_string, get_day, get_meal
from datetime import datetime, date
import pytest


def test_food():
    food = Food("lettuce", "dinner", 230415)
    assert food.name == "lettuce"
    assert food.meal == "dinner"
    assert food.date == 230415
    assert food.__repr__() == "230415 dinner: lettuce"


def test_day_string():
    date = datetime(2023, 4, 22)
    assert day_string(date) == "Saturday 22 April 2023"

    with pytest.raises(TypeError):
        day_string("220423")


def test_printable_string():
    date_string = "230422"
    assert printable_string(date_string) == "SATURDAY 22 APRIL 2023"

    with pytest.raises(ValueError):
        printable_string("231304")


def test_get_day(monkeypatch):
    test_input = StringIO("0")
    monkeypatch.setattr('sys.stdin', test_input)
    assert get_day() == date.today()


def test_get_day2(monkeypatch):
    test_input = StringIO("220423")
    monkeypatch.setattr('sys.stdin', test_input)
    assert get_day() == datetime(2023, 4, 22)


def test_get_meal(monkeypatch):
    test_input = StringIO("1")
    monkeypatch.setattr('sys.stdin', test_input)
    assert get_meal() == "breakfast"


def test_get_meal2(monkeypatch):
    test_input = StringIO("5")
    monkeypatch.setattr('sys.stdin', test_input)
    with pytest.raises(IndexError):
        get_meal()
