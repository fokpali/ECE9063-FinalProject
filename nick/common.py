import os
import time
import pandas as pd


DATA_FOLDER = 'nfl-playing-surface-analytics'
CUST_FOLDER = 'custom_csv_files'


def load_data(fname, data_path=CUST_FOLDER, verbose=True):
    """
    Loads a csv file from the given file name and data_path.

    Parameters
    ----------
    fname : str
        The name of the csv file to load.
    data_path : str
        The folder where the csv file is located.

    Returns
    -------
    df : pandas.DataFrame
        The loaded csv file as a pandas DataFrame.
    """
    start = time.time()
    df = pd.read_csv(os.path.join(data_path, fname))
    if verbose:
        print('{} csv loaded in {} seconds...'.format(fname, time.time() - start))
        print('{} shape: {}'.format(fname, df.shape))
    return df


def injury_severity_to_string(value):
    if value == 4:
        return '42 or more days missed due to injury'
    elif value == 3:
        return '28 or more days missed due to injury'
    elif value == 2:
        return '7 or more days missed due to injury'
    elif value == 1:
        return '1 or more days missed due to injury'
    else:
        return 'No injury'
    

def decode_position_type(key):
    if key == 'LB':
        return 'Linebacker'
    elif key == 'WR':
        return 'Wide Receiver'
    elif key == 'OL':
        return 'Offensive Lineman'
    elif key == 'DL':
        return 'Defensive Lineman'
    elif key == 'S':
        return 'Safety'
    elif key == 'CB':
        return 'Cornerback'
    elif key == 'RB':
        return 'Running Back'
    elif key == 'TE':
        return 'Tight End'
    elif key == 'QB':
        return 'Quarterback'
    elif key == 'K':
        return 'Kicker'
    else:
        return 'Unknown Position'
    
