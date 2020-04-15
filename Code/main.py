from room import Room
from wall import Wall
from line import Line

room1 = Room()
m = []
mur1 = Wall(0.5, [(-1,0),(-1,5)], "brique")
mur2 = Wall(0.5, [(1,0),(1,5)], "brique")
mur3 = Wall(0.5, [(-1,3), (1,3)], "brique")
j = [mur1,mur2, mur3]
room1.liste_walls = j

"""print("stp")"""

room1.ray_tracing(m, 3, room1.transmitter, room1.receiver, j)
print(room1.calculate(room1.transmitter,room1.receiver))
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
