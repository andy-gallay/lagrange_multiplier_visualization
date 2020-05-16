import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")

import ellipse
import point_2d

import cmath as math

import matplotlib.patches as mpatches

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import matplotlib.animation as animation
from matplotlib import style

import numpy as np

style.use("ggplot")

from tkinter import ttk

LARGE_FONT = ("Verdana", 12)


class ModulePrincipal(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, A_Propos, Configuration, PageGraphe):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]  # cont is the key of the frame we want to display
        frame.tkraise()

def qf(param):
    print(param)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Visualisation des multiplicateurs de Lagrange", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="À propos",
                            command=lambda: controller.show_frame(A_Propos))
        button1.pack(padx = 10, pady = 10, side = tk.LEFT)

        button2 = tk.Button(self, text="Configuration",
                            command=lambda: controller.show_frame(Configuration))
        button2.pack(padx = 10, pady = 10, side = tk.RIGHT)

        button2 = tk.Button(self, text="Graphe",
                            command=lambda: controller.show_frame(PageGraphe))
        button2.pack(padx=10, pady=10, side=tk.RIGHT)


class A_Propos(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="À propos", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        texte_a_propos = tk.Label(self, pady=10, text="Logiciel développé par Andy GALLAY - École Polytechnique de Montréal")
        texte_a_propos.pack()

        button1 = tk.Button(self, text="Menu principal",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

class Configuration(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Configuration", font=LARGE_FONT, anchor='n')
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Menu principal",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

class PageGraphe(tk.Frame):

    def __init__(self, parent, controller):

        # METHODES POUR CALCULER COORDONNÉES CERCLE

        def cercle_x(rayon, angle):
            return rayon*math.cos(angle)

        def cercle_y(rayon, angle):
            return rayon*math.sin(angle)

        def ellipse_x(origine_x, grand_axe, angle):
            return np.absolute(origine_x+grand_axe*math.cos(angle))

        def ellipse_y(origine_y, petit_axe, angle):
            return np.absolute(origine_y+petit_axe*math.sin(angle))


        # Méthode déterminant la différence entre deux points en comparant
        # la valeur en x et en y de chaque point puis en faisant la moyenne
        # de ces deux différences
        def difference_points(point_1, point_2):
            difference_x = np.absolute(point_1.x_ - point_2.x_)
            difference_y = np.absolute(point_1.y_ - point_2.y_)
            difference_globale = (difference_x + difference_y) / 2

            return difference_globale


        # Methode retournant le point le plus proche en comparant deux points
        # à l'aide de la méthode difference_points
        def point_le_plus_proche(point, liste_point):

            minimum = 100

            for element in liste_point:
                difference = difference_points(point, element)
                if difference < minimum:
                    minimum = difference

            for element in liste_point:
                if difference_points(point, element) == minimum:
                    return element


        ###########################################

        class Point:
            def __init__(self, x, y):
                self.x_ = np.real(x)
                self.y_ = np.real(y)

            def afficher(self):
                print(str(self.x_) + "; " + str(self.y_))

        def fonction(x, y):
            return (1 - x) ** 2 + (y - x ** 2) ** 2

        def gradient_fonction_X(x, y):
            return (2*x-2+4*x**3-4*y*x)

        def gradient_fonction_Y(x, y):
            return (2*y-2*x**2)

        global point_actuel
        point_actuel = Point(0, 0)

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graphe", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Menu principal",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(6,6), dpi = 100)
        a = f.add_subplot(111)

        x, y = np.meshgrid(np.linspace(-1, 1, 201), np.linspace(-1, 1, 201))
        z = fonction(x, y)

        graphe = a.contour(x, y, z, 30)

        # a.plot([1, 2, 3, 4, 5], [1, 7, 8, 9, 10])

        points_cercle = []

        for Angle in range(360):
            point = Point(cercle_x(0.5, Angle), cercle_y(0.5, Angle))
            points_cercle.append(point)

        global cercle
        cercle = mpatches.Circle(xy = [0, 0], radius=0.5, fill=0, linewidth=1, color="red")
        a.add_patch(cercle)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack()

        ########## AJOUT/ENLEVEMENT DE CONTRAINTE CIRCULAIRE ###########
        # La variable contrainte_presente permet d'ajouter ou de retirer
        # une contrainte, elle est globale car manipulée dans les deux
        # fonctions RetirerContrainte() et AjouterContrainte()
        global contrainte_presente
        contrainte_presente = True

        def RetirerContrainte():
            global cercle
            global contrainte_presente
            cercle.remove()
            contrainte_presente = False
            canvas.draw()
            return

        def AjouterContrainte():
            global cercle
            global contrainte_presente
            if contrainte_presente == False:
                a.add_patch(cercle)
                contrainte_presente = True
                canvas.draw()
            return

        Bouton_retirer = tk.Button(self, text="Retirer Contrainte", command=RetirerContrainte)
        Bouton_ajouter = tk.Button(self, text="Ajouter Contrainte", command=AjouterContrainte)
        Bouton_retirer.pack(side=tk.RIGHT)
        Bouton_ajouter.pack(side=tk.RIGHT)

        global aff_gradient_contrainte
        aff_gradient_contrainte = False

        def afficher_gradient_contrainte():
            global aff_gradient_contrainte
            if aff_gradient_contrainte == False:
                aff_gradient_contrainte = True
            else:
                aff_gradient_contrainte = False

        Bouton_ajouter_gradient_contrainte = tk.Button(self, text="Afficher gradient contrainte", command = afficher_gradient_contrainte)
        Bouton_ajouter_gradient_contrainte.pack()

        ###############################################################



        def Survol(event):

            global aff_gradient_contrainte
            global point_actuel # point où se trouve le curseur

            point_actuel.x_ = event.xdata
            point_actuel.y_ = event.ydata

            if not event.inaxes: # if the mouse cursor is not on the graph, do nothing
                return

            arrow = mpatches.FancyArrowPatch((event.xdata, event.ydata),
                                             (gradient_fonction_X(event.xdata, event.ydata)/2.5,
                                              gradient_fonction_Y(event.xdata, event.ydata)/2.5),
                                             mutation_scale=15)

            a.add_patch(arrow)

            point_actuel.afficher()
            point_contrainte = point_le_plus_proche(point_actuel, points_cercle)

            gradient_x = 0
            gradient_y = 0

            def define_x_contrainte(x):
                return 2*x

            def define_y_contrainte(y):
                return 2*y


            gradient_contrainte = mpatches.FancyArrowPatch((point_contrainte.x_, point_contrainte.y_),
                                             (define_x_contrainte(point_contrainte.x_), define_y_contrainte(point_contrainte.y_)),
                                             mutation_scale=10, color='r')

            # gradient_contrainte = mpatches.FancyArrowPatch((point_contrainte.x_, point_contrainte.y_),
            #                                  (point_contrainte.x_+0.5, point_contrainte.y_ + 0.5),
            #                                  mutation_scale=10, color='r')

            if aff_gradient_contrainte == True:
                a.add_patch(gradient_contrainte)

            canvas.draw()

            arrow.set_visible(False)
            gradient_contrainte.set_visible(False)


        cid = canvas.mpl_connect('motion_notify_event', Survol)



app = ModulePrincipal()
app.iconbitmap('../img/abeille_icon.ico') # defining the bee icon (POLYTECHNIQUE MONTREAL)
app.wm_title("Lagrange Multiplier Visualizer")
app.mainloop()
