import time
import pandas as pd
import numpy as np
from tabulate import tabulate


CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }


def check_data_entry(prompt, valid_entries):
    """
    Asks user to type some input and verify if the entry typed is valid.
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted 
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        user_input = str(input(prompt)).lower().title()
        while user_input not in valid_entries:
            print("Not an appropriate choice.")
            print("Try again")
            user_input = str(input(prompt)).lower().title()
        return user_input
            
    except:
        print('Seems like there is an issue with your input')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    valid_cities = CITY_DATA.keys()
    cities_prompt = 'Please choose city to analyze its data (Chicago, New York City, Washington): '
    city = check_data_entry(cities_prompt, valid_cities)
    
    valid_months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    months_prompt = 'Please enter month to analyze data (choose from january to june or all for all months): '
    month = check_data_entry(months_prompt, valid_months)
    
    valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
    days_prompt = 'Please choose weekday name to analyze data (choose from monday to sunday or all for all weekdays): '
    day = check_data_entry(days_prompt, valid_days)
    
    print('-'*120)
    print('\nData to analyze\n\nCity:\t\t{}\nMonth period:\t{}\nDays period:\t{}\n'.format(city, month, day))
    print('-'*120)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df.rename(columns={'Unnamed: 0':'Trip_id'}, inplace=True)
    df.set_index('Trip_id', inplace=True)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #df['day_of_week'] += 1

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        #month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'All':
        # use the index of the months list to get the corresponding int
        #days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        #day = days.index(day)+1
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    try:
        # display the most common month
        popular_month = df['month'].value_counts().idxmax()
        print('Most common month: \t\t', popular_month)

        # display the most common day of week
        popular_weekday = df['day_of_week'].value_counts().idxmax()
        print('Most common day of week: \t', popular_weekday)

        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].value_counts().idxmax()
        print('Most common hour: \t\t', popular_hour)
    except KeyError:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
        # display most commonly used start station
        popular_start_station = df['Start Station'].value_counts().idxmax()
        print('Most commonly used start station:\t\t\t', popular_start_station)

        # display most commonly used end station
        popular_end_station = df['End Station'].value_counts().idxmax()
        print('Most commonly used end station:\t\t\t\t', popular_end_station)

        # display most frequent combination of start station and end station trip
        df['start_end_comb'] = '(' + df['Start Station'] + ') & (' + df['End Station'] + ')'
        popular_freq_comb = df['start_end_comb'].value_counts().idxmax()
        print('Most frequent combination of start and end station trip:', popular_freq_comb)
    except KeyError:
        pass
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:
        # display total travel time
        total_travel_time = df['Trip Duration'].sum()
        print('Total travel time: \t', total_travel_time)

        # display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        print('Mean travel time: \t', mean_travel_time)
    except KeyError:
        pass
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    try:
        # Display counts of user types
        user_type_counts = df['User Type'].value_counts().to_string()
        print('Counts of user types:\n{}'.format(user_type_counts), '\n')
    
        # Display counts of gender
        gender_counts = df['Gender'].value_counts().to_string()
        print('Counts of gender:\n{}'.format(gender_counts), '\n')
    
        # Display earliest, most recent, and most common year of birth
        earliest_YOB = df['Birth Year'].min()
        most_recent_YOB = df['Birth Year'].max()
        most_common_YOB = df['Birth Year'].value_counts().idxmax()
        print('earliest YOB\t\t{}\nmost recent YOB\t\t{}\nmost common YOB\t\t{}'.format(earliest_YOB, most_recent_YOB, most_common_YOB))

    except KeyError:
        pass
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        default_cols = df.columns
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        if view_data != 'yes':
            print('\nYou choose not to display individual trip data\n')
        else:
            start_loc = 0
            keep_asking = True
            while (keep_asking):
                for i in range(5):
                    print(df[default_cols].iloc[start_loc].to_string(), '\n')
                    start_loc += 1
                view_display = input("Do you wish to continue?: \n").lower()
                if view_display == "no": 
                    keep_asking = False

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\nYou choose exit\nThank You')
            break

if __name__ == "__main__":
	main()
