import time
import datetime as dt
import pandas as pd
import numpy as np
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

CITY_DATA = {'chicago':'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Welcome to this interactive data analysis tool! Let\'s explore some bikeshare data!')

    while True:
        try:
            city = input('Enter the name of your chosen city (chicago, new york city, washington):').lower()
            if city not in ['chicago','new york city','washington']:
                print('Invalid selection, please enter city name from the list')
            else:
                break
        except:
            print('Invalid selection, please enter city name from the list')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Choose month to analyse (all, january, february, march, april, may, june):').lower()
            if month not in ['all','january','february', 'march', 'april', 'may', 'june']:
                print('Invalid selection, please enter month from the list')
            else:
                break
        except:
            print('Invalid selection, please enter month from the list')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Choose day of the week (all, monday, tuesday, ...):').lower()
            if day not in ['all','monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                print('Invalid selection, please enter a day of the week')
            else:
                break
        except:
            print('Invalid selection, please enter a day of the week')

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.day_name()
        
    if month != 'all':
        months = ['january','february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # extract hour from the Start Time column to create an hour column
    months = ['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', months[popular_month - 1])

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['station_combo'] = df['Start Station'] + df['End Station']
    popular_station_combo = df['station_combo'].mode()[0]
    print('Most Popular Station Combination:', popular_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()/60
    print('Total Travel Time (minutes):', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    print('Mean Travel Time (minutes):', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user = dict(df['User Type'].value_counts())
    print('Count of User Types:', count_user)

    # Display counts of gender
    if city in ['chicago', 'new york city']:
        count_gender = dict(df['Gender'].value_counts())
        print('Count of Gender:', count_gender)

    # Display earliest, most recent, and most common year of birth
    if city in ['chicago', 'new york city']:
        common_birth_year = df['Birth Year'].mode()[0]
        recent_birth_year = df['Birth Year'].max()
        early_birth_year = df['Birth Year'].min()
        print('Most Common Birth Year:', common_birth_year)
        print('Most Recent Birth Year:', recent_birth_year)
        print('Earliest Birth Year:', early_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        view_data = input('\nWould you like to see the top 5 lines of data? Enter yes or no.\n')
        if view_data.lower() == 'yes':
            i = 0
            print(df.loc[i:i+4,:])
            more_lines = 'yes'
            while more_lines == 'yes':
                more_lines = input('\nWould you like to see 5 more? Enter yes or no.\n')
                if more_lines.lower() == 'yes':
                    i += 5
                    print(df.loc[i:i+4,:])

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
