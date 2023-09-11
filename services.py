# Services subsystem
# Last edited: 30 Aug 2023
# Version 1.0

# import other subsystems
from control import polling_loop

# set initial user defined variables
pollingTime = 1.0


def clear_console():
    """
    Prints empty lines to clear the console
    :return: None
    """
    print("\n")
    print("=" * 50)


def main_menu():
    """
    This function prints all the operation modes available to select in the main menu
    :return: None
    """
    clear_console()
    print("HVAC SYSTEM MAIN MENU")
    print("=" * 50)
    print("\n")
    print("You have the following modes to select from:")
    print("\t1. NORMAL OPERATION MODE")
    print("\t2. MAINTENANCE ADJUSTMENT MODE")
    print("\t3. DATA OBSERVATION MODE")
    print("\t4. SHUT DOWN SYSTEM")
    print("\n")


def normal_operation_main():
    """
    This function handles all program logic related to the normal operation mode
    :return: None
    """
    clear_console()
    print("NORMAL OPERATION MODE")
    print("=" * 50)
    print("\n")
    polling_loop(pollingTime)


def maintenance_adjustment_menu():
    """
    This function prints the menu for the maintenance adjustment menu
    :return: None
    """
    clear_console()
    print("MAINTENANCE ADJUSTMENT MODE LOCKED")
    print("=" * 50)
    print("\n")
    print("The MAINTENANCE ADJUSTMENT MODE requires an access PIN (1234 for now)")
    print("\n")


def system_parameters_menu():
    """
    This function prints the menu for the system parameters menu in the maintenance adjustment menu
    :return: None
    """
    clear_console()
    print("MAINTENANCE ADJUSTMENT MODE - ACCESS GRANTED")
    print("=" * 50)
    print("\n")
    print("You have the following menu options:")
    print("\t1. Edit system parameter 1")
    print("\t2. Edit system parameter 2")
    print("\t3. Return to the main menu.")
    print("\n")


def maintenance_adjustment_main():
    """
    This function handles all program logic related to the maintenance adjustment mode
    :return: None
    """
    maintenance_adjustment_menu()
    while True:
        userInput = input(
            "Enter the PIN or '1' to go back: ")
        if userInput == "1234":
            system_parameters_menu()
            while True:
                userInput = input("Please select a menu option: ")
                if (userInput == "1" or userInput == "2"):
                    print("System parameter edited.")
                    break
                elif userInput == "3":
                    break
                else:
                    print("You have not entered a valid menu option!",
                          "Please try again.")
            break
        elif userInput == "1":
            break
        else:
            print("The pin is incorrect. Please try again")
    print("Exiting MAINTENANCE ADJUSTMENT MODE")


def data_observation_menu():
    """
    This function prints the menu for the data observation menu
    :return: None
    """
    clear_console()
    print("DATA OBSERVATION MODE")
    print("=" * 50)
    print("\n")
    print("Graphing data not available yet.")
    print("\n")
    print("You have the following menu options:")
    print("\t1. Return to main menu")
    print("\n")


def data_observation_main():
    """
    This function handles all program logic related to the data observation mode
    :return: None
    """
    data_observation_menu()
    while True:
        userInput = input("Please enter a menu option: ")
        if userInput == "1":
            break
        else:
            print("You have not entered a valid menu option!",
                  "Please try again.")
    print("Exiting DATA OBSERVATION MODE")


def main():
    """
    This function handles all program logic related to the main menu.
    :return: None
    """

    while True:
        # Print the mode options
        main_menu()
        menuInput = input("Please enter a menu option: ")

        if menuInput == "1":
            normal_operation_main()
        elif menuInput == "2":
            maintenance_adjustment_main()
        elif menuInput == "3":
            data_observation_main()
        elif menuInput == "4":
            print("Shutting down HVAC System.")
            break
        else:
            # Invalid input option
            print("You have not selected a valid mode!",
                  "Please try again.")


if __name__ == "__main__":
    main()      # Execute the main() function if this file is run
