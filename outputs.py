# Outputs subsystem
# Last edited: 11 Sep 2023
# Version 1.0

from pymata4 import pymata4

def temperature_outputs(board, temperature: int, goalTempRange: list[float] = [20,25]) -> None:
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
    
    :return None
    """
    
    # These are placeholder values, change them if needed
    ledPinRed = 4
    ledPinBlue = 3
    ledSpeedPins = [5,6] # [Low speed LED, High speed LED]
    highSpeedDiff = 10 # Temperature diffrence to tigger high ventilation speed.

    highSpeed = True # See note

    minGoalTemp = goalTempRange[0]
    maxGoalTemp = goalTempRange[1]

    board.set_pin_mode_digital_output(ledPinBlue)
    board.set_pin_mode_digital_output(ledPinRed)
    for pin in ledSpeedPins:
        board.set_pin_mode_digital_output(pin)

    # Initally switch off all LEDs for a new polling cycle
    board.digital_pin_write(ledPinBlue,0)
    board.digital_pin_write(ledPinRed,0)
    for pin in ledSpeedPins:
        board.digital_pin_write(pin,0)

    if temperature >= minGoalTemp and temperature <= maxGoalTemp:
        print("Ambient temperature is within the goal temperature range.")
    
    elif temperature < minGoalTemp:
        print('Ambient temperature is below the goal temperature range, heating ventilation commencing.')
        board.digital_pin_write(ledPinRed,1)
        board.digital_pin_write(ledSpeedPins[0],1)
        if (temperature - minGoalTemp) > highSpeedDiff:
            board.digital_pin_write(ledSpeedPins[1],1)
    
    elif temperature > maxGoalTemp:
        print("Ambient temperature is above the goal temperature range, cooling ventilation commencing.")
        board.digital_pin_write(ledPinBlue,1)
        board.digital_pin_write(ledSpeedPins[0],1)
        if (maxGoalTemp - temperature) > highSpeedDiff:
            board.digital_pin_write(ledSpeedPins[1],1)

    return

# Test code
if __name__ == '__main__':
    board = pymata4.Pymata4()

