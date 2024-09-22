import csv


def read_csv_data_and_convert(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data_to_post_list = []

        temp_dict = {}

        for row in reader:
            if len(row) < 2:
                continue  # Skip any rows that don't have enough columns

            key = row[0].strip('"')  # Remove quotes from key if they exist
            value = row[1].strip('"')  # Remove quotes from value if they exist

            temp_dict[key] = value

            # When we have collected all keys for a single entry
            if key == "id":
                # Create the output dictionary
                data_to_post = {
                    "userId": int(temp_dict.get("userId", 1)),  # Default to 1 if not found
                    "title": temp_dict.get("title", ""),
                    "body": temp_dict.get("body", ""),
                    "id": int(temp_dict.get("id", 101))
                }
                data_to_post_list.append(data_to_post)
                # Clear temp_dict for the next entry
                temp_dict = {}

    return data_to_post_list


def load_csv_data(filename):
    """Load data from the CSV file."""
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = {rows[0].strip('"'): rows[1].strip('"') for rows in reader}
    return data

