import numpy as np
import point_2d
import cmath

class Vecteur:
    def __init__(self, point_origine, point_fin):
        self.point_origine_ = point_origine
        self.point_fin_ = point_fin
        self.norme_ = cmath.sqrt((self.point_origine_.x_ - self.point_fin_.x_)**2+
                                (self.point_origine_.y_ - self.point_fin_.y_)**2)
        self.x_ = self.point_fin_.x_ - self.point_origine_.x_
        self.y_ = self.point_fin_.y_ - self.point_origine_.y_

    def verifier_colinearite(self, vecteur):
        if self.x_ != 0 and self.y_ != 0:
            if np.absolute(self.x_/vecteur.x_-self.y_/vecteur.y_) <= 0.10:
                return True
            else:
                return False
        else:
            return False

    def print_rapport(self, vecteur):
        print("rapport x: " + str(self.x_/vecteur.x_))
        print("rapport y: " + str(self.y_/vecteur.y_))

    def print_multiplicateur(self, vecteur):
        print(np.real(self.norme_ / vecteur.norme_))

    def get_multiplicateur(self, vecteur):
        return np.real(self.norme_ / vecteur.norme_)