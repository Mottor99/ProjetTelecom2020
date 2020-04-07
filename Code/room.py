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
        ray0 = creation_ray(sous_liste_mur0)
        liste_rays.append(ray0)
        for i in liste_walls :
            sous_liste_mur1 = []
            sous_liste_mur1.append(i)
            ray1 = creation_ray(self, sous_liste_mur1)
            liste_rays.append(ray1)
            for j in liste_walls :
                if j == i :
                    continue
                sous_liste_mur2 = []
                sous_liste_mur2.append(i)
                sous_liste_mur2.append(j)
                ray2 = creation_ray(self, sous_liste_mur2)
                liste_rays.append(ray2)
                for k in liste_walls :
                    if k == i or k == j :
                        continue
                    sous_liste_mur3 = []
                    sous_liste_mur3.append(i)
                    sous_liste_mur3.append(j)
                    sous_liste_mur3.append(k)
                    ray3 = creation_ray(self, sous_liste_mur3)
                    liste_rays.append(ray3)
        return liste_rays

    def calculate(self, transmitter, receiver):

        return 0

    def affichage_graphique(self):
        return 0

    def image(self, point, mur):

        return point

    def verif_transmission(self, ray, liste_walls):
        for i in range(len(ray.liste_points)-2):
            portion_ray = Line(ray.liste_points[i],ray.liste_points[i+1])
            for j in liste_walls:
                intersection = portion_ray.intersection(j.droite)
                for k in range(len(j.points))
        return 0




    def coef_reflexion(self, mur, theta):

        return 0

    def creation_ray(self, sous_liste_mur, emetteur, recepteur):
        point = emetteur.position
        liste_images = []
        for i in sous_liste_mur:
            point = image(point, i)
            liste_images.append(point)
        for j in range len(liste_image-1):
            ray.liste_points.append(recepteur.position)
            if i == 0 :
                droite = line(recepteur.position, liste_image[len(liste_image-1)])
                point = droite.intersection(sous_liste_mur[len(liste_image-1)].droite)
                ray.liste_points.append(point)
            else :



        return 0