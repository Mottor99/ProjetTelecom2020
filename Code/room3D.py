from ray3D import Ray
from line3D import Line
import copy
import math
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from receiver3D import Receiver


class Room:

    def __init__(self):
        self.list_of_walls = []
        self.list_of_transmitters = []
        self.list_of_receivers = []
        self.direct_wave_calculated = False

    def power_distribution(self, etages, length, width):
        f = []
        for i in range(etages):
            doc = "debitbinaire"+str(i)+".txt"
            f.append(open(doc, "w"))
            for j in range(int(length*2.5*4/3)):
                for k in range(int(width*2.5*4/3)):
                    self.list_of_receivers.append(Receiver((k*0.3,j*0.3,1+i*2),1,i))

        for receiver in self.list_of_receivers:
            #print("postion:"+str(receiver.position))
            for transmitter in self.list_of_transmitters:
                list_of_rays = []
                self.ray_tracing([], 1, transmitter, receiver, self.list_of_walls, list_of_rays)
                receiver.captured_power += self.calculate(list_of_rays, transmitter, receiver)
                self.direct_wave_calculated = False
                if (receiver.position == (9.6,9.6,1)) and (transmitter == self.list_of_transmitters[0]):
                    self.graphical_display(list_of_rays)
            self.power_to_bit_rate(receiver, receiver.captured_power)
            f[receiver.etage].write(str(receiver.position[0]) + " " + str(receiver.position[1]) + " " + str(
                receiver.captured_bit_rate) + "\n")
        for i in range(etages):
            f[i].close()
            self.power_graphic_display("debitbinaire"+str(i)+".txt", i)


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


    def graphical_display(self, list_of_rays):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z');

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
        ax.plot(X, Y, Z,color='orange')
        return 0

    def draw_wall(self, wall, ax):
        dist12 = self.dist(wall.point1, wall.point2)
        dist13 = self.dist(wall.point1, wall.point3)
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
        #ax.plot_surface(x, y, z, color='b')

    def calculate(self, list_of_rays, transmitter, receiver):
        average_power = 0
        compteur = 0
        for rayy in list_of_rays:
            compteur += 1
            if rayy.distance == 0:
                rayy.distance = 0.1
            E = math.sqrt(transmitter.power*60 * transmitter.G(rayy.theta_emission, rayy.phi_emission)) / rayy.distance
            #print("E:"+str(E))
            hE = E * abs(np.dot(receiver.h(rayy.theta_reception,rayy.phi_reception,transmitter.frequency),rayy.polarisation))
            #print("polarisation:"+ str(rayy.polarisation))
            #print("h:"+str(receiver.h(rayy.theta_reception,rayy.phi_reception,transmitter.frequency)))
            average_power = average_power + hE ** 2
            #print("hE:"+str(hE**2))
            if receiver.position == (6,6,3):
                #print(average_power)
                a = 1
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

    def verif_transmission(self, point1, point2, ray, reflection_walls):
        inter_walls = []
        ordre = []
        n_walls = 0
        portion_ray = Line(point1, point2)

        for j in self.list_of_walls:
            if j in reflection_walls:
                continue
            intersection = j.plane.intersection(portion_ray)
            if intersection[0] == point2[0] and intersection[1] == point2[1] and intersection[2] == point2[2]:
                continue
            if not j.point_not_in_wall(intersection):
                if self.entre(intersection, point1, point2):
                    inter_walls.append(j)
                    ordre.append(self.dist(intersection, point2))
                    n_walls += 1
        while n_walls != 0:
            i = np.argmax(ordre)
            ray.transmission_total_coefficient_calculation(inter_walls[i], portion_ray)
            #print(ray.polarisation)
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

            vector_emission = ray.list_of_points[len(ray.list_of_points) - 2] - np.dot(1, transmitter.position)
            rho = np.linalg.norm(vector_emission)
            if rho == 0:
                rho = 1
            ray.theta_emission = math.acos(vector_emission[2] / rho)
            if vector_emission[0] != 0:
                ray.phi_emission = math.atan(vector_emission[1] / vector_emission[0])
            else:
                ray.phi_emission = math.pi / 2

            vector_reception = ray.list_of_points[1] - np.dot(1, ray.list_of_points[0])
            rho = np.linalg.norm(vector_reception)
            if rho ==0:
                rho = 1
            ray.theta_reception = math.acos(vector_reception[2] / rho)
            if vector_reception[0] != 0:
                ray.phi_reception = math.atan(vector_reception[1] / vector_reception[0])
            else:
                ray.phi_reception = math.pi / 2



            pol0 = math.cos(ray.theta_emission) * math.cos(ray.phi_emission)
            pol1 = math.cos(ray.theta_emission) * math.sin(ray.phi_emission)
            pol2 = math.sin(ray.theta_emission) * -1
            ray.polarisation = [pol0,pol1,pol2]
            #print(ray.polarisation)

            """
            if ray.phi_emission!=math.pi and ray.phi_emission!=0:
                ray.list_of_points = []"""


        if len(ray.list_of_points) != 0:
            self.coef_order(ray, sub_list_of_walls)

        return ray


    def entre(self, point1, point2, point3):
        entre_12 = False
        if point2[0] == point3[0]:
            if point2[1] == point3[1]:
                if (point1[2] >= point2[2] and point1[2] <= point3[2]) or (
                        point1[2] <= point2[2] and point1[2] >= point3[2]):
                    entre_12 = True
            else:
                if (point1[1] >= point2[1] and point1[1] <= point3[1]) or (
                        point1[1] <= point2[1] and point1[1] >= point3[1]):
                    entre_12 = True
        else:
            if (point1[0] >= point2[0] and point1[0] <= point3[0]) or (point1[0] <= point2[0] and point1[0] >= point3[0]):
                entre_12 = True
        return entre_12


    def coef_order(self, ray, sub_list_of_walls):
        for i in range(len(ray.list_of_points) - 1):
            reflection_walls = []
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
            if i < len(ray.list_of_points) - 2:
                ray.reflection_total_coefficient_calculation(sub_list_of_walls[i],
                                                             Line(ray.list_of_points[len(ray.list_of_points)-1-i],
                                                                  ray.list_of_points[len(ray.list_of_points)-2-i]))
                #print(ray.polarisation)

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

    def power_graphic_display(self, str, etage):

        x, y, temp = np.loadtxt(str).T  # Transposed for easier unpacking
        plt.scatter(x=x, y=y, c=temp, s=10)
        plt.colorbar()

        for wall in self.list_of_walls:
            if etage in wall.etages:
                plt.plot([wall.point1[0], wall.point2[0]], \
                         [wall.point1[1], wall.point2[1]], "k",
                         linewidth=8 * wall.thickness)

        for transmitter in self.list_of_transmitters:
            plt.scatter(transmitter.position[0], transmitter.position[1], s=30, c="blue")
        plt.show()
        return 0