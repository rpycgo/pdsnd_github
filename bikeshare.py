import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = {'all', 'january', 'february', 'march', 'april', 'may', 'june'}
# DATES = {'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'all'}
DATES = {'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('input city: ').lower()
        
        if city not in CITY_DATA:
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('input month: ').lower()
        
        if month not in MONTHS:
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('input day: ').lower()
        
        if day not in DATES:
            continue
        else:
            break


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
    df = pd.read_csv(CITY_DATA.get(city))
    
    is_next = True if input('If you want to check original data, enter yes') == 'yes' else False
    i = 0
    while is_next:
        print(df.iloc[i:i+5])
        
        is_next = True if input('If you want to check next original data, enter yes') == 'yes' else False
        i += 5

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
   	 	# use the index of the months list to get the corresponding int
        months = ('january', 'february', 'march', 'april', 'may', 'june')
        month_index = months.index(month) + 1

        df = df.query(f'month == {month_index}')

    if day != 'all':
        df = df.query(f'day_of_week == "{day.title()}"')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common day:', common_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print(f'Most Commonly used start station: {start_station}')

    # TO DO: display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print(f'Most Commonly used end station: {end_station}')

    # TO DO: display most frequent combination of start station and end station trip
    combination_station = df.groupby(['Start Station', 'End Station']).count()
    print(f'Most Commonly used combination of (start station, end station trip): ({start_station}, {end_station})')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    ONE_DAY_TO_SECONDS = 86400
    # TO DO: display total travel time
    trip_duration = sum(df['Trip Duration']) / ONE_DAY_TO_SECONDS
    print(f'Total travel time: {trip_duration: .2f} Days')

    # TO DO: display mean travel time
    ONE_MINUTE_TO_SECOND = 60
    mean_travel_time = df['Trip Duration'].mean() / ONE_MINUTE_TO_SECOND
    print(f'Mean travel time: {mean_travel_time: .2f} Minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'User Types: {user_types}')

    # TO DO: Display counts of gender
    try:
        genders = df['Gender'].value_counts()
        print(f'Genders:{genders}')
    except KeyError as error:
        print(error)
    except Exception as error:
        print(error)

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        print(f'Earliest: {earliest}')
    except KeyError as error:
        print(error)
    except Exception as error:
        print(error)

    try:
        most_recent = int(df['Birth Year'].max())
        print(f'Most Recent: {most_recent}')
    except KeyError as error:
        print(error)
    except Exception as error:
        print(error)


    try:
        most_common_year = int(df['Birth Year'].value_counts().idxmax())
        print(f'Most Common Year: {most_common_year}')
    except KeyError as error:
        print(error)
    except Exception as error:
        print(error)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
