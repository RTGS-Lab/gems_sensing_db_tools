

def notify(analysis_result):
    if analysis_result["status"] == "flagged":
        print("⚠️ ALERT: Battery issue detected!")
        print(analysis_result["message"])
    elif analysis_result["status"] == "ok":
        print("✅ Battery status normal.")
        print(analysis_result["message"])
    elif analysis_result["status"] == "no_data":
        print("ℹ️ No recent diagnostic data with Kestrel found.")
