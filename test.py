import pandas as pd

def get_data(path):
    return pd.read_csv(path, parse_dates=['FlightDate'])


df = get_data('.\\data\\merged\\2022.csv')

mean = df[['DepDelay', 'ArrDelay']].groupby(df['Reporting_Airline']).mean().reset_index()
print(mean.head())