from pymata4 import pymata4
import time

# Define the lookup dictionary
lookupDictionary = {
    "0": "1111110",
    "1": "0110000",
    "2": "1101101",
    "3": "1111001",
    "4": "0110011",
    "5": "1011011",
    "6": "1011111",
    "7": "1110000",
    "8": "1111111",
    "9": "1110011",
    "A": "1110111",
    "B": "0011111",
    "C": "1001110",
    "D": "0111101",
    "E": "1001111",
    "F": "1000111",
    "G": "1011110",
    "H": "0110111",
    "I": "0110000",
    "J": "0111000",
    "K": "0010111",
    "L": "0001110",
    "M": "0110111",
    "N": "0010101",
    "O": "1111110",
    "P": "1100111",
    "Q": "1111111",
    "R": "1110111",
    "S": "1011011",
    "T": "0001111",
    "U": "0111110",
    "V": "0111110",
    "W": "0110111",
    "X": "0110111",
    "Y": "0110011",
    "Z": "1101101",
    "a": "1110111",
    "b": "0011111",
    "c": "1001110",
    "d": "0111101",
    "e": "1001111",
    "f": "1000111",
    "g": "1011110",
    "h": "0110111",
    "i": "0110000",
    "j": "0111000",
    "k": "0010111",
    "l": "0001110",
    "m": "0110111",
    "n": "0010101",
    "o": "1111110",
    "p": "1100111",
    "q": "1111111",
    "r": "1110111",
    "s": "1011011",
    "t": "0001111",
    "u": "0111110",
    "v": "0111110",
    "w": "0110111",
    "x": "0110111",
    "y": "0110011",
    "z": "1101101",
    " ": "0000000",
}


# Create a function to display a character on a single digit
def display_character(board, char, digit):
    if char in lookupDictionary:
        segmentData = lookupDictionary[char]
        for i in range(7):
            board.digital_write(segmentPins[i], int(segmentData[i]))
        # Turn on the selected digit
        board.digital_write(digitPins[digit], 0)
        time.sleep(0.005)
        board.digital_write(digitPins[digit], 1)


# Initialize the pymata4 board
board = pymata4.Pymata4()

# Set the pins for the 4-digit 7-segment display
segmentPins = [18, 16, 19, 3, 2, 17, 4]

# Set the common pins for the digits (anodes)
digitPins = [5, 7, 8, 9]

# Set the pins as OUTPUT
for pin in segmentPins + digitPins:
    board.set_pin_mode_digital_output(pin)

# Display a message
message = "8888"
while True:
    for digit in range(4):
        display_character(board, message[digit], digit)

# Clear the display
for pin in segment_pins:
    board.digital_write(pin, 0)

# Release the board
board.shutdown()
