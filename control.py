# Control subsystem
# Last edited: 30 Aug 2023
# Version 1.0

import time

# import other subsystems
from inputs import thermistor_processing, thermistor
from outputs import outputs


def polling_loop():
    """
    This function constantly polls the thermistor sensor for data until stopped by user
    :return print statements (as of now)
    """

    while True:
        try:
            print("Press CRTL+C at any time to exit the NORMAL OPERATION MODE")
            print("--- Starting polling cycle ---")

            # starts the polling loop timer
            start_polling_time = time.time()

            # collects the raw thermistor data
            thermistor()

            # processes the thermistor data
            thermistor_processing("data placeholder")

            # sends temperature data to outputs
            outputs()

            print("--- Ending polling cycle ---")
            # this delay has been added to show the duration of the polling loop in practice
            time.sleep(2)
            print("--- Total polling loop cycle duration: %s seconds ---" %
                  (time.time() - start_polling_time))

            print()

        except KeyboardInterrupt:
            print("Polling loop has ended. Exiting NORMAL OPERATION MODE")
            print()
            break
