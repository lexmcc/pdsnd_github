import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print()
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = ''

    while city not in CITY_DATA:

        print()

        city = input('Which city would you like? Choose "Chicago", "New York City", or "Washington": ').lower()

        if city not in CITY_DATA:
            print()
            print('Oops! That doesn\'t look like a city we have on file. Please check your spelling.')

            print()
            retry = input('Would you like to try again? Please enter y or n: ' ).lower()

            # check if the user has entered something that we assume means 'yes' if starting with 'y', so we handle yes,yeah,yup,etc. If it doesn't, we'll exit the program.
            if retry.startswith('y') == False:

                print()
                print('Ok, thanks for stopping by.')

                exit()

        print()
        print('Ok great, we\'ll look for data from {}'.format(city.title()))
        print()



    # get user input for month (all, january, february, ... , june)
    month = ''

    while month not in months:

        month = input('Which month would you like to look up? We have data from January to June. If you want to see data from all months, just type "all": ').lower()

        if month not in months:

            print('Oh no, we haven\'t got data for {}, please check your spelling.'.format(month))

            print()
            retry = input('Would you like to try again? Please enter y or n: ' ).lower()

            # check if the user has entered something that we assume means 'yes' if starting with 'y', so we handle yes,yeah,yup,etc. If it doesn't, we'll exit the program.
            if retry.startswith('y') == False:

                print()
                print('Ok, thanks for stopping by.')

                exit()

        elif month == 'all':

            print()
            print('Cool, well look at data for all months.')
            print()

        else:
            print()
            print('Cool, we\'ll look for data from {}.'.format(month.capitalize()))
            print()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''

    while day not in days:

        day = input('Alrighty, finally which day of the week would you like to see data for? Choose "Monday" through to "Sunday", or "all" for data from every day: ' ).lower()

        if day not in days:

            print('Oh no, we haven\'t got data for {}, please check your spelling.'.format(day))

            print()
            retry = input('Would you like to try again? Please enter y or n: ' ).lower()

            # check if the user has entered something that we assume means 'yes' if starting with 'y', so we handle yes,yeah,yup,etc. If it doesn't, we'll exit the program.
            if retry.startswith('y') == False:

                print()
                print('Ok, thanks for stopping by.')

                exit()

        elif day == 'all':

            print()
            print('Data for all days it is.')
            print()

        else:
            print()
            print('Data from {} it is.'.format(day.capitalize()))
            print()



    print('-'*40)
    print('-'*40)
    print()
    print('Grand, to confirm, we\'re going to look at data for: \n \n City: {} \n Month: {} \n Day: {} '.format(city.title(),month.capitalize(),day.capitalize()))
    print()
    print('-'*40)
    print('-'*40)
    print()


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
    # Load the requested city data into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # Filter by the selected month
    if month != 'all':

        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df.month == month]

    if day != 'all':

        df = df[df.day_of_week == day.title()]

    return df


def check_data(city,month,day,df):
    ''' Enables the user to decide if they would like to see the first 5 lines of raw data from the DataFrame before continuing. If they do, they also can decide to change the filters they are searching for, if they've made a mistake, and a new updated DataFrame will be generated for statistical analysis.'''

    while True:
        check = input('Would you like to check the first 5 lines of data to make sure it\'s what you want? Enter Yes or No: ')

        if check.lower().startswith('y') == False:

            print('No probs, let\'s see those stats...')

            break

        first_5 = df.head()

        print(first_5)
        print()

        check_again = input('That look good to you? If not, to change your filters enter "Change", or else just hit enter: ')

        if check_again.lower() == 'change':

            city, month, day = get_filters()
            df = load_data(city, month, day)


        else:
            print()
            print('Ok, let\'s see those stats...')

            break

    return city, month, day, df

def time_stats(df,city,month,day):
    """Displays statistics on the most frequent times of travel.

    If we are looking at a specific day or month, the most_common_day or most_common_month are not shown. """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print()
    print('In {}...'.format(city.title()))
    print()


    # display the most common month only if we are looking at all months, else just show the month we are looking at.

    if month == 'all':
        most_common_month = df['month'].value_counts().idxmax()
        most_common_month_name = months[most_common_month - 1]
        print('The most common month of travel is {}.'.format(most_common_month_name.capitalize()))

    else:

        print('In the month of {}...'.format(month.title()))


    # display the most common day of week only if we are looking at all days, else just show the day we are looking at.
    if day == 'all':
        most_common_day = df['day_of_week'].value_counts().idxmax()
        print('The most common day of travel is {}.'.format(most_common_day.capitalize()))

    else:
        print('On {}s...'.format(day.title()))


    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['start_hour'].value_counts().idxmax()
    print('The most common start hour is {}:00.'.format(most_common_start_hour))


    print('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print('The most common start station is {}.'.format(most_common_start_station.title()))

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print('The most common end station is {}.'.format(most_common_end_station.title()))


    # display most frequent combination of start station and end station trip
    df['Start End Pairs'] = df['Start Station'] + ' ' + 'to' + ' ' + df['End Station']
    most_common_start_end_station_combo = df['Start End Pairs'].value_counts().idxmax()
    print('The most common Start and End Station combo is {}.'.format(most_common_start_end_station_combo))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = round(pd.to_numeric(df['Trip Duration']).sum() / 60**2,2)
    print('The total travel time was {} hours.'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = round(pd.to_numeric(df['Trip Duration']).mean() / 60,2)
    print('The average travel time was {} minutes.'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def gender_stats(df):
    '''Arguments: DataFrame.
    Output: If there is Gender data, then display the volumes of each, else tell us there's no Gender data'''

    if 'Gender' in df.columns:

        gen_types = df.groupby('Gender')['Gender'].count()
        gen_types = gen_types.to_dict()

        for gen_type in gen_types:

            print("There are {} {}s.".format(gen_types[gen_type], gen_type))


    else:

        print('We don\'t seem to have any gender data for this data set.')



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby('User Type')['User Type'].count()
    user_types = user_types.to_dict()

    for user_type in user_types:

        print("There are {} {}s.".format(user_types[user_type], user_type))



    # Display counts of gender
    ## If Gender not in the df, then say we have no gender data.

    gender_stats(df)

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.index:

        earliest_dob = int(df['Birth Year'].min())
        print('The earliest date of birth is: {}.'.format(earliest_dob))

        most_recent_dob = int(df['Birth Year'].max())
        print('The most recent date of birth is: {}.'.format(most_recent_dob))

        most_common_dob = int(df['Birth Year'].value_counts().idxmax())
        print('The most common date of birth is: {}.'.format(most_common_dob))

    else:

        print('We don\'t have any age related data for this data set.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        city, month, day, df = check_data(city,month,day,df)


        time_stats(df,city,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
