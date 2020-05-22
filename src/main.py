# MODULES PERSONNALISES
import ellipse
import point_2d
import vecteur
#######################

# MODULES EXISTANTS
from time import time
import tkinter as tk
import cmath as math
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
import numpy as np
import matplotlib
from PIL import ImageTk, Image

matplotlib.use("TkAgg")
########################

# STYLE GRAPHIQUE MATPLOTLIB
style.use("ggplot")
########################

# STYLE GRAPHIQUE TKINTER
LARGE_FONT = ("Verdana", 17)
MEDIUM_FONT = ("Verdana", 14)
SMALL_FONT = ("Verdana", 11)
########################

class ModulePrincipal(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageA_Propos, PageConfiguration, PageGraphe):

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

        path_image_lagrange = "../img/portrait_lagrange.png"
        global img_lagrange
        img_lagrange = ImageTk.PhotoImage(Image.open(path_image_lagrange))
        global label_lagrange
        label_lagrange = tk.Label(self, image=img_lagrange)
        label_lagrange.place(x=0, y=0, relwidth=1, relheight=1)

        label_titre = tk.Label(self, text="Visualisation des multiplicateurs de Lagrange", font=LARGE_FONT)
        label_titre.pack(pady=10, padx=10)

        bouton_graphe = tk.Button(self, text="Graphe", width=30,
                                  command=lambda: controller.show_frame(PageGraphe))
        bouton_graphe.pack(padx=10, pady=10)

        bouton_apropos = tk.Button(self, text="À propos", width=30,
                            command=lambda: controller.show_frame(PageA_Propos))
        bouton_apropos.pack(padx=10, pady=10)

        bouton_configuration = tk.Button(self, text="Configuration", width=30,
                            command=lambda: controller.show_frame(PageConfiguration))
        bouton_configuration.pack(padx = 10, pady = 10)

        legende_lagrange = tk.Label(self, text="Joseph-Louis Lagrange, image tirée de Wikipédia")
        legende_lagrange.pack(side=tk.BOTTOM)


class PageA_Propos(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="À propos", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        texte_a_propos = tk.Label(self, pady=10, text="Logiciel développé par Andy GALLAY - École Polytechnique de Montréal")
        texte_a_propos.pack()

        button1 = tk.Button(self, text="Menu principal",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

class PageConfiguration(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Configuration", font=LARGE_FONT, anchor='n')
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Menu principal",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

class PageGraphe(tk.Frame):

    def __init__(self, parent, controller):

        ###########################################

        # Définition de la fonction de Rosenbrock étudiée dans le graphe
        def fonction_rosenbrock(x, y):
            return (1 - x) ** 2 + (y - x ** 2) ** 2

        # Définition de la fonction permettant de calculer la position en
        # x et en y du gradient de la fonction de Rosenbrock
        def gradient_rosenbrock_X(x, y):
            return (2*x-2+4*x**3-4*y*x)

        def gradient_rosenbrock_Y(x, y):
            return (2*y-2*x**2)

        ###########################################

        global point_actuel
        point_actuel = point_2d.Point_2D(0, 0)

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graphe", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        ###########################################
        # FRAMES D'INTERFACE

        frame_droite = tk.LabelFrame(self, text="Menu", padx=10, pady=50, font=MEDIUM_FONT) # Frame droite
        frame_droite.pack(side=tk.RIGHT)

        frame_option = tk.LabelFrame(frame_droite, text="Options", padx=10, pady=50, font=MEDIUM_FONT) # Frames des options
        frame_option.pack()

        frame_donnees = tk.LabelFrame(frame_droite, text="Données", padx=10, pady=10,
                                      width=330, height=130, font=MEDIUM_FONT) # Frames des données
        frame_donnees.pack()
        frame_donnees.pack_propagate(False)

        ###########################################

        bouton_menu_principal = tk.Button(frame_option, text="Menu principal", pady=10, padx=5,
                            command=lambda: controller.show_frame(StartPage))
        bouton_menu_principal.pack()

        f = Figure(figsize=(6,6), dpi = 100)
        a = f.add_subplot(111)

        x, y = np.meshgrid(np.linspace(-1, 1, 201), np.linspace(-1, 1, 201))
        z = fonction_rosenbrock(x, y)

        graphe = a.contour(x, y, z, 30)

        # DEFINITION DES POINTS D'UNE ELLIPSE
        ellipse_data = ellipse.Ellipse(point_2d.Point_2D(0, 0), 1.0, 0.6)

        # DEFINITION DE LA FIGURE D'UNE ELLIPSE
        global ellipse_figure
        ellipse_figure = mpatches.Ellipse([0,0], 1, 0.6, linewidth=1, fill=0, color="red")
        a.add_patch(ellipse_figure)

        # Permet de tracer un cercle comme contrainte
        # global cercle
        # cercle = mpatches.Circle(xy = [0, 0], radius=0.5, fill=0, linewidth=1, color="red")
        # a.add_patch(cercle)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        canvas._tkcanvas.pack()

        ########## AJOUT/ENLEVEMENT DE CONTRAINTE ELLIPTIQUE ###########
        # La variable contrainte_presente permet d'ajouter ou de retirer
        # une contrainte, elle est globale car manipulée dans les deux
        # fonctions RetirerContrainte() et AjouterContrainte()
        global contrainte_presente
        contrainte_presente = True

        def RetirerContrainte():
            # global cercle
            global ellipse_figure
            global contrainte_presente
            # cercle.remove()
            ellipse_figure.remove()
            contrainte_presente = False
            canvas.draw()
            return

        def AjouterContrainte():
            # global cercle
            global ellipse_figure
            global contrainte_presente
            if contrainte_presente == False:
                # a.add_patch(cercle)
                a.add_patch(ellipse_figure)
                contrainte_presente = True
                canvas.draw()
            return

        Bouton_retirer = tk.Button(frame_option, text="Retirer Contrainte", pady=10, padx=5,
                                   command=RetirerContrainte)
        Bouton_ajouter = tk.Button(frame_option, text="Ajouter Contrainte", pady=10, padx=5,
                                   command=AjouterContrainte)
        Bouton_retirer.pack()
        Bouton_ajouter.pack()

        global aff_gradient_contrainte
        aff_gradient_contrainte = False

        def afficher_gradient_contrainte():
            global aff_gradient_contrainte
            if aff_gradient_contrainte == False:
                aff_gradient_contrainte = True
            else:
                aff_gradient_contrainte = False

        Bouton_ajouter_gradient_contrainte = tk.Button(frame_option, text="Afficher gradient contrainte",
                                                       command = afficher_gradient_contrainte, pady=10, padx=5)
        Bouton_ajouter_gradient_contrainte.pack()

        ###############################################################
        # VALEUR MULTIPLICATEUR DE LAGRANGE

        global valeur_multiplicateur
        valeur_multiplicateur = 0
        global label_multiplicateur
        label_multiplicateur = tk.Label(frame_donnees, text="Aucun point critique rencontré", fg="red", font=MEDIUM_FONT)
        label_multiplicateur.pack()

        global curseur_x
        global curseur_y
        global label_curseur_x
        global label_curseur_y
        curseur_x = 0
        curseur_y = 0
        label_curseur_x = tk.Label(frame_donnees, text="X: " + str(curseur_x), font=SMALL_FONT)
        label_curseur_y = tk.Label(frame_donnees, text="Y: " + str(curseur_y), font=SMALL_FONT)
        label_curseur_x.pack()
        label_curseur_y.pack()

        ###############################################################

        bouton_nettoyer_graphe = tk.Button(frame_droite, text="Nettoyer graphe", pady = 10)
        bouton_nettoyer_graphe.pack()

        ###############################################################

        global point_critique_present
        point_critique_present = False

        def Survol(event):

            if not event.inaxes: # if the mouse cursor is not on the graph, do nothing
                return

            ### VARIABLES GLOBALES ###

            global aff_gradient_contrainte
            global point_actuel # point où se trouve le curseur

            global valeur_multiplicateur
            global label_multiplicateur

            global curseur_x
            global curseur_y

            global label_curseur_x
            global label_curseur_y

            global point_critique_present

            label_curseur_x.pack_forget()
            label_curseur_y.pack_forget()
            curseur_x = np.round(event.xdata, 3)
            curseur_y = np.round(event.ydata, 3)
            label_curseur_x = tk.Label(frame_donnees, text="X: " + str(curseur_x), font=SMALL_FONT)
            label_curseur_y = tk.Label(frame_donnees, text="Y: " + str(curseur_y), font=SMALL_FONT)
            label_curseur_x.pack()
            label_curseur_y.pack()

            ##########################

            point_actuel = point_2d.Point_2D(event.xdata, event.ydata)


            fig_gradient_rosenbrock = mpatches.FancyArrowPatch((point_actuel.x_, point_actuel.y_),
                                             (gradient_rosenbrock_X(point_actuel.x_, point_actuel.y_)/5,
                                              gradient_rosenbrock_Y(point_actuel.x_, point_actuel.y_)/5),
                                             mutation_scale=15)

            a.add_patch(fig_gradient_rosenbrock)

            # point_actuel.afficher()
            point_contrainte = point_actuel.trouver_point_proche(ellipse_data.points_)

            # print("Point de l'ellipse le plus proche: ")
            # point_contrainte.afficher()

            fig_gradient_contrainte = mpatches.FancyArrowPatch((point_contrainte.x_, point_contrainte.y_),
                                             (ellipse_data.gradient_x(point_contrainte)/5,
                                              ellipse_data.gradient_y(point_contrainte)/5),
                                             mutation_scale=8, color='r')

            # gradient_contrainte = mpatches.FancyArrowPatch((point_contrainte.x_, point_contrainte.y_),
            #                                  (point_contrainte.x_+0.5, point_contrainte.y_ + 0.5),
            #                                  mutation_scale=10, color='r')

            if aff_gradient_contrainte == True and point_actuel.def_distance(point_contrainte)<0.1\
                    and contrainte_presente == True:
                a.add_patch(fig_gradient_contrainte)


            canvas.draw()

            vecteur_gradient_contrainte = vecteur.Vecteur(point_contrainte, point_2d.Point_2D(ellipse_data.gradient_x(point_contrainte),
                                                                                              ellipse_data.gradient_y(point_contrainte)))
            vecteur_gradient_rosenbrock = vecteur.Vecteur(point_actuel, point_2d.Point_2D(gradient_rosenbrock_X(point_actuel.x_, point_actuel.y_)
                                                                                          ,gradient_rosenbrock_Y(point_actuel.x_, point_actuel.y_)))

            # if vecteur_gradient_contrainte.verifier_colinearite(vecteur_gradient_rosenbrock):
            #     print("Point Critique")
            # else:
            #     print("null")

            # vecteur_gradient_contrainte.print_rapport(vecteur_gradient_rosenbrock)
            # print("Norme gradient rosenbrock: " + str(np.real(vecteur_gradient_rosenbrock.norme_)))
            # print("Norme gradient contrainte: " + str(np.real(vecteur_gradient_contrainte.norme_)))
            # print(vecteur_gradient_contrainte.verifier_colinearite(vecteur_gradient_rosenbrock))
            # vecteur_gradient_contrainte.print_multiplicateur(vecteur_gradient_rosenbrock)

            if aff_gradient_contrainte == True and vecteur_gradient_contrainte.verifier_colinearite(vecteur_gradient_rosenbrock):
                valeur_multiplicateur = np.round(vecteur_gradient_contrainte.get_multiplicateur(vecteur_gradient_rosenbrock), 2)
                label_multiplicateur.pack_forget()
                label_multiplicateur = tk.Label(frame_donnees, fg="green", text="Valeur de λ : " + str(valeur_multiplicateur), font=MEDIUM_FONT)
                label_multiplicateur.pack()

                if point_critique_present == False:
                    point_critique_present = True
                    a.scatter(point_actuel.x_, point_actuel.y_, s=25, c="red")


            fig_gradient_rosenbrock.set_visible(False)
            fig_gradient_contrainte.set_visible(False)

        cid = canvas.mpl_connect('motion_notify_event', Survol)

app = ModulePrincipal()
app.iconbitmap('../img/abeille_icon.ico') # defining the bee icon (POLYTECHNIQUE MONTREAL)
app.wm_title("Lagrange Multiplier Visualizer")
app.mainloop()
