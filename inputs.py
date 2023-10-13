# Inputs subsystem
# Last edited: 13 Oct 2023
# Version 1.0

# import functions and files
from settings import *
import math


def poll_thermistor():
    """
    This function retrieves data from the thermistor input
    :return rawData (int)
    """

    thermistorPin = 0

    # initialise pins as inputs/outputs
    board.set_pin_mode_analog_input(thermistorPin)  # thermistor input

    rawThermistorData = board.analog_read(thermistorPin)[0]
    # print("Raw thermistor data has been retrieved.")
    return rawThermistorData


def thermistor_processing(rawThermistorData):
    """
    This function converts the resistance measurements from the thermistor into temperature measurements
    :param rawData (int)
    :return temperature (float)
    """

    try:
        voltageIn = 5  # voltage supply
        resistor1 = 10000  # resistor in series with thermistor (Ohms)

        # calculating the resistance of the thermistor
        # print(f"Raw thermistor value (analog): {rawThermistorData}")
        voltageOut = rawThermistorData * (voltageIn/1023)
        # print(f"Voltage Out: {voltageOut}")
        resistance = (resistor1 * voltageOut) / (voltageIn - voltageOut)
        # print(f"Resistance: {resistance}")

        # converting the resistance to temperature
        temperature = -9*(resistance/1000) + 125
    except ValueError:
        temperature = 0
    except ZeroDivisionError:
        temperature = 0

    # print("Thermistor data has been processed and now returning temperature measurement.")
    return temperature


def poll_button():
    """
    This function retrieves data from the button input
    :return 
    """

    buttonPin = 15
    board.set_pin_mode_digital_input(buttonPin)

    # to generate a single trigger per press of button
    if (board.digital_read(buttonPin)[0] == 1):
        while True:
            if (board.digital_read(8)[0] == 0):
                return ("PUSH")
            
def poll_ldr():
    """
    This function retrieves data from the ldr input
    :return 
    """

    ldrPin = 0

    # initialise pins as inputs/outputs
    board.set_pin_mode_analog_input(ldrPin)  # ldr input

    rawLDRData = board.analog_read(ldrPin)[0]

    return rawLDRData
