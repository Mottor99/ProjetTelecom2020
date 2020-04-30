
import math

class Line:


    def __init__(self, point1, point2):
        self.point = point1
        self.norm_vector = self.dist(point1, point2)
        if self.norm_vector == 0:
            self.direction_vector = (0, 0)
        else:
            self.direction_vector = ((point1[0] - point2[0])/self.norm_vector, (point1[1] - point2[1])/self.norm_vector)


    def dist(self, point1, point2):
        euclidian_distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1]-point2[1])**2)
        return euclidian_distance

    def intersection(self, intersected_line):
        A = self.point[0]
        B = self.point[1]
        C = self.direction_vector[0]
        D = self.direction_vector[1]
        E = intersected_line.point[0]
        F = intersected_line.point[1]
        G = intersected_line.direction_vector[0]
        H = intersected_line.direction_vector[1]
        if D*G == C*H:
            x, y = -1,-1
        else:
            I = F*G - E*H - B*G + A*H
            I = I/ (D*G - C*H)
            x, y = tuple(map(sum, zip(self.point, tuple(i*I for i in self.direction_vector))))
        return x, y;





    def incident_angle_calculation(self, ray_line):
        #calcul de l'angle entre la normale de la droite (self) et une autre droite
        vx_1 = self.direction_vector[0]
        vy_1 = self.direction_vector[1]
        #norm_v_1 = self.dist((0,0), self.direction_vector)
        vx_2 = ray_line.direction_vector[0]
        vy_2 = ray_line.direction_vector[1]
        """norm_v_2 = self.dist((0,0), ray_line.direction_vector)
        cos_theta_i = (vx_1*vx_2+vy_1*vy_2)/norm_v_1*norm_v_2
        if cos_theta_i < 0:
            theta_i = math.pi - math.acos(cos_theta_i)
        else :
            theta_i = math.acos(cos_theta_i)"""
        cos_theta = (vx_1*vx_2+vy_1*vy_2)
        if cos_theta < 0:
            theta_i = math.acos(cos_theta) - math.pi/2
        else :
            theta_i = math.pi/2 - math.acos(cos_theta)

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