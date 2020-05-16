import numpy as np 

class Point_2D:
    def __init__(self, x, y):
        self.x_ = x
        self.y_ = y
    
    def afficher(self):
        print("x: " + str(self.x_) + " y: " + str(self.y_))
