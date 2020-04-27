from room3D import Room
from wall3D import Wall
from transmitter3D import Transmitter
from receiver3D import Receiver
from plane3D import Plane
from line3D import Line

"""
plane1 = Plane((0,0,0),(1,0,0),(0,1,0))
line1 = Line((0,0,2),(0,0,3))
intersection = plane1.intersection(line1)
print(intersection)
room1 = Room()
image = room1.image((0,0,-1), plane1)
print(image)


"""
room1 = Room()
m = []
mur1 = Wall(0.5, (-1,-1,0), (-1,6,0), (-1,-1,4), "brique")
mur2 = Wall(0.5, (-1,-1,0), (7,-1,0), (-1,-1,4), "brique")
mur3 = Wall(0.5, (3,-1,0), (3,6,0), (3,-1,4), "brique")
mur4 = Wall(0.5, (7,-1,0), (7,6,0), (7,-1,4), "brique")
mur5 = Wall(0.5, (-1,3,0), (7,3,0), (-1,3,4), "brique")
mur6 = Wall(0.5, (-1,6,0),(3,6,0),(-1,6,4), "brique")
mur7 = Wall(0.5, (0,7,0),(7,5,0),(0,7,4), "brique")
mur8 = Wall(0.5, (-3,-3,0),(-3,5,0),(5,-3,0), "brique")
mur9 = Wall(0.5, (-3,-3,4),(-3,5,4),(5,-3,4), "brique")
j = [mur1,mur2,mur3,mur4,mur5,mur6,mur7,mur8,mur9]
room1.list_of_walls = j
room1.list_of_transmitters.append(Transmitter((0,0,1), 1))
room1.list_of_receivers.append(Receiver((0,5,1), 1))





room1.power_distribution()


"""
line1 = Line((0,0),(0,1))
line2 = Line((-2,2), (-3,2))
intersection = line1.intersection(line2)
s = ""
for i in intersection:
    s+= str(i)
    s+= " "
print(s)"""
