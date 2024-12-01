import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from main import (
    INTERNAL_BLACKLIST,
    add_number,
    generate_number,
    generate_unique_number,
    get_last_number,
    is_available_number,
    is_valid_number,
    load_all_blacklisted_numbers,
    load_generated_numbers,
    save_generated_numbers,
)


@pytest.fixture
def temp_storage(tmp_path, monkeypatch):
    test_file = tmp_path / "generated_numbers.json"
    monkeypatch.setattr("main.STORAGE_FILE", test_file)
    return test_file


def test_generate_unique_number():
    number = generate_unique_number()
    assert 1000 <= number <= 9999
    assert len(set(str(number))) == 4


def test_initial_state(temp_storage):
    if temp_storage.exists():
        temp_storage.unlink()

    assert load_generated_numbers() == set()

    new_number = generate_number()
    assert isinstance(new_number, int)
    assert 1000 <= new_number <= 9999
    assert len(set(str(new_number))) == 4

    saved_numbers = load_generated_numbers()
    assert len(saved_numbers) == 1
    assert new_number in saved_numbers


def test_is_valid_number():
    assert is_valid_number(1234)
    assert not is_valid_number(1233)
    assert not is_valid_number(123)
    assert not is_valid_number(12345)
    assert not is_valid_number("12345")
    assert not is_valid_number("abc123")


def test_save_and_load_numbers(temp_storage):
    test_date = datetime.now().strftime("%Y-%m-%d")
    numbers_data = [
        {"number": 1234, "dateCreated": test_date},
        {"number": 5678, "dateCreated": test_date},
    ]
    save_generated_numbers(numbers_data)
    loaded = load_generated_numbers()
    assert loaded == {1234, 5678}


def test_get_last_number(temp_storage):
    test_date = datetime.now().strftime("%Y-%m-%d")
    numbers_data = [
        {"number": 1234, "dateCreated": test_date},
        {"number": 5678, "dateCreated": test_date},
    ]
    save_generated_numbers(numbers_data)
    assert get_last_number() == 5678


def test_get_last_number_empty(temp_storage):
    if temp_storage.exists():
        temp_storage.unlink()
    assert get_last_number() is None


def test_internal_blacklist():
    blacklisted = load_all_blacklisted_numbers()
    assert 1234 in blacklisted
    assert 4321 in blacklisted

    # Test generated number isn't in blacklist
    number = generate_unique_number()
    assert number not in INTERNAL_BLACKLIST


def test_is_available_number(temp_storage):
    # Valid and available number
    assert is_available_number(9876) == True

    # Number in internal blacklist
    assert is_available_number(1234) == False

    # Invalid number (repeating digits)
    assert is_available_number(1122) == False

    # Add a number to generated_numbers.json
    numbers_data = [
        {"number": 5678, "dateCreated": datetime.now().strftime("%Y-%m-%d")}
    ]
    save_generated_numbers(numbers_data)

    # Number already in generated_numbers.json
    assert is_available_number(5678) == False


def test_add_number(temp_storage):
    # Valid number
    assert add_number(9876) == True
    assert 9876 in load_generated_numbers()

    # Already added number
    assert add_number(9876) == False

    # Blacklisted number
    assert add_number(1234) == False

    # Invalid number
    assert add_number(1122) == False
