from room import Room
from wall import Wall
from transmitter import Transmitter
from receiver import Receiver



def list_of_receivers_creation(len_x, len_y):
    x_min = x_max = y_min = y_max = 0
    for wall in list:
        if x_max < wall.list_of_points[0][0]:
            x_max = wall.list_of_points[0][0]
        if x_max < wall.list_of_points[1][0]:
            x_max = wall.list_of_points[1][0]
        if x_min > wall.list_of_points[0][0]:
            x_min = wall.list_of_points[0][0]
        if x_min > wall.list_of_points[1][0]:
            x_min = wall.list_of_points[1][0]
        if y_max < wall.list_of_points[0][1]:
            y_max = wall.list_of_points[0][1]
        if y_max < wall.list_of_points[1][1]:
            y_max = wall.list_of_points[1][1]
        if y_min > wall.list_of_points[0][1]:
            y_min = wall.list_of_points[0][1]
        if y_min > wall.list_of_points[1][1]:
            y_min = wall.list_of_points[1][1]

    len_x = len_x
    len_y = len_y
    for i in range(x_min, len_x * (x_max - x_min)):
        for j in range(y_min, len_y * (y_max - y_min)):
            room1.list_of_receivers.append(Receiver((x_min + (i + 1) / len_x, y_min + (j + 1) / len_y), 1))
    return 0






room1 = Room()
m = []
mur1 = Wall(0.1, [(-1,-1),(-1,11)], "brique")
mur2 = Wall(0.1, [(3,-1),(3,11)], "brique")
mur3 = Wall(0.1, [(-1,4), (11,4)], "brique")
mur4 = Wall(0.1, [(-1,-1), (11,-1)], "brique")
mur5 = Wall(0.1, [(-1,6), (11,6)], "brique")
mur6 = Wall(0.1, [(11,-1), (11,11)], "brique")
mur7 = Wall(0.1, [(0,7), (7,11)], "brique")

list = [mur1, mur3, mur4, mur5, mur6, mur7, mur2]
room1.list_of_walls = list
room1.list_of_transmitters.append(Transmitter((1, 8), 1))
"""room1.list_of_transmitters.append(Transmitter((4, 2), 1))
room1.list_of_transmitters.append(Transmitter((4, 8), 1))
room1.list_of_transmitters.append(Transmitter((1, 1), 1))"""


list_of_receivers_creation(4, 4)


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
