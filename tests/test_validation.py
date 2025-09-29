from datetime import date
from utils.validation import validate_form


def test_empty_form():
    result = validate_form("", None, "", {})
    assert result == "Please fill out the form before submitting."


def test_invalid_age():
    result = validate_form("abc", date.today(), "Male", {"q1": "Yes"})
    assert result == "Please enter a valid numeric age."


def test_missing_date():
    result = validate_form("25", None, "Male", {"q1": "Yes"})
    assert result == "Please select a date of visit."


def test_missing_gender():
    result = validate_form("25", date.today(), "", {"q1": "Yes"})
    assert result == "Please select a gender."


def test_incomplete_responses():
    result = validate_form("25", date.today(), "Male", {"q1": ""})
    assert result == "Please answer all survey questions."


def test_valid_form():
    result = validate_form("25", date.today(), "Male", {"q1": "Yes"})
    assert result is None
