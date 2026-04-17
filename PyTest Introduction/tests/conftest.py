import pytest
import csv
import os

# Fixture to read the CSV file
@pytest.fixture(scope="session")
def read_csv_content(request):
    dir = os.path.dirname(__file__)
    csv_path = os.path.abspath(os.path.join(dir, "../../PyTest Introduction/src/data/data.csv"))
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Fixture to validate the schema of the file
@pytest.fixture(scope="session")
def expected_schema():
    return ['id', 'name', 'age', 'email', 'is_active']

@pytest.fixture(scope="session")
def validate_schema(read_csv_content):
    if read_csv_content:
        return list(read_csv_content[0].keys())
    return []

# Pytest hook to mark unmarked tests with a custom mark
def pytest_collection_modifyitems(session, config, items):
    for item in items:
        if not item.own_markers:
            item.add_marker(pytest.mark.unmarked)
