from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import pprint
from gems_sensing_db_tools.error_code_parser import parse_json_file

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


parse_json_file("error_codes.json")