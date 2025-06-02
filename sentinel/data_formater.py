# data_formater.py

def format_battery_data(battery_row):
    if not battery_row:
        return None

    return {
        "node_id": battery_row["node_id"],
        "timestamp": battery_row["publish_time"],
        "voltage": battery_row["battery_voltage"]
    }