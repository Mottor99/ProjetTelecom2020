from line import Line
import math

class Wall:

    omega = 2 * math.pi * 5 * 10 ** 9
    mu0 = 4*math.pi*10**-7
    conductivite = 0.0
    permittivite_rel = 0.0
    permittivite = 0.0
    droite = 0.0
    epaisseur = 0.0

    def __init__(self, epaisseur, liste_de_points, materiau):
        if (materiau == "brique"):
            self.conductivite = 0.02
            self.permittivite_rel = 4.6
        elif (materiau == "béton"):
            self.conductivite = 0.014
            self.permittivite_rel = 5.0
        elif (materiau == "cloison"):
            self.conductivite = 0.04
            self.permittivite_rel = 2.25
        self.permittivite = self.permittivite_rel*8.854*10**(-12)
        self.epaisseur = epaisseur
        self.droite = Line(liste_de_points[0], liste_de_points[1])
        self.beta = self.omega*math.sqrt(self.mu0*self.permittivite/2)\
                    *math.sqrt(math.sqrt(1+(self.conductivite/(self.omega*self.permittivite))**2)+1)





