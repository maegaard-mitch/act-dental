import pandas as pd

def to_date(data):
    
    date_cols = [col for col in data.columns if '_dte' in col]
    time_cols = [col for col in data.columns if '_dtm' in col]
    
    for col in date_cols:
        data[col] = pd.to_datetime(data[col]).dt.date
    
    for col in time_cols:
        data[col] = pd.to_datetime(data[col])
    
    return data

def fill_missing(data):
    # set aside specific columns
    id_cols = [col for col in data.columns if '_id' in col]
    nme_cols = [col for col in data.columns if '_nme' in col]
    dsc_cols = [col for col in data.columns if '_dsc' in col]
    cnt_cols = [col for col in data.columns if '_cnt' in col]
    amt_cols = [col for col in data.columns if '_amt' in col]
    nbr_cols = [col for col in data.columns if '_nbr' in col]
    dte_cols = [col for col in data.columns if '_dtm' in col]
    addr_cols = [col for col in data.columns if '_addr' in col]
    
    # impute values
    for col in (id_cols + cnt_cols + amt_cols + nbr_cols):
        data[col].fillna(-1, inplace=True)
    
    for col in (nme_cols + dsc_cols + addr_cols):
        data[col].fillna('', inplace=True)
    
    for col in (dte_cols):
        data[col].fillna('1900-01-01', inplace=True)
    
    return data
