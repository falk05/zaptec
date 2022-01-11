import json
import datetime as dt
from os import read
import pandas as pd
import numpy as np
from pandas.io import html
import csv

"""
Python script that calculates Hochtarif and Niedertarif kWh consumed by Zaptec charging devices.

Takes as input a file called 'response.json' contained in the same directory as the script.
response.json is received from Zaptec "chargehistory" API endpoint:
https://api.zaptec.com/api/chargehistory

Creates an xlsx table showing sum of kWh, by device ID, year and tarif HT/NT

Github location of this script:
https://github.com/falk05/zaptec.git

"""


def load_file():
    """" Read the response file from Zaptec and turn the timestamped kWh readings for each charging station into a pandas dataframe """

    file = 'response.json'
    df={}

    # open json file
    with open (file) as f:
        df = json.load (f)
    
    readings=[]

    # iterate through json response and build list of readings
    for d in df['Data']:
        if 'SignedSession' in d:   # because SignedSession does not seem to exist for all entries
            dss = json.loads(d['SignedSession'].strip('OCMF|'))
            for t in dss['RD']:   # iterate through readings of all sessions and create list of required attributes
                deviceid = d['DeviceName']
                timestamp = t['TM']
                reading = float(t['RV'])
                entry=[deviceid,timestamp,reading]  # convert to tuple
                readings.append(entry)  # append tuple to list

    readingsdf = pd.DataFrame(readings, columns=['DeviceID','Timestamp','kWh'])  # make pandas dataframe from list

    # Convert timestamp to datetime format
    readingsdf['Timestamp'] = pd.to_datetime(readingsdf['Timestamp'].str[0:23])
    
    # Add timezone GMT then convert to Europe/Zurich timezone in order to account for daylight savings time (Winterzeit/Sommerzeit)
    # TODO:  This should correctly be done by first querying the timezone of the installation using another API endpoint

    # This is to correct for the fact that Zaptec reading time series seem to omit Winterzeit/Sommerzeit
    readingsdf['Timestamp'] = readingsdf['Timestamp'].dt.tz_localize('Etc/GMT')
    readingsdf['Timestamp'] = readingsdf['Timestamp'].dt.tz_convert('Europe/Zurich')

    # Sort by DeviceID and kWh ascending
    # note:  cannot sort by timestamp because then kWh is not monotonically ascending (maybe Zaptec bug?)
    readingsdf.sort_values(by=['DeviceID','kWh'],inplace=True)
    
    # Create convenience rows for later calculation and grouping
    readingsdf['month'] = pd.DatetimeIndex(readingsdf['Timestamp']).month
    readingsdf['Year'] = pd.DatetimeIndex(readingsdf['Timestamp']).year
    readingsdf['dayofweek'] = pd.DatetimeIndex(readingsdf['Timestamp']).dayofweek
    
    # For each DeviceID, add the kWh added from the kWh reading of the previous row
    grouped_by_device = readingsdf.groupby('DeviceID')
    readingsdf = readingsdf.groupby('DeviceID').apply(calc_kWh_added)

    return readingsdf


def calc_kWh_added (group):
    """
    Calculate the kWh added since previous kWh reading
    """
    # kWh_added is the difference of the kWh reading of the current row minus the kWh reading of the preceding row
    group['kWh_added'] = group['kWh'] - group['kWh'].shift(1)
    return group


def determine_HTorNT (ts):
    """
    Takes a pd.datetime timestamp and returns HT or NT

    Tarifzeiten (Hochtarif HT, Niedertarif NT)
    Der Hochtarif gilt von Montag bis Freitag von 07.00 bis 20.00 Uhr und am Samstag von 07.00 bis 13.00 Uhr.
    Der Niedertarif gilt für die übrige Zeit. Sofern keine getrennte Messung möglich ist, wird der Hochtarif verrechnet.
    """

    if ts.dayofweek == 6:
        return ('NT')  # Sundays are always NT
    elif ts.dayofweek == 5:
        if ts.hour<7 or ts.hour>12:
            return ('NT')  # Saturdays are NT before 0700 and after 1300 hours
        else:
            return ('HT') # Otherwise, Saturdays are HT
    else:
        if ts.hour<7 or ts.hour>19:
            return ('NT')  # Monday to Friday are NT before 0700 and after 2000 hours
        else:
            return ('HT')  # all other times are HT
    

def determine_tarifs (df):
    """"
    Create a new "tarif" column by applying the determine_HTorNT function to the timestamp column
    """
    df['Tarif'] = df['Timestamp'].apply(determine_HTorNT)
    return df

    
def print_output(df):
    """"
    Prints an output table that shows sum of kWh , by device ID, year and tarif HT/NT
    Args
        df:  pandas dataframe
    """
    dfp = df.groupby(by=['DeviceID','Year','Tarif'])['kWh_added'].sum().reset_index(name='kWh')
    print('\nTabelle mit bezogenen kWh, nach Ladestationen / Jahr / Tarif:\n')
    print (dfp)
    print('\nTabelle gespeichert nach Datei zaptec.xlsx\n')
    dfp.to_excel ('zaptec.xlsx', index=False)
    


def main():
    readingsdf=load_file()
    readingsdf=determine_tarifs(readingsdf)

    print ('\nTotal kWh delivered to date: {}'.format(int(readingsdf['kWh_added'].sum())))

    print ('\nThe earliest timestamp in the dataset is: {}'.format(readingsdf['Timestamp'].min()))
    print ('\nThe most recent timestamp in the dataset is: {}\n'.format(readingsdf['Timestamp'].max()))

    print_output(readingsdf)

if __name__ == "__main__":
	main()

