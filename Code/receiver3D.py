import math
from transmitter3D import Transmitter


class Receiver:

    def __init__(self, position, type, level):
        self.position = position
        self.resistance = 73
        self.captured_power = 0
        self.level = level  # étage sur lequel se trouve le récepteur

    def h(self, theta, phi):
        """
        hauteur équivalente
        """

        if theta != 0 and theta != math.pi:
            a = math.cos(math.pi / 2 * math.cos(theta))
            a = a / (math.sin(theta) * math.sin(theta))
        else:
            a = 0
        return 0, 0, -1 * Transmitter.wavelength / math.pi * a