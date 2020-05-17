from line import Line
import math
from math import sqrt
from transmitter import Transmitter


class Wall:

    omega = 2 * math.pi * Transmitter.frequency
    mu0 = 4*math.pi*10**-7

    def __init__(self, thickness, list_of_points, material):
        """

        :param list_of_points: ensemble de segments parallèles (définis par 2 points) définissant le mur

        """
        if material == "brique":
            self.conductivity = 0.02
            self.epsilon_rel = 2.25
        elif material == "béton":
            self.conductivity = 0.014
            self.epsilon_rel = 5.0
        elif material == "cloison":
            self.conductivity = 0.04
            self.epsilon_rel = 2.25
        self.epsilon = self.epsilon_rel * 8.854 * 10 ** (-12)
        self.thickness = thickness
        self.line = Line(list_of_points[0], list_of_points[1])
        self.alpha = self.omega*sqrt(self.mu0 * self.epsilon / 2)\
            * sqrt(sqrt(1 + (self.conductivity / (self.omega * self.epsilon)) ** 2) - 1)
        self.beta = self.omega*sqrt(self.mu0 * self.epsilon / 2)\
            * sqrt(sqrt(1 + (self.conductivity / (self.omega * self.epsilon)) ** 2) + 1)
        self.little_gamma = complex(self.alpha, self.beta)
        self.a = (sqrt(self.mu0)/(2*sqrt(2)*(self.epsilon**2+self.conductivity**2/self.omega**2)**0.25))\
            * sqrt(4-(3*self.epsilon)/(sqrt(self.epsilon**2+self.conductivity**2/self.omega**2)))
        self.b = (sqrt(self.mu0)/(sqrt(2)*(self.epsilon**2+self.conductivity**2/self.omega**2)**0.25))\
            * sqrt(1-self.epsilon/(sqrt(self.epsilon**2+self.conductivity**2/self.omega**2)))
        self.intrinsic_impedance = complex(self.a, self.b)
        self.list_of_points = list_of_points

    def point_not_in_wall(self, point):
        """

        vérifie que le point appartient au mur, qu'il ne se trouve pas dans l'espace d'une porte par exemple

        :return: True si le point ne se trouve pas sur le mur

        """
        x1 = point[0]
        y1 = point[1]
        v_x = self.line.direction_vector[0]
        point_not_in_wall = True
        if v_x == 0:
            for k in range(len(self.list_of_points) // 2):
                if self.list_of_points[2 * k][1] <= y1 <= self.list_of_points[2 * k + 1][1]:
                    point_not_in_wall = False
                    break
        else:
            for k in range(len(self.list_of_points) // 2):
                if self.list_of_points[2 * k][0] <= x1 <= self.list_of_points[2 * k + 1][0]:
                    point_not_in_wall = False
                    break

        return point_not_in_wall
