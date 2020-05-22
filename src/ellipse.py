import numpy as np 
import cmath
import point_2d

class Ellipse:

    def __define_x(self, angle):
        return np.real(self.centre_.x_ + self.grand_axe_*cmath.cos(angle))
    
    def __define_y(self, angle):
        return np.real(self.centre_.y_ + self.petit_axe_*cmath.sin(angle))
        
    def __init__(self, centre, grand_axe, petit_axe):

        self.centre_ = centre
        self.grand_axe_ = grand_axe/2
        self.petit_axe_ = petit_axe/2

        self.points_ = []

        for angle in range(360):
            point = point_2d.Point_2D(self.__define_x(angle), 
                                    self.__define_y(angle))
            self.points_.append(point)

    def afficher(self):
        print("Le centre de l'ellipse est: ")
        self.centre_.afficher()
        print("Grand axe: " + str(self.grand_axe_) + " Petit axe: " + str(self.petit_axe_))

    def gradient_x(self, point):
        return (2/self.grand_axe_**2)*point.x_

    def gradient_y(self, point):
        return (2/self.petit_axe_**2)*point.y_