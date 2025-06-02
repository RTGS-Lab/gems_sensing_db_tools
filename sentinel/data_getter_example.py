#gets data from a database
#inputs: timeframe, database, project, credentials, node_ids
#outputs: csv file
# utilizes functions from get_sensing_data

from get_sensing_data import create_engine_from_credentials, save_data, get_raw_data

def get_data(start_date, end_date, node_ids):
    #create engine using get_sensing_data methods
    #get the raw data using get_sensning_data methods
    #save the data using the same methods
    #return filepath to csv
