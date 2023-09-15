# Settings file where all global user-modifiable variables are initialised
# Creator: HVAC Project T14
# Last edited: 12 Sep

# import functions and files
from pymata4 import pymata4

# ---- initialise board ----
global board
global temperatureList
board = pymata4.Pymata4()
temperatureList = []


# ---- constant variables ----
LOOKUP_DICTIONARY = {
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
    "N": "1101010",
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
    "n": "1101010",
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

# ---- set initial user modifiable variables ----

global systemSettings

systemSettings = {
    "blankSetting": None,  # blank placeholder setting
    "maintenancePIN": 1234,  # the user PIN to gain access to maintenance settings
    "pollingTime": 1.0,  # polling time of polling loop
    "setting3": "hello"  # placeholder setting
}

systemSettingsParameters = {
    "blankSetting": None,  # blank placeholder setting
    # the user PIN must be between a value of 0 and 9999 (4 digits)
    "maintenancePIN": [0, 9999],
    "pollingTime": [1.0, 3.0],  # polling time must be between 1 and 3 seconds
    "setting3": None  # placeholder setting
}
