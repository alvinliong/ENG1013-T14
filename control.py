# Control subsystem
# Last edited: 15 Sep 2023
# Version 1.0

# import functions and files
from settings import *
from outputs import temperature_led_outputs, seven_segment_display
from inputs import thermistor_processing, poll_thermistor
import time


def polling_loop(pollingTime):
    """
    This function begins the polling loop until exited via CTRL C. 
    The seven-segment display and LEDs are constantly updated at a high frequency,
    however, the thermistor is only polled at a rate per the pollingTime
    :return print statements
    :param: polling_time (secs) (float)
    """
    global temperatureList

    loopTimeStart = time.time()
    modeMessage = "    "
    currentTemperature = 0
    filteredTemperature = 0
    lastTempValues = []
    print("Press CRTL+C at any time to exit the NORMAL OPERATION MODE")

    while True:
        try:
            # outputs LEDs based on temperature
            modeMessage, consoleMessage = temperature_led_outputs(
                filteredTemperature)

            # prints current mode to seven segment display
            seven_segment_display(modeMessage)

            # collects the raw thermistor data
            rawThermistorData = poll_thermistor()

            # processes the thermistor data and converts to temperature
            currentTemperature = thermistor_processing(rawThermistorData)
            temperatureList.append(currentTemperature)

            # collects all temperature values in past second
            lastTempValues.append(currentTemperature)

            # if number of seconds has elapsed acoording to polling time, poll sensor for an update
            if (abs(loopTimeStart - time.time()) >= systemSettings["pollingTime"]):

                filteredTemperature = sum(lastTempValues) / len(lastTempValues)

                print("--- Polling time: " + str(pollingTime) + " secs ---")
                print("--- Starting polling cycle ---\n")

                # print average temperature
                print(f"Temperature: {filteredTemperature}")

                # clear last temp values
                lastTempValues = []

                # prints mode the HVAC is currently in (heat/cool/idle)
                print(consoleMessage)

                print("\n--- Ending polling cycle ---")
                print("--- Total polling loop cycle duration: %s seconds ---\n" %
                      (time.time() - loopTimeStart))

                # resets loop stopwatch
                loopTimeStart = time.time()

        except KeyboardInterrupt:
            print("Polling loop has ended. Exiting NORMAL OPERATION MODE")
            print()
            break
