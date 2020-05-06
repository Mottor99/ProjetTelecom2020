from ray import Ray
from line import Line
import copy
import math
import matplotlib.pyplot as plt
import numpy as np
import cmath

from scipy.stats import kde
import matplotlib.colors as colors


class Room:

    def __init__(self):
        self.list_of_walls = []
        self.list_of_transmitters = []
        self.list_of_receivers = []
        self.direct_wave_calculated = False

    def power_distribution(self, receiver_position, graphic_display_choice):
        f1 = open("debitbinaire_local.txt", "w")
        f2 = open("debitbinaire_moyen.txt", "w")
        for receiver in self.list_of_receivers:
            for transmitter in self.list_of_transmitters:
                self.direct_wave_calculated = False
                list_of_rays = []

                self.ray_tracing([], 1, transmitter, receiver, self.list_of_walls, list_of_rays)
                if "m" in graphic_display_choice:
                    receiver.captured_mean_power += self.calculate_mean(list_of_rays, transmitter)
                if "l" in graphic_display_choice:
                    receiver.captured_local_power += self.calculate_local(list_of_rays, transmitter)
                if ("r" in graphic_display_choice) and (receiver.position == receiver_position) and (
                        transmitter == self.list_of_transmitters[0]):
                    self.ray_graphical_display(receiver, transmitter, list_of_rays)

            if "l" in graphic_display_choice:
                self.end_calculate_local(receiver)
                self.power_to_bit_rate(receiver, receiver.captured_local_power)
                f1.write(str(receiver.position[0]) + " " + str(receiver.position[1]) + " " + str(
                    receiver.captured_bit_rate) + "\n")
            if "m" in graphic_display_choice:
                self.power_to_bit_rate(receiver, receiver.captured_mean_power)
                f2.write(str(receiver.position[0]) + " " + str(receiver.position[1]) + " " + str(
                    receiver.captured_bit_rate) + "\n")
            if (receiver.position == receiver_position):
                print("puissance = " + str(receiver.captured_mean_power))

        f1.close()
        f2.close()
        if "l" in graphic_display_choice:
            self.power_graphic_display("debitbinaire_local.txt")
        if "m" in graphic_display_choice:
            self.power_graphic_display("debitbinaire_moyen.txt")

    def ray_tracing(self, m, max_number_reflection, transmitter, receiver, list_of_walls, list_of_rays):
        if max_number_reflection == 0:
            sub_list_of_walls = []
            if self.direct_wave_calculated == False:
                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)  # ajout du rayon direct
                list_of_rays.append(ray)
                self.direct_wave_calculated = True

        elif max_number_reflection != 1:
            max_number_reflection = max_number_reflection - 1
            for j in range(len(list_of_walls)):
                if len(m) == 0:
                    pass
                elif j == m[len(m) - 1]:  # ne pas ajouter 2 murs identiques dans la liste de murs
                    continue
                l = copy.deepcopy(m)
                l.append(j)  # l/m = liste des indices des murs qu'on mettra dans ray_creation
                # l deepcopy de m pour qu'à l'itération suivante m ait été sauvegardé
                # self.printt(l)

                sub_list_of_walls = []
                for k in l:
                    sub_list_of_walls.append(list_of_walls[k])  # liste unique par itération
                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)
                if len(ray.list_of_points) != 0:
                    list_of_rays.append(ray)
                self.ray_tracing(l, max_number_reflection, transmitter, receiver, list_of_walls, list_of_rays)

        elif max_number_reflection == 1:
            sub_list_of_walls = []
            if self.direct_wave_calculated == False:
                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)  # ajout du rayon direct
                list_of_rays.append(ray)
                self.direct_wave_calculated = True
            for j in range(len(list_of_walls)):
                if not m:
                    pass
                elif j == m[len(m) - 1]:
                    continue
                l = copy.deepcopy(m)
                l.append(j)
                # self.printt(l)

                sub_list_of_walls = []

                for k in l:
                    sub_list_of_walls.append(list_of_walls[k])
                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)
                if ray.list_of_points:
                    list_of_rays.append(ray)

    def power_graphic_display(self, str):

        x, y, temp = np.loadtxt(str).T  # Transposed for easier unpacking
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

    def printt(self, m):
        s = ""
        for i in m:
            s += str(i)
            s += " "
        # print(s)
        return 0

    def ray_graphical_display(self, receiver, transmitter, list_of_rays):
        plt.axis([-2, 12, -2, 12])

        for ray in list_of_rays:
            self.plott(ray.list_of_points)
        for wall in self.list_of_walls:
            for i in range(len(wall.list_of_points) // 2):
                plt.plot([wall.list_of_points[2 * i][0], wall.list_of_points[2 * i + 1][0]], \
                         [wall.list_of_points[2 * i][1], wall.list_of_points[2 * i + 1][1]], "k")
        plt.scatter(receiver.position[0], receiver.position[1], s=30, c="red")
        plt.scatter(transmitter.position[0], transmitter.position[1], s=30, c="blue")
        plt.show()

        return 0

    def plott(self, list_of_points):
        X = []
        Y = []
        for i in list_of_points:
            X.append(i[0])
            Y.append(i[1])
        plt.plot(X, Y)
        return 0

    def calculate_local(self, list_of_rays, transmitter):
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
            hE = transmitter.he * E
            power += hE
        power /= 2 * math.sqrt(2) * math.sqrt(transmitter.resistance)
        return power

    def end_calculate_local(self, receiver):
        receiver.captured_local_power = (abs(receiver.captured_local_power)) ** 2
        return 0

    def calculate_mean(self, list_of_rays, transmitter):
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
            hE = transmitter.he * E
            mean_power = mean_power + hE ** 2
        mean_power = mean_power / (8 * transmitter.resistance)
        return mean_power

    def power_to_bit_rate(self, receiver, power):
        if (power == 0):
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

    def image(self, origin_point, line):
        A = origin_point[0]
        B = origin_point[1]
        C = line.direction_vector[0]
        """print(str(C) +":C")"""
        D = line.direction_vector[1]
        """print(str(D) + ":D")"""
        E = line.point[0]
        F = line.point[1]
        H = -E * D + F * C + A * D - C * B
        H = H / (D ** 2 + C ** 2)
        image_point = tuple(map(sum, zip(origin_point, (2 * H * (-1) * D, 2 * H * C))))
        # print("image")
        self.printt(image_point)

        return image_point

    def dist(self, point1, point2):
        euclidian_distance = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        return euclidian_distance

    def verif_transmission(self, ray, list_of_walls):
        for i in range(len(ray.list_of_points) - 1):
            portion_ray = Line(ray.list_of_points[i], ray.list_of_points[i + 1])
            for j in list_of_walls:
                intersection = portion_ray.intersection(j.line)
                """
                if (intersection =="""
                if not j.point_not_in_wall(intersection):
                    if self.between(intersection, ray.list_of_points[i], ray.list_of_points[i + 1]):
                        self.transmission_coefficient(j, ray, portion_ray)
                        # print("transmission")
                        self.printt(intersection)
        return 0

    def reflection_coefficient(self, wall, ray, ray_line):
        coeff = ray.reflection_coefficient_calculation(wall, ray_line)
        ray.reflection_coefficient.append(coeff)
        return 0

    def transmission_coefficient(self, wall, ray, ray_line):
        coeff = ray.transmission_coefficient_calculation(wall, ray_line)
        ray.transmission_coefficient.append(coeff)
        return 0

    def ray_creation(self, sub_list_of_walls, transmitter, receiver):
        point = transmitter.position
        list_of_images = []
        ray = Ray([])
        for wall in sub_list_of_walls:
            image_point = self.image(point, wall.line)
            """
            print("point image")
            self.printt(point_image)"""
            list_of_images.append(image_point)
            point = image_point
        ray.list_of_points.append(receiver.position)
        ray_point = receiver.position  # point de départ du tracé du rayon
        if len(sub_list_of_walls) != 0:
            ray.distance = self.dist(receiver.position, list_of_images[
                len(list_of_images) - 1])  # utile dans calcul des coeff de reflex/transm
        else:
            ray.distance = self.dist(receiver.position, transmitter.position)
        for j in range(len(list_of_images)):
            ray_line = Line(ray_point, list_of_images[len(list_of_images) - 1 - j])
            intersection_point = ray_line.intersection(
                sub_list_of_walls[len(list_of_images) - 1 - j].line)  # point d'intersection mur/rayon
            """
            print("droite mur")
            self.printt(sous_liste_mur[len(list_of_images)-1-j].droite.point)
            self.printt(sous_liste_mur[len(list_of_images) - 1 - j].droite.vecteur_directeur)
            print("intersection")
            self.printt(intersection_point)"""
            if sub_list_of_walls[len(list_of_images) - 1 - j].point_not_in_wall(intersection_point):
                # s'il y a une porte par exemple
                ray.list_of_points = []
                # print("rayon_non_admissible")
                break

            if self.between(intersection_point, ray_point, list_of_images[len(list_of_images) - 1 - j]):
                # si le point d'intersection du mur n'appartient pas au segment [image, récepteur]
                ray_point = intersection_point
                ray.list_of_points.append(ray_point)

            else:
                ray.list_of_points = []
                break
            self.reflection_coefficient(sub_list_of_walls[len(list_of_images) - 1 - j], ray, ray_line)

        if len(ray.list_of_points) != 0:
            ray.list_of_points.append(transmitter.position)

        for i in ray.list_of_points:
            """print("wop")"""
            self.printt(i)

        if len(ray.list_of_points) != 0:
            self.verif_transmission(ray, self.list_of_walls)

        return ray

    def between(self, point1, point2, point3):
        between_12 = False
        if point2[0] == point3[0]:
            if (point1[1] > point2[1] and point1[1] < point3[1]) or (point1[1] < point2[1] and point1[1] > point3[1]):
                between_12 = True
        else:
            if (point1[0] > point2[0] and point1[0] < point3[0]) or (point1[0] < point2[0] and point1[0] > point3[0]):
                between_12 = True
                """print("entre=true")"""
        return between_12