
import math

class Line:


    def __init__(self, point1, point2):
        self.point = point1
        self.vecteur_directeur = (point1[0]-point2[0], point1[1] -point2[1])


    def dist(self, point1, point2):
        distance_euclidienne = math.sqrt((point1[0] - point2[0])**2 + (point1[1]-point2[1])**2)
        return distance_euclidienne

    def intersection(self, droite_intersectee):
        A = self.point[0]
        B = self.point[1]
        C = self.vecteur_directeur[0]
        D = self.vecteur_directeur[1]
        E = droite_intersectee.point[0]
        F = droite_intersectee.point[1]
        G = droite_intersectee.vecteur_directeur[0]
        H = droite_intersectee.vecteur_directeur[1]
        if D*G == C*H:
            x, y = -1,-1
        else:
            I = F*G - E*H - B*G + A*H
            I = I/ (D*G - C*H)
            x, y = res = tuple(map(sum, zip(self.point, tuple(i*I for i in self.vecteur_directeur))))
        return x, y;





    def incident_angle_calculation(self, ray_line):
        #calcul de l'angle entre la normale de la droite (self) et une autre droite
        vx_1 = self.vecteur_directeur[0]
        vy_1 = self.vecteur_directeur[1]
        norm_v_1 = self.dist(vx_1, vy_1)
        vx_2 = ray_line.vecteur_directeur[0]
        vy_2 = ray_line.vecteur_directeur[1]
        norm_v_2 = self.dist(vx_2, vy_2)
        cos_theta_i = (vx_1*vx_2+vy_1*vy_2)/norm_v_1*norm_v_2
        if cos_theta_i < 0:
            theta_i = math.pi - math.acos(cos_theta_i)
        else :
            theta_i = math.acos(cos_theta_i)

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