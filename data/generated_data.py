from enum import Enum
from faker import Faker

# Initialize Faker
faker = Faker()


class PostAttributes(Enum):
    USER_ID = "userId"
    TITLE = "title"
    BODY = "body"
    ENTRY_ID = "id"


def generate_post_data():
    """Generate a post with fake data."""
    user_id = faker.random_int(min=1, max=10)
    title = faker.sentence(nb_words=faker.random_int(min=2, max=10))
    body = faker.text(max_nb_chars=faker.random_int(min=50, max=100))
    entry_id = 101

    return {
        PostAttributes.USER_ID.value: user_id,
        PostAttributes.TITLE.value: title,
        PostAttributes.BODY.value: body,
        PostAttributes.ENTRY_ID.value: entry_id
    }