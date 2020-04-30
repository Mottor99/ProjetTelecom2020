from room import Room
from wall import Wall
from transmitter import Transmitter
from receiver import Receiver

room1 = Room()
m = []
mur1 = Wall(0.5, [(-1,-1),(-1,11)], "brique")
mur2 = Wall(0.5, [(-1,-1),(11,-1)], "brique")
mur3 = Wall(0.5, [(11,-1), (11,11)], "brique")
mur4 = Wall(0.5, [(-1,4), (11,4)], "brique")
mur5 = Wall(0.5, [(-1,6), (11,6)], "brique")
mur6 = Wall(0.5, [(7,-1), (7,6)], "brique")
mur7 = Wall(0.5, [(0,7), (7,5)], "brique")
j = [mur1,mur3,mur4,mur5]
room1.list_of_walls = j
room1.list_of_transmitters.append(Transmitter((0, 5), 1))
room1.list_of_receivers.append(Receiver((10, 5), 1))




room1.power_distribution()

