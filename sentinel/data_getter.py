from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import pprint
from error_code_parser import parse_json_file
from error_code_parser import load_error_database

load_dotenv()  # Load environment variables from .env

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor  # Makes query results dict-like instead of tuples
    )


# Example usage of the get_connection function
def fetch_latest_raw_entries(limit=5):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
                SELECT * 
                FROM public.raw 
                ORDER BY ingest_time DESC 
                LIMIT {limit};
                """) # DESC is descending order
    
    rows = cur.fetchall() # The data type is a list of dict-like objects due to RealDictCursor
    cur.close()
    conn.close()
    return rows

'''
Get the most recent diagnostic/v2 row for a given node_id where the message contains 
a Kestrel object inside Diagnostic -> Devices, and then
extract the first value in PORT_V as the battery level.
'''
def fetch_latest_battery(node_id):
    conn = get_connection()
    cur = conn.cursor()
    
    query = """
    SELECT
      node_id,
      publish_time,
      (kestrel_data->'PORT_V'->>0)::float AS battery_voltage
    FROM public.raw,
      jsonb_array_elements((message::jsonb)->'Diagnostic'->'Devices') device_data,
      LATERAL (
        SELECT device_data->'Kestrel' AS kestrel_data
        WHERE device_data ? 'Kestrel'
      ) sub
    WHERE
      event = 'diagnostic/v2'
      AND node_id = %s
    ORDER BY publish_time DESC
    LIMIT 1;
    """
    
    cur.execute(query, (node_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    return row

# node_id = "e00fce68f374e425e2d6b891" 
# battery = fetch_latest_battery(node_id)

# if battery:
#     print(f"Latest battery reading (voltage) for node {battery['node_id']} on \n[{battery['publish_time']}] is: {battery['battery_voltage']}")
#     # print(f"[{battery['publish_time']}] Battery voltage: {battery['battery_voltage']} V")
# else:
#     print("No recent diagnostic entry with Kestrel found.")




# sentinel/main.py
# Load error database (fetches from github if not found locally)
error_db = load_error_database(None) # 
if not error_db:
  print("Failed to load error database. Cannot continue.")
generate_graph = False
node_filter = []
# Parse the JSON file and generate the graph if needed

'''
This function will parse the JSON file containing error codes and generate a graph if specified.
Parameters:
- json_file: The path to the JSON file containing error codes.
- error_db: The error database to load the error codes into.
- node_filter: A list of nodes to filter the error codes by.
Returns:
- Dictionary containing the parsed nodes and the frequency of their errors.
{
    "all": Counter({
        "0x80070000": 3,
        "0x500400f6": 2,
        "0xf00500f9": 1
    }),
    "nqepuig3898tva7fg": Counter({
        "0x80070000": 2,
        "0x500400f6": 1
    }),
    "qiubgv9q984g3qreg": Counter({
        "0x80070000": 1,
        "0x500400f6": 1,
        "0xf00500f9": 1
    })
}

Keys are strings: "all" and possibly node IDs (like "12345", "nodeA", etc.).
Values are collections.Counter objects, which are like dictionaries that count occurrences of things.
'''
error_counters = parse_json_file("error_codes.json", error_db, node_filter)

for node, errors in error_counters.items():
    print(f"Node: {node}")
    for error, count in errors.items():
        print(f"  Error: {error}, Count: {count}")
    print("\n")


def visualize_error_counts(error_counters):
    """
    Visualize the output of parse_json_file() as bar charts.
    Each key in error_counters is a node (or 'all'), and its value is a Counter of error codes.
    """
    import matplotlib.pyplot as plt

    for node_id, counter in error_counters.items():
        if not counter:
            continue
        codes, counts = zip(*counter.most_common())
        plt.figure(figsize=(12, 6))
        plt.bar(codes, counts, color='skyblue')
        plt.title(f"Error Code Frequency for Node '{node_id}'")
        plt.xlabel("Error Code")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

# Example usage:
# error_counters = parse_json_file('your_file.json', error_db)
# visualize_error_counts(error_counters)