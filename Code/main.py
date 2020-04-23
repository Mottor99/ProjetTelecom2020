from room import Room
from wall import Wall
from transmitter import Transmitter
from receiver import Receiver

room1 = Room()
m = []
mur1 = Wall(0.5, [(-1,-1),(-1,6)], "brique")
mur2 = Wall(0.5, [(3,-1),(3,6)], "brique")
mur3 = Wall(0.5, [(-1,4), (7,4)], "brique")
mur4 = Wall(0.5, [(-1,-1), (7,-1)], "brique")
mur5 = Wall(0.5, [(-1,6), (3,6)], "brique")
mur6 = Wall(0.5, [(7,-1), (7,6)], "brique")
mur7 = Wall(0.5, [(0,7), (7,5)], "brique")
j = [mur1,mur3]
room1.list_of_walls = j
room1.list_of_transmitters.append(Transmitter((0, 0), 1))
room1.list_of_receivers.append(Receiver((0, 6), 1))



"""print("stp")"""

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
