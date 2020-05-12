
import math

class Line:


    def __init__(self, point1, point2):
        self.point = point1
        self.norm_vector = self.dist(point1, point2)
        if self.norm_vector == 0:
            self.direction_vector = (0,0,1)
        else:
            self.direction_vector = ((point1[0] - point2[0])/self.norm_vector, (point1[1] - point2[1])/self.norm_vector, (point1[2] - point2[2])/self.norm_vector)


    def dist(self, point1, point2):
        euclidian_distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1]-point2[1])**2 + (point1[2]-point2[2])**2)
        return euclidian_distance

    def incident_angle_calculation(self, ray_line):
        # calcul de l'angle entre la normale de la droite (self) et une autre droite
        v1_x = self.direction_vector[0]
        v1_y = self.direction_vector[1]
        # norm_v_1 = self.dist((0,0), self.direction_vector)
        v2_x = ray_line.direction_vector[0]
        v2_y = ray_line.direction_vector[1]
        """norm_v_2 = self.dist((0,0), ray_line.direction_vector)
        cos_theta_i = (vx_1*vx_2+vy_1*vy_2)/norm_v_1*norm_v_2
        if cos_theta_i < 0:
            theta_i = math.pi - math.acos(cos_theta_i)
        else :
            theta_i = math.acos(cos_theta_i)"""
        cos_theta = (v1_x * v2_x + v1_y * v2_y)
        if cos_theta < 0:
            theta_i = math.acos(cos_theta) - math.pi / 2
        else:
            theta_i = math.pi / 2 - math.acos(cos_theta)

        return theta_i

    def transmitted_angle_calculation(self, wall, theta_i):

        sin_theta_t = math.sqrt(1/wall.epsilon_rel)*math.sin(theta_i)
        theta_t = math.asin(sin_theta_t)
        return theta_t

    """def equation_cartesienne(self):
    je m'appelle 
        a = (self.point1[2]-self.point2[2])/(self.point1[1]-self.point2[1])
        b = self.point1[2]-a*self.point1[1]
        return a, b;"""