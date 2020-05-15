import math

class Transmitter:

    frequency = 5*10**9
    epsilon0 = 8.854 * 10 ** -12
    mu0 = 4 * math.pi * 10 ** -7
    wavelength = 1/(math.sqrt(mu0*epsilon0)*frequency)


    def __init__(self, position, type):
        self.position = position
        self.resistance = 73
        if type == 1:
            self.gain = 3/2
            self.power = 0.1
            self.he = self.wavelength/math.pi #le signe n'importe pas car on en prendra le carré
        else:
            self.gain = 1
            self.power = 0.1
            self.he = 1




