# Control subsystem
# Last edited: 30 Aug 2023
# Version 1.0

import time

# import other subsystems
from inputs import thermistor_processing, poll_thermistor
from outputs import temperature_outputs


def polling_loop(pollingTime):
    """
    This function constantly polls the thermistor sensor for data until stopped by user
    :return print statements (as of now)
    :param: polling_time (secs) (float)
    """

    while True:
        try:
            print("Press CRTL+C at any time to exit the NORMAL OPERATION MODE")
            print("--- Polling time: " + str(pollingTime) + " secs ---")
            print("--- Starting polling cycle ---")

            # starts the polling loop timer
            startPollingTime = time.time()

            # collects the raw thermistor data
            rawThermistorData = poll_thermistor()

            # processes the thermistor data
            print(f"Temperature: {thermistor_processing(rawThermistorData)}")

            # sends temperature data to outputs
            temperature_outputs()

            print("--- Ending polling cycle ---")
            # this delay has been added to show the duration of the polling loop in practice
            time.sleep(pollingTime)
            print("--- Total polling loop cycle duration: %s seconds ---" %
                  (time.time() - startPollingTime))

            print()

        except KeyboardInterrupt:
            print("Polling loop has ended. Exiting NORMAL OPERATION MODE")
            print()
            break
