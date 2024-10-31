from http.client import HTTPResponse

import requests
import allure
import random
from allure import step
from user_data import user_data
from dbs_connector.db_connector import init_db, insert_post, fetch_post, delete_database
from config import BASE_URL
from logger import CustomLogger
from validation_response import validate_response  # Import the validation function
from http_status import HTTPStatus  # Import the http status

# Initialize the logger
logger = CustomLogger(log_to_file=False)


@step("Get a random user")
def get_random_user():
    logger.info("Fetching a random user ID from user data.")
    random_user_id = random.choice(list(user_data.keys()))
    logger.info(f"Random user ID selected: {random_user_id}")
    return random_user_id


@step("Retrieve the user email from user_id ")
def get_user_email(user_id):
    logger.info(f"Retrieving email for user ID: {user_id}")
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        response.raise_for_status()
        user_response = response.json()
        user_email = user_response["email"]
        logger.info(f"Email retrieved for user ID {user_id}: {user_email}")
        return user_email
    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving user email for ID {user_id}: {e}")
        allure.step(f"Error retrieving user email: {e}")
        raise allure.severity_level.CRITICAL


@step("Get the user posts")
def get_user_posts(user_id):
    logger.info(f"Fetching posts for user ID: {user_id}")
    res = {}
    list_res = []
    try:
        response = requests.get(f"{BASE_URL}/posts")
        response.raise_for_status()
        posts = response.json()
        for data in posts:
            if user_id == data["userId"]:
                list_res.append(data["id"])
        res[user_id] = list_res
        logger.info(f"Posts fetched for user ID {user_id}: {list_res}")
        return res
    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving posts for user ID {user_id}: {e}")
        allure.step(f"Error retrieving posts: {e}")
        raise allure.severity_level.CRITICAL


@step("Validate the user posts IDs")
def validate_user_posts_ids(posts):
    logger.info(f"Validating user posts IDs: {posts}")
    for res in posts.values():
        for post_id in res:
            assert isinstance(post_id,
                              int) and 1 <= post_id <= 100, f"Post ID {post_id} is out of range or not an integer."


@step("Create a post")
def create_post(user_id, title, body):
    logger.info(f"Creating post for user ID: {user_id} with title: '{title}' and body: '{body}'")
    data = {"userId": user_id, "title": title, "body": body}
    try:
        response = requests.post(f"{BASE_URL}/posts", json=data)
        logger.info(f"Post creation response: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating post for user ID {user_id}: {e}")
        allure.step(f"Error creating post: {e}")
        raise allure.severity_level.CRITICAL


@step("Validate the csv creation")
def validate_csv_data(csv_data):
    logger.info(f"Validating CSV data: {csv_data}")
    assert 1 <= csv_data["userId"] <= 10 and isinstance(csv_data["userId"], int), \
        "userId must be between 1 and 10 and an integer."
    assert csv_data["id"] == 101 and isinstance(csv_data["id"], int), "id must be 101 and an integer."
    assert len(csv_data["title"]) >= 2 and isinstance(csv_data["title"], str), \
        "title must be a string with at least 2 characters."
    assert len(csv_data["body"]) >= 20 and isinstance(csv_data["body"], str), \
        "body must be a string with at least 20 characters."


@step("Validate the post response")
def validate_post_response(response, user_id, post_id, title, body):
    logger.info(f"Validating post response for user ID {user_id} with post ID {post_id}.")
    # Initialize a list to hold assertion errors
    assertion_errors = []
    validate_response(response_status_code=response.status_code, expected_data=HTTPStatus.CREATED)
    # assert response.status_code == 201, f"Unexpected response code: {response.status_code}"
    created_post = response.json()
    logger.info(f"Post created: {created_post}.")
    # Collect assertions
    if created_post["userId"] != user_id:
        assertion_errors.append(f"Expected userId {user_id}, but got {created_post['userId']}.")
    if created_post["id"] != post_id:
        assertion_errors.append(f"Expected post ID {post_id}, but got {created_post['id']}.")
    if created_post["title"] != title:
        assertion_errors.append(f"Expected title '{title}', but got '{created_post['title']}'.")
    if created_post["body"] != body:
        assertion_errors.append(f"Expected body '{body}', but got '{created_post['body']}'.")

    # Raise an exception if there are any assertion errors
    if assertion_errors:
        raise AssertionError("Validation failed with the following errors:\n" + "\n".join(assertion_errors))


@step("Initialize the database")
def init_db_sqlite():
    logger.info("Initializing the database.")
    init_db()


@step("Delete the after test database.")
def delete_db():
    if delete_database():
        logger.info("Deleting the database.")
    else:
        logger.info("No need to delete the database.")


@step("Fetch post from the database")
def fetch_post_data(post_id):
    logger.info(f"Fetching post from the database with post ID: {post_id}.")
    data = fetch_post(post_id)
    logger.info(f"Post data fetched: {data}.")
    return data


@step("Fetch and test data post from the database")
def validate_post_data_from_db(user_id, title, body, post_id):
    logger.info(f"Validating post data from DB for post ID: {post_id}.")
    # Initialize a list to hold assertion errors
    assertion_errors = []
    post = fetch_post(post_id)
    if post is None:
        assertion_errors.append("Post not found in the database.")
    else:
        logger.info(f"Post data retrieved: {post}.")
    # Collect assertions
    if post[0] != user_id:
        assertion_errors.append(f"Expected userId {user_id}, but got {post[0]}.")
    if post[1] != title:
        assertion_errors.append(f"Expected title '{title}', but got '{post[1]}'.")
    if post[2] != body:
        assertion_errors.append(f"Expected body '{body}', but got '{post[2]}'.")
    if post[3] != post_id:
        assertion_errors.append(f"Expected post ID {post_id}, but got {post[3]}.")

    # Raise an exception if there are any assertion errors
    if assertion_errors:
        raise AssertionError("Validation failed with the following errors:\n" + "\n".join(assertion_errors))


@step("Insert data to the database")
def insert_post_to_db(user_id, title, body, post_id):
    logger.info(f"Inserting post to the database: {user_id}, {title}, {body}, {post_id}.")
    insert_post(user_id, title, body, post_id)


@step("Convert data from the database to Dictionary")
def convert_post_data(post_data):
    logger.info(f"Converting post data from DB to dictionary: {post_data}.")
    data_to_post = {
        "userId": post_data[0],
        "title": post_data[1],
        "body": post_data[2],
        "id": post_data[3]
    }
    logger.info(f"Converted data: {data_to_post}.")
    return data_to_post


@step("Validate that the received message matches the sent message")
def validate_received_message(received_message, expected_message):
    logger.info("Validating received message.")
    assert received_message == expected_message, "The received message does not match the sent message."
