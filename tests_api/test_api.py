import pytest
import allure
import allure_steps
from allure import feature, title
from user_data import data_to_post
from data.generated_data import PostAttributes, generate_post_data


@feature("Testing JSONPlaceholder API")
class TestAPI:
    # Generate data with Faker
    generated_data = generate_post_data()

    @pytest.mark.retry(3)  # Retry failed test 3 times
    @title("Retrieve Random User and view his/her email")
    def test_user_email(self, user_id):
        user_email = allure_steps.get_user_email(user_id)
        allure.attach(f"{user_email}", name="user email", attachment_type=allure.attachment_type.TEXT)

    @pytest.mark.retry(3)  # Retry failed test 3 times
    @title("View the user and Posts")
    def test_user_posts(self, user_id):
        posts = allure_steps.get_user_posts(user_id)
        allure_steps.validate_user_posts_ids(posts)

    @pytest.mark.retry(3)  # Retry failed test 3 times
    @title("New Post validation")
    def test_new_post(self, user_id):
        response = allure_steps.create_post(user_id, data_to_post["title"],
                                            data_to_post["body"])
        allure_steps.validate_post_response(response, user_id, data_to_post["id"],
                                            data_to_post["title"], data_to_post["body"])

    @pytest.mark.retry(3)  # Retry failed test 3 times
    @title("New Post validation from mock csv data")
    @pytest.mark.parametrize("csv_file", ["mock_data.csv"], indirect=True)
    def test_new_post_from_csv(self, csv_file, generate_csv_data, load_csv_data):
        load_csv_data = load_csv_data[0]
        allure_steps.validate_csv_data(load_csv_data)
        response = allure_steps.create_post(load_csv_data["userId"], load_csv_data["title"],
                                            load_csv_data["body"])
        allure_steps.validate_post_response(response, load_csv_data["userId"], load_csv_data["id"],
                                            load_csv_data["title"], load_csv_data["body"])

    @pytest.mark.retry(3)
    @title("Fetch and post data from the database")
    @pytest.mark.parametrize("user_id, title, body, post_id", [(10, "Test Title", "Test Body", 101),
                                                               (generated_data[PostAttributes.USER_ID.value],
                                                                generated_data[PostAttributes.TITLE.value],
                                                                generated_data[PostAttributes.BODY.value],
                                                                generated_data[PostAttributes.ENTRY_ID.value])
                                                               ])
    def test_fetch_data_from_db_and_post(self, user_id, title, body, post_id):
        allure_steps.delete_database()
        allure_steps.init_db()
        allure_steps.insert_post_to_db(user_id, title, body, post_id)
        post_data = allure_steps.fetch_post(post_id)
        data_post = allure_steps.convert_post_data(post_data)
        allure_steps.validate_post_data_from_db(data_post["userId"], data_post["title"],
                                                data_post["body"], data_post["id"])
        response = allure_steps.create_post(data_post["userId"], data_post["title"],
                                            data_post["body"])
        allure_steps.validate_post_response(response, data_post["userId"], data_post["id"],
                                            data_post["title"], data_post["body"])