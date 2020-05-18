from ray3D import Ray
from line3D import Line
import copy
import math
import numpy as np
import matplotlib.pyplot as plt
from receiver3D import Receiver


class Room:

    def __init__(self):
        self.list_of_walls = []
        self.list_of_transmitters = []
        self.list_of_receivers = []
        self.direct_wave_calculated = False

    def ray_and_power_distribution(self, levels, length, width, max_number_reflection):
        """
        :param levels: nombre d'étages du bâtiment
        :param length: longueur (selon l'axe y) du bâtiment
        :param width: largeur (selon l'axe x) du bâtiment
        :param max_number_reflection: nombre max de réflexions que peut faire un rayon pour être comptabilisé
        """
        #
        # f est la liste des fichiers où on écrit les débits binaires
        #
        f = []

        for i in range(levels):
            doc = "debitbinaire"+str(i)+".txt"
            f.append(open(doc, "w"))
            for j in range(int(length)):
                for k in range(int(width)):
                    self.list_of_receivers.append(Receiver((k-0.5,j-0.5,1+i*2.20),1,i))
                    #
                    # on crée des récepteurs équidistants à chaque étage
                    #

        # on calcule la puissance captée par chaque récepteur
        for receiver in self.list_of_receivers:
            for transmitter in self.list_of_transmitters:
                list_of_rays = []
                #
                # appel de la fonction récursive de ray tracing
                #
                self.ray_tracing([], max_number_reflection, transmitter, receiver, self.list_of_walls, list_of_rays)
                receiver.captured_power += self.calculate(list_of_rays, transmitter, receiver)
                self.direct_wave_calculated = False
                if (receiver.position == (-0.5,2.5,3.20)) and (transmitter == self.list_of_transmitters[0]):
                    # on représente les rayons pour un récepteur et un émetteur
                    self.graphical_display(list_of_rays)

            self.power_to_bit_rate(receiver, receiver.captured_power)
            # on écrit le débit binaire dans un fichier pour pouvoir le représenter
            f[receiver.level].write(str(receiver.position[0]) + " " + str(receiver.position[1]) + " " + str(
                receiver.captured_bit_rate) + "\n")
        plt.figure(figsize=(8, 6))
        for i in range(levels):
            f[i].close()
            # on représente le débit binaire pour chaque étage
            plt.subplot(int(math.sqrt(levels))+1,int(math.sqrt(levels))+1,i+1)
            self.power_graphic_display("debitbinaire"+str(i)+".txt", i)
        plt.show()


    def ray_tracing(self, m, max_number_reflection, transmitter, receiver, list_of_walls, list_of_rays):
        """
        fonction récursive de ray tracing, à chaque appel de la fonction, max_number_reflection est décrémenté d'une unité
        :param m: liste qui permet la sauvegarde d'une liste d'une itération à l'autre
        :param max_number_reflection: nombre maximal de réflexions permises.
        :param list_of_walls: ensemble des murs de la pièce.
        :param list_of_rays: liste qui contiendra l'ensemble des rayons.
        """
        if max_number_reflection != 1:
            # condition où la récursivité continue à avoir lieu
            # max_number_reflection étant décrémenté pour l'itération suivante
            max_number_reflection = max_number_reflection - 1
            for j in range(len(list_of_walls)):
                if len(m) == 0:
                    pass
                elif j == m[len(m) - 1]:
                    continue
                l = copy.deepcopy(m)
                l.append(j)

                sub_list_of_walls = []
                # on crée les listes de murs sur lequel les rayons vont être réfléchis
                for k in l:
                    sub_list_of_walls.append(list_of_walls[k])

                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)
                if ray.list_of_points:
                    list_of_rays.append(ray)
                self.ray_tracing(l, max_number_reflection, transmitter, receiver, list_of_walls, list_of_rays)

        elif max_number_reflection == 1:
            # dernière étape de la récursivité
            sub_list_of_walls = []

            if self.direct_wave_calculated == False:
                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)  # ajout du rayon direct
                if ray.list_of_points:
                    list_of_rays.append(ray)
                self.direct_wave_calculated = True
            for j in range(len(list_of_walls)):
                if not m:
                    pass
                elif j == m[len(m) - 1]:
                    continue
                l = copy.deepcopy(m)
                l.append(j)

                sub_list_of_walls = []

                for k in l:
                    sub_list_of_walls.append(list_of_walls[k])
                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)
                if ray.list_of_points:
                    list_of_rays.append(ray)


    def ray_creation(self, sub_list_of_walls, transmitter, receiver):
        """
        création du rayon passant par la sub_list_of_walls et reliant transmitter à receiver
        """
        point = transmitter.position
        list_of_images = []
        ray = Ray([])
        for wall in sub_list_of_walls:
            # on crée toutes les images et les rassemble dans une liste
            image_point = self.image(point, wall.plane)
            list_of_images.append(image_point)
            point = image_point
        ray.list_of_points.append(receiver.position)
        ray_point = receiver.position  # point de départ du tracé du rayon
        if sub_list_of_walls:
            ray.distance = self.dist(receiver.position, list_of_images[
                len(list_of_images) - 1])  # taille du rayon
        else:
            ray.distance = self.dist(receiver.position, transmitter.position)  # cas du rayon direct

        for j in range(len(list_of_images)):
            # on applique la méthode des images pour tracer le rayon
            ray_line = Line(ray_point, list_of_images[len(list_of_images) - 1 - j])
            intersection_point = sub_list_of_walls[len(list_of_images) - 1 - j].plane.intersection(
                ray_line)  # point d'intersection mur/rayon
            if sub_list_of_walls[len(list_of_images) - 1 - j].point_not_in_wall(intersection_point):
                ray.list_of_points = []  # pas d'intersection avec le mur, rayon non comptabilisé
                break

            if self.between(intersection_point, ray_point, list_of_images[len(list_of_images) - 1 - j]):
                # si le point d'intersection du mur n'appartient pas au segment [image, récepteur]
                ray_point = intersection_point
                ray.list_of_points.append(ray_point)
            else:
                ray.list_of_points = []
                break

        # point final du tracé du rayon
        if len(ray.list_of_points) != 0:
            # si la liste de points du rayon est vide, c'est que ce rayon n'existe pas
            ray.list_of_points.append(transmitter.position)

            # on calcule les angles d'émission
            vector_emission = ray.list_of_points[len(ray.list_of_points) - 2] - np.dot(1, transmitter.position)
            rho = np.linalg.norm(vector_emission)
            if rho == 0:
                rho = 1
            ray.theta_emission = math.acos(vector_emission[2] / rho)

            if vector_emission[0] != 0:
                ray.phi_emission = math.atan(vector_emission[1] / vector_emission[0])
            else:
                ray.phi_emission = math.pi / 2

            # on calcule les angles de réception
            vector_reception = ray.list_of_points[1] - np.dot(1, ray.list_of_points[0])
            rho = np.linalg.norm(vector_reception)
            if rho == 0:
                rho = 1
            ray.theta_reception = math.acos(vector_reception[2] / rho)
            if vector_reception[0] != 0:
                ray.phi_reception = math.atan(vector_reception[1] / vector_reception[0])
            else:
                ray.phi_reception = math.pi / 2

            # on déduit la polarisation initiale des angles d'émission
            pol0 = math.cos(ray.theta_emission) * math.cos(ray.phi_emission)
            pol1 = math.cos(ray.theta_emission) * math.sin(ray.phi_emission)
            pol2 = math.sin(ray.theta_emission) * -1
            ray.polarisation = [pol0,pol1,pol2]

            # on calcule les coefficients de transmission et de réflexion dans l'ordre
            self.coef_order(ray, sub_list_of_walls)

        return ray

    def coef_order(self, ray, sub_list_of_walls):
        """
        Calcule toutes les interactions d'un rayon dans l'ordre où il les subit
        """
        for i in range(len(ray.list_of_points) - 1):
            reflection_walls = []
            # les murs sur lesquels le segment de rayon est réfléchi ne peuvent pas être compté comme des murs où il y a une transmission
            if i == 0:
                if sub_list_of_walls:
                    reflection_walls.append(sub_list_of_walls[0])
            elif i == len(ray.list_of_points)-2:
                reflection_walls.append(sub_list_of_walls[len(sub_list_of_walls)-1])
            else:
                reflection_walls.append(sub_list_of_walls[i])
                reflection_walls.append(sub_list_of_walls[i-1])

            self.verif_transmission(ray.list_of_points[len(ray.list_of_points)-1-i],
                                    ray.list_of_points[len(ray.list_of_points)-2-i], ray,reflection_walls)
            if not ray.list_of_points:
                # ceci se produit si le rayon passe par un coin. verif_transmission vide alors sa liste de points
                return 0
            if i < len(ray.list_of_points) - 2:
                ray.reflection_total_coefficient_calculation(sub_list_of_walls[i],
                                                             Line(ray.list_of_points[len(ray.list_of_points)-1-i],
                                                                  ray.list_of_points[len(ray.list_of_points)-2-i]))

        return 0

    def image(self, origin_point, plane):
        """
        renvoie l'image de original_point par symétrie orthogonale par rapport au plan plane
        """
        lam = plane.d - np.dot(plane.normal_vector, origin_point)
        image_point = origin_point + np.dot(2 * lam, plane.normal_vector)
        return image_point

    def dist(self, point1, point2):
        euclidian_distance = math.sqrt(
            (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)
        return euclidian_distance

    def verif_transmission(self, point1, point2, ray, reflection_walls):
        """
        calcule toutes les transmissions d'un segment de rayon contenu entre le point1 et le point2
        """
        inter_walls = []
        order = []
        n_walls = 0
        portion_ray = Line(point1, point2)

        for j in self.list_of_walls:
            if j in reflection_walls:
                continue
                # on fait en sorte de ne pas compter des transmissions au travers des murs de reflexions
                # aux extrémités du segment
            intersection = j.plane.intersection(portion_ray)

            # on vérifie que le rayon a bien une intersection avec le mur
            if not j.point_not_in_wall(intersection):
                if intersection[0] == point2[0] and intersection[1] == point2[1] and intersection[2] == point2[2]:
                    # ceci se produit si le rayon est réfléchi dans un coin
                    ray.list_of_points = []
                    return 0
                # on vérifie que l'intersection de la droite définie par point1 et point2 et du mur
                # se trouve bien entre point1 et point2
                if self.between(intersection, point1, point2):
                    inter_walls.append(j)
                    # inter_walls est la liste des murs au travers desquels le rayon passe
                    order.append(self.dist(intersection, point2))
                    n_walls += 1
                    # n_walls est le nombre de mur au travers desquels il y a transmission
        while n_walls != 0:
            # on connait maintenant tous les murs au travers desquels il y a transmission
            # on veut maintenant calculer leur effet dans l'ordre où le rayon les rencontre
            i = np.argmax(order)
            ray.transmission_total_coefficient_calculation(inter_walls[i], portion_ray)
            order[i] = 0
            n_walls -= 1

        return 0

    def between(self, point1, point2, point3):
        """
        vérifie que point1 appartient au segment [point2, point3], en sachant qu'il appartient déjà à leur droite
        :return: True si c'est le cas
        """
        point1_is_between_point2_and_point3 = False
        if point2[0] == point3[0]:
            if point2[1] == point3[1]:
                if (point2[2] <= point1[2] <= point3[2]) or (
                        point2[2] >= point1[2] >= point3[2]):
                    point1_is_between_point2_and_point3 = True
            else:
                if (point2[1] <= point1[1] <= point3[1]) or (
                        point2[1] >= point1[1] >= point3[1]):
                    point1_is_between_point2_and_point3 = True
        else:
            if (point2[0] <= point1[0] <= point3[0]) or (point2[0] >= point1[0] >= point3[0]):
                point1_is_between_point2_and_point3 = True
        return point1_is_between_point2_and_point3

    def graphical_display(self, list_of_rays):
        """
        affichage graphique de l'ensemble des rayons calculés précédemment reliant transmitter à receiver
        """

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_zlim(0, 4)

        for ray in list_of_rays:
            self.plott(ray.list_of_points, ax)

        for wall in self.list_of_walls:
            self.draw_wall(wall, ax)
        plt.show()
        return 0

    def plott(self, list_of_points, ax):
        X = []
        Y = []
        Z = []
        for i in list_of_points:
            X.append(i[0])
            Y.append(i[1])
            Z.append(i[2])
        ax.plot(X, Y, Z)
        return 0

    def draw_wall(self, wall, ax):
        """
        :param wall: un mur que l'on veut représenter
        :param ax: la figure sur laquelle on veut dessiner
        """
        dist12 = self.dist(wall.point1, wall.point2)
        dist13 = self.dist(wall.point1, wall.point3)
        dist12 = int(dist12)
        dist13 = int(dist13)
        x1 = wall.point1[0]
        y1 = wall.point1[1]
        z1 = wall.point1[2]
        x2 = wall.point2[0]
        y2 = wall.point2[1]
        z2 = wall.point2[2]
        x3 = wall.point3[0]
        y3 = wall.point3[1]
        z3 = wall.point3[2]
        # on crée une liste de points appartenant au mur parce que plot_surface en a besoin
        # pour plot le mur. On sépare la liste de points en 3 listes pour chaque coordonée
        x21 = np.linspace(0, x2 - x1, int(dist12*4))
        x31 = np.linspace(0, x3 - x1, int(dist13*4))
        y21 = np.linspace(0, y2 - y1, int(dist12*4))
        y31 = np.linspace(0, y3 - y1, int(dist13*4))
        z21 = np.linspace(0, z2 - z1, int(dist12*4))
        z31 = np.linspace(0, z3 - z1, int(dist13*4))
        x = x1 + np.add.outer(x21, x31)
        y = y1 + np.add.outer(y21, y31)
        z = z1 + np.add.outer(z21, z31)
        if -2 in wall.level:
            # si on ne veut pas représenter le mur
            pass
        elif -3 in wall.level:
            # si on veut représente le mur dans une autre couleur
            # par exemple le plafond
            ax.plot_surface(x, y, z, color='r', alpha=0.4)
        elif -1 not in wall.level:
            ax.plot_surface(x, y, z, color='b', alpha=0.25)
        else:
            ax.plot_surface(x, y, z, color='g', alpha=1)

    def calculate(self, list_of_rays, transmitter, receiver):
        """
        calcul de la puissance moyenne tenant compte de l'ensemble des rayons reliant transmitter à receiver
        """
        average_power = 0
        for ray in list_of_rays:
            if ray.distance == 0:
                # cas limite
                ray.distance = 0.1
            E = math.sqrt(transmitter.power*60 * transmitter.G(ray.theta_emission, ray.phi_emission)) / ray.distance

            # puissance due à un rayon
            hE = E * abs(np.dot(receiver.h(ray.theta_reception,ray.phi_reception),ray.polarisation))
            average_power = average_power + hE ** 2
        average_power = average_power / (8 * receiver.resistance)

        return average_power


    def power_to_bit_rate(self, receiver, power):
        """
        convertit la puissance (power) en débit binaire (bit_rate)
        """
        if power == 0:
            receiver.captured_bit_rate = 0
        else:
            sensibility = 10 * math.log10(power / 10 ** -3)
            if sensibility < -82:
                receiver.captured_bit_rate = 0
            elif sensibility > -51:
                receiver.captured_bit_rate = 433
            else:
                receiver.captured_bit_rate = 12.23 * sensibility + 1056
        return 0

    def power_graphic_display(self, string, level):
        """
        affichage graphique de la puissance moyenne
        :param string: le fichier avec les valeurs de débit binaire
        :param level: l'étage pour lequel on veut afficher le débit
        """

        x, y, temp = np.loadtxt(string).T
        plt.scatter(x=x, y=y, c=temp, s=10, vmin=0,vmax=433)
        plt.colorbar()

        for wall in self.list_of_walls:
            if level in wall.level:
                plt.plot([wall.point1[0], wall.point2[0]], \
                         [wall.point1[1], wall.point2[1]], "k",
                         linewidth=8 * wall.thickness)

        if level == 0:
            for transmitter in self.list_of_transmitters:
                 plt.scatter(transmitter.position[0], transmitter.position[1], s=30, c="blue")
        plt.title("débit binaire de l'étage " + str(level), pad = 4)
        return 0
