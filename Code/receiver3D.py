import math
class Receiver:

    position = 0.0
    resistance = 0.0

    def __init__(self, position, type):
        self.position = position
        self.resistance = 1
        self.captured_power = 0

    def h(self, x, y, f):
        a = math.cos(math.pi / 2 * math.cos(x))
        a = a / (math.sin(x) * math.sin(x))
        c = 3 * 10 ** 8
        lamb = c / f
        return (0, 0, -1 * lamb / math.pi * a)