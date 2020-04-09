import math

import math

class Line:

    a = 0.0
    b = 0.0

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        if (self.point1[0]-self.point2[0]) == 0:
            self.a = 100000
            self.b = point1[0]
        else:
             self.a = (self.point1[1]-self.point2[1])/(self.point1[0]-self.point2[0])
             self.b = self.point1[1]-self.a*self.point1[0]


    def intersection(self, droite_intersectee):
        if self.a == 100000:
            if droite_intersectee.a == 100000:
                x = y = -1
            else:
                x = self.b
                y = droite_intersectee.a * x + droite_intersectee.b
        elif droite_intersectee.a == 100000:
            x = droite_intersectee.b
            y = self.a * x + self.b

        elif ((self.a-droite_intersectee.a)/self.a) < 0.01 :
            x = y = -1
        else :
            x = (droite_intersectee.b - self.b)/(self.a - droite_intersectee.a)
            y = self.a*x + self.b
        return x, y;


    def incident_angle_calculation(self, ray_line):
        #calcul de l'angle entre la normale de la droite (self) et une autre droite
        m1 = self.a
        m2 = ray_line.a
        tan_theta = math.abs((m2-m1)/(1+m1*m2)) #l'angle a toujours moins de 90 degrés
        theta = math.atan(tan_theta)
        theta_i = (math.pi)/2 - theta
        return theta_i

    def transmitted_angle_calculation(self, wall, theta_i):
        sin_theta_t = math.sqrt(1/wall.permittivite_rel)*math.sin(theta_i)
        theta_t = math.asin(sin_theta_t)
        return theta_t

    """def equation_cartesienne(self):
    je m'appelle 
        a = (self.point1[2]-self.point2[2])/(self.point1[1]-self.point2[1])
        b = self.point1[2]-a*self.point1[1]
        return a, b;"""