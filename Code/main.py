from room import Room
from wall import Wall
from line import Line

room1 = Room()
m = []
mur1 = Wall(0.5, [(-1,-1),(-1,6)], "brique")
mur2 = Wall(0.5, [(3,-1),(3,6)], "brique")
mur3 = Wall(0.5, [(-1,3), (7,3)], "brique")
mur4 = Wall(0.5, [(-1,-1), (7,-1)], "brique")
mur5 = Wall(0.5, [(-1,6), (3,6)], "brique")
mur6 = Wall(0.5, [(7,-1), (7,6)], "brique")
mur7 = Wall(0.5, [(0,7), (7,5)], "brique")
j = [mur1,mur3,mur4,mur5,mur6,mur7]
room1.liste_walls = j

"""print("stp")"""

room1.ray_tracing(m, 1, room1.transmitter, room1.receiver, j)
print(room1.calculate())
print(len(room1.liste_rays))
print("voila")
room1.affichage_graphique()

"""
line1 = Line((0,0),(0,1))
line2 = Line((-2,2), (-3,2))
intersection = line1.intersection(line2)
s = ""
for i in intersection:
    s+= str(i)
    s+= " "
print(s)"""
