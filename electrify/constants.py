import math

# Fundamental physical constant.
# Equal to the negative electric charge of an electron.
# Measured in coulombs.
ELEMENTARY_CHARGE = 1.602176634e-19

# The speed of light in a vacuum, measured in meters per second (m/s).
SPEED_OF_LIGHT = c = 299792458.0

# Boltzmann constant (k_B) as a measure in joules per kelvin (J/K)
BOLTZMANN_CONSTANT = 1.380649e-23

# Effective impedances
OPEN_CIRCUIT = math.inf
SHORT_CIRCUIT = 0


### POWERS/MAGNITUDES ###


FEMTO = 1e-15
PICO = 1e-12
NANO = 1e-9
MICRO = 1e-6
MILLI = 1e-3
KILO = 1e3
MEGA = 1e6
GIGA = 1e9
TERA = 1e12
PETA = 1e15


VALUE_TYPES = {
    ("femto", "f"): FEMTO,
    ("pico", "p"): PICO,
    ("nano", "n"): NANO,
    ("micro", "u", "µ"): MICRO,
    ("milli", "m"): MILLI,
    ("kilo", "k"): KILO,
    ("mega", "M"): MEGA,
    ("giga", "G"): GIGA,
    ("tera", "T"): TERA,
    ("peta", "P"): PETA
}


### Units of Measure ###


FARAD = "farad"  # Unit of capacitance
HENRY = "henry"  # Unit of inductance
OHM = "ohm"  # Unit of resistance & reactance
SIEMENS = "siemens"  # Unit of conductance and susceptance
HERTZ = "hertz"  # Unit of frequency
VOLT = "volt"  # Unit of electromotive force
AMPERE = "ampere"  # Unit of current
WATT = "watt"  # Unit of power
COULOMB = "coulomb"  # Unit of charge
METER = "meter"  # Unit of distance (e.g. wavelength)
SECOND = "second"  # Unit of time (2nd 1/60th of an hour)
MINUTE = "minute"  # Unit of time (1/60th of an hour)
HOUR = "hour"  # Unit of time
JOULE = "joule"  # Unit of energy


# Primary unit symbols
UNIT_SYMBOLS = {
    FARAD: "F",
    HENRY: "H",
    OHM: "Ω",
    HERTZ: "Hz",
    SIEMENS: "℧",
    VOLT: "V",
    AMPERE: "A",
    WATT: "W",
    COULOMB: "C",
    METER: "meter",
    SECOND: "sec",
    HOUR: "hour",
    JOULE: "J",
}


### Standard Component Values ###


COMPONENT_VALUE_MULTIPLES = {
    "E12": [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2],

    "E24": [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
            3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1],

    "E48": [1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54, 1.62, 1.69,
            1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49, 2.61, 2.74, 2.87, 3.01,
            3.16, 3.32, 3.48, 3.65, 3.83, 4.02, 4.22, 4.42, 4.64, 4.87, 5.11, 5.36,
            5.62, 5.90, 6.19, 6.49, 6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53],

    "E96": [1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30,
            1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74,
            1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 2.16, 2.21, 2.26, 2.32,
            2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09,
            3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12,
            4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49,
            5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32,
            7.50, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76]
}


### Conversion factors for sinusoidal voltages and currents ###


PEAK_TO_EFFECTIVE = 0.707
PEAK_TO_AVERAGE = 0.637
EFFECTIVE_TO_PEAK = 1.414
AVERAGE_TO_EFFECTIVE = 1.11
AVERAGE_TO_PEAK = 1.57
EFFECTIVE_TO_AVERAGE = 0.9


## RESISTOR COLOR CODES ##


BLACK = 0
BROWN = 1
RED = 2
ORANGE = 3
YELLOW = 4
GREEN = 5
BLUE = 6
VIOLET = 7
GRAY = 8
WHITE = 9
GOLD = 1 / 10.0
SILVER = 1 / 100.0

COLOR_CODES = {
    "black": BLACK,
    "brown": BROWN,
    "red": RED,
    "orange": ORANGE,
    "yellow": YELLOW,
    "green": GREEN,
    "blue": BLUE,
    "violet": VIOLET,
    "gray": GRAY,
    "white": WHITE,
    "gold": GOLD,
    "silver": SILVER
}



BUTTERWORTH_COEF_MAX_FLAT:dict[int, list[float]] = {
    1: [2.0000],
    2: [1.414, 1.414],
    3: [1, 2, 1],
    4: [0.7654, 1.85, 1.85, 0.7654],
    5: [0.618, 1.618, 2, 1.618, 0.618],
    6: [0.5176, 1.414, 1.932, 1.932, 1.1414, 0.5176],
    7: [0.445, 1.247, 1.802, 2, 1.802, 1.247, 0.445],
    8: [0.3902, 1.1111, 1.6629, 1.9615, 1.9615, 1.6629, 1.1111, 0.3902],
    9: [0.3473, 1.0, 1.5321, 1.8794, 2.0, 1.897, 1.5321, 1.0, 0.3473],
    10: [0.3129, 0.9080, 1.4142, 1.7820, 1.9754, 1.9754, 1.7820, 1.4142, 0.9080, 0.3129]
}

BUTTERWORTH_COEF_LINEAR_PHASE:dict[int, list[float]] = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: []
}
