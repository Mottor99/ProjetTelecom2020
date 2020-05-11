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


murext1 = Wall(0.5, [(-1,-1),(-1,2),(-1,3.4),(-1,4)], "cloison")
murext2 = Wall(0.5, [(-1,4),(1,4)], "cloison")
murext3 = Wall(0.5, [(1,4), (1,7)], "cloison")
murext4 = Wall(0.5, [(-1,7), (4,7), (5,7),(13,7)], "cloison")
murext5 = Wall(0.5, [(-1,7), (-1,12)], "cloison")
murext6 = Wall(0.5, [(-1,12), (5,12)], "cloison")
murext7 = Wall(0.5, [(5,12), (5,7)], "cloison")
murext8 = Wall(0.5, [(13,7), (13,2)], "cloison")
murext9 = Wall(0.5, [(13,2), (8,2)], "brique")
murext10 = Wall(0.5, [(8,2), (8,-1)], "brique")
murext11 = Wall(0.5, [(8,-1), (-1,-1)], "cloison")
murint1 = Wall(0.2, [(5,7), (5,4)], "brique")
murint2 = Wall(0.2, [(5,4), (7,4),(8,4),(9,4),(10,4),(12,4)], "brique")
murint3 = Wall(0.2, [(8,4), (8,7)], "brique")
murint5 = Wall(0.2, [(10,4), (10,7)], "brique")
murint4 = Wall(0.2, [(5,7), (5,4)], "brique")
murint6 = Wall(0.2, [(8,2), (3,2)], "brique")
murint7 = Wall(0.2, [(3,1), (3,-1)], "brique")

mur1 = Wall(0.5, [(0,0), (12,0)], "brique")
mur2 = Wall(0.5, [(0,12), (12,12)], "brique")
mur3 = Wall(0.5, [(0,0), (0,12)], "brique")
mur4 = Wall(0.5, [(4,0), (4,12)], "brique")
mur5 = Wall(0.5, [(8,0), (8,12)], "brique")
mur6 = Wall(0.5, [(12,0), (12,12)], "brique")
mur7 = Wall(0.5, [(0,8), (12,8)], "brique")
mur8 = Wall(0.5, [(0,4), (4,4)], "brique")
mur9 = Wall(0.5, [(8,4), (12,4)], "brique")

list = [mur1,mur2,mur3,mur4,mur5,mur6,mur7,mur8,mur9]
room1.list_of_walls = list
room1.list_of_transmitters.append(Transmitter((6, 4), 1))

"""room1.list_of_transmitters.append(Transmitter((4, 2), 1))
room1.list_of_transmitters.append(Transmitter((4, 8), 1))
room1.list_of_transmitters.append(Transmitter((1, 1), 1))"""


list_of_receivers_creation(3, 3)


room1.power_distribution((2,2), "ml")



"""
line1 = Line((0,0),(0,1))
line2 = Line((-2,2), (-3,2))
intersection = line1.intersection(line2)
s = ""
for i in intersection:
    s+= str(i)
    s+= " "
print(s)"""