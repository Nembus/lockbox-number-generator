# tests/test_generator.py
import pytest
from pathlib import Path
import json
from main import (
    generate_unique_number,
    is_valid_number,
    load_generated_numbers,
    save_generated_numbers,
    get_last_number,
    STORAGE_FILE,
)

@pytest.fixture
def temp_storage(tmp_path, monkeypatch):
    test_file = tmp_path / "generated_numbers.json"
    monkeypatch.setattr('main.STORAGE_FILE', test_file)
    return test_file

def test_generate_unique_number():
    number = generate_unique_number()
    assert 1000 <= number <= 9999
    assert len(set(str(number))) == 4

def test_is_valid_number():
    assert is_valid_number(1234)
    assert not is_valid_number(1233)
    assert not is_valid_number(123)
    assert not is_valid_number(12345)
    assert not is_valid_number('12345')
    assert not is_valid_number('abc123')

def test_save_and_load_numbers(temp_storage):
    numbers = {1234, 5678}
    save_generated_numbers(numbers)
    loaded = load_generated_numbers()
    assert loaded == numbers

def test_get_last_number(temp_storage):
    numbers = {1234, 5678}
    save_generated_numbers(numbers)
    assert get_last_number() == 5678

def test_get_last_number_empty(temp_storage):
    if temp_storage.exists():
        temp_storage.unlink()
    assert get_last_number() is None