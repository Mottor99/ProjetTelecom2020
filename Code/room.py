from wall import Wall
from transmitter import Transmitter
from receiver import Receiver
from ray import Ray
from line import Line
import copy
import math
import matplotlib.pyplot as plt





class Room:

    def __init__(self):
        self.list_of_walls = []
        self.liste_rays = []
        self.transmitter = Transmitter((3.0,0.0), 1)
        self.receiver = Receiver((3.0,5.0), 1)


    def ray_tracing(self, m, max_reflection, transmitter, receiver, list_of_walls):
        if max_reflection != 1:
            max_reflection = max_reflection - 1
            for j in range(len(list_of_walls)):
                if not m:
                    pass
                elif j == m[len(m) - 1]:
                    continue
                l = copy.deepcopy(m)
                l.append(j)
                self.printt(l)

                sous_liste_de_murs = []
                for k in l:
                    sous_liste_de_murs.append(list_of_walls[k])
                rayy = self.creation_ray(sous_liste_de_murs, transmitter, receiver)
                if rayy.liste_de_points:
                    self.liste_rays.append(rayy)
                self.ray_tracing(l, max_reflection, transmitter, receiver, list_of_walls)
        elif max_reflection == 1:
            for j in range(len(list_of_walls)):
                if not m:
                    pass
                elif j == m[len(m) - 1]:
                    continue
                l = copy.deepcopy(m)
                l.append(j)
                self.printt(l)

                sous_liste_de_murs = []

                for k in l:
                    sous_liste_de_murs.append(list_of_walls[k])
                rayy = self.creation_ray(sous_liste_de_murs, transmitter, receiver)
                if rayy.liste_de_points:
                    self.liste_rays.append(rayy)




    def printt(self, m):
        s = ""
        for i in m:
            s += str(i)
            s += " "
        print(s)
        return 0

    def plott(self,liste_points):
        X =[]
        Y = []
        for i in liste_points:
            X.append(i[0])
            Y.append(i[1])
        plt.plot(X,Y)
        return 0



    def calculate(self):
        average_power = 0
        for rayy in self.liste_rays:
            attenuation = 1
            for coef_ref in rayy.coefficient_de_reflexion:
                attenuation = attenuation * coef_ref
            for coef_trans in rayy.coefficient_de_transmission:
                attenuation = attenuation * coef_trans
            E = attenuation * math.sqrt(60 * self.transmitter.power) / rayy.distance
            average_power = average_power + E**2
            average_power = average_power/(8* self.receiver.resistance)
        return average_power

    def affichage_graphique(self):
        plt.axis([-2, 8, -2, 8])
        for ray in self.liste_rays:
            self.plott(ray.liste_de_points)
        for wall in self.liste_walls:
            for i in range(len(wall.liste_de_points)//2):
                plt.plot([wall.liste_de_points[2*i][0],wall.liste_de_points[2*i+1][0]],\
                         [wall.liste_de_points[2*i][1], wall.liste_de_points[2*i+1][1]], "k")
        plt.show()
        return 0




    def image(self, point_origine, droite):
        A = point_origine[0]
        B = point_origine[1]
        C = droite.vecteur_directeur[0]
        """print(str(C) +":C")"""
        D = droite.vecteur_directeur[1]
        """print(str(D) + ":D")"""
        E = droite.point[0]
        F = droite.point[1]
        H = -E*D + F*C + A*D - C * B
        H = H/(D**2 + C**2)
        point_image = tuple(map(sum, zip(point_origine, (2*H*(-1)*D,2*H*C))))
        print("image")
        self.printt(point_image)

        return point_image




    def dist(self, point1, point2):
        distance_euclidienne = math.sqrt((point1[0] - point2[0])**2 + (point1[1]-point2[1])**2)
        return distance_euclidienne


    def verif_transmission(self, ray, liste_walls):
        for i in range(len(ray.liste_de_points)-1):
            portion_ray = Line(ray.liste_de_points[i],ray.liste_de_points[i+1])
            for j in liste_walls:
                intersection = portion_ray.intersection(j.droite)
                """
                if (intersection =="""
                if not j.point_not_in_wall(intersection):
                    """
                    self.transmission_coefficient(j, ray, portion_ray)"""
                    print("transmission")
        return 0


    def reflection_coefficient(self, wall, ray, ray_line):
        coeff = ray.reflection_coefficient_calculation(wall, ray_line)
        ray.coefficient_de_reflexion.append(coeff)
        return 0

    def transmission_coefficient(self, wall, ray, ray_line):
        coeff = ray.transmission_coefficient_calculation(wall, ray_line)
        ray.coefficient_de_transmission.append(coeff)
        return 0

    def creation_ray(self, sous_liste_mur, transmitter, receiver):
        point = transmitter.position
        liste_images = []
        ray = Ray([])
        for i in sous_liste_mur:
            point_image = self.image(point, i.droite)
            """
            print("point image")
            self.printt(point_image)"""
            liste_images.append(point_image)
            point = point_image
        ray.liste_de_points.append(receiver.position)
        point_ray = receiver.position
        ray.distance = self.dist(receiver.position, liste_images[len(liste_images) - 1])
        for j in range(len(liste_images)):
            droite_ray = Line(point_ray, liste_images[len(liste_images)-1-j])
            point_intersection = droite_ray.intersection(sous_liste_mur[len(liste_images)-1-j].droite)
            """
            print("droite mur")
            self.printt(sous_liste_mur[len(liste_images)-1-j].droite.point)
            self.printt(sous_liste_mur[len(liste_images) - 1 - j].droite.vecteur_directeur)
            print("intersection")
            self.printt(point_intersection)"""
            if sous_liste_mur[len(liste_images)-1-j].point_not_in_wall(point_intersection):
                ray.liste_de_points = []
                print("rayon_non_admissible")
                break
            """
            self.reflection_coefficient(sous_liste_mur[len(liste_images)-1-j], ray, droite_ray)"""
            if self.entre(point_intersection,point_ray, liste_images[len(liste_images)-1-j]):
                point_ray = point_intersection
                ray.liste_de_points.append(point_ray)
            else:
                ray.liste_de_points = []
                break

        if ray.liste_de_points:
            ray.liste_de_points.append(transmitter.position)

        for i in ray.liste_de_points:
            print("wop")
            self.printt(i)

        if ray.liste_de_points:
            self.verif_transmission(ray, self.liste_walls)

        return ray

    def entre(self, point1, point2, point3):
        entre_12 = False
        if (point1[0]>=point2[0] and point1[0]<=point3[0]) or (point1[0]<= point2[0] and point1[0] >= point3[0]):
            if (point1[1]>=point2[1] and point1[1]<=point3[1]) or (point1[1]<= point2[1] and point1[1] >= point3[1]):
                entre_12 = True
                print("entre=true")
        return entre_12