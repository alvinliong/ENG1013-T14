# Control subsystem
# Last edited: 30 Aug 2023
# Version 1.0

from settings import *
from outputs import temperature_led_outputs, seven_segment_display
from inputs import thermistor_processing, poll_thermistor
import time


# import functions and files


def polling_loop(pollingTime):
    """
    This function constantly polls the thermistor sensor for data until stopped by user
    :return print statements (as of now)
    :param: polling_time (secs) (float)
    """

    while True:
        # Run seven segment display
        try:
            print("Press CRTL+C at any time to exit the NORMAL OPERATION MODE")
            print("--- Polling time: " + str(pollingTime) + " secs ---")
            print("--- Starting polling cycle ---")

            # starts the polling loop timer
            startPollingTime = time.time()

            # collects the raw thermistor data
            rawThermistorData = poll_thermistor()

            # processes the thermistor data
            currentTemperature = thermistor_processing(rawThermistorData)
            print(f"Temperature: {currentTemperature}")

            # sends temperature data to LEDs
            temperature_led_outputs(currentTemperature)

            # add polling delay
            time.sleep(pollingTime)

            seven_segment_display("COOL")  # testing (still being worked on)

            print("--- Ending polling cycle ---")

            print("--- Total polling loop cycle duration: %s seconds ---" %
                  (time.time() - startPollingTime))

            print()

        except KeyboardInterrupt:
            print("Polling loop has ended. Exiting NORMAL OPERATION MODE")
            print()
            break
