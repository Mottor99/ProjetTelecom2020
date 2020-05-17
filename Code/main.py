from room import Room
from wall import Wall
from transmitter import Transmitter
from receiver import Receiver


def list_of_receivers_creation(room, len_x, len_y):
    """
     ajout des récepteurs dans toute la pièce. Sur l'axe horizontal un récepteur tous les (1/len_x) mètre,
           sur l'axe vertical un récepteur tous les (1/len_y) mètre
    """

    x_min = x_max = y_min = y_max = 0
    for wall in room.list_of_walls:
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
            room.list_of_receivers.append(Receiver((x_min + (i + 1) / len_x, y_min + (j + 1) / len_y), "lambda-demi"))
    return 0


murext_materiau = "cloison"
murint_materiau = "brique"

#
# création des murs de la pièce
#

murext1 = Wall(0.3, [(-1,-1),(-1,4),(-1,7), (-1,12)], murext_materiau)
murext2 = Wall(0.3, [(-1,4),(1,4)], murext_materiau)
murext3 = Wall(0.3, [(1,4), (1,7)], murext_materiau)
murext4 = Wall(0.3, [(-1,7), (4,7), (5,7),(13,7)], murext_materiau)
murext5 = Wall(0.3, [(-1,12), (5,12)], murext_materiau)
murext6 = Wall(0.3, [(5,7), (5,12)], murext_materiau)
murext7 = Wall(0.3, [(13,2), (13,7)], murext_materiau)
murext8 = Wall(0.3, [(8,2), (13,2)], murext_materiau)
murext9 = Wall(0.3, [(8,-1), (8,2)], murext_materiau)
murext10 = Wall(0.3, [(-1,-1), (8,-1)], murext_materiau)
murint1 = Wall(0.2, [(5,4), (5,7)], murint_materiau)
murint2 = Wall(0.2, [(5,4), (7,4),(8,4),(9,4),(10,4),(12,4)], murint_materiau)
murint3 = Wall(0.2, [(8,4), (8,7)], murint_materiau)
murint5 = Wall(0.2, [(10,4), (10,7)], murint_materiau)
murint4 = Wall(0.2, [(5,4), (5,7)], murint_materiau)
murint6 = Wall(0.2, [(3,2), (8,2)], murint_materiau)
murint7 = Wall(0.2, [(3,-1), (3,1)], murint_materiau)

list_walls = [murext1, murext2, murext3, murext4, murext5,
            murext6, murext7, murext8, murext9, murext10,
            murint1, murint2, murint3, murint4,
            murint5, murint6, murint7]

#
# création de la pièce
#
room1 = Room()

room1.list_of_walls = list_walls

#
# ajout d'un émetteur dans la pièce
#
transmitter = Transmitter((5, 0), "lambda-demi")
room1.list_of_transmitters.append(transmitter)

#
# ajout de récepteurs couvrant toute la pièce
# utiles au calcul de la puissance
#
list_of_receivers_creation(room1, 3, 3)

#
# fonction principale de l'algorithme de ray-tracing
#
room1.ray_and_power_distribution((0, 6), 2, "m")