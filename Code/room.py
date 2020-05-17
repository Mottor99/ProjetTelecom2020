from ray import Ray
from line import Line
import copy
import math
import matplotlib.pyplot as plt
import numpy as np
import cmath


class Room:

    def __init__(self):
        self.list_of_walls = []
        self.list_of_transmitters = []
        self.list_of_receivers = []
        self.direct_ray_calculated = False

    def ray_and_power_distribution(self, receiver_position, max_number_reflection, str_graphical_display):
        """
         Arguments : - receiver_position : position du récepteur pour l'affichage des rayons.
                    - max_number_reflection : nombre maximal de réflexions permises.
                    - str_graphical_display : contient "r" si on veut un affichage graphique des rayons,
                                             "m" si on veut un affichage graphique de la puissance moyenne et
                                             "l" si on veut un affichage graphique de la puissance locale.

        """

        #
        # les fichiers f1 et f2 contiendront les valeurs de débit binaire en chaque position de récepteur
        #
        f1 = open("debitbinaire_local.txt", "w")
        f2 = open("debitbinaire_moyen.txt", "w")
        for receiver in self.list_of_receivers:
            for transmitter in self.list_of_transmitters:
                self.direct_ray_calculated = False
                list_of_rays = []
                #
                # appel de la fonction récursive de ray tracing
                #
                self.ray_tracing([], max_number_reflection, transmitter, receiver, self.list_of_walls, list_of_rays)
                if "m" in str_graphical_display:
                    receiver.captured_mean_power += self.calculate_mean_power(list_of_rays, receiver, transmitter)
                if "l" in str_graphical_display:
                    receiver.captured_local_power += self.calculate_local_power(list_of_rays, receiver, transmitter)
                if ("r" in str_graphical_display) and (receiver.position == receiver_position) and \
                        (transmitter == self.list_of_transmitters[0]):
                    self.ray_graphical_display(receiver, transmitter, list_of_rays)

            if "l" in str_graphical_display:
                self.end_calculate_local(receiver)
                receiver.captured_bit_rate = self.power_to_bit_rate(receiver.captured_local_power)
                f1.write(str(receiver.position[0]) + " " + str(receiver.position[1]) + " " + str(
                    receiver.captured_bit_rate) + "\n")
            if "m" in str_graphical_display:
                receiver.captured_bit_rate = self.power_to_bit_rate(receiver.captured_mean_power)
                f2.write(str(receiver.position[0]) + " " + str(receiver.position[1]) + " " + str(
                    receiver.captured_bit_rate) + "\n")

        f1.close()
        f2.close()
        if "l" in str_graphical_display:
            self.power_graphical_display("debitbinaire_local.txt")
        if "m" in str_graphical_display:
            self.power_graphical_display("debitbinaire_moyen.txt")

    def ray_tracing(self, m, max_number_reflection, transmitter, receiver, list_of_walls, list_of_rays):
        """

        fonction récursive de ray tracing, à chaque appel de la fonction, max_number_reflecion est décrémenté d'une unité

        :param m: liste
        :param max_number_reflection: nombre maximal de réflexions permises.
        :param list_of_walls: ensemble des murs de la pièce.
        :param list_of_rays: liste qui contiendra l'ensemble des rayons.

        """
        if max_number_reflection == 0:
            # cas où on n'admet que le rayon direct
            sub_list_of_walls = []
            if self.direct_ray_calculated is False:
                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)  # création du rayon direct
                list_of_rays.append(ray)
                self.direct_ray_calculated = True

        elif max_number_reflection != 1:
            # condition où la récursivité continue à avoir lieu
            # max_number_reflection étant décrémenté pour l'itération suivante
            max_number_reflection = max_number_reflection - 1
            for j in range(len(list_of_walls)):
                if len(m) == 0:
                    pass
                elif j == m[len(m) - 1]:  # ne pas ajouter 2 murs identiques dans la liste de murs
                    continue
                copy_m = copy.deepcopy(m)
                copy_m.append(j)  # copy_m et m = listes des indices des murs qu'on mettra dans ray_creation
                                  # copy_m est une deepcopy de m pour que m soit sauvegardé d'une itération à l'autre

                sub_list_of_walls = []
                for k in copy_m:
                    sub_list_of_walls.append(list_of_walls[k])  # liste unique par itération
                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)
                if len(ray.list_of_points) != 0:
                    list_of_rays.append(ray)
                self.ray_tracing(copy_m, max_number_reflection, transmitter, receiver, list_of_walls, list_of_rays)

        elif max_number_reflection == 1:
            # dernière étape de la récursivité
            sub_list_of_walls = []
            if self.direct_ray_calculated is False:
                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)  # création du rayon direct
                list_of_rays.append(ray)
                self.direct_ray_calculated = True
            for j in range(len(list_of_walls)):
                if not m:
                    pass
                elif j == m[len(m) - 1]:
                    continue
                copy_m = copy.deepcopy(m)
                copy_m.append(j)

                sub_list_of_walls = []
                for k in copy_m:
                    sub_list_of_walls.append(list_of_walls[k])
                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)
                if ray.list_of_points:
                    list_of_rays.append(ray)

    def ray_creation(self, sub_list_of_walls, transmitter, receiver):
        """

        création de l'ensemble des rayons passant par la sub_list_of_walls et reliant transmitter à receiver

        """
        point = transmitter.position
        list_of_images = []
        ray = Ray([])
        for wall in sub_list_of_walls:
            # création de toutes les images
            image_point = self.image(point, wall.line)
            list_of_images.append(image_point)
            point = image_point
        ray.list_of_points.append(receiver.position)
        ray_point = receiver.position  # point de départ du tracé du rayon
        if len(sub_list_of_walls) != 0:
            ray.distance = self.dist(receiver.position, list_of_images[
                len(list_of_images) - 1])  # utile dans calcul des coeff de reflex/transm
        else:
            ray.distance = self.dist(receiver.position, transmitter.position)  # cas du rayon direct
        for j in range(len(list_of_images)):
            # création de l'entièreté du rayon
            ray_line = Line(ray_point, list_of_images[len(list_of_images) - 1 - j])
            intersection_point = ray_line.intersection(
                sub_list_of_walls[len(list_of_images) - 1 - j].line)  # point d'intersection mur/rayon
            if sub_list_of_walls[len(list_of_images) - 1 - j].point_not_in_wall(intersection_point):
                ray.list_of_points = []  # pas d'intersection avec le mur, rayon non comptabilisé
                break

            if self.between(intersection_point, ray_point, list_of_images[len(list_of_images) - 1 - j]):
                # vérifier que le point d'intersection appartient bien au segment [image, récepteur]
                ray_point = intersection_point
                ray.list_of_points.append(ray_point)
            else:
                ray.list_of_points = []  # rayon non comptabilisé
                break

            # calcul de chaque coefficient de réflexion du rayon
            self.reflection_coefficient_calc(sub_list_of_walls[len(list_of_images) - 1 - j], ray, ray_line)

        # point final du tracé du rayon
        if len(ray.list_of_points) != 0:
            ray.list_of_points.append(transmitter.position)

        # calcul de l'ensemble des coefficients de transmission
        if len(ray.list_of_points) != 0:
            self.verif_transmission(ray, self.list_of_walls, sub_list_of_walls)

        return ray

    def image(self, original_point, line):
        """

        renvoie l'image de original_point par symétrie orthogonale par rapport à la droite line

        """

        x1 = original_point[0]
        y1 = original_point[1]
        x2 = line.point[0]
        y2 = line.point[1]
        v_x = line.direction_vector[0]
        v_y = line.direction_vector[1]
        d = (y2 - y1) * v_x - (x2 - x1) * v_y
        v_perp = (-v_y * d, v_x * d)
        image_point = tuple(map(sum, zip(original_point, v_perp, v_perp)))
        return image_point

    def dist(self, point1, point2):
        euclidian_distance = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        return euclidian_distance

    def reflection_coefficient_calc(self, wall, ray, ray_line):
        coeff = ray.reflection_coefficient_calculation(wall, ray_line)
        ray.reflection_coefficient.append(coeff)
        return 0

    def transmission_coefficient_calc(self, wall, ray, ray_line):
        coeff = ray.transmission_coefficient_calculation(wall, ray_line)
        ray.transmission_coefficient.append(coeff)
        return 0

    def verif_transmission(self, ray, list_of_walls, sub_list_of_walls):
        T = len(sub_list_of_walls)
        for i in range(len(ray.list_of_points) - 1):
            portion_ray = Line(ray.list_of_points[i], ray.list_of_points[i + 1])
            reflection_walls = []
            if i == 0:
                if sub_list_of_walls:
                    reflection_walls.append(sub_list_of_walls[T - 1])
            elif i == len(ray.list_of_points) - 2:
                reflection_walls.append(sub_list_of_walls[0])
            else:
                reflection_walls.append(sub_list_of_walls[T - i])
                reflection_walls.append(sub_list_of_walls[T - i - 1])
            for j in list_of_walls:
                if j in reflection_walls:
                    continue
                intersection = portion_ray.intersection(j.line)
                if not j.point_not_in_wall(intersection):
                    if intersection == ray.list_of_points[i] or intersection == ray.list_of_points[i + 1]:
                        ray.list_of_points = []
                        return 0
                    if self.between(intersection, ray.list_of_points[i], ray.list_of_points[i + 1]):
                        self.transmission_coefficient_calc(j, ray, portion_ray)

        return 0

    def between(self, point1, point2, point3):
        """

        vérifie que point3 appartient au segment [point1, point2]

        :return: True si c'est le cas

        """
        point3_is_between_point1_and_point2 = False
        if point2[0] == point3[0]:
            if (point2[1] <= point1[1] <= point3[1]) or (point2[1] >= point1[1] >= point3[1]):
                point3_is_between_point1_and_point2 = True
        else:
            if (point2[0] <= point1[0] <= point3[0]) or (point2[0] >= point1[0] >= point3[0]):
                point3_is_between_point1_and_point2 = True

        return point3_is_between_point1_and_point2

    def ray_graphical_display(self, receiver, transmitter, list_of_rays):
        """

        affichage graphique de l'ensemble des rayons calculés précédemment reliant transmitter à receiver

        """
        plt.axis([-2, 14, -2, 14])

        for ray in list_of_rays:
            self.plott(ray.list_of_points)
        for wall in self.list_of_walls:
            for i in range(len(wall.list_of_points) // 2):
                plt.plot([wall.list_of_points[2 * i][0], wall.list_of_points[2 * i + 1][0]], \
                         [wall.list_of_points[2 * i][1], wall.list_of_points[2 * i + 1][1]], "k")
        plt.scatter(receiver.position[0], receiver.position[1], s=40, c="red")
        plt.scatter(transmitter.position[0], transmitter.position[1], s=40, c="blue")
        plt.show()

        return 0

    def plott(self, list_of_points):
        """

        trace des segments de droite à partir de couples de points

        """
        X = []
        Y = []
        for i in list_of_points:
            X.append(i[0])
            Y.append(i[1])
        plt.plot(X, Y)
        return 0

    def calculate_local_power(self, list_of_rays, receiver, transmitter):
        """

        calcul de la puissance locale tenant compte de l'ensemble des rayons reliant transmitter à receiver

        """
        power = 0
        for ray in list_of_rays:
            attenuation = 1
            for coeff_ref in ray.reflection_coefficient:
                attenuation = attenuation * coeff_ref
            for coeff_trans in ray.transmission_coefficient:
                attenuation = attenuation * coeff_trans
            if ray.distance == 0:
                continue
            E = attenuation * math.sqrt(60 * transmitter.gain * transmitter.power) * cmath.exp(
                -1j * ray.beta_air * ray.distance) / ray.distance
            hE = receiver.he * E
            power += hE

        power /= math.sqrt(8) * math.sqrt(transmitter.resistance)
        return power

    def end_calculate_local(self, receiver):
        """

        finit le calcul de la puissance locale

        """
        receiver.captured_local_power = (abs(receiver.captured_local_power)) ** 2
        return 0

    def calculate_mean_power(self, list_of_rays, receiver, transmitter):
        """

        calcul de la puissance moyenne tenant compte de l'ensemble des rayons reliant transmitter à receiver

        """
        mean_power = 0
        for ray in list_of_rays:
            attenuation = 1
            for coeff_ref in ray.reflection_coefficient:
                attenuation = attenuation * abs(coeff_ref)
            for coeff_trans in ray.transmission_coefficient:
                attenuation = attenuation * abs(coeff_trans)
            if ray.distance == 0:
                continue
            E = attenuation * math.sqrt(60 * transmitter.gain * transmitter.power) / ray.distance
            hE = receiver.he * E
            mean_power = mean_power + hE ** 2

        mean_power = mean_power / (8 * transmitter.resistance)
        return mean_power

    def power_to_bit_rate(self, power):
        """

        convertit la puissance (power) en débit binaire (bit_rate)

        """
        if power == 0:
            bit_rate = 0
        else:
            sensibility = 10 * math.log10(power / 10 ** -3)
            if sensibility < -82:
                bit_rate = 0
            elif sensibility > -51:
                bit_rate = 433
            else:
                bit_rate = 12.23 * sensibility + 1056
        return bit_rate

    def power_graphical_display(self, string):
        """

        affichage graphique de la puissance, moyenne ou locale en fonction du string

        """

        x, y, temp = np.loadtxt(string).T
        plt.scatter(x=x, y=y, c=temp, s=10)
        plt.colorbar()

        for wall in self.list_of_walls:
            for i in range(len(wall.list_of_points) // 2):
                plt.plot([wall.list_of_points[2 * i][0], wall.list_of_points[2 * i + 1][0]], \
                         [wall.list_of_points[2 * i][1], wall.list_of_points[2 * i + 1][1]], "k",
                         linewidth=8 * wall.thickness)
        for transmitter in self.list_of_transmitters:
            plt.scatter(transmitter.position[0], transmitter.position[1], s=30, c="blue")
        plt.show()

        return 0

