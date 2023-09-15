# Services subsystem
# Last edited: 15 Sep 2023
# Version 1.0

# import other subsystems
from control import polling_loop
from settings import *
from outputs import graph_temperature


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
    polling_loop(systemSettings["pollingTime"])


def maintenance_adjustment_menu():
    """
    This function prints the menu for the maintenance adjustment menu
    :return: None
    """
    clear_console()
    print("MAINTENANCE ADJUSTMENT MODE LOCKED")
    print("=" * 50)
    print("\n")
    print("The MAINTENANCE ADJUSTMENT MODE requires an access PIN (default: 1234)")
    print("\n")


def system_parameters_menu():
    """
    This function prints the menu for the system parameters menu in the maintenance adjustment menu
    :return: None
    """
    clear_console()
    print("MAINTENANCE ADJUSTMENT MODE - SYSTEM PARAMETERS")
    print("=" * 50)
    print("\n")
    print("You have the following menu options:")
    for i in range(1, len(systemSettings)):
        print("\t" + str(i) + ". Edit " + list(systemSettings)[i])
    print("\t" + str(len(systemSettings)) + ". Return to main menu")
    print("\n")


def edit_system_setting_menu(setting, settingType, settingParameters):
    """
    This function prints the menu for the edit system setting menu
    :return: None
    """

    clear_console()
    print("EDIT SYSTEM PARAMATER - " + setting)
    print("=" * 50)
    print("\n")
    print("Current value: " + str(systemSettings[setting]))
    print("Setting type: " + str(settingType))
    if settingParameters != None:
        print("Allowable setting paramaters: Between " +
              str(settingParameters[0]) + " and " + str(settingParameters[1]))
    else:
        print("Allowable setting paramaters: No parameters")
    print("\n")


def edit_system_setting_main(settingNumber):
    """
    This function handles all program logic for editing a system setting
    :return: None
    """
    setting = list(systemSettings)[settingNumber]
    settingType = type(systemSettings[setting])
    settingParameters = systemSettingsParameters[setting]
    edit_system_setting_menu(setting, settingType, settingParameters)
    while True:
        try:
            userInput = input(
                "Enter a new value or ENTER to go back: ")
            if settingParameters == None and userInput != "":
                if settingType == str:
                    systemSettings[setting] = str(userInput)
                    print("Setting updated.")
                    break
                elif settingType == int:
                    systemSettings[setting] = int(userInput)
                    print("Setting updated.")
                    break
                elif settingType == float:
                    systemSettings[setting] = float(userInput)
                    print("Setting updated.")
                    break
            elif settingParameters != None and userInput != "":
                if settingType == str:
                    systemSettings[setting] = str(userInput)
                    break
                elif settingType == int:
                    if settingParameters[0] <= int(userInput) <= settingParameters[1]:
                        systemSettings[setting] = int(userInput)
                        print("Setting updated.")
                        break
                    else:
                        print("Value is not in required range.")
                elif settingType == float:
                    if settingParameters[0] <= float(userInput) <= settingParameters[1]:
                        systemSettings[setting] = float(userInput)
                        print("Setting updated.")
                        break
                    else:
                        print("Value is not in required range.")
            elif userInput == "":
                break

        except ValueError:
            print(
                "Your input is not of the correct type for this setting. Please enter a " + str(settingType) + ".")


def maintenance_adjustment_main():
    """
    This function handles all program logic related to the maintenance adjustment mode
    :return: None
    """
    maintenance_adjustment_menu()
    while True:
        try:
            userInput = (input(
                "Enter the PIN or '1' to go back: "))
            if userInput == str(systemSettings["maintenancePIN"]):
                system_parameters_menu()
                while True:
                    try:
                        userInput = int(input("Please select a menu option: "))
                        if (0 < userInput < len(systemSettings)):
                            edit_system_setting_main(userInput)
                            system_parameters_menu()
                        elif userInput == len(systemSettings):
                            break
                        else:
                            print("You have not entered a valid menu option!",
                                  "Please try again.")
                    except ValueError:
                        print("Please enter a valid menu option (number)")
                break
            elif userInput == "1":
                break
            else:
                print("The pin is incorrect. Please try again")
        except ValueError:
            print("Please enter a valid four digit PIN (numbers only)")
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
    graph_temperature(temperatureList)
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
