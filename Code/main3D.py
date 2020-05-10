from room3D import Room
from wall3D import Wall
from transmitter3D import Transmitter
from receiver3D import Receiver
from plane3D import Plane
from line3D import Line

room1 = Room()
m = []
mur1 = Wall(0.5, (-1,-1,0), (-1,6,0), (-1,-1,8), "brique")
mur2 = Wall(0.5, (-1,-1,0), (7,-1,0), (-1,-1,8), "brique")
mur3 = Wall(0.5, (3,-1,0), (3,6,0), (3,-1,8), "brique")
mur4 = Wall(0.5, (7,-1,0), (7,6,0), (7,-1,8), "brique")
mur5 = Wall(0.5, (-1,2.5,0), (7,2.5,0), (-1,2.5,8), "brique")
mur6 = Wall(0.5, (-1,6,0),(7,6,0),(-1,6,8), "brique")
mur7 = Wall(0.5, (0,7,0),(7,5,0),(0,7,8), "brique")
mur8 = Wall(0.5, (-1,-1,0),(7,-1,0),(-1,6,0), "brique")
mur9 = Wall(0.5, (-1,-1,8),(7,-1,8),(-1,6,8), "brique")

mur10 = Wall(0.5, (-1,-1,0),(-1,6,0),(-1,-1,4), "brique")
mur11 = Wall(0.5, (-1,4,0), (7,4,0), (-1,4,4), "brique")

j = [mur1,mur2,mur4,mur6,mur8,mur9]
room1.list_of_walls = j
room1.list_of_transmitters.append(Transmitter((2,0,4), 1))
room1.list_of_receivers.append(Receiver((0,5,4), 1))





room1.power_distribution()
