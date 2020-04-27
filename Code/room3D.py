
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


    def power_distribution(self):
        for receiver in self.list_of_receivers:
            for transmitter in self.list_of_transmitters:
                list_of_rays = []
                self.ray_tracing([], 3, transmitter, receiver, self.list_of_walls, list_of_rays)
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
                self.printt(l)

                sub_list_of_walls = []
                for k in l:
                    sub_list_of_walls.append(list_of_walls[k])
                ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)
                if ray.list_of_points:
                    list_of_rays.append(ray)
                self.ray_tracing(l, max_number_reflection, transmitter, receiver, list_of_walls, list_of_rays)

        elif max_number_reflection == 1:
            """
            sub_list_of_walls = []
            ray = self.ray_creation(sub_list_of_walls, transmitter, receiver)
            list_of_rays.append(ray)"""
            for j in range(len(list_of_walls)):
                if not m:
                    pass
                elif j == m[len(m) - 1]:
                    continue
                l = copy.deepcopy(m)
                l.append(j)
                self.printt(l)

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
        print(s)
        return 0

    def graphical_display(self, list_of_rays):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        for ray in list_of_rays:
            self.plott(ray.list_of_points,ax)
            """
        for wall in self.list_of_walls:
            for i in range(len(wall.list_of_points)//2):
                plt.plot([wall.list_of_points[2*i][0], wall.list_of_points[2*i+1][0]],\
                         [wall.list_of_points[2*i][1], wall.list_of_points[2*i+1][1]], "k")
                         """
        plt.show()
        return 0


    def plott(self,list_of_points,ax):
        X = []
        Y = []
        Z = []
        for i in list_of_points:
            X.append(i[0])
            Y.append(i[1])
            Z.append(i[2])
        ax.plot(X,Y,Z)
        return 0



    def calculate(self, list_of_rays, transmitter, receiver):
        average_power = 0
        for rayy in list_of_rays:
            attenuation = 1
            for coeff_ref in rayy.reflection_coefficient:
                attenuation = attenuation * coeff_ref
            for coeff_trans in rayy.transmission_coefficient:
                attenuation = attenuation * coeff_trans
            E = attenuation * math.sqrt(60 * transmitter.power) / rayy.distance
            hE = transmitter.he * E
            average_power = average_power + hE**2
            average_power = average_power/(8* receiver.resistance)
        return average_power





    def image(self, origin_point, plane):
        lam = plane.d - np.dot(plane.normal_vector,origin_point)
        image_point = origin_point + np.dot(2*lam, plane.normal_vector)
        return image_point




    def dist(self, point1, point2):
        euclidian_distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1]-point2[1])**2 +(point1[2]-point2[2])**2)
        return euclidian_distance


    def verif_transmission(self, ray, list_of_walls):
        for i in range(len(ray.list_of_points)-1):
            portion_ray = Line(ray.list_of_points[i], ray.list_of_points[i+1])
            for j in list_of_walls:
                intersection = j.plane.intersection(portion_ray)
                if not j.point_not_in_wall(intersection):
                    if self.entre(intersection, ray.list_of_points[i], ray.list_of_points[i+1]):

                        self.transmission_coefficient(j, ray, portion_ray)
                        print("transmission")
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
            image_point = self.image(point, wall.plane)
            list_of_images.append(image_point)
            point = image_point
        ray.list_of_points.append(receiver.position)
        ray_point = receiver.position #point de départ du tracé du rayon
        if sub_list_of_walls:
            ray.distance = self.dist(receiver.position, list_of_images[len(list_of_images) - 1]) #utile dans calcul des coeff de reflex/transm
        else:
            ray.distance = self.dist(receiver.position, transmitter.position)
        for j in range(len(list_of_images)):
            ray_line = Line(ray_point, list_of_images[len(list_of_images)-1-j])
            intersection_point = sub_list_of_walls[len(list_of_images) - 1 - j].plane.intersection(ray_line) #point d'intersection mur/rayon
            if sub_list_of_walls[len(list_of_images) - 1 - j].point_not_in_wall(intersection_point):
                #s'il y a une porte par exemple
                ray.list_of_points = []
                print("rayon_non_admissible")
                break

            self.reflection_coefficient(sub_list_of_walls[len(list_of_images)-1-j], ray, ray_line)
            if self.entre(intersection_point, ray_point, list_of_images[len(list_of_images)-1-j]):
                #si le point d'intersection du mur n'appartient pas au segment [image, récepteur]
                ray_point = intersection_point
                ray.list_of_points.append(ray_point)
            else:
                ray.list_of_points = []
                break

        if len(ray.list_of_points) != 0:
            ray.list_of_points.append(transmitter.position)

        for i in ray.list_of_points:
            print("wop")
            self.printt(i)

        if len(ray.list_of_points) != 0:
            self.verif_transmission(ray, self.list_of_walls)

        return ray

    def entre(self, point1, point2, point3):
        entre_12 = False
        if point2[0] == point3[0]:
            if point2[1] == point3[1]:
                if (point1[2] > point2[2] and point1[2] < point3[2]) or (point1[2] < point2[2] and point1[2] > point3[2]):
                    entre_12 = True
            else:
                if (point1[1] > point2[1] and point1[1] < point3[1]) or (point1[1] < point2[1] and point1[1] > point3[1]):
                    entre_12 = True
        else:
            if (point1[0] > point2[0] and point1[0] < point3[0]) or (point1[0] < point2[0] and point1[0] > point3[0]):
                entre_12 = True
        return entre_12