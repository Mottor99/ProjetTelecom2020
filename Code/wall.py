from line import Line
import math
from math import sqrt
from transmitter import Transmitter
import cmath

class Wall:

    omega = 2 * math.pi * Transmitter.frequency
    mu0 = 4*math.pi*10**-7
    conductivity = 0.0
    epsilon_rel = 0.0
    epsilon = 0.0
    line = 0.0
    thickness = 0.0
    intrinsic_impedance = 0.0

    def __init__(self, thickness, list_of_points, material):
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
        self.line = Line(list_of_points[0], list_of_points[1])
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
        self.list_of_points = list_of_points

    def point_not_in_wall(self, point):
        A = point[0]
        B = point[1]
        v_D_x = self.line.direction_vector[0]
        point_not_in_wall = True
        if v_D_x == 0:
            for k in range(len(self.list_of_points) // 2):
                if B > self.list_of_points[2 * k][1] and B < self.list_of_points[2 * k + 1][1]:
                    point_not_in_wall = False
                    break
        else:
            for k in range(len(self.list_of_points) // 2):
                if A > self.list_of_points[2 * k][0] and A < self.list_of_points[2 * k + 1][0]:
                    point_not_in_wall = False
                    break
        return point_not_in_wall

    def entre(self, point1, point2, point3):
        entre2 = False
        if point2[0] == point3[0]:
            if (point1[1] > point2[1]) and (point1[1] < point3[1]):
                entre2 = True
        else:
            if (point1[0] > point2[0]) and (point1[0] < point3[0]):
                entre2 = True

        return entre2





