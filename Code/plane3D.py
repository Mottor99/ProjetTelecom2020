import numpy as np
import math

class Plane:
    def __init__(self, point1, point2, point3):
        self.point = point1
        self.direction_vector1 = ((point1[0] - point2[0]), (point1[1] - point2[1]), (point1[2] - point2[2]))
        self.direction_vector2 = ((point1[0] - point3[0]), (point1[1] - point3[1]), (point1[2] - point3[2]))
        self.normal_vector = np.cross(self.direction_vector1,self.direction_vector2)
        self.normal_vector = self.normal_vector/np.linalg.norm(self.normal_vector)
        self.d = np.dot(self.normal_vector, self.point)

    def intersection(self, intersected_line):
        a = np.dot(self.normal_vector, intersected_line.direction_vector)
        if a != 0:
            lam = self.d - np.dot(self.normal_vector, intersected_line.point)
            lam = lam/a
            intersection = intersected_line.point + np.dot(lam, intersected_line.direction_vector)
        else:
            intersection = (-5,-5,-5)
        return intersection

    def incident_angle_calculation(self, ray_line):
        cos_theta_i = np.dot(self.normal_vector, ray_line.direction_vector)
        if cos_theta_i < 0:
            cos_theta_i = -cos_theta_i
        if cos_theta_i > 1:
            cos_theta_i = 1
        theta_i = math.acos(cos_theta_i)
        return theta_i

    def transmitted_angle_calculation(self, wall, theta_i):
        sin_theta_t = math.sqrt(1 / wall.epsilon_rel) * math.sin(theta_i)
        theta_t = math.asin(sin_theta_t)
        return theta_t

        return theta_t