# MODULES PERSONNALISES
import ellipse
import point_2d
import vecteur
import fonctionsMath as fnct
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

import webbrowser

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

# Les variables globales sont en MAJUSCULE et les variables non globales utilisent la convention CamelCase

# TODO: trouver un nom pour le logiciel (LMV?...)

# TODO: effecuter du nettoyage dans le code, par exemple pour retirer les variables inutiles (globales etc)
# TODO: encapsuler un maximum de code dans des fichiers .py externes

# TODO: modifier le curseur de la souris lorsqu'il est sur le plot du graphe
# TODO: [DONE] définir une norme de codage pour les différents objets Tkinter (Bouton, Checkboxes, etc...)
# TODO: [IN-PROGRESS] implémenter les fonctions mathématiques dans un fichier secondaire (ex: fncnt.py)
# TODO: [IN-PROGRESS] implémenter des nouvelles contraintes (possiblement dans un fichier contraintes.py)
# TODO: [DONE] regrouper les éléments Tkinter d'un même type ensemble (lorsque possible)
# TODO: transitionner vers grid() plutôt que pack() avec Tkinter
# TODO: étoffer la partie À Propos du logiciel
# TODO: définir des options de configurations pour le logiciel
# TODO: ajouter la langue anglaise (non prioritaire)
# TODO: permettre d'avoir plusieurs multiplicateurs dessinés sur une même figure

# TODO: étoffer le README de GitHub pour permettre aux utilisateurs de créer un exécutable pour leur plateforme


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

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        path_image_lagrange = "../img/portrait_lagrange.png"
        global IMG_LAGRANGE
        IMG_LAGRANGE = ImageTk.PhotoImage(Image.open(path_image_lagrange))
        global LABEL_LAGRANGE
        LABEL_LAGRANGE = tk.Label(self, image=IMG_LAGRANGE)
        LABEL_LAGRANGE.place(x=0, y=0, relwidth=1, relheight=1)

        LABEL_titre = tk.Label(self, text="Visualisation des multiplicateurs de Lagrange", font=LARGE_FONT)
        LABEL_titre.pack(pady=10, padx=10)

        BOUTON_graphe = tk.Button(self, text="Graphe", width=30,
                                  command=lambda: controller.show_frame(PageGraphe))
        BOUTON_graphe.pack(padx=10, pady=10)

        BOUTON_apropos = tk.Button(self, text="À propos", width=30,
                            command=lambda: controller.show_frame(PageA_Propos))
        BOUTON_apropos.pack(padx=10, pady=10)

        BOUTON_configuration = tk.Button(self, text="Configuration", width=30,
                            command=lambda: controller.show_frame(PageConfiguration))
        BOUTON_configuration.pack(padx = 10, pady = 10)

        LABEL_texte_a_propos = tk.Label(self, pady=10,
                                        text="Logiciel développé par Andy GALLAY - École Polytechnique de Montréal - 2020",
                                        font=MEDIUM_FONT, fg="blue")

        LABEL_email = tk.Label(self, pady=10, text="andy.gallay@polymtl.ca", font=MEDIUM_FONT)

        LABEL_legende_lagrange = tk.Label(self, text="Joseph-Louis Lagrange, image tirée de Wikipédia")

        LABEL_legende_lagrange.pack(side=tk.BOTTOM)
        LABEL_email.pack(side=tk.BOTTOM)
        LABEL_texte_a_propos.pack(side=tk.BOTTOM)


class PageA_Propos(tk.Frame):

    def __init__(self, parent, controller):

        def callback(url):
            webbrowser.open_new(url)

        global LANGUE

        tk.Frame.__init__(self, parent)
        LABEL_titre = tk.Label(self, text="À propos", font=LARGE_FONT)

        LABEL_titre.pack(pady=10, padx=10)

        LABEL_texte_a_propos = tk.Label(self, pady=10, text="Logiciel développé par Andy GALLAY - École Polytechnique de Montréal", font=MEDIUM_FONT, fg="blue")
        LABEL_email = tk.Label(self, pady=10, text="andy.gallay@polymtl.ca", font=MEDIUM_FONT, fg="blue")
        LABEL_description_lien = tk.Label(self, pady=10, text="Ce logiciel est open-source, lien du dépôt GitHub: ")
        LABEL_lien_git = tk.Label(self, pady=10, text="https://github.com/andy-gallay/lagrange_multiplier_visualization",
                                  fg="blue")

        LABEL_lien_git.bind("<Button-1>", lambda e: callback("https://github.com/andy-gallay/lagrange_multiplier_visualization"))

        LABEL_texte_a_propos.pack()
        LABEL_email.pack()
        LABEL_description_lien.pack()
        LABEL_lien_git.pack()

        BUTTON_menu_principal = tk.Button(self, text="Retour Menu principal",
                            command=lambda: controller.show_frame(StartPage))
        BUTTON_menu_principal.pack()

class PageConfiguration(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Configuration", font=LARGE_FONT, anchor='n')
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Retour Menu principal",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        frame_langues = tk.LabelFrame(self, text="Langue")
        frame_langues.pack()



class PageGraphe(tk.Frame):

    def __init__(self, parent, controller):

        global POINT_ACTUEL # Point (x, y) pointé par le curseur de la souris
        POINT_ACTUEL = point_2d.Point_2D(0, 0)

        tk.Frame.__init__(self, parent)
        LABEL_titre = tk.Label(self, text="Graphe", font=LARGE_FONT)
        LABEL_titre.pack(pady=10, padx=10)

        ###########################################
        ''' FRAMES D'INTERFACE '''

        # pack_propagate(False) permet d'éviter que la frame se redimensionne toute seule à cause des données
        # qu'elle contient

        FRAME_droite = tk.LabelFrame(self, text="Menu", padx=10, pady=10, font=MEDIUM_FONT) # Frame droite
        FRAME_droite.pack(side=tk.RIGHT)

        FRAME_options = tk.LabelFrame(FRAME_droite, text="Options", padx=10, pady=10, font=MEDIUM_FONT) # Frames des options
        FRAME_options.pack()

        FRAME_donnees = tk.LabelFrame(FRAME_droite, text="Données", padx=10, pady=20,
                                      width=330, height=230, font=MEDIUM_FONT) # Frames des données

        SUB_FRAME_donnees_curseur = tk.LabelFrame(FRAME_donnees, text="Curseur", width=110, height=80)

        SUB_FRAME_donnees_gradient_fonction = tk.LabelFrame(FRAME_donnees, text="Grdt. fonct.",
                                                           width=110, height=80) # Frame des coord. du gradt de la fnct

        SUB_FRAME_donnees_gradient_contrainte = tk.LabelFrame(FRAME_donnees, text="Grdt. contr.",
                                                           width=110, height=80) # Frame des coord. du gradt. de la contr

        SUB_FRAME_donnees_gradient_contrainte.pack(side=tk.RIGHT)
        SUB_FRAME_donnees_gradient_contrainte.pack_propagate(False)

        SUB_FRAME_donnees_gradient_fonction.pack(side=tk.RIGHT)
        SUB_FRAME_donnees_gradient_fonction.pack_propagate(False)

        SUB_FRAME_donnees_curseur.pack(side=tk.RIGHT)
        SUB_FRAME_donnees_curseur.pack_propagate(False)

        FRAME_lambda = tk.LabelFrame(FRAME_droite, width=330, height=30, font=SMALL_FONT)
        FRAME_lambda.pack()
        FRAME_lambda.pack_propagate(False)

        FRAME_donnees.pack()
        FRAME_donnees.pack_propagate(False)

        ###########################################

        f = Figure(figsize=(6, 6), dpi=100)
        a = f.add_subplot(111)

        x, y = np.meshgrid(np.linspace(-1.2, 1.2, 201), np.linspace(-1.2, 1.2, 201))
        z = fnct.fonction_rosenbrock(x, y)

        graphe = a.contour(x, y, z, 40, zorder=0)
        a.autoscale(False) # évite que le graphe se redimensionne

        # DEFINITION DES POINTS D'UNE ELLIPSE
        ellipse_data = ellipse.Ellipse(point_2d.Point_2D(0, 0), 1.0, 0.6)

        # DEFINITION DE LA FIGURE D'UNE ELLIPSE
        global ELLIPSE_FIGURE
        ELLIPSE_FIGURE = mpatches.Ellipse([0, 0], 1, 0.6, linewidth=1, fill=0, color="red")
        a.add_patch(ELLIPSE_FIGURE)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        canvas._tkcanvas.pack()

        ########## AJOUT/ENLEVEMENT DE CONTRAINTE ELLIPTIQUE ###########
        # La variable contrainte_presente permet d'ajouter ou de retirer
        # une contrainte, elle est globale car manipulée dans la fonction
        # AjouterRetirerContrainte

        global CONTRAINTE_PRESENTE
        CONTRAINTE_PRESENTE = True

        def RetirerContrainte():
            # global cercle
            global ELLIPSE_FIGURE
            global CONTRAINTE_PRESENTE
            # cercle.remove()
            ELLIPSE_FIGURE.remove()
            CONTRAINTE_PRESENTE = False
            canvas.draw()
            return

        def AjouterContrainte():
            # global cercle
            global ELLIPSE_FIGURE
            global CONTRAINTE_PRESENTE
            if CONTRAINTE_PRESENTE == False:
                # a.add_patch(cercle)
                a.add_patch(ELLIPSE_FIGURE)
                CONTRAINTE_PRESENTE = True
                canvas.draw()
            return


        global AFFICHER_GRDT_CONTRAINTE
        AFFICHER_GRDT_CONTRAINTE = False

        def afficher_gradient_contrainte():
            global AFFICHER_GRDT_CONTRAINTE
            if AFFICHER_GRDT_CONTRAINTE == False:
                AFFICHER_GRDT_CONTRAINTE = True
            else:
                AFFICHER_GRDT_CONTRAINTE = False

        ###############################################################
        # VALEUR MULTIPLICATEUR DE LAGRANGE

        global VALEUR_MULTIPLICATEUR
        VALEUR_MULTIPLICATEUR = 0
        global LABEL_MULTIPLICATEUR
        LABEL_MULTIPLICATEUR = tk.Label(FRAME_lambda, text="Aucun point critique rencontré", fg="red", font=SMALL_FONT)
        LABEL_MULTIPLICATEUR.pack()

        global CURSEUR_X
        global CURSEUR_Y

        global LABEL_CURSEUR_X
        global LABEL_CURSEUR_Y

        global LABEL_GRADIENT_FONCTION_X
        global LABEL_GRADIENT_FONCTION_Y

        global LABEL_GRADIENT_CONTRAINTE_X
        global LABEL_GRADIENT_CONTRAINTE_Y

        CURSEUR_X = 0
        CURSEUR_Y = 0

        ## DONNEES CURSEUR ##
        LABEL_CURSEUR_X = tk.Label(SUB_FRAME_donnees_curseur, text="X: " + str(CURSEUR_X), font=SMALL_FONT)
        LABEL_CURSEUR_Y = tk.Label(SUB_FRAME_donnees_curseur, text="Y: " + str(CURSEUR_Y), font=SMALL_FONT)

        LABEL_CURSEUR_X.pack()
        LABEL_CURSEUR_Y.pack()
        #####################

        ## DONNEES GRADIENT FONCTION ##
        LABEL_GRADIENT_FONCTION_X = tk.Label(SUB_FRAME_donnees_gradient_fonction, text="X: " + str(0),
                                             font=SMALL_FONT)
        LABEL_GRADIENT_FONCTION_Y = tk.Label(SUB_FRAME_donnees_gradient_fonction, text="Y: " + str(0),
                                             font=SMALL_FONT)

        LABEL_GRADIENT_FONCTION_X.pack()
        LABEL_GRADIENT_FONCTION_Y.pack()
        ###############################

        ## DONNEES GRADIENT CONTRAINTE ##
        LABEL_GRADIENT_CONTRAINTE_X = tk.Label(SUB_FRAME_donnees_gradient_contrainte, text="X: " + str(0),
                                               font=SMALL_FONT)
        LABEL_GRADIENT_CONTRAINTE_Y = tk.Label(SUB_FRAME_donnees_gradient_contrainte, text="Y: " + str(0),
                                               font=SMALL_FONT)

        LABEL_GRADIENT_CONTRAINTE_X.pack()
        LABEL_GRADIENT_CONTRAINTE_Y.pack()
        #################################


        ###############################################################

        global POINT_CRITIQUE_PRESENT
        POINT_CRITIQUE_PRESENT = False

        def Survol(event):

            if not event.inaxes: # if the mouse cursor is not on the graph, do nothing
                return

            ### VARIABLES GLOBALES ###

            global AFFICHER_GRDT_CONTRAINTE
            global POINT_ACTUEL # point où se trouve le curseur

            global VALEUR_MULTIPLICATEUR
            global LABEL_MULTIPLICATEUR

            global CURSEUR_X
            global CURSEUR_Y

            global LABEL_CURSEUR_X
            global LABEL_CURSEUR_Y

            global LABEL_GRADIENT_FONCTION_X
            global LABEL_GRADIENT_FONCTION_Y

            global LABEL_GRADIENT_CONTRAINTE_X
            global LABEL_GRADIENT_CONTRAINTE_Y

            global POINT_CRITIQUE_PRESENT

            ##############################

            LABEL_CURSEUR_X.pack_forget()
            LABEL_CURSEUR_Y.pack_forget()
            CURSEUR_X = np.round(event.xdata, 3)
            CURSEUR_Y = np.round(event.ydata, 3)
            LABEL_CURSEUR_X = tk.Label(SUB_FRAME_donnees_curseur, text="X: " + str(CURSEUR_X), font=SMALL_FONT)
            LABEL_CURSEUR_Y = tk.Label(SUB_FRAME_donnees_curseur, text="Y: " + str(CURSEUR_Y), font=SMALL_FONT)
            LABEL_CURSEUR_X.pack()
            LABEL_CURSEUR_Y.pack()

            ##########################

            POINT_ACTUEL = point_2d.Point_2D(event.xdata, event.ydata)


            fig_gradient_rosenbrock = mpatches.FancyArrowPatch((POINT_ACTUEL.x_, POINT_ACTUEL.y_),
                                                               (fnct.gradient_rosenbrock_X(POINT_ACTUEL.x_, POINT_ACTUEL.y_),
                                              fnct.gradient_rosenbrock_Y(POINT_ACTUEL.x_, POINT_ACTUEL.y_)),
                                                               mutation_scale=15)

            a.add_patch(fig_gradient_rosenbrock)

            # point_actuel.afficher()
            point_contrainte = POINT_ACTUEL.trouver_point_proche(ellipse_data.points_)

            # print("Point de l'ellipse le plus proche: ")
            # point_contrainte.afficher()

            fig_gradient_contrainte = mpatches.FancyArrowPatch((point_contrainte.x_, point_contrainte.y_),
                                             (ellipse_data.gradient_x(point_contrainte),
                                              ellipse_data.gradient_y(point_contrainte)),
                                             mutation_scale=8, color='r')

            # gradient_contrainte = mpatches.FancyArrowPatch((point_contrainte.x_, point_contrainte.y_),
            #                                  (point_contrainte.x_+0.5, point_contrainte.y_ + 0.5),
            #                                  mutation_scale=10, color='r')

            if AFFICHER_GRDT_CONTRAINTE == True and POINT_ACTUEL.def_distance(point_contrainte)<0.1\
                    and CONTRAINTE_PRESENTE == True:
                a.add_patch(fig_gradient_contrainte)


            canvas.draw()

            vecteur_gradient_contrainte = vecteur.Vecteur(point_contrainte, point_2d.Point_2D(ellipse_data.gradient_x(point_contrainte),
                                                                                              ellipse_data.gradient_y(point_contrainte)))
            vecteur_gradient_rosenbrock = vecteur.Vecteur(POINT_ACTUEL, point_2d.Point_2D(fnct.gradient_rosenbrock_X(POINT_ACTUEL.x_, POINT_ACTUEL.y_)
                                                                                          , fnct.gradient_rosenbrock_Y(POINT_ACTUEL.x_, POINT_ACTUEL.y_)))

            # if vecteur_gradient_contrainte.verifier_colinearite(vecteur_gradient_rosenbrock):
            #     print("Point Critique")
            # else:
            #     print("null")

            # vecteur_gradient_contrainte.print_rapport(vecteur_gradient_rosenbrock)
            # print("Norme gradient rosenbrock: " + str(np.real(vecteur_gradient_rosenbrock.norme_)))
            # print("Norme gradient contrainte: " + str(np.real(vecteur_gradient_contrainte.norme_)))
            # print(vecteur_gradient_contrainte.verifier_colinearite(vecteur_gradient_rosenbrock))
            # vecteur_gradient_contrainte.print_multiplicateur(vecteur_gradient_rosenbrock)

            LABEL_GRADIENT_FONCTION_X.pack_forget()
            LABEL_GRADIENT_FONCTION_Y.pack_forget()
            LABEL_GRADIENT_FONCTION_X = tk.Label(SUB_FRAME_donnees_gradient_fonction,
                                                 text="X: " + str(np.round(vecteur_gradient_rosenbrock.x_, 2)),
                                                 font=SMALL_FONT)
            LABEL_GRADIENT_FONCTION_Y = tk.Label(SUB_FRAME_donnees_gradient_fonction,
                                                 text="Y: " + str(np.round(vecteur_gradient_rosenbrock.y_, 2)),
                                                 font=SMALL_FONT)
            LABEL_GRADIENT_FONCTION_X.pack()
            LABEL_GRADIENT_FONCTION_Y.pack()

            if AFFICHER_GRDT_CONTRAINTE == True and vecteur_gradient_contrainte.verifier_colinearite(vecteur_gradient_rosenbrock):
                VALEUR_MULTIPLICATEUR = np.round(vecteur_gradient_contrainte.get_multiplicateur(vecteur_gradient_rosenbrock), 2)
                LABEL_MULTIPLICATEUR.pack_forget()
                LABEL_MULTIPLICATEUR = tk.Label(FRAME_lambda, fg="green", text="Valeur approx. de λ : " + str(np.round(VALEUR_MULTIPLICATEUR, 1)), font=SMALL_FONT)
                LABEL_MULTIPLICATEUR.pack()

                LABEL_GRADIENT_CONTRAINTE_X.pack_forget()
                LABEL_GRADIENT_CONTRAINTE_Y.pack_forget()
                LABEL_GRADIENT_CONTRAINTE_X = tk.Label(SUB_FRAME_donnees_gradient_contrainte, text="X: " + str(np.round(vecteur_gradient_contrainte.x_, 2)),
                                                       font=SMALL_FONT)
                LABEL_GRADIENT_CONTRAINTE_Y = tk.Label(SUB_FRAME_donnees_gradient_contrainte, text="Y: " + str(np.round(vecteur_gradient_contrainte.y_, 2)),
                                                       font=SMALL_FONT)
                LABEL_GRADIENT_CONTRAINTE_X.pack()
                LABEL_GRADIENT_CONTRAINTE_Y.pack()

                ## PERMET D'AJOUTER UN POINT SUR LA FIGURE LORSQU'UN POINT CRITIQUE EST RENCONTRÉ
                if POINT_CRITIQUE_PRESENT == False:
                    # point_critique_present = True
                    # a.scatter(point_actuel.x_, point_actuel.y_, s=30, c="red")
                    POINT_CRITIQUE_PRESENT = True
                    global POINT_CRITIQUE_FIG
                    POINT_CRITIQUE_FIG = a.scatter(point_contrainte.x_, point_contrainte.y_, s=30, c="red")

            else:
                LABEL_MULTIPLICATEUR.pack_forget()
                LABEL_MULTIPLICATEUR = tk.Label(FRAME_lambda, fg="red",
                                                text="Le point actuel n'est pas critique", font=SMALL_FONT)
                LABEL_MULTIPLICATEUR.pack()

            fig_gradient_rosenbrock.set_visible(False)
            fig_gradient_contrainte.set_visible(False)

        def enlever_point_critique_fig():
            global POINT_CRITIQUE_PRESENT
            global POINT_CRITIQUE_FIG
            if POINT_CRITIQUE_PRESENT == True:
                POINT_CRITIQUE_PRESENT = False
                POINT_CRITIQUE_FIG.remove()
                canvas.draw()

        ''' BOUTONS D'INTERFACE '''

        BUTTON_menu_principal = tk.Button(FRAME_options, text="Retour Menu principal", pady=10, padx=5,
                            command=lambda: controller.show_frame(StartPage), width=40)
        BUTTON_menu_principal.pack()

        BUTTON_ajouter_contrainte = tk.Button(FRAME_options, text="Ajouter Contrainte", pady=10, padx=5,
                                   command=AjouterContrainte, width=40)

        BUTTON_retirer_contrainte = tk.Button(FRAME_options, text="Retirer Contrainte", pady=10, padx=5,
                                   command=RetirerContrainte, width=40)

        BUTTON_ajouter_contrainte.pack()
        BUTTON_retirer_contrainte.pack()

        BUTTON_nettoyer_graphe = tk.Button(FRAME_options, text="Nettoyer graphe", padx=5, pady=10, width=40,
                                           command=enlever_point_critique_fig)
        BUTTON_nettoyer_graphe.pack()

        ''' ###################### '''

        ''' CHECKBOXES D'INTERFACE '''

        CHECK_aff_gradient_contrainte = tk.Checkbutton(FRAME_options, text="Afficher gradient contrainte", command=afficher_gradient_contrainte,
                                                       font=SMALL_FONT)
        CHECK_aff_gradient_contrainte.pack()

        ''' #####################  '''

        cid = canvas.mpl_connect('motion_notify_event', Survol)

app = ModulePrincipal()
app.iconbitmap('../img/graph_icon.ico') # defining the bee icon (POLYTECHNIQUE MONTREAL)
app.wm_title("Lagrange Multiplier Visualizer")
app.mainloop()
