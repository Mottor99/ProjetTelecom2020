import math

class Transmitter:

    frequency = 5*10**9
    wavelength = frequency*3*10**8


    def __init__(self, position, type):
        self.position = position
        if type == 1:
            self.power = (16/(3*math.pi))
            self.he = self.wavelength/math.pi #le signe n'importe pas car on en prendra le carré
        else:
            self.power = 1
            self.he = 1


    def G(self, x, y):
        return 1