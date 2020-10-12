import datetime as dt
import pandas as pd


def preprocess(df, is_est=False):
    """Format title and concat datetime
    """
    df.columns = [col.lower().replace('/', '').replace(' ', '') for col in df.columns] # format title
    
    # concat datetime
    df['datetime'] = df.date + df.time
    df['datetime'] = df['datetime'].apply(lambda x : dt.datetime.strptime(x, "%m/%d/%Y%H:%M:%S"))
    
    # filter out irregular timestamps
    if is_est:
        df = df[df['time'].isin(['23:00:00', '03:00:00', '07:00:00', '11:00:00', '15:00:00', '19:00:00'])]
    else:
        df = df[df['time'].isin(['00:00:00', '04:00:00', '08:00:00', '12:00:00', '16:00:00', '20:00:00'])]
        
    return df
    