import pytest
import re
import csv

def test_file_not_empty(read_csv_content):
    content = read_csv_content
    assert content, "CSV file is empty!"

@pytest.mark.xfail(reason="Duplicate row validation is expected to fail")
def test_duplicates(read_csv_content):
    seen = set()
    for row in read_csv_content:
        row_tuple = tuple(row.items())
        assert row_tuple not in seen, f"Duplicate row found: {row}"
        seen.add(row_tuple)

def test_validate_schema(validate_schema, expected_schema):
    assert validate_schema==expected_schema, f"Schema mismatch! Expected: {expected_schema}, Found: {list(actual_schema)}"

@pytest.mark.skip(reason="Age validation is skipped as per requirements")
def test_age_column_valid(read_csv_content):
    for row in read_csv_content:
        age = int(row['age'])
        assert 0 <= age <= 100, f"Invalid age {age} for id {row['id']}"

def test_email_column_valid(read_csv_content):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    for row in read_csv_content:
        email = row['email']
        assert re.match(email_regex, email), f"Invalid email '{email}' for id {row['id']}"

@pytest.mark.parametrize("id,expected_active", [(1, False), (2, True)])
def test_active_players(read_csv_content, id, expected_active):
    for row in read_csv_content:
        if int(row['id']) == id:
            actual = row['is_active'].lower() == 'true'
            assert actual == expected_active, \
                f"is_active for id={id} expected {expected_active}, found {actual}"

def test_active_player(read_csv_content):
    for row in read_csv_content:
        if int(row['id']) == 2:
            actual = row['is_active'].lower() == 'true'
            assert actual is True, "is_active for id=2 should be True"
