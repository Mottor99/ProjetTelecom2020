from room3D import Room
from wall3D import Wall
from transmitter3D import Transmitter
from receiver3D import Receiver
from plane3D import Plane
from line3D import Line
from ray3D import Ray

room1 = Room()

mur11 = Wall(0.5, (0,0,0), (0,12,0), (0,0,6), "brique",[0,1,2])
mur21 = Wall(0.5, (12,0,0), (12,12,0), (12,0,6), "brique",[0,1,2])
mur31 = Wall(0.5, (0,0,0), (12,0,0), (0,0,6), "brique",[0,1,2])
mur41 = Wall(0.5, (0,12,0), (12,12,0), (0,12,6), "brique",[0,1,2])
mur51 = Wall(0.5, (4,0,0), (4,12,0), (4,0,2), "brique",[0])
mur61 = Wall(0.5, (8,0,0), (8,12,0), (8,0,2), "brique",[0])
mur71 = Wall(0.5, (0,8,0), (12,8,0), (0,8,2), "brique",[0])
mur81 = Wall(0.5, (0,4,0), (4,4,0), (0,4,2), "brique",[0])
mur91 = Wall(0.5, (8,4,0), (12,4,0), (8,4,2), "brique",[0])


mur12 = Wall(0.5, (5,0,2), (5,12,2), (4,0,4), "brique",[1])
mur22 = Wall(0.5, (0,3,2), (5,3,0), (0,3,4), "brique",[1])
mur32 = Wall(0.5, (0,6,2), (5,6,2), (0,6,4), "brique",[1])
mur42 = Wall(0.5, (0,9,2), (5,9,2), (0,9,4), "brique",[1])


mur13 = Wall(0.5, (7,4,4), (7,12,4), (7,4,6), "brique",[2])
mur23 = Wall(0.5, (7,4,4), (12,4,4), (7,4,6), "brique",[2])
mur33 = Wall(0.5, (0,9,4), (7,9,4), (0,9,6), "brique",[2])
mur43 = Wall(0.5, (0,12,4), (12,12,4), (0,12,6), "brique",[2])


mur5 = Wall(0.5, (0,0,0), (12,0,0), (0,12,0), "brique",[-1])
mur6 = Wall(0.5, (0,0,2), (12,0,2), (0,12,2), "brique",[-1])
mur7 = Wall(0.5, (0,0,4), (12,0,4), (0,12,4), "brique",[-1])
mur8 = Wall(0.5, (0,0,6), (12,0,6), (0,12,6), "brique",[-1])


mur91test = Wall(0.5, (-1,10,0), (11,10,0), (-1,10,2), "brique",[0])
mur101test = Wall(0.5, (-1,9,0), (11,9,0), (-1,9,2), "brique",[0])


j = [mur11,mur21,mur31,mur41,mur51,mur61,mur71,mur81,mur91]
room1.list_of_walls = j
room1.list_of_transmitters.append(Transmitter((6,4,1), 1))



room1.power_distribution(3,12.3,12.3)
