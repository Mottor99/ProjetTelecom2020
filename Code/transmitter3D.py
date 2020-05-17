import math

class Transmitter:

    frequency = 5*10**9
    wavelength = frequency*3*10**8


    def __init__(self, position, type):
        self.position = position
        if type == "lambda-demi":
            self.power = 0.1
        else:
            pass

    def G(self, theta, phi):
        """gain"""
        a = 0.13 * 4 * math.pi * (math.sin(theta)) ** 3
        return abs(a)