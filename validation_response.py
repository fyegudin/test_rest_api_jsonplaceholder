from http_status import HTTPStatus


def validate_response(response_status_code: object, expected_data: HTTPStatus) -> None:
    """
    Validates a response object against expected data using a list of assertions.

    Args:
        response_status_code (int): The response code to validate.
        expected_data (HTTPStatus): An enum containing expected values.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    if getattr(expected_data, "value") != response_status_code:
        error_message = f"Expected {expected_data.name} ({expected_data.value}), got {response_status_code}"
        raise AssertionError(error_message)