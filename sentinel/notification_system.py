

# def notify(analysis_result):
#     if analysis_result["status"] == "flagged":
#         print("⚠️ ALERT: Battery issue detected!")
#         print(analysis_result["message"])
#     elif analysis_result["status"] == "ok":
#         print("✅ Battery status normal.")
#         print(analysis_result["message"])
#     elif analysis_result["status"] == "no_data":
#         print("ℹ️ No recent diagnostic data with Kestrel found.")


def notify(analysis_results):
    if isinstance(analysis_results, dict) and "status" in analysis_results:
        # Single node
        _notify_single(analysis_results)
    else:
        # Multiple nodes
        for node_id, result in analysis_results.items():
            print(f"\nNode: {node_id}")
            _notify_single(result)

def _notify_single(result):
    if result["status"] == "flagged":
        print("⚠️ ALERT: Battery issue detected!")
        print(result["message"])
    elif result["status"] == "ok":
        print("✅ Battery status normal.")
        print(result["message"])
    elif result["status"] == "no_data":
        print("ℹ️ No recent diagnostic data with Kestrel found.")
        print(result.get("message", ""))
    elif result["status"] == "unknown":
        print("❓ Battery voltage unknown.")
        print(result.get("message", ""))