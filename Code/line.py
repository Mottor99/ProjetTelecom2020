
class Line:

    a = 0.0
    b = 0.0

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.a = (self.point1[2]-self.point2[2])/(self.point1[1]-self.point2[1])
        self.b = self.point1[2]-self.a*self.point1[1]

    def intersection(self, droite_intersectee):
        if ((self.a-droite_intersectee.a)/self.a) < 0.01 :
            x = y = -1
        else :
            x = (droite_intersectee.b - self.b)/(self.a - droite_intersectee.a)
            y = self.a*x + self.b
        return x, y;


    """def equation_cartesienne(self):
    je m'appelle 
        a = (self.point1[2]-self.point2[2])/(self.point1[1]-self.point2[1])
        b = self.point1[2]-a*self.point1[1]
        return a, b;"""