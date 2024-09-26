import pytest
import allure_steps
from csv_files.csv_mock_data import generate_mock_data
from csv_files.read_csv_file import read_csv_data_and_convert


@pytest.fixture(scope="module")
def user_id():
    user_id = allure_steps.get_random_user()
    assert isinstance(user_id, int) and 1 <= user_id <= 10
    return user_id  # Return a random user for use in tests


@pytest.fixture()
def generate_csv_data(csv_file):
    # Fixture to generate CSV data
    generate_mock_data(csv_file)
    return csv_file  # Return the generated csv_file for use in tests


@pytest.fixture
def csv_file(request):
    # This fixture could provide a default CSV file name
    return request.param if request.param else "default.csv"


@pytest.fixture()
def load_csv_data(csv_file):
    # Fixture to load CSV data
    data = read_csv_data_and_convert(csv_file)
    return data


@pytest.fixture
def queue_name(request):
    # This fixture could provide a default queue name
    return request.param if hasattr(request, 'param') else "my_message"

