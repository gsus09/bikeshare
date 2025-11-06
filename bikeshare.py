import time
import pandas as pd
from typing import Tuple

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters() -> Tuple[str, str, str]:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    cities = ['chicago', 'new york city', 'washington']
    while city not in cities:
        city = input("Please enter a city (chicago, new york city, washington): ").lower()
        if city not in cities:
            print("Invalid input. Please try again.")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    month = ""
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month not in months:
        month = input(
            "Please enter a month (january, february, march, april, may, june, ...) "
            "or 'all' to apply no month filter: "
        ).lower()
        if month not in months:
            print("Invalid input. Please try again.")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while day not in days:
        day = input(
            "Please enter a day of the week (monday, tuesday, wednesday, thursday, "
            "friday, saturday, sunday) or 'all' to apply no day filter: "
        ).lower()
        if day not in days:
            print("Invalid input. Please try again.")
        else:
            break
    print('-'*40)
    return city, month, day


def load_data(city: str, month: str, day: str) -> pd.DataFrame:
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
    # Print statistics of NA values per column
    na_counts = df.isna().sum()
    if na_counts.sum() > 0:
        print("NA values per column:")
        print(na_counts[na_counts > 0].to_string())
        print(f"for a total of rows {df.shape[0]}")
        print('-'*40)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'all':
        month_num = pd.to_datetime(month, format='%B').month
        df = df[df['Start Time'].dt.month == month_num]

    if day != 'all':
        df = df[df['Start Time'].dt.day_name().str.lower() == day]
    return df


def time_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(
        f"most common month StartDate: {df['Start Time'].dt.month.mode()[0]} "
        f"with count {df['Start Time'].dt.month.value_counts().iloc[0]}"
    )
    # display the most common day of week
    print(
        f"most common day of week StartDate: "
        f"{df['Start Time'].dt.day_name().mode()[0]} "
        f"with count {df['Start Time'].dt.day_name().value_counts().iloc[0]}"
    )
    # display the most common start hour
    print(
        f"most common start hour: {df['Start Time'].dt.hour.mode()[0]} "
        f"with count {df['Start Time'].dt.hour.value_counts().iloc[0]}"
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(
        f"most commonly used start station: {df['Start Station'].mode()[0]} "
        f"with count {df['Start Station'].value_counts().iloc[0]}"
    )

    # display most commonly used end station
    print(
        f"most commonly used end station: {df['End Station'].mode()[0]} "
        f"with count {df['End Station'].value_counts().iloc[0]}"
    )

    # display most frequent combination of start station and end station trip
    df['Start-End Combination'] = df['Start Station'] + " to " + df['End Station']
    print(
        "most frequent combination of start station and end station trip: "
        f"{df['Start-End Combination'].mode()[0]} "
        f"with count {df['Start-End Combination'].value_counts().iloc[0]}"
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(f"total travel time: {df['Trip Duration'].sum()} minutes")

    # display mean travel time
    print(f"mean travel time: {df['Trip Duration'].mean()} minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df: pd.DataFrame) -> None:
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(f"counts of {df['User Type'].value_counts().to_string()}")

    # Display counts of gender
    if 'Gender' in df.columns:
        print(f"counts of {df['Gender'].value_counts().to_string()}")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print(f"earliest year of birth: {int(df['Birth Year'].min())}")
        print(f"most recent year of birth: {int(df['Birth Year'].max())}")
        print(f"average year of birth: {df['Birth Year'].mean():.2f}")
        print(
            f"most common year of birth: {int(df['Birth Year'].mode()[0])} "
            f"with count {df['Birth Year'].value_counts().iloc[0]}"
        )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df: pd.DataFrame) -> None:
    """Displays raw data upon user request."""
    show_data = input('\nWould you like to see the raw data? Enter yes or no.\n').lower()
    start_loc = 0
    while show_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        if start_loc >= len(df):
            print("No more data to display.")
            break
        show_data = input('\nWould you like to see 5 more rows of data? Enter yes or no.\n').lower()


def main():
    """Main function to run the bikeshare data analysis program."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
