#evaluate formatted data based on anns parameters
#inputs: dictionary of formatted data
#outputs: nofication ready data

def analyze_battery_data(data):
    if not data:
        return {"status": "no_data", "message": "No battery data available."}

    if data["voltage"] < 3.6:
        return {
            "status": "flagged",
            "message": f"Battery LOW at {data['voltage']}V on node {data['node_id']} at {data['timestamp']}."
        }
    else:
        return {
            "status": "ok",
            "message": f"Battery is healthy at {data['voltage']}V on node {data['node_id']}."
        }
