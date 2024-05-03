import time
import pandas as pd
import numpy as np
import os
import datetime as dt


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# old no longer used variable
# CITIES = ('chicago', 'new york city', 'washington')
MONTHS = ('all', 'january', 'february', 'march', 'april', 'may', 'june', 'july')
DAYS = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

#    variable = input("Enter a number: ")

    lower_city = ''
#    while lower_city not in CITIES:ch
#        for mycity in CITIES: 
    while lower_city not in CITY_DATA.keys():
        for mycity in CITY_DATA.keys():
            print(mycity)
        input_city = input('Enter a city : ')
        lower_city = input_city.lower()
        city = lower_city

   # get user input for month (all, january, february, ... , june)
    lower_month = ''
    while lower_month not in MONTHS:
        for mymonth in MONTHS: 
            print(mymonth)
        input_month = input('Enter a month : ')
        lower_month = input_month.lower()
        month = lower_month

    # get user input for day of week (all, monday, tuesday, ... sunday)
    lower_day = ''
    while lower_day not in DAYS:
        for myday in DAYS: 
            print(myday)
        input_day = input('Enter a day : ')
        lower_day = input_day.lower()
        day = lower_day

    print(city)
    print(month)
    print(day)
    print('-'*40)
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
    # From Practice Solution No 3
    # dt.weekday_name no longer supported instead use : dt.day_name()

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # print(df)
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (df) dataframe on which time stat calculation should be processed
    """



    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_month = df['month'].mode()[0]

    print('Most month:', MONTHS[most_month])

    print('---other infos---')
    # print(df['month']==6)
    
    # Option 1
    # print('Count of most month :', len(df[df['month']==most_month]))

    # Option 2
    print('Count of most month :', (df['month']==most_month).sum())

    print('---other infos---')

    # cnt_most_month = df.groupby(['month']).count()
    # print('test:', cnt_most_month)

    # display the most common day of week
    most_day = df['day_of_week'].mode()[0]
    print('Most day:', most_day)

    # display the most common start hour
    most_hour = df['hour'].mode()[0]
    print('Most hour:', most_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (df) dataframe on which time stat calculation should be processed
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    print('Most used start station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most used End station:', df['End Station'].mode()[0])


    # display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + '-' + df['End Station']
    print('Most used route:', df['route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        (df) dataframe on which time stat calculation should be processed
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['travel_time'] = pd.to_datetime(df['End Time']).subtract(df['Start Time'])
    # print(df)

    print('Total travel time :', (df['travel_time']).sum())


    # display mean travel time
    print('Mean travel time :', (df['travel_time']).mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


   

def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    Args:
        (df) dataframe on which time stat calculation should be processed
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    for uu in df['User Type'].unique():
        print(f'Count of User Type {uu} :', (df['User Type']==uu).sum())
    


    column_name = 'Gender'
    if column_name in df.columns:
        # Display counts of gender
        value_counts = df['Gender'].value_counts(dropna=False)
        for ug in df['Gender'].unique():
            # missed nan Value
            #print(f'Count of Gender {ug} :', (df['Gender']==ug).sum(skipna=False))
            #print(f'Count of Gender {ug} :', (df['Gender']==ug).value_counts())
            print(f'Count of Gender {ug} :',value_counts[ug])
    
        #value_counts = df['Gender'].value_counts(dropna=False)
        #print(value_counts)

    else:
        print(f"Information '{column_name}' does not exist for choosen city.")

    
    # Display earliest, most recent, and most common year of birth
    column_name = 'Birth Year'
    if column_name in df.columns:
        print('Oldest person birthdate :', df['Birth Year'].min())
        print('Youngest person birthdate :', df['Birth Year'].max())
        print('Most common birthdate :', df['Birth Year'].value_counts().idxmax())
    
        #value_counts = df['Gender'].value_counts(dropna=False)
        #print(value_counts)

    else:
        print(f"Information '{column_name}' does not exist for choosen city.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Displays statistics on bikeshare users.
    
    Args:
        (df) dataframe on which time stat calculation should be processed
    """
    show = input('\nWould you like to see raw data? Enter yes or no.\n')
    if show.lower() == 'yes':
        start_index = 0
        step = 5
        while True:

            print(df[start_index:start_index+step])
    
            cnt = input('\nWould you like to see more? Enter yes or no.\n')
    
            if cnt.lower() != 'yes':
                break
    

def main():

    print('---- Welcome ----')
    while True:
        #city = 'chicago'
        #month = 'all'
        #day = 'monday'

        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
