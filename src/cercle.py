import point_2d
import numpy as np
import cmath

class Cercle:

    # DEFINITION DES COORDONNEES EN X D'UN CERCLE EN UTILISANT LA FORME POLAIRE
    def __define_x(self, angle):
        return np.absolute(self.rayon_*cmath.cos(angle)) # absolute permet d'éviter de retourner un complexe intraitable

    # DEFINITION DES COORDONNEES EN Y D'UN CERCLE EN UTILISANT LA FORME POLAIRE
    def __define_y(self, angle):
        return np.absolute(self.rayon_*cmath.sin(angle))

    def __init__(self, centre, rayon):
        self.centre_ = centre
        self.rayon_ = rayon
        self.points_ = []

        # REMPLISSABLE D'UNE LISTE CONTENANT LES 360 POINTS DU CERCLE, UTILE POUR APPROXIMATION LORS
        # DU TRACE
        for angle in range(360):
            point = point_2d.Point_2D(self.__define_x(angle), self.__define_y(angle))
            self.points_.append(point)


    def afficher(self):
        print("Cercle de centre: ")
        self.centre_.afficher()
        print("et de rayon " + str(self.rayon_))

    def gradient_x(self, point):
        return (2 * point.x_)

    def gradient_y(self, point):
        return (2 * point.y_)
