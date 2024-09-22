from data.generated_data import PostAttributes, generate_post_data


def generate_mock_data(filename, n=1):
    generated_data = generate_post_data()
    with open(filename, 'w', newline='') as csvfile:

        for _ in range(n):
            # Generate data
            user_id = generated_data[PostAttributes.USER_ID.value]
            title = generated_data[PostAttributes.TITLE.value]
            body = generated_data[PostAttributes.BODY.value]
            entry_id = generated_data[PostAttributes.ENTRY_ID.value]

            # Write each key-value pair
            csvfile.write(f'"userId",{user_id}\n')
            csvfile.write(f'"title","{title}"\n')
            csvfile.write(f'"body","{body}"\n')
            csvfile.write(f'"id",{entry_id}\n')
