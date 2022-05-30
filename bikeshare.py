#Importing the needed packages
import time, datetime, os
import pandas as pd

#Defining global variables
city_name = ""
city_options = ["chicago", "new york", "washington", "all"]
city_data = pd.DataFrame()
user_name = ""

#Defining repetitive functions
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
"""Clears the terminal clutter whenever needed for neat experience"""

def pick_city():
    """
    Asks the user for the required city and handles invalid input.
    Calls a function to retrieve the city data.
    Calls a function to display the main menu.
    """
    global city_name, city_data
    city_name = ""
    clear()

    #Asking the user for the city name until it's recognized
    while not(city_name in city_options):
        print("Ok, {}.".format(user_name))    #Welcome message
        city_name = input("Which city are you interested in: Chicago, New York, Washington, or all of them?\n").lower().replace(" ","")

        if city_name == "newyork":    #Resplitting newyork
            city_name = "new york"

        if "all" in city_name:    #In case the user inputs "all of them" or any other combination with "all"
            city_name = "all"
        if not(city_name in city_options):
            print("\nSorry, we didn't catch your input :(\nLet's try again...\n==========\n\n")

    #Printing feedback on recognition
    print("\nGreat! You selected: '{}'. Let's dive in.\nLoading Data...".format(city_name.title()))

    #If trying to retrieve the city data failed, make sure the csv files are in place
    while not(fill_city_data(city_name).any().any()):
        print("Something went wrong when selecting the files!")
        input("Please make sure you have the right csv files in the same directory of the program and press enter.")
    
    #Retrieving data and displaying main menu
    city_data = fill_city_data(city_name)
    main()    #Go to main menu


def fill_city_data(city):
    """
    Retrieves the selected city data from the csv files,
    sorted according to the first column (got its name by experimenting with python interactive terminal :D).

    Args:
    (str) city - the name of the selected city
    Returns:
    data - the pandas dataframe of the selected city
    """
    data = pd.DataFrame()
    if city == "chicago":
        data = pd.read_csv('chicago.csv').sort_values("Unnamed: 0").reset_index()
    elif city == "new york":
        data = pd.read_csv('new_york_city.csv').sort_values("Unnamed: 0").reset_index()
    elif city == "washington":
        data = pd.read_csv('washington.csv').sort_values("Unnamed: 0").reset_index()
    elif city == "all":
        data = pd.read_csv('chicago.csv').append(pd.read_csv('new_york_city.csv').append(pd.read_csv('washington.csv'))).sort_values("Unnamed: 0").reset_index()
    return data

def explore_raw_data():
    """
    Asks which data are required and handles invalid input.
    Only breaks and returns to the main menu if "back" is in the user's input.
    """
    clear()

    while True:
        display_rawdata_request = input("\nWhich data would you like to explore?\nExpected kind of input: 'first 5', 'last 2', 'all', or 'back'. You can pick the numbers you want of course!\n\n")
        display_rawdata_request = display_rawdata_request.strip().split()

        try:
            if "back" in display_rawdata_request[0]:
                break
            elif "all" in display_rawdata_request[0]:
                print(city_data)
            elif display_rawdata_request[0] == "first":
                if int(display_rawdata_request[1]) > 0:
                    print(city_data.head(int(display_rawdata_request[1])))
                else:
                    print("What do you mean by {} :)\nPlease type a valid number".format(display_rawdata_request[1]))
            elif display_rawdata_request[0] == "last":
                if int(display_rawdata_request[1]) > 0:
                    print(city_data.tail(int(display_rawdata_request[1])))
                else:
                    print("What do you mean by {} :)\nPlease type a valid number".format(display_rawdata_request[1]))
            else:
                print("\nHmm.. Did you type 'first', 'last', 'all' or 'back' in your input? Make sure you're typing like we explained.")
        except:
            input("Oops! Either the csv file has no enough cells, or you didn't type like how we are expecting.\nPress enter to go back.\n")

    main()

def explore_time_stats():
    """

    """
    #Preprocessing: mapping the start times in city data to datetime, defining weekdays and months
    clear()
    print("Loading times...")
    start_times_in_datetime = city_data["Start Time"].map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    weekdays = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}

    #Displaying the options menu until the back option is chosen
    while True:
        option=""
        clear()

        #Making sure the input is among the listed options
        while not(option in ["1", "2", "3", "4"]):
            option = input("So, {}, you would like to explore statistics related to times of travel in {} city(ies).\
                \nWhat operation would you like to perform?\n1. Calcualte the most common months.\
                    \n2. Calcluate the most common days of week.\n3. Calucualte the most common hours of day.\
                        \n4. Back to the main menu.\n=========\n".format(user_name, city_name.title()))
            if not(option in ["1", "2", "3", "4"]):
                print("\nLooks like you picked an option that's not listed. Please try again.\n\n")

        try:
            if option == "1":
                #Preprocessing: mapping the datetimes to months and month instances
                month_rank = ""
                print("Loading months...")
                months_counts = pd.DataFrame(start_times_in_datetime.map(lambda x: x.month).to_list(), columns=["Month"]).value_counts("Month")
                clear()

                #Asking for which month is required, handling errors, and calculating statistics
                while not(month_rank.isnumeric()):
                    month_rank = input("What month rank would you like to know?\nType 1 for the most popular month, 2 for the 2nd most popular, etc.\nType back to return to the previous menu.\n==========\n")
                    if "back" in month_rank:
                        break
                    elif month_rank.isnumeric:
                        month_rank = int(month_rank)-1
                        if months_counts.index.max()-1 >= month_rank >= months_counts.index.min()-1:
                            start_time = time.time()
                            print("The month of rank #{} is: {}, and counts {} time(s).".format(month_rank+1, months[months_counts.index[month_rank]], months_counts.iloc[month_rank]))
                            print("That took: {} second(s) to calculate.".format(round(time.time() - start_time, 3)))
                            input("Press enter to continue.\n\n")
                        else:
                            print("There is no month in the database ranking that.\nPlease try again.\n")
                    else:
                        input("Looks like you entered an invalid input. Press enter to go back.\n")
                    month_rank = ""

            elif option == "2":
                #Preprocessing: mapping the datetimes to isoweekdays and isoweekdays instances
                day_rank = ""
                print("Loading days...")
                day_of_week_counts = pd.DataFrame(start_times_in_datetime.map(lambda x: x.isoweekday()).to_list(), columns=["Week Day"]).value_counts("Week Day")
                clear()

                #Asking for which isoweekday is required, handling errors, and calculating statistics
                while not(day_rank.isnumeric()):
                    day_rank = input("What month rank would you like to know?\nType 1 for the most popular month, 2 for the 2nd most popular, etc.\nType back to return to the previous menu.\n==========\n")
                    if "back" in day_rank:
                        break
                    elif day_rank.isnumeric:
                        day_rank = int(day_rank)-1
                        if months_counts.index.max()-1 >= day_rank >= months_counts.index.min()-1:
                            start_time = time.time()
                            print("The month of rank #{} is: {}, and counts {} time(s).".format(day_rank+1, weekdays[day_of_week_counts.index[day_rank]], day_of_week_counts.iloc[day_rank]))
                            print("That took: {} second(s) to calculate.".format(round(time.time() - start_time, 3)))
                            input("Press enter to continue.\n\n")
                        else:
                            print("There is no month in the database ranking that.\nPlease try again.\n")
                    else:
                        print("Looks like you entered an invalid input. Please try again.\n")
                    day_rank = ""
                    
            elif option == "3":
                #Preprocessing: mapping the datetimes to hours and hour instances
                hour_rank = ""
                print("Loading hours...")
                hour_of_day_counts = pd.DataFrame(start_times_in_datetime.map(lambda x: x.hour).to_list(), columns=["Hour"]).value_counts("Hour")
                clear()

                #Asking for which hour is required, handling errors, and calculating statistics
                while not(hour_rank.isnumeric()):
                    hour_rank = input("What hour rank would you like to know?\nType 1 for the most popular hour, 2 for the 2nd most popular, etc.\nType back to return to the previous menu.\n==========\n")
                    if "back" in hour_rank:
                        break
                    elif hour_rank.isnumeric():
                        hour_rank = int(hour_rank)-1
                        if hour_of_day_counts.index.max() >= hour_rank >= hour_of_day_counts.index.min():
                            start_time = time.time()
                            print("The hour of rank #{} is: {}, and counts {} time(s).".format(hour_rank+1, hour_of_day_counts.index[hour_rank], hour_of_day_counts.iloc[hour_rank]))
                            print("That took: {} second(s) to calculate.".format(round(time.time() - start_time, 3)))
                            input("Press enter to continue.\n\n")
                        else:
                            print("There is no hour in the database ranking that.\nPlease try again.\n")
                    else:
                        print("Looks like you entered an invalid input. Please try again.\n")
                    hour_rank = ""

            elif option == "4":
                #When back option is chosen, break to go back to the main menu
                break
            else:
                print("\nHmm.. Did you type 'first', 'last', 'all' or 'back' in your input? Make sure you're typing like we explained.")
        except:
            input("Oops! Either the csv file has no enough cells, or you didn't type like how we are expecting.\nPress enter to go back\n")

    main()


def explore_station_stats():
    """
    Diaplays a menu for different station and trip stats options.
    Calculates the statistics according to the chosen option.
    """
    #Asking the user for an option, until a valid option is chosen.
    while True:
        option=""
        clear()
        while not(option in ["1", "2", "3", "4"]):
            option = input("So, {}, you would like to explore statistics related to start and end stations in {} city(ies).\
                \nWhat operation would you like to perform?\n1. Calcualte the most common start stations.\
                \n2. Calcluate the most common end stations.\n3. Calucualte the most common trips.\
                \n4. Back to the main menu.\n==========\n".format(user_name, city_name.title()))
            if not(option in ["1", "2", "3", "4"]):
                print("\nLooks like you picked an option that's not listed. Please try again.\n\n")

        try:
            if option == "1":
                #Asking which start station is required, calculating and displaying the required statistics
                clear()

                while True:
                    station_rank = input("Ok. Which station rank would you like to know now?\nType 1 for the most common start station, 2 for the 2nd most common, etc.\nType back to go the previous menu.\n==========\n")
                    if "back" in station_rank:
                        break
                    elif station_rank.isnumeric:
                        station_rank = int(station_rank) - 1
                        if station_rank >= 0:
                            start_time = time.time()
                            start_station_and_count = (city_data["Start Station"].value_counts()[[station_rank]].index[0], city_data["Start Station"].value_counts()[station_rank])
                            print("The start station ranked #{} is '{}', and it counts ({}) time(s).".format(station_rank+1, *start_station_and_count))
                            print("That took: {} seconds to calculate.\n==========\n".format(round(time.time() - start_time, 3)))
                        else:
                            print("What do you mean by {} :)\nPlease type a positive number".format(station_rank+1))
                    else:
                        print("It looks like your input is not a valid number and doesn't say back.\nPlease try again.")

            elif option == "2":
                #Asking which end station is required, calculating and displaying the required statistics
                clear()

                while True:
                    station_rank = input("Ok. Which station rank would you like to know now?\nType 1 for the most common end station, 2 for the 2nd most common, etc.\nType back to go the previous menu.\n")
                    if "back" in station_rank:
                        break
                    elif station_rank.isnumeric:
                        station_rank = int(station_rank) - 1
                        if station_rank >= 0:
                            start_time = time.time()
                            end_station_and_count = (city_data["End Station"].value_counts()[[station_rank]].index[0], city_data["End Station"].value_counts()[station_rank])
                            print("The end station ranked #{} is '{}', and it counts ({}) time(s).".format(station_rank+1, *end_station_and_count))
                            print("That took: {} seconds to calculate.\n==========\n".format(round(time.time() - start_time, 3)))
                        else:
                            print("What do you mean by {} :)\nPlease type a positive number".format(station_rank+1))
                    else:
                        print("It looks like your input is not a valid number and doesn't say back.\nPlease try again.")

            elif option == "3":
                #Asking which trip is required, calculating and displaying the required statistics
                clear()

                trips_sorted = city_data.groupby(["Start Station", "End Station"]).size().sort_values(ascending=False)
                while True:
                    trip_rank = input("Ok. Which trip rank would you like to know now?\nType 1 for the most common trip, 2 for the 2nd most common, etc.\nType back to go the previous menu.\n")
                    if "back" in trip_rank:
                        break
                    elif trip_rank.isnumeric:
                        trip_rank = int(trip_rank) - 1
                        if trip_rank >= 0:
                            start_time = time.time()
                            trip_start_end_count = (*trips_sorted.index[trip_rank], trips_sorted[trip_rank])
                            print("The trip ranked #{} is '{}' to '{}', and it counts ({}) time(s).".format(trip_rank+1, *trip_start_end_count))
                            print("That took: {} seconds to calculate.\n==========\n".format(round(time.time() - start_time, 3)))
                        else:
                            print("What do you mean by {} :)\nPlease type a positive number".format(trip_rank+1))
                    else:
                        print("It looks like your input is not a valid number and doesn't say back.\nPlease try again.")

            elif option == "4":
                #When the back option is chosen, break to go back to the main menu.
                break

            else:
                #Alerts the user for an invalid input
                print("\nAre you sure you chose a number corresponding to a listed option?")

        except:
            input("Oops! Either the csv file has no enough cells, or you didn't type like how we are expecting.\nPress enter to go back.\n")

    main()

def explore_duration_stats():
    """Calculates and displays simple statistics on the trip durations: Average, Total, Maximum, and Minimum."""
    clear()
    start_time = time.time()

    print("Here are interesting statistics on trip durations:")
    print("Average travel time: {}.".format(str(datetime.timedelta(seconds=city_data["Trip Duration"].mean()))))
    print("Total travel time: {}.".format(str(datetime.timedelta(seconds=float(city_data["Trip Duration"].sum())))))
    print("Maximum travel time: {}.".format(str(datetime.timedelta(seconds=city_data["Trip Duration"].max()))))
    print("Minimum travel time: {}.".format(str(datetime.timedelta(seconds=city_data["Trip Duration"].min()))))
    print("\nThat took {} seconds to calculate.\n".format(round(time.time() - start_time, 3)))

    input("Press enter to return to the main menu.")

    main()

def explore_user_stats():
    """
    Calculates and prints the user statistics: "User Type" in all cities, "Gender", "Birth Date" in Chicago and NYC only.
    """
    clear()

    #Calculating and printing the counts of each user type
    start_time = time.time()
    print("Here are some interesting statistics in {} city(ies):".format(city_name))
    user_types = city_data.groupby("User Type").size().sort_values(ascending=False)
    for i in range(len(user_types)):
        print("No. of {} users = {}".format(user_types.index[i], user_types[i]))

    #The 
    if city_name == "chicago" or city_name == "new york":
        print()

        #Calculating and printing the counts of each gender
        user_genders = city_data.dropna().groupby("Gender").size().sort_values(ascending=False)
        for i in range(len(user_genders)):
            print("No. of {} users = {}".format(user_genders.index[i], user_genders[i]))
        print()

        #Calculating and printing the statistics of ages
        print("The earliest year of birth is: {}".format(city_data.dropna().sort_values("Birth Year").reset_index()["Birth Year"].iloc[0]))
        print("The most recent year of birth is: {}".format(city_data.dropna().sort_values("Birth Year").reset_index()["Birth Year"].iloc[-1]))
        year_of_birth_frequencies = city_data.groupby("Birth Year").size().sort_values(ascending=False)
        print("The most frequent year of birth is: {}, which counts {} time(s).".format(year_of_birth_frequencies.index[0], year_of_birth_frequencies.iloc[0]))

    print("\nThat took {} seconds to calculate.\n".format(round(time.time() - start_time, 3)))

    input("Press enter to go back to the main menu.")

    main()


def exit_program_nicely():
    """
    Exits the program with a 'thank you' message.
    Used when the program exits in the legitimate way.
    """
    print("Thank you for using our program. We hope it gave you useful insights.\nGoodbye!\n")
    exit()

def main():
    """
    This function is the axis of the program flow.
    It lists the available options to the user whenever needed, and call the relevant functions on the right selections.
    """
    #Declaring the global variable to be used anywhere else
    global city_name
    option=""
    clear()

    #Lists the different sections of the program, handles invalid input, and calls the relevant function to the chosen section.
    while not(option in ["1", "2", "3", "4", "5", "6", "7"]):
        option = input("Here is a bunch of things you can do with {} data. \
            --Type the corresponding number to choose the operation you want.\
                \n1. Explore some raw data.\n2. Explore statistics on times of traveling.\
                \n3. Explore statistics on stations.\n4. Explore statistics on journey durations.\
                \n5. Explore statistics on users.\n6. Back to choosing the city.\
                \n7. Exit the program.\n==========\n".format(city_name.title()))
        if not(option in ["1", "2", "3", "4", "5", "6", "7"]):
            print("\nLooks like you picked an option that's not listed. Please try again.\n\n")
        elif option == "1":
            explore_raw_data()
        elif option == "2":
            explore_time_stats()
        elif option == "3":
            explore_station_stats()
        elif option == "4":
            explore_duration_stats()
        elif option == "5":
            explore_user_stats()
        elif option == "6":
            pick_city()
        elif option == "7":
            exit_program_nicely()



def initiate():
    """
    This function is initiated when the program starts.
    It starts the program flow and asks for the user name.
    """
    global user_name
    clear()

    #Introducing the user to the program
    print("Welcome to Motivate's bike share system!\nThis program introduces you to the bikeshare data in New York, Chicago, and Washington. Get ready to unleash the power of data.")

    #Being friendly and asking for user's name
    user_name = input("What's your name? (leave empty for default: User)\n")
    if user_name.replace(" ", "") == "":
        user_name = "User"

    #Directing the user to choose the city
    pick_city()
    

#Initiating the program, handling keyboard interrupt, and printing unexpected exceptions.
if __name__ == "__main__":
    try:
        initiate()
    except KeyboardInterrupt:
        print("\nSorry if you're facing problems with the program :(\nExitting...\n\n")
        exit()
    except Exception as e:
        print("Hmm... It seems that the program encoutered an unknown error.\nExitting...\n\n")
        print(e)
        exit()

