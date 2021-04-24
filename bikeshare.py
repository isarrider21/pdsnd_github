import time
import pandas as pd
import numpy as np
import plotly.express as px

cities = {0: "all cities", 1: "Chicago", 2: "New York City", 3: "Washington"}
months = {0: "all months", 1: "January", 2: "February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
days = {0: "all weekdays", 1: "Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturady", 7:"Sunday"}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze by choosing from a set of numbers.
    Note: Improvement towards a more intuitive customer experience and interface: Allows the user to choose from numbers instead of taking the time to type and risk for errors.

    Returns:
        (int) city - key of the city to analyze; see cities for keys and values
        (int) month - key of the month to filter by; see months for keys and values
        (int) day - key of the day of week to filter by; see days keys and values
        (str) insights - filters if user wants to see and excerpt of the data and details on NaNs
    """
    print("\n" + "-"*40 + "\nHello! Let\'s explore some US bikeshare data!\n" + "-"*40)

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = int(input("\nPlease type in the number of the desired CITY \n{}: ".format(cities)))
            if 0 <= city <= 3:
                break
            raise ValueError()
        except ValueError:
            print("\nERROR: That\'s not valid number. Please enter a number between 0 and 3 to select the desired CITY.\n")

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = int(input("\nPlease type in the number of the desired MONTH  \n{} ".format(months)))
            if 0 <= month <= 12:
                break
            raise ValueError()
        except ValueError:
            print("\nERROR: That\'s not valid number. Please enter a number between 0 and 12 to select the desired MONTH.\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = int(input("\nPlease type in the number of the desired WEEKDAY  \n{}: ".format(days)))
            if 0 <= day <= 7:
                break
            raise ValueError()
        except ValueError:
            print("\nERROR: That\'s not valid number. Please enter a number between 0 and 7 to select the desired WEEKDAY.\n")

    # get user input for dataframe excerpt and further details on NaNs
    while True:
        try:
            insights = str(input('\nWould you like to see an data excerpt and details on missing data? Enter yes or no.\n'))
            break
        except ValueError:
            print("\nERROR: That\'s not a valid input. Please enter yes or no.\n")

    print('-'*40)
    print("Your data set of choice: {} for {} on {}(s).\n".format(cities[city], months[month], days[day]))

    return city, month, day, insights


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (int) city - key of the city to analyze; see cities for keys and values
        (int) month - key of the month to filter by, or "all" to apply no month filter; see months for keys and values
        (int) day - key of the day of week to filter by, or "all" to apply no day filter; see months for keys and values
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load data; if "all cities" was chosen, join csvs into one data frame; if not, load only the respective csv
    if city == 0:
        df = pd.concat(map(pd.read_csv, ["chicago.csv", "new_york_city.csv", "washington.csv"]))
    else:
        df = pd.read_csv(cities[city].lower().replace(" ","_") + ".csv")

    # convert the Start Time & End Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    # extract month, day, start hour and travel time (in minutes) in datetime and create respective columns; add 1 to get the true weekday value
    df["Month"] = df["Start Time"].dt.month
    df["Day"] = df["Start Time"].dt.weekday + 1
    df["Start Hour"] = df["Start Time"].dt.hour
    df["Travel Time"] = df["End Time"] - df["Start Time"]
    df["Travel Minutes"] = df["Travel Time"].dt.total_seconds().div(60).astype(int)

    # filter by month and day
    if month != 0 and day !=0:
        df = df.loc[(df["Month"] == month) & (df["Day"] == day)]
    elif month != 0:
        df = df.loc[df["Month"] == month]
    elif day != 0:
        df = df.loc[df["Day"] == day]

    return df

def display_data(df, insights):
    """
    Shows the user excerpts of the data and information on missing data as long as he/she wants

    Args:
    (str) insights - filters if user wants to see and excerpt of the data and details on NaNs
    """
    if insights.lower() == "yes":

        # display number of NaN values in the selected DataFrame and create a dict for NaNs in columns
        x = df.isnull().sum().sum()
        X = {}

        for col_name in df.columns:
            X[col_name] = df[col_name].isnull().sum().sum()

        print("\nNumber of total NaN values in the chosen DataFrame: {}".format(x))
        print("Details: {}\n".format(X))

        # print the first rows of the dataframe to get an indication on the data
        print(df.head())

        # show the user more data, if desired; start_loc = 5 due to df.head() beforehand
        start_loc = 5
        while True:
            view_data = str(input("\nWould you like to view 5 more rows of trip data? Enter yes or no: \n"))

            if view_data.lower() == "yes":
                print(df.iloc[:start_loc + 5])
                start_loc += 5
            else:
                break

    print('-'*40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_popular_month = df["Month"].mode()[0]
    print("Most popular month: {}".format(months.get(most_popular_month)))

    # display the most common day of week
    most_popular_weekday = df["Day"].mode()[0]
    print("Most popular weekday: {}".format(days.get(most_popular_weekday)))

    # display the most common start hour
    most_popular_starthour = df["Start Hour"].mode()[0]
    print("Most popular start hour: {}:00 h".format(most_popular_starthour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular_startstation = df["Start Station"].mode()[0]
    print("Most popular start station: {}".format(most_popular_startstation))

    # display most commonly used end station
    most_popular_endstation = df["End Station"].mode()[0]
    print("Most popular end station: {}".format(most_popular_endstation))

    # display most frequent combination of start station and end station trip
    most_popular_trip = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print("Most popular trip: From {} to {}".format(most_popular_trip[0], most_popular_trip[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Returns:
        (int) travel_time_minutes - travel time in inputs for calculating the revenue
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df["Travel Time"].sum()
    print("Total travel time: {}".format(travel_time))

    # display total travel time in minutes:
    travel_time_minutes = df["Travel Minutes"].sum()
    print("Total travel time in minutes: {}".format(travel_time_minutes))

    # display mean travel time
    mean_travel_time = df["Travel Time"].mean()
    print("Mean travel time: {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return travel_time_minutes

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("Subscribers: {}\nCustomers: {}".format(user_types[0], user_types[1]))

    # plot gender distribution with a pie chart
    print('\nCalculating Chart "User Type Distribution"...\n')

    fig = px.pie(values = user_types.values.tolist(), names = user_types.index.tolist(), title="User Type Distribution")
    fig.show()

    # Display counts of gender
    if "Gender" in df.columns:
        gender_types = df["Gender"].value_counts()
        print("\nMale: {}\nFemale: {}".format(gender_types[0], gender_types[1]))

        # plot gender distribution with a pie chart
        print('\nCalculating Chart "Gender Distribution"...\n')

        fig = px.pie(values = gender_types.values.tolist(), names = gender_types.index.tolist(), title="Gender Distribution")
        fig.show()
    else:
        print("No data on gender available in the chosen dataframe.")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        early_birth = df["Birth Year"].min()
        recent_birth = df["Birth Year"].max()
        common_birth = df["Birth Year"].mode()

        print("\nEarliest year of birth: {}".format(int(early_birth)))
        print("Most recent year of birth: {}".format(int(recent_birth)))
        print("Most common year of birth: {}".format(int(common_birth)))

    else:
        print("No data on birth year available in the chosen dataframe.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def revenue(df, travel_time_minutes):
    """Takes user input for price per minute and displays statistics on revenue.

    Args:
        - (int) travel_time_minutes - travel time in minutes
    """

    print("\nRevenue Calculation - Price Input")

    # get user input for the price per minutes
    while True:
        try:
            price = float(input("Please enter a price per minute in $ with decimal point (e.g. 0.35): "))
            break
        except ValueError:
            print("That is not a valid price.\n")

    print('\nCalculating Revenue...\n')
    start_time = time.time()

    # Display revenue
    rev = travel_time_minutes * price
    print("Your revenue for the chosen dataframe and given price is: ${}".format(rev))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day, insights = get_filters()
        df = load_data(city, month, day)
        insights = display_data(df, insights)

        stat = {0: "All", 1: "Time Statistics", 2: "Station Statistics", 3: "Trip Duration Statistics", 4: "User Statistics", 5:"Revenue"}

        # get user input for the desired statistics
        while True:
            try:
                stat_input = int(input("\nWhat STATISTICS do want to calculate? \n{}: ".format(stat)))
                if 0 <= stat_input <= 5:
                    break
                raise ValueError()
            except ValueError:
                print("\nERROR: That\'s not valid number. Please enter a number between 0 and 5 to select the desired STATISTICS.\n")

        print('-'*40)

        if stat_input == 0:
            time_stats(df)
            station_stats(df)
            travel_time_minutes = trip_duration_stats(df)
            user_stats(df)
            revenue(df, travel_time_minutes)
        elif stat_input == 1:
            time_stats(df)
        elif stat_input == 2:
            station_stats(df)
        elif stat_input == 3:
            travel_time_minutes = trip_duration_stats(df)
        elif stat_input == 4:
            user_stats(df)
        elif stat_input == 5:
            revenue(df, travel_time_minutes)

        restart = input('\nWould you like to restart the program? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
