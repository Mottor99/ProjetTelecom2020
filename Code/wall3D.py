from plane3D import Plane
import math
from math import sqrt
from transmitter import Transmitter
import numpy as np

class Wall:

    omega = 2 * math.pi * Transmitter.frequency
    mu0 = 4*math.pi*10**-7
    conductivity = 0.0
    epsilon_rel = 0.0
    epsilon = 0.0
    line = 0.0
    thickness = 0.0
    intrinsic_impedance = 0.0

    def __init__(self, thickness, point1, point2, point3, material,etage):
        self.etage = etage
        if (material == "brique"):
            self.conductivity = 0.02
            self.epsilon_rel = 4.6
        elif (material == "béton"):
            self.conductivity = 0.014
            self.epsilon_rel = 5.0
        elif (material == "cloison"):
            self.conductivity = 0.04
            self.epsilon_rel = 2.25
        self.epsilon = self.epsilon_rel * 8.854 * 10 ** (-12)
        self.thickness = thickness
        self.plane = Plane(point1, point2, point3)
        self.alpha = self.omega*sqrt(self.mu0 * self.epsilon / 2)\
                    *sqrt(sqrt(1 + (self.conductivity / (self.omega * self.epsilon)) ** 2) - 1)
        self.beta = self.omega*sqrt(self.mu0 * self.epsilon / 2)\
                    *sqrt(sqrt(1 + (self.conductivity / (self.omega * self.epsilon)) ** 2) + 1)
        self.little_gamma = complex(self.alpha, self.beta)
        self.a = (sqrt(self.mu0)/(2*sqrt(2)*(self.epsilon**2+self.conductivity**2/self.omega**2)**0.25))\
                    *sqrt(4-(3*self.epsilon)/(sqrt(self.epsilon**2+self.conductivity**2/self.omega**2)))
        self.b = (sqrt(self.mu0)/(sqrt(2)*(self.epsilon**2+self.conductivity**2/self.omega**2)**0.25))\
                    *sqrt(1-self.epsilon/(sqrt(self.epsilon**2+self.conductivity**2/self.omega**2)))
        self.intrinsic_impedance = complex(self.a, self.b)
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.extremite33 = np.dot(point3, self.plane.direction_vector2)
        self.extremite31 = np.dot(point1, self.plane.direction_vector2)
        self.extremite21 = np.dot(point1, self.plane.direction_vector1)
        self.extremite22 = np.dot(point2, self.plane.direction_vector1)

    def point_not_in_wall(self, point):
        point_not_in_wall = True
        a = np.dot(point, self.plane.direction_vector1)
        if (a>self.extremite21 and a<self.extremite22) or (a<self.extremite21 and a>self.extremite22):
            b = np.dot(point, self.plane.direction_vector2)
            if (b > self.extremite31 and b < self.extremite33) or (b < self.extremite31 and b > self.extremite33):
                point_not_in_wall = False
        return point_not_in_wall