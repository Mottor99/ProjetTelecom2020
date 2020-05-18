import math
from transmitter import Transmitter


class Receiver:

    def __init__(self, position, type):
        self.position = position
        self.captured_mean_power = 0
        self.captured_local_power = 0
        self.captured_bit_rate = 0
        if type == "lambda-demi":
            self.he = Transmitter.wavelength/math.pi  # le signe n'importe pas car on en prendra le carré
        else:
            pass