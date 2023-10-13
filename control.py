# Control subsystem
# Last edited: 15 Sep 2023
# Version 1.0

# import functions and files
from settings import *
from outputs import temperature_led_outputs, seven_segment_display, thermometer_outputs, temperature_diff
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
    global digitShiftTimeStart
    digitShiftTimeStart = time.time()

    loopTimeStart = time.time()
    modeMessage = "    "
    currentTemperature = 0
    filteredTemperature = 0
    lastTempValues = []
    scrollSpeed = 0.5 
    print("Press CRTL+C at any time to exit the NORMAL OPERATION MODE")

    while True:
        try:
            # outputs LEDs based on temperature
            modeMessage, consoleMessage = temperature_led_outputs(
                filteredTemperature)
        
            thermometer_outputs(filteredTemperature)
            
             # add extra space for 4+ character message to loop clearly
            if len(modeMessage) > 4:
                modeMessage = "  " + modeMessage + "  "
            
            
            digitShiftTimer = time.time() - digitShiftTimeStart
            currentDigit = round(digitShiftTimer/scrollSpeed) 
            if (digitShiftTimer/scrollSpeed > len(modeMessage) - 4):
                digitShiftTimeStart = time.time()

            # prints current mode to seven segment display
            seven_segment_display(modeMessage, currentDigit)

            # collects the raw thermistor data
            rawThermistorData = poll_thermistor()

            # detect rapid change
            # temperature_diff(temperatureList)

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
