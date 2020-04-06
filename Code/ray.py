class Ray:

    def __init__(self, liste_de_points):
        self.points = liste_de_points
        self.distance = 0
        self.angle_emetteur = 0
        self.coefficient_de_reflexion = []
        self.coefficient_de_transmission = []