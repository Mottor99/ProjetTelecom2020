from room import Room
from wall import Wall

room1 = Room()
m = []
mur1 = Wall(0.5, [(1,1),(1,5)], "brique")
mur2 = Wall(0.5, [(1,1),(5,1)], "brique")
mur3 = Wall(0.5, [(1,5),(5,4)], "brique")
j = [mur1,mur2,mur3]

"""print("stp")"""

room1.ray_tracing(m, 3, room1.transmitter, room1.receiver, j)