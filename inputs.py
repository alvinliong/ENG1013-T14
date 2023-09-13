# Inputs subsystem
# Last edited: 30 Aug 2023
# Version 1.0

# import functions and files
from settings import *
import math


def poll_thermistor():
    """
    This function retrieves data from the thermistor input
    :return rawData (int)
    """

    # initialise pins as inputs/outputs
    board.set_pin_mode_analog_input(1)  # thermistor input

    rawThermistorData = board.analog_read(1)[0]
    print("Raw thermistor data has been retrieved.")
    return rawThermistorData


def thermistor_processing(rawThermistorData):
    """
    This function converts the resistance measurements from the thermistor into temperature measurements
    :param rawData (int)
    :return temperature (float)
    """

    voltageIn = 5  # voltage supply
    resistor1 = 10000  # resistor in series with thermistor (Ohms)

    # calculating the resistance of the thermistor
    print(f"Raw thermistor value (analog): {rawThermistorData}")
    voltageOut = rawThermistorData * (voltageIn/1023)
    print(f"Voltage Out: {voltageOut}")
    resistance = (resistor1 * voltageOut) / (voltageIn - voltageOut)
    print(f"Resistance: {resistance}")

    # converting the resistance to temperature
    try:
        temperature = -21.21*math.log(resistance/1000) + 72.203
    except ValueError:
        temperature = 0

    print("Thermistor data has been processed and now returning temperature measurement.")
    return temperature
