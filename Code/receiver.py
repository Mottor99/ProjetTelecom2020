class Receiver:

    position = 0.0
    resistance = 0.0

    def __init__(self, position, type):
        self.position = position
        self.resistance = 1

    def h(self, x, y):
        return 1