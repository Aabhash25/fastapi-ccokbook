TEST_DATABASE_FILE = (
    "test_tasks.csv"  # this is the file pytest will create temporatrily
)

TEST_TASKS_CSV = [  # this represents how csv stores data
    {
        "id": "1",
        "title": "Test Task One",
        "description": "Test Description One",
        "status": "Incomplete",
    },
    {
        "id": "2",
        "title": "Test Task Two",
        "description": "Test Description Two",
        "status": "Ongoing",
    },
]

TEST_TASKS = [
    {**task_json, "id": int(task_json["id"])} for task_json in TEST_TASKS_CSV
]  # converts id fropm string to int
import pytest
import csv, os
from pathlib import Path
from unittest.mock import patch


@pytest.fixture(
    autouse=True
)  # autouse=True runs before every test automatically, no need to call it manually in your test function
def create_test_database():
    database_file_location = str(
        Path(__file__).parent / TEST_DATABASE_FILE
    )  # create the path for temp csv
    with patch(
        "operations.DATABASE_FILENAME",
        database_file_location,
    ) as csv_test:
        with open(database_file_location, mode="w", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=["id", "title", "description", "status"],
            )
            writer.writeheader()
            writer.writerows(TEST_TASKS_CSV)
            print("")
        yield csv_test  # The fixture pauses here and lets pytest run your test functions.
        os.remove(
            database_file_location
        )  # The temporary CSV file is deleted after testing is done.
