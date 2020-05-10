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

murext_materiau = "brique"
murint_materiau = "brique"

murext1 = Wall(0.5, [(-1,-1),(-1,2),(-1,3.4),(-1,4)], murext_materiau)
murext2 = Wall(0.5, [(-1,4),(1,4)], murext_materiau)
murext3 = Wall(0.5, [(1,4), (1,7)], murext_materiau)
murext4 = Wall(0.5, [(-1,7), (4,7), (5,7),(13,7)], murext_materiau)
murext5 = Wall(0.5, [(-1,7), (-1,12)], murext_materiau)
murext6 = Wall(0.5, [(-1,12), (5,12)], murext_materiau)
murext7 = Wall(0.5, [(5,12), (5,7)], murext_materiau)
murext8 = Wall(0.5, [(13,7), (13,2)], murext_materiau)
murext9 = Wall(0.5, [(13,2), (8,2)], murext_materiau)
murext10 = Wall(0.5, [(8,2), (8,-1)], murext_materiau)
murext11 = Wall(0.5, [(8,-1), (-1,-1)], murext_materiau)
murint1 = Wall(0.2, [(5,7), (5,4)], murint_materiau)
murint2 = Wall(0.2, [(5,4), (7,4),(8,4),(9,4),(10,4),(12,4)], murint_materiau)
murint3 = Wall(0.2, [(8,4), (8,7)], murint_materiau)
murint5 = Wall(0.2, [(10,4), (10,7)], murint_materiau)
murint4 = Wall(0.2, [(5,7), (5,4)], murint_materiau)
murint6 = Wall(0.2, [(8,2), (3,2)], murint_materiau)
murint7 = Wall(0.2, [(3,1), (3,-1)], murint_materiau)

list = [murext1, murext2, murext3,
        murext4, murext5, murext6,
        murext7, murext8, murext9, murext10, murext11,
        murint1, murint2, murint3, murint4,
        murint5, murint6, murint7]
room1.list_of_walls = list
room1.list_of_transmitters.append(Transmitter((5, 0), 1))
room1.list_of_transmitters.append(Transmitter((3, 8), 1))
room1.list_of_transmitters.append(Transmitter((1, 1), 1))


list_of_receivers_creation(3, 3)


room1.power_distribution((2,2), "r")



"""
line1 = Line((0,0),(0,1))
line2 = Line((-2,2), (-3,2))
intersection = line1.intersection(line2)
s = ""
for i in intersection:
    s+= str(i)
    s+= " "
print(s)"""