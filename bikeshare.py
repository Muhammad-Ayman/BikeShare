import time
import pandas as pd
import numpy as np
from sys import exit
from click import clear
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday']


def get(question,ls=('y','n')):
    while True:
        try:
            ans = input(question)
        except ValueError:
            question = "Sorry, I didn't understand that. Please try again.\n> "
            continue

        ans = [i.lower().strip() for i in ans.split(',')]
        if(ans[0] == 'all'):
            return ls

        if(ans[0] == "cancel"):
            exit()

        filtered = list(filter(lambda x: x in ls,ans))
        if(filtered == ans):
           break
        question ="{} Not a valid choice(s). Please try again.\n> ".format( np.setdiff1d(ans, filtered))
    return ans



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-----Type cancel any time you would like to exit the program-----')
    print('-----Type all when you want to select all options-----\n')
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get("Please select the city(ies) you wanna explore it\'s data, [New York City, Chicago or Washington]:\n> ",
               CITY_DATA.keys())

    #get user input for month (all, january, february, ... , june)
    month = get('what month(s) do you want to filter data by, [january, february, march, april, may, june]:\n> ',
                months)

    #get user input for day of week (all, monday, tuesday, ... sunday)
    day = get('what day(s) do you wanna filter data by, [sunday, monday, tuesday, wednesday, thursday, friday, saturday]:\n> ',
              days)

    #print('-'*40)
    clear()
    print('Filters:  \nCities:{}\nMonths:{}\nDays:{}'.format(city,month,day))
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #if isinstance(city,list):
    df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]),city),sort= True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    df = pd.concat(map(lambda x: df[df['Month'] == months.index(x)+1],month))
    df = pd.concat(map(lambda x: df[df['Day'] == x.title()],day))

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    print('The most common month: {}\n'.format(months[df['Month'].mode()[0]-1]))

    #display the most common day of week
    print('The most common day: {}\n'.format(df['Day'].mode()[0]))

    #display the most common start hour
    print('The most common hour: {}\n'.format(df['Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    print('The most common start station: {}\n'.format(df['Start Station'].mode()[0]))

    #display most commonly used end station
    print('The most common end station: {}\n'.format(df['End Station'].mode()[0]))


    #display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station'] + ' > ' + df['End Station']
    print('The most frequent combination of start station and end station trip: {}\n'.format(df['Combination'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    print('Total travel time: {}\n'.format(df['Trip Duration'].sum()))

    #display mean travel time
    print('Mean travel time: {}\n'.format(df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    count = pd.DataFrame(df['User Type'].value_counts())
    count = count.reset_index()
    count.columns = ['User Type','Count']
    print('Counts of user types:\n{}\n'.format(count))

    #Display counts of gender
    try:
        count = pd.DataFrame(df['Gender'].value_counts())
    except:
        print('Data dosn\'t have gender column')
    else:
        count = count.reset_index()
        count.columns = ['Gender','Count']
        print('Count of each gender:\n{}\n'.format(count))
    #Display earliest, most recent, and most common year of birth
    try:
        BY = df['Birth Year']
    except:
        print('Data dosn\'t have Birth Year column')
    else:
        print('The earliest year of birth: {}\n'.format(BY.min()))
        print('The most recent year of birth: {}\n'.format(BY.max()))
        print('The most common year of birth: {}\n'.format(BY.mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            viewData = input("Would you like to see the raw data? Type 'Yes' or 'No': ")
            if viewData.lower() == "yes":
                row = 0
                print(df[row:row+5])
                row += 5
            else:
                break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' or restart.lower() == 'cancel':
            break


if __name__ == "__main__":
	main()
