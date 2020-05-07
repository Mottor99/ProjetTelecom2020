from ray3D import Ray
from line3D import Line
import copy
import math
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


class Room:

    def __init__(self):
        self.list_of_walls = []
        self.list_of_transmitters = []
        self.list_of_receivers = []
        self.direct_wave_calculated = False

    def power_distribution(self):
        for receiver in self.list_of_receivers:
            for transmitter in self.list_of_transmitters:
                list_of_rays = []
                self.ray_tracing([], 2, transmitter, receiver, self.list_of_walls, list_of_rays)
                receiver.captured_power += self.calculate(list_of_rays, transmitter, receiver)
                if (receiver == self.list_of_receivers[0]) and (transmitter == self.list_of_transmitters[0]):
                    self.graphical_display(list_of_rays)

    def ray_tracing(self, m, max_number_reflection, transmitter, receiver, list_of_walls, list_of_rays):
        if max_number_reflection != 1:
            max_number_reflection = max_number_reflection - 1
            for j in range(len(list_of_walls)):
                if len(m) == 0:
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

                sub_list_of_walls = []

                for k in l:
                    sub_list_of_walls.append(list_of_walls[k])
                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)
                if ray.list_of_points:
                    list_of_rays.append(ray)

    def printt(self, m):
        s = ""
        for i in m:
            s += str(i)
            s += " "
        return 0

    def graphical_display(self, list_of_rays):
        fig = plt.figure()
        ax = fig.gca(projection='3d')

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
        #dist12 = self.dist(wall.point1, wall.point2)
        #dist13 = self.dist(wall.point1, wall.point3)
        dist12 = 2
        dist13 = 2
        x1 = wall.point1[0]
        y1 = wall.point1[1]
        z1 = wall.point1[2]
        x2 = wall.point2[0]
        y2 = wall.point2[1]
        z2 = wall.point2[2]
        x3 = wall.point3[0]
        y3 = wall.point3[1]
        z3 = wall.point3[2]
        x21 = np.linspace(0, x2 - x1, dist12)
        x31 = np.linspace(0, x3 - x1, dist13)
        y21 = np.linspace(0, y2 - y1, dist12)
        y31 = np.linspace(0, y3 - y1, dist13)
        z21 = np.linspace(0, z2 - z1, dist12)
        z31 = np.linspace(0, z3 - z1, dist13)
        x = x1 + np.add.outer(x21, x31)
        y = y1 + np.add.outer(y21, y31)
        z = z1 + np.add.outer(z21, z31)
        ax.plot_wireframe(x, y, z, color='b')

    def calculate(self, list_of_rays, transmitter, receiver):
        average_power = 0
        for rayy in list_of_rays:
            E = math.sqrt(60 * transmitter.power * transmitter.G(rayy.phi, rayy.theta)) / rayy.distance
            hE = transmitter.he * E
            average_power = average_power + hE ** 2
            average_power = average_power / (8 * receiver.resistance)
        return average_power

    def image(self, origin_point, plane):
        lam = plane.d - np.dot(plane.normal_vector, origin_point)
        image_point = origin_point + np.dot(2 * lam, plane.normal_vector)
        return image_point

    def dist(self, point1, point2):
        euclidian_distance = math.sqrt(
            (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)
        return euclidian_distance

    def verif_transmission(self, point1, point2, ray):
        inter_walls = []
        ordre = []
        n_walls = 0
        portion_ray = Line(point1, point2)
        for j in self.list_of_walls:
            intersection = j.plane.intersection(portion_ray)
            if not j.point_not_in_wall(intersection):
                if self.entre(intersection, point1, point2):
                    inter_walls.append(j)
                    ordre.append(self.dist(intersection, point2))
                    n_walls += 1
        while n_walls != 0:
            i = np.argmax(ordre)
            ray.transmission_total_coefficient_calculation(inter_walls[i], portion_ray)
            ordre[i] = 0
            n_walls -= 1

        return 0

    def ray_creation(self, sub_list_of_walls, transmitter, receiver):
        point = transmitter.position
        list_of_images = []
        ray = Ray([])
        for wall in sub_list_of_walls:
            image_point = self.image(point, wall.plane)
            list_of_images.append(image_point)
            point = image_point
        ray.list_of_points.append(receiver.position)
        ray_point = receiver.position  # point de départ du tracé du rayon
        if sub_list_of_walls:
            ray.distance = self.dist(receiver.position, list_of_images[
                len(list_of_images) - 1])  # utile dans calcul des coeff de reflex/transm
        else:
            ray.distance = self.dist(receiver.position, transmitter.position)

        for j in range(len(list_of_images)):
            ray_line = Line(ray_point, list_of_images[len(list_of_images) - 1 - j])
            intersection_point = sub_list_of_walls[len(list_of_images) - 1 - j].plane.intersection(
                ray_line)  # point d'intersection mur/rayon
            if sub_list_of_walls[len(list_of_images) - 1 - j].point_not_in_wall(intersection_point):
                ray.list_of_points = []
                break

            if self.entre(intersection_point, ray_point, list_of_images[len(list_of_images) - 1 - j]):
                # si le point d'intersection du mur n'appartient pas au segment [image, récepteur]
                ray_point = intersection_point
                ray.list_of_points.append(ray_point)
            else:
                ray.list_of_points = []
                break

        if len(ray.list_of_points) != 0:
            ray.list_of_points.append(transmitter.position)

            vector = ray.list_of_points[len(ray.list_of_points) - 2] - np.dot(1, transmitter.position)
            rho = np.linalg.norm(vector)
            ray.theta = math.acos(vector[2] / rho)
            if vector[0] != 0:
                ray.phi = math.atan(vector[1] / vector[0])
            else:
                ray.phi = math.pi / 2

        if len(ray.list_of_points) != 0:
            self.coef_order(ray, sub_list_of_walls)
            print(ray.polarisation)

        return ray

    def entre(self, point1, point2, point3):
        entre_12 = False
        if point2[0] == point3[0]:
            if point2[1] == point3[1]:
                if (point1[2] > point2[2] and point1[2] < point3[2]) or (
                        point1[2] < point2[2] and point1[2] > point3[2]):
                    entre_12 = True
            else:
                if (point1[1] > point2[1] and point1[1] < point3[1]) or (
                        point1[1] < point2[1] and point1[1] > point3[1]):
                    entre_12 = True
        else:
            if (point1[0] > point2[0] and point1[0] < point3[0]) or (point1[0] < point2[0] and point1[0] > point3[0]):
                entre_12 = True
        return entre_12

    def coef_order(self, ray, sub_list_of_walls):
        for i in range(len(ray.list_of_points) - 1):
            self.verif_transmission(ray.list_of_points[i], ray.list_of_points[i + 1], ray)
            if i < len(ray.list_of_points) - 2:
                ray.reflection_total_coefficient_calculation(sub_list_of_walls[i],
                                                             Line(ray.list_of_points[i], ray.list_of_points[i + 1]))
                print("line")
                a = Line(ray.list_of_points[i], ray.list_of_points[i + 1])
                print(a.direction_vector)