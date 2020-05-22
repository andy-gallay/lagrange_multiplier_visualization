import numpy as np
import cmath

class Point_2D:
    def __init__(self, x, y):
        self.x_ = x
        self.y_ = y

    def def_distance(self, point_a_comparer):
        distance = cmath.sqrt((self.x_-point_a_comparer.x_)**2 + (self.y_-point_a_comparer.y_)**2)
        return np.real(distance)
    
    def afficher(self):
        print("x: " + str(self.x_) + " y: " + str(self.y_))

    def trouver_point_proche(self, ensemble_points):
        distance = self.def_distance(ensemble_points[0])
        for point in ensemble_points:
            if self.def_distance(point) < distance:
                distance = self.def_distance(point)

        for point in ensemble_points:
            if self.def_distance(point) == distance:
                return point
