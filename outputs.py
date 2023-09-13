# Outputs subsystem
# Last edited: 11 Sep 2023
# Version 1.0

# import functions and files
from settings import *
import time


def temperature_led_outputs(temperature: int, goalTempRange: list[float] = [20, 25]) -> None:
    """
    This function triggers several outputs based on the inputted temperature

    NOTE:
        There isn't any condition on how ventilation speed should be controlled that I could find.
        For now I have set it so that differences in temperature greater than 10 degrees above/below
        the temperature range will trigger a high ventilation speed.

        I have also left an unused boolean variable highSpeed to use if you want to set high ventilation
        manually within the function code. To use it, replace (temperature - minGoalTemp) > highSpeedDiff
        and the other highSpeedDiff check with just highSpeed.

    :param board, The arduino board on which the LED ouputs are sent to
    :param temperature(int), The temperature reading(C) from the thermistor processing
    :param goalTempRange(list[float]), The range covering the goal temperature. 
    Arranged as [Minimum, Maximum]. Has a default value of 20 to 25 degrees(C)

    :return modeMessage, consoleMessage
    """

    # These are the pin values, change them if needed
    ledPinRed = 13
    ledPinBlue = 12
    ledSpeedPins = [10, 11]  # [Low speed LED, High speed LED]

    # Temperature difference to trigger high ventilation speed.
    highSpeedDiff = 10

    highSpeed = True  # See note

    minGoalTemp = goalTempRange[0]
    maxGoalTemp = goalTempRange[1]

    board.set_pin_mode_digital_output(ledPinBlue)
    board.set_pin_mode_digital_output(ledPinRed)
    for pin in ledSpeedPins:
        board.set_pin_mode_digital_output(pin)

    # Initally switch off all LEDs for a new polling cycle
    board.digital_pin_write(ledPinBlue, 0)
    board.digital_pin_write(ledPinRed, 0)
    for pin in ledSpeedPins:
        board.digital_pin_write(pin, 0)

    if temperature >= minGoalTemp and temperature <= maxGoalTemp:
        consoleMessage = "Ambient temperature is within the goal temperature range."
        modeMessage = "IDLE"

    elif temperature < minGoalTemp:
        consoleMessage = 'Ambient temperature is below the goal temperature range, heating ventilation commencing.'
        modeMessage = "HEAT"
        board.digital_pin_write(ledPinRed, 1)
        board.digital_pin_write(ledSpeedPins[0], 1)
        if abs(temperature - minGoalTemp) > highSpeedDiff:
            board.digital_pin_write(ledSpeedPins[1], 1)

    elif temperature > maxGoalTemp:
        consoleMessage = "Ambient temperature is above the goal temperature range, cooling ventilation commencing."
        modeMessage = "COOL"
        board.digital_pin_write(ledPinBlue, 1)
        board.digital_pin_write(ledSpeedPins[0], 1)
        if abs(maxGoalTemp - temperature) > highSpeedDiff:
            board.digital_pin_write(ledSpeedPins[1], 1)

    return [modeMessage, consoleMessage]


def seven_segment_display(currentMessage):

    # Set the pins for the 4-digit 7-segment display
    segmentPins = [6, 8, 4, 3, 2, 7, 5]
    # Set the common pins for the digits (anodes)
    digitPins = [16, 17, 18, 19]

    # Set the pins as OUTPUT
    for pin in segmentPins + digitPins:
        board.set_pin_mode_digital_output(pin)

    # Display the message
    for digit in range(4):
        char = currentMessage[digit]
        if char in LOOKUP_DICTIONARY:
            segmentData = LOOKUP_DICTIONARY[char]
            for i in range(7):
                board.digital_write(segmentPins[i], int(segmentData[i]))
        # Turn on the selected digit
        board.digital_write(digitPins[digit], 0)
        time.sleep(0.0025)
        board.digital_write(digitPins[digit], 1)
