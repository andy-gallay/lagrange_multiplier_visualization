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

'''FONCTION SIGMOIDE'''
def fonction_sigmoide(x):
    return 1/(1+cmath.exp(-x))

'''FONCTION DROITE'''
def fonction_droite(x):
    return x+0.5

