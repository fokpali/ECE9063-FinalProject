import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from common import load_data, DATA_FOLDER, CUST_FOLDER

# print the number of NaN values in each column
def print_na_info(df):
    for col in df.columns:
        print('{} : {}'.format(col, df[col].isna().sum()))


if __name__ == '__main__':

    # ----- STEP 1: Load all dataframes ----- #
    df_injuries = load_data('injuries_fixed.csv', verbose=False)
    df_distances = load_data('distances.csv', verbose=False)
    df_playlist = load_data('PlayList.csv', DATA_FOLDER, verbose=False)

    # Create new dataframe with relevant information from playlist
    dropped_cols = ['PlayKey', 'PlayerDay', 'PlayType', 'PlayerGamePlay', 'Position', 'PositionGroup']
    main_df = df_playlist.drop(columns=dropped_cols)
    main_df = main_df.groupby('GameID').first().reset_index()

    # ----- STEP 2: Merge Distance Data into Main Dataframe ----- #
    main_df = pd.merge(main_df, df_distances, how='left', on='GameID')
    main_df['GameDist'] = main_df['GameDist'].fillna(0)

    # ----- STEP 3: Merge Injury Data into Main Dataframe ----- #
    main_df = pd.merge(main_df, df_injuries, how='left', on='GameID')
    main_df['BodyPart'] = main_df['BodyPart'].fillna('None')
    main_df['InjurySeverity'] = main_df['InjurySeverity'].fillna(0)
    main_df['InjurySeverity'] = main_df['InjurySeverity'].astype(int)
    # print('Main df shape: {}'.format(main_df.shape))

    # ----- STEP 4: Remove uneeded features and fill NaN ----- #
    main_df = main_df.drop(columns=['BodyPart', 'Temperature'])
    main_df['StadiumType'] = main_df['StadiumType'].fillna('Unknown')
    main_df['Weather'] = main_df['Weather'].fillna('Unknown')

    # ----- STEP 5: Fix Column values ----- #
    main_df = main_df.rename(columns={'RosterPosition': 'Position'})
    main_df['Position'] = main_df['Position'].replace({
        'Linebacker': 'LB',
        'Wide Receiver': 'WR',
        'Offensive Lineman': 'OL',
        'Safety': 'S',
        'Defensive Lineman': 'DL',
        'Cornerback': 'CB',
        'Running Back': 'RB',
        'Tight End': 'TE',
        'Quarterback': 'QB',
        'Kicker': 'K'
    })

    main_df['Weather'] = main_df['Weather'].replace({
        'N/A (Indoors)': 'Indoor',
        'N/A (Indoor)': 'Indoor',
        'N/A Indoor': 'Indoor',
        'Indoors': 'Indoor',
        'Controlled Climate': 'Indoor',

        'Partly Cloudy': 'PartlyCloudy',
        'Partly Clouidy': 'PartlyCloudy',
        'Party Cloudy': 'PartlyCloudy',
        'Sun & clouds': 'PartlyCloudy',
        'Mostly Cloudy': 'PartlyCloudy',
        'Partly sunny': 'PartlyCloudy',
        'Clear to Partly Cloudy': 'PartlyCloudy',
        'Partly cloudy': 'PartlyCloudy',
        'Partly Sunny': 'PartlyCloudy',
        'Partly clear': 'PartlyCloudy',

        'Coudy': 'Cloudy',
        'Cloudy with periods of rain, thunder possible. Winds shifting to WNW, 10-20 mph.': 'Cloudy',
        'Cloudy, chance of rain': 'Cloudy',
        'Cloudy and cold': 'Cloudy',
        'Cloudy and Cool': 'Cloudy',
        'Cloudy, fog started developing in 2nd quarter': 'Cloudy',
        'Hazy': 'Cloudy',
        'Mostly Coudy': 'Cloudy',
        'Overcast': 'Cloudy',
        'cloudy': 'Cloudy',
        'Mostly cloudy': 'Cloudy',

        'Clear and Sunny': 'Clear',
        'Clear and sunny': 'Clear',
        'Sunny and clear': 'Clear',
        'Sunny and warm': 'Clear',
        'Sunny and cold': 'Clear',
        'Sunny Skies': 'Clear',
        'Sunny, Windy': 'Clear',
        'Sunny, highs to upper 80s': 'Clear',
        'Mostly Sunny Skies': 'Clear',
        'Mostly Sunny': 'Clear',
        'Mostly sunny': 'Clear',
        'Fair': 'Clear',
        'Clear Skies': 'Clear',
        'Clear skies': 'Clear',
        'Clear and Cool': 'Clear',
        'Clear and warm': 'Clear',
        'Clear and cold': 'Clear',
        'Clear and Cool': 'Clear',
        'Sunny': 'Clear',

        'Heavy lake effect snow': 'Snow',
        'Cloudy, light snow accumulating 1-3"': 'Snow',

        'Rain shower': 'Rain',
        'Cloudy, Rain': 'Rain',
        'Showers': 'Rain',
        'Rain likely, temps in low 40s.': 'Rain',
        '10% Chance of Rain': 'Rain',
        'Scattered Showers': 'Rain',
        'Rainy': 'Rain',
        'Cloudy, 50% change of rain': 'Rain',
        'Rain Chance 40%': 'Rain',
        '30% Chance of Rain': 'Rain',
        'Light Rain': 'Rain',

        'Cold': 'Unknown',
        'Heat Index 95': 'Unknown',
    })

    main_df['StadiumType'] = main_df['StadiumType'].replace({
        'Outdoors': 'Outdoor',
        'Oudoor': 'Outdoor',
        'Ourdoor': 'Outdoor',
        'Outddors': 'Outdoor',
        'Outside': 'Outdoor',
        'Outdor': 'Outdoor',
        'Domed, open': 'Outdoor',
        'Domed, Open': 'Outdoor',
        'Indoor, Open Roof': 'Outdoor',
        'Retr. Roof-Open': 'Outdoor',
        'Retr. Roof - Open': 'Outdoor',
        'Open': 'Outdoor',
        'Outdoor Retr Roof-Open': 'Outdoor',
        'Heinz Field': 'Outdoor',
        'Bowl': 'Outdoor',

        'Indoors': 'Indoor',
        'Indoor, Roof Closed': 'Indoor',
        'Domed, closed': 'Indoor',
        'Retr. Roof-Closed': 'Indoor',
        'Retr. Roof - Closed': 'Indoor',
        'Closed Dome': 'Indoor',
        'Dome, closed': 'Indoor',
        'Retr. Roof Closed': 'Indoor',
        'Domed': 'Indoor',
        'Dome': 'Indoor',

        'Retractable Roof': 'Unknown',
        'Cloudy': 'Unknown',
    })

    main_df.loc[main_df['Weather'] == 'Indoor', 'StadiumType'] = 'Indoor' # ensure indoor weather == indoor stadium

    # Reorder columns
    main_df = main_df[['GameID', 'PlayerKey', 'PlayerGame', 'Position', 'GameDist', 'CumulativeDist', 'StadiumType', 'FieldType', 'Weather', 'InjurySeverity']]

    print(main_df.head())
    print('Num of injuries in df: {}'.format(main_df.query('`InjurySeverity` > 0').shape[0]))
    print('Final shape: {}'.format(main_df.shape))

    # ----- Save to csv ----- #
    main_df.to_csv(os.path.join(CUST_FOLDER, 'exp2_data.csv'), index=False)

