# temporary script to extract unique node_ids from a CSV file

import os
import csv

# Set of valid message types
valid_message_types = {"diagnostic/v2", "data/v2", "metadata/v2", "error/v2"}

# Path to the data directory and CSV file
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
csv_filename = "20250602_20250603_ALL_20250603152211.csv"
# csv_path = os.path.join(data_dir, csv_filename)
csv_path = "data/20250602_20250603_ALL_20250603152211.csv"

# Function to get unique node_ids from the CSV file
def get_unique_node_ids(csv_path):
    unique_node_ids = set()
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            message_type = row.get("event")
            node_id = row.get("node_id")
            if message_type in valid_message_types and node_id:
                unique_node_ids.add(node_id)
    return unique_node_ids

if __name__ == "__main__":
    unique_node_ids = get_unique_node_ids(csv_path)
    print("Unique node_ids:", unique_node_ids)
    print("Count:", len(unique_node_ids))


