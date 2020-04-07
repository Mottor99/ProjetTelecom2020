from wall import Wall
from transmitter import Transmitter
from receiver import Receiver
from ray import Ray
from line import Line
import copy

class Room:

    def __init__(self):
        self.liste_walls = []
        self.liste_rays = []
        self.transmitter = Transmitter((0,0), 1)
        self.receiver = Receiver((5,5), 1)


    def ray_tracing(self, m, max_reflection, transmitter, receiver, liste_walls):
        if max_reflection != 1:
            max_reflection = max_reflection - 1
            for j in range(len(liste_walls)):
                repetition = False
                for h in m:
                    if h == j:
                        repetition = True
                        continue
                if repetition:
                    continue
                sous_liste_de_murs = []
                for k in m:
                    sous_liste_de_murs.append(liste_walls[k])
                self.liste_rays.append(creation_ray(sous_liste_de_murs))
                l = copy.deepcopy(m)
                l.append(j)
                ray_tracing(n, l)
        elif max_reflection == 1:
            for j in range(len(liste_walls)):
                repetition = False
                for h in m:
                    if h == j:
                        repetition = True
                        continue
                if repetition:
                    continue

                l = copy.deepcopy(m)
                l.append(j)
                sous_liste_de_murs = []
                for k in m:
                    sous_liste_de_murs.append(liste_walls[k])
                self.liste_rays.append(creation_ray(sous_liste_de_murs))


    def calculate(self, transmitter, receiver):

        return 0

    def affichage_graphique(self):
        return 0

    def image(self, point_origine, droite):
        A = point_origine[1]
        B = point_origine[2]
        point_intersection = droite.intersection(Line(point_origine, (0, (A / droite.a) + B)))
        C = point_intersection[1]
        D = point_intersection[2]
        point_image = (A + 2 * (C - A), B + 2 * (D - B))
        return point_image


    def verif_transmission(self, ray, liste_walls):
        for i in range(len(ray.liste_points)-1):
            portion_ray = Line(ray.liste_points[i],ray.liste_points[i+1])
            for j in liste_walls:
                intersection = portion_ray.intersection(j.droite)
                for k in range(len(j.points)/2):
                    if intersection[0] < wall.points[k][0] and intersection[0] > wall.points[k+1][0]:
                        reflection_coefficient(self, j.droite, ray, portion_ray)
                        break
        return 0




    def reflection_coefficient(self, wall_line, ray, ray_line):
        coeff = ray.reflection_coeff_calculation(wall_line, ray_line)
        ray.coefficient_de_reflexion.append(coeff)
        return 0

    def transmission_coefficient(self, wall_line, ray, ray_line):
        coeff = ray.transmission_coeff_calculation(wall_line, ray_line)
        ray.coefficient_de_transmission.append(coeff)
        return 0

    def creation_ray(self, sous_liste_mur, transmitter, receiver):
        point = transmitter.position
        liste_images = []
        ray = Ray([])
        for i in sous_liste_mur:
            point_image = self.image(point, i.droite)
            liste_images.append(point_image)
            point = point_image
        point_ray = receiver.position
        for j in range(len(liste_images)):
            droite_ray = Line(point_ray, liste_images[len(liste_images-1-j)])
            point_intersection = droite_ray.intersection(sous_liste_mur[len(liste_images-1-j)].droite)
            if (sous_liste_mur[len(liste_images-1-j)].point_not_in_wall(point_intersection)):
                ray.liste_de_points = []
                break
            self.reflection_coefficient(sous_liste_mur[len(liste_images-1-j)].droite, ray, droite_ray)
            ray.liste_de_points.append(point_ray)
            point_ray = point_intersection

        self.verif_transmission(ray, self.liste_walls)

        return ray