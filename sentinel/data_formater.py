# data_formater.py
# takes a csv from get_sensing_data and formats it into a dictionary to pass to data_analyzer

def format_battery_data(battery_row):
    if not battery_row:
        return None

    return {
        "node_id": battery_row["node_id"],
        "timestamp": battery_row["publish_time"],
        "voltage": battery_row["battery_voltage"]
    }