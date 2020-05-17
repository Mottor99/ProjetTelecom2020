
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


