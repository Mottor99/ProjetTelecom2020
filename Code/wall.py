from line import Line

class Wall:

    conductivite = 0.0
    permittivite_rel = 0.0
    permittivite = 0.0
    droite = 0.0

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

        droite = Line(liste_de_points[0], liste_de_points[1])





