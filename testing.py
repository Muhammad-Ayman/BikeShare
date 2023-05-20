import pandas as pd
from sys import exit
from click import clear
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
city = pd.read_csv('chicago.csv')
"""city = list(CITY_DATA.keys())
df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]),city),sort= True)

months = ['january', 'february', 'march', 'april', 'may', 'june']

days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday']
df['Start Time'] = pd.to_datetime(df['Start Time'])
df['End Time'] = pd.to_datetime(df['End Time'])
df['Month'] = df['Start Time'].dt.month
df['Day'] = df['Start Time'].dt.weekday_name
df['Hour'] = df['Start Time'].dt.hour
df = pd.concat(map(lambda month: df[df['Month'] == months.index(month)+1],months))
for i in range(4):
    clear()
    print('hih')
exit()"""
print(city['Gender'].value_counts().idxmax())