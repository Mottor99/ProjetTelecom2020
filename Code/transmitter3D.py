import math


class Transmitter:

    frequency = 5*10**9
    epsilon0 = 8.854 * 10 ** -12
    mu0 = 4 * math.pi * 10 ** -7
    wavelength = 1 / (math.sqrt(mu0 * epsilon0) * frequency)

    def __init__(self, position, type):
        self.position = position
        if type == "lambda-demi":
            self.power = 0.1
        else:
            pass

    def G(self, theta, phi):
        """
        Gain
        """
        gain = 0.13 * 4 * math.pi * (math.sin(theta)) ** 3
        return gain