import os
import pandas as pd
from datetime import datetime as dt
import requests
import json
import database as db # our script for simpler db integration
from config import config # pull sensitive data from .ini files
from util import *

# set data directory
data_path = (os.getcwd() + "/Data/")

# connection to Postgres database
conn = db.connect()

JSON_KEYS = read_dict('pipe_keys.pkl')

def get_data(endpoint, start, limit):
    
    params = config(section='pipedrive')
    params.update({'start':start,'limit':limit})
    
    response = requests.get(params['company_domain'] + endpoint, params=params)
    
    if response.status_code == 200:
        json_msg = response.json()
    else:
        print(response.status_code)
        return
    
    data = json_msg['data']
    
    if endpoint not in ['deals','organizations','persons','pipelines']:
        next_start = len(data)
    else:
        if json_msg['additional_data']['pagination']['more_items_in_collection']:
            next_start = json_msg['additional_data']['pagination']['next_start']
        elif data is None:
            next_start = start
        else:
            next_start = start + len(data)
    
    return data, next_start

def json_to_df(json_data, json_keys, df_rename):
    
    data = pd.json_normalize(json_data)[json_keys]
    
    data.rename(columns=dict(zip(json_keys, df_rename)), inplace=True)
    
    data = fill_missing(data)
    data = to_date(data)
    
    return data

def etl(endpoint, limit=500):
    """
    arguments:
        endpoint - Pipedrive endpoint to retreive data from
        limit - the amount of data to retrieve in this batch
    
    returns output message for failure/success
    """
    
    if endpoint not in [*JSON_KEYS]:
        print('{} is not a valid endpoint. Please try again.'.format(endpoint))
        return False
    
    start = db.execute_query(conn, "select start_nbr from endpoints where endpoint_nme = '{}';".format(endpoint))
    
    if start == -1: return False
    start = start[0][0] # unpack tuple
    
    # read max rows from most recently stored data
    json_data, next_start = get_data(endpoint, start=start, limit=limit)
    
    if (start == next_start) or (json_data is None):
        print('No new data in {}. Check back later.'.format(endpoint))
        return False
    
    if endpoint == 'users': table = 'employees'
    else: table = endpoint
    
    table_cols = db.execute_query(conn, "select column_name from information_schema.columns where table_name = '{}';".format(table))
    name_updates = [col_name for i in table_cols for col_name in i]
    
    data = json_to_df(
        json_data, # json data
        JSON_KEYS[endpoint], # data names from json
        name_updates # new column names for df
    )
    
    # write data to database (will rollback if not successful)
    write_data = db.execute_values(conn, data, table)

    if write_data == -1: return False

    # increment tracker to new start
    update_endpoint = db.execute_query(conn, "update endpoints set start_nbr = {pos}, update_dtm = current_timestamp where endpoint_nme = '{endpoint}'".format(pos=next_start, endpoint=endpoint))

    if update_endpoint == -1: return False
    
    print('Loaded {} data ({} to {}) to database.'.format(endpoint, start, next_start))
    return True

def get_missing_data(endpoint):
    
    if endpoint == 'users': table = 'employees'
    else: table = endpoint
    
    table_cols = db.execute_query(conn, "select column_name from information_schema.columns where table_name = '{}';".format(table))
    name_updates = [col_name for i in table_cols for col_name in i]
    
    ids = db.execute_query(conn,"""
        SELECT all_ids AS missing_ids
        FROM generate_series(1, (SELECT MAX({id}) FROM {table})) all_ids
        EXCEPT 
        SELECT {id} FROM {table}
        order by missing_ids;
    """.format(table=table, id=table_cols[0][0]))
    
    if not ids:
        print('No additional data from {}'.format(endpoint))
        return False
    
    # initialize columns
    data = pd.DataFrame(columns=name_updates)
    
    for i in ids:
        data = data.append(json_to_df(
            get_data('{endpoint}/{id}'.format(endpoint=endpoint, id=i[0]),0,10)[0],
            JSON_KEYS[endpoint],
            name_updates
        ), ignore_index=True)
    
    write_data = db.execute_values(conn, data, table)
    
    if write_data == -1: return False
    
    print('Loaded missing {} data to database.'.format(endpoint))
    
    return True

if __name__ == '__main__':
    for endpoint in [*JSON_KEYS]:
        continue_load = True

        # API -> Postgres until no new data
        while continue_load: continue_load = etl(endpoint)

        # get id's that may have been skipped (deleted, inactive, etc.)
        if endpoint == 'organizations': get_missing_data(endpoint)
