from room3D import Room
from wall3D import Wall
from transmitter3D import Transmitter
from receiver3D import Receiver
from plane3D import Plane
from line3D import Line
from ray3D import Ray

room1 = Room()
mur1 = Wall(0.5, (-1,-1,0), (-1,11,0), (-1,-1,2), "brique",0)
mur2 = Wall(0.5, (11,-1,0), (11,11,0), (11,-1,2), "brique",0)
mur3 = Wall(0.5, (-1,-1,0), (11,-1,0), (-1,-1,2), "brique",0)
mur4 = Wall(0.5, (-1,11,0), (11,11,0), (-1,11,2), "brique",0)
mur5 = Wall(0.5, (-1,-1,0), (11,-1,0), (-1,11,0), "brique",-1)
mur6 = Wall(0.5, (-1,-1,2), (11,-1,2), (-1,11,2), "brique",-1)
mur7 = Wall(0.5, (6,-1,0), (6,11,0), (6,-1,2), "brique",0)
mur8 = Wall(0.5, (4,-1,0), (4,11,0), (4,-1,2), "brique",0)
mur9 = Wall(0.5, (-1,10,0), (11,10,0), (-1,10,2), "brique",0)
mur10 = Wall(0.5, (-1,9,0), (11,9,0), (-1,9,2), "brique",0)


j = [mur1,mur2,mur3,mur4,mur7,mur8]
room1.list_of_walls = j
room1.list_of_transmitters.append(Transmitter((5,0,1), 1))



room1.power_distribution(1,11.3,11.3)
