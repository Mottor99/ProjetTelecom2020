class Receiver:

    position = 0.0
    resistance = 0.0

    def __init__(self, position, type):
        self.position = position
        self.captured_mean_power = 0
        self.captured_local_power = 0
        self.captured_bit_rate = 0

    def h(self, x, y):
        return 1