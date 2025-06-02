# takes a csv from get_sensing_data and formats it into a dictionary to pass to data_analyzer
# using error code parser methods
#input: csv filepath
#output: dictionary with node id as key and error counter with battery and systme info added

from error_code_parser import load_error_database, parse_json_file

def format_data(filepath):
    #load error database from ERRORCODE.md file, or github
    #parse json file with the error database (two other params)
    #add battery info to dictionary
    #add system info to dictionary
