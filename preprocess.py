import pandas as pd

def get_data(path):
    return pd.read_csv(path, parse_dates=['FlightDate'])


df = get_data('.\\data\\merged\\2022.csv')
df=df.drop_duplicates()
df=df[df['FlightDate'] < '2022-04-01']
df['Avg_Delay']=df.apply(lambda x: (x.DepDelay + x.ArrDelay)/2, axis=1)

delay_type = lambda x:((0,1)[x > 5],2)[x > 45]

df['Delay_Level'] = df['Avg_Delay'].apply(delay_type)
df.to_csv('.\\data\\cleaned\\2022.csv', index=False)