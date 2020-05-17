import math
class Receiver:

    position = 0.0
    resistance = 0.0

    def __init__(self, position, type, level):
        self.position = position
        self.resistance = 73
        self.captured_power = 0
        self.level = level #étage sur lequel se trouve le récepteur

    def h(self, theta, phi, f):
        """
        :param f: fréquence de l'onde reçue
        :return: hauteur équivalente
        """
        c = 3 * 10 ** 8
        lamb = c / f
        if theta != 0 and theta != math.pi:
            a = math.cos(math.pi / 2 * math.cos(theta))
            a = a / (math.sin(theta) * math.sin(theta))
        else:
            a = 0
        return (0, 0, -1 * lamb / math.pi * a)