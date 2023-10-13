# Outputs subsystem
# Last edited: 15 Sep 2023
# Version 1.0

# import functions and files
from settings import *
import time
import matplotlib.pyplot as plt


def temperature_led_outputs(temperature: float, goalTempRange: list[float] = [20, 25]):
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
        modeMessage = "TEMP IN RANGE - MODE: IDLE"

    elif temperature < minGoalTemp:
        consoleMessage = 'Ambient temperature is below the goal temperature range, heating ventilation commencing.'
        modeMessage = "TEMP UNDER - MODE: HEATING"
        board.digital_pin_write(ledPinRed, 1)
        board.digital_pin_write(ledSpeedPins[0], 1)
        if abs(temperature - minGoalTemp) > highSpeedDiff:
            board.digital_pin_write(ledSpeedPins[1], 1)

    elif temperature > maxGoalTemp:
        consoleMessage = "Ambient temperature is above the goal temperature range, cooling ventilation commencing."
        modeMessage = "TEMP OVER - MODE: COOLING"
        board.digital_pin_write(ledPinBlue, 1)
        board.digital_pin_write(ledSpeedPins[0], 1)
        if abs(maxGoalTemp - temperature) > highSpeedDiff:
            board.digital_pin_write(ledSpeedPins[1], 1)

    return [modeMessage, consoleMessage]

def thermometer_outputs(temperature: float):

    temperature = 3
    """
    Writes the LEDs for the thermometer. The LEDs use a shift register
    """
    serPin = 19
    srclkPin = 2
    rclkPin = 18
    srclrPin = 5
    oePin = 6

    tempRange = [0,30] # [Min, Max] temperature
    tempRange = [tempRange[0]] + [(tempRange[1]-tempRange[0])*i/7 for i in range(1,8)]
    # Qa is the coldest LED, Qh is the hottest

    bits = []
    for temp in tempRange:
        if temperature > temp:
            bits.append(1)
        else:
            bits.append(0)
    bits = bits[::-1]

    board.digital_pin_write(rclkPin, 0)
    
    clear = [0]*8
    for i in clear:
        board.digital_pin_write(serPin, i)
        board.digital_pin_write(srclkPin, 1)
        board.digital_pin_write(srclkPin, 0)
        board.digital_pin_write(serPin, 0)
    board.digital_pin_write(rclkPin, 1)
    board.digital_pin_write(rclkPin, 0)

    for i in bits:
        board.digital_pin_write(serPin, i)
        board.digital_pin_write(srclkPin, 1)
        board.digital_pin_write(srclkPin, 0)
        board.digital_pin_write(serPin, 0)
    
    board.digital_pin_write(rclkPin, 1)





def graph_temperature(tempList: list[float]):
    """
    Graphs past 20 seconds of thermistor readings
    :param tempList, A list containing recorded temperature values with the latest value at the end
    :return None
    """
    pollingTime = systemSettings.get('pollingTime')
    length = int(20//pollingTime)
    times = [-1*(i*pollingTime) for i in range(length, 0, -1)]

    if len(tempList) < length:
        print('Insufficient data to plot graph. Minimum 20 seconds needed.')
        return
    elif len(tempList) >= length:
        tempList = tempList[-length:]

        plt.figure(1)
        plt.xlabel("Time (s)")
        plt.ylabel("Temperature (C)")
        plt.title("Temperature over past 20 seconds")
        plt.xlim(times[0], times[-1])
        plt.plot(times, tempList)
        figure = plt.gcf()
        plt.show()

    # wait for figure window to close, then save to file
    while True:
        if not plt.fignum_exists(1):
            # get current time for file name
            currentTime = time.strftime(
                '%d-%m-%Y-%H:%M:%S', time.localtime(time.time()))
            fileName = "Graph_" + currentTime
            figure.savefig(fileName)
            break

def temperature_diff(tempList:list[float]) -> float:
    '''
    Prints a console message and sounds a buzzer if the rate of temperature change is of high enough magnitude. Also returns the rate of change when called
    :param tempList, A list containing recorded temperature values with the latest value at the end
    '''
    buzzerPin = 2
    board.set_pin_mode_pwm_output(buzzerPin)
    magnitude = 5 # Max change in one polling loop time before alert triggers
    sample = 3 # How many dT/dt values it samples to get temperature change
    dt = systemSettings.get('pollingTime')
    dT = [tempList[i] - tempList[i-1] for i in range(1,len(tempList))]

    if len(dT) < sample:
        dTdt = [dT/dt for dT in dT] # Calculates dT with what it has if not enough values to sample
    else:
        dT = dT[len(dT)-sample:]
        dTdt = [dT/dt for dT in dT]
    
    dTdt = sum(dTdt)/len(dTdt)

    if dTdt > magnitude:
        print(f'Temperature rapidly increasing! dT/dt = {dTdt: .2f}')
        board.pwm_write(buzzerPin, 110)
    elif dTdt < -magnitude:
        print(f'Temperature rapidly decreasing! dT/dt = {dTdt: .2f}')
        board.pwm_write(buzzerPin, 220)
    else:
        board.pwm_write(buzzerPin, 0)

    return dTdt




def seven_segment_display(currentMessage, currentDigit):
    """
    Displays a four digit static message on the seven segment display
    :param currentMessage (string)
    :return None
    """

    # Set the pins for the 4-digit 7-segment display
    # segmentPins = [18, 16, 19, 3, 2, 17, 4]
    serPin = 3
    rclkPin = 4
    srclkPin = 5
    # Set the common pins for the digits (anodes)
    digitPins = [6, 7, 8, 9]

    # Set the pins as OUTPUT
    for pin in digitPins:
        board.set_pin_mode_digital_output(pin)

    board.set_pin_mode_digital_output(serPin)
    board.set_pin_mode_digital_output(rclkPin)
    board.set_pin_mode_digital_output(srclkPin)

    currentMessage = currentMessage[currentDigit:currentDigit+4]
    
    for digit in range(4):
        char = currentMessage[digit]
        if char in LOOKUP_DICTIONARY:
            segmentData = LOOKUP_DICTIONARY[char][::-1]
            for i in range(7):
                board.digital_write(serPin, int(segmentData[i]))
                board.digital_write(srclkPin, 0)
                board.digital_write(srclkPin, 1)
            board.digital_write(rclkPin, 0)
            board.digital_write(rclkPin, 1)
        # Turn on the selected digit
        board.digital_write(digitPins[digit], 0)
        time.sleep(0.003)
        board.digital_write(digitPins[digit], 1)
    


if __name__ == '__main__':
    tempList = [100 - 5.1*i for i in range(1, 21)]
    print(tempList)
    temperature_diff(tempList)
    graph_temperature(tempList)