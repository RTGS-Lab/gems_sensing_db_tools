import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_getter import fetch_latest_battery
from data_formater import format_battery_data
from data_analyzer import analyze_battery_data
from notification_system import notify

node_id = "e00fce68243ac35987c6c910" 

raw_battery_data = fetch_latest_battery(node_id)
formatted_battery_data = format_battery_data(raw_battery_data)
analysis_result = analyze_battery_data(formatted_battery_data)
notify(analysis_result)