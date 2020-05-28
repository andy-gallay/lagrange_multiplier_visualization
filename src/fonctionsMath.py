# fonctionMath.py
# Fichier contenant l'implémentations de différentes fonctions mathématiques pouvant être utilisées
# dans différents contextes

import numpy as np
import cmath

'''ROSENBROCK'''
def fonction_rosenbrock(x, y): # cette fonction de Rosenbrock est légèrement différente de l'originale
    return (1 - x) ** 2 + (y - x ** 2) ** 2

def gradient_rosenbrock_X(x, y):
    return (2 * x - 2 + 4 * x ** 3 - 4 * y * x)

def gradient_rosenbrock_Y(x, y):
    return (2 * y - (2 * x ** 2))

#################################

''' FONCTIONS 2 VARIABLES '''

def fonction_1(x, y):
    return (x**4 + y**4 - 4*x*y + 1)

def gradient_fonction_1_X(x, y):
    return (4*x**3 - 4*y)

def gradient_fonction_1_Y(x, y):
    return (4*y**3 - 4*x)

####

def fonction_2(x, y):
    return (4 + x**3 + y**3 - 3*x*y)

def gradient_fonction_2_X(x, y):
    return (3*x**2 - 3*y)

def gradient_fonction_2_Y(x, y):
    return (3*y**2 - 3*x)

'''FONCTION SIGMOIDE'''
def fonction_sigmoide(x):
    return 1/(1+cmath.exp(-x))

'''FONCTION DROITE'''
def fonction_droite(x):
    return x+0.5

