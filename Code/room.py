from wall import Wall
from transmitter import Transmitter
from receiver import Receiver
from ray import Ray
from line import Line

class Room:

    def __init__(self):
        self.liste_walls = []
        self.liste_rays = []
        self.transmitter = Transmitter((0,0), 1)
        self.receiver = Receiver((5,5), 1)


    def ray_tracing(self, transmitter, receiver, liste_walls):
        liste_rays = []
        sous_liste_mur0 = []
        ray0 = self.creation_ray(sous_liste_mur0, transmitter, receiver)
        liste_rays.append(ray0)
        for i in liste_walls :
            sous_liste_mur1 = []
            sous_liste_mur1.append(i)
            ray1 = self.creation_ray(self, sous_liste_mur1, transmitter, receiver)
            liste_rays.append(ray1)
            for j in liste_walls :
                if j == i :
                    continue
                sous_liste_mur2 = []
                sous_liste_mur2.append(i)
                sous_liste_mur2.append(j)
                ray2 = self.creation_ray(self, sous_liste_mur2, transmitter, receiver)
                liste_rays.append(ray2)
                for k in liste_walls :
                    if k == i or k == j :
                        continue
                    sous_liste_mur3 = []
                    sous_liste_mur3.append(i)
                    sous_liste_mur3.append(j)
                    sous_liste_mur3.append(k)
                    ray3 = self.creation_ray(self, sous_liste_mur3, transmitter, receiver)
                    liste_rays.append(ray3)
        return liste_rays

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
        return 0




    def reflection_coefficient(self, wall_line, ray, ray_line):
        coeff = ray.reflection_coeff_calculation(wall_line, ray_line)
        ray.coefficient_de_reflexion.append(coeff)
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