import math

class Transmitter:

    frequency = 5*10**9
    wavelength = 3*10**8/frequency


    def __init__(self, position, type):
        self.position = position
        self.resistance = 73
        if type == 1:
            self.gain = (16/(3*math.pi))
            self.power = 0.1
            self.he = self.wavelength/math.pi #le signe n'importe pas car on en prendra le carré
        else:
            self.gain = 1
            self.power = 0.1
            self.he = 1




