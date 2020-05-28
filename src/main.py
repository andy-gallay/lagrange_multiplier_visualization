# MODULES PERSONNALISES
import ellipse
import cercle
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

# NOMS POTENTIELS: LMV (pour Lagrange Multiplier Visualizer)

# TODO: trouver un nom pour le logiciel (LMV?...)

# TODO: encapsuler un maximum de code dans des fichiers .py externes
# TODO: modifier le curseur de la souris lorsqu'il est sur le plot du graphe
# TODO: transitionner vers grid() plutôt que pack() avec Tkinter
# TODO: définir des options de configurations pour le logiciel
# TODO: ajouter la langue anglaise (non prioritaire)

# TODO: [IN-PROGRESS] implémenter des nouvelles contraintes

# TODO: [DONE] effecuter du nettoyage dans le code, par exemple pour retirer les variables inutiles (globales etc)
# TODO: [DONE] définir une norme de codage pour les différents objets Tkinter (Bouton, Checkboxes, etc...)
# TODO: [DONE] implémenter les fonctions mathématiques dans un fichier secondaire (ex: fncnt.py)
# TODO: [DONE] regrouper les éléments Tkinter d'un même type ensemble (lorsque possible)
# TODO: [DONE] étoffer la partie À Propos du logiciel
# TODO: [DONE] permettre d'avoir plusieurs points critiques dessinés sur une même figure

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

        LABEL_titre = tk.Label(self, text="LMV - LAGRANGE MULTIPLIER VISUALIZER", font=LARGE_FONT)
        LABEL_titre.pack()

        LABEL_sous_titre = tk.Label(self, text="Outil de visualisation des multiplicateurs de Lagrange", font=MEDIUM_FONT)
        LABEL_sous_titre.pack(pady=10, padx=10)

        BOUTON_graphe = tk.Button(self, text="Graphe", width=30,
                                  command=lambda: controller.show_frame(PageGraphe), font=MEDIUM_FONT)
        BOUTON_graphe.pack(padx=10, pady=10)

        BOUTON_apropos = tk.Button(self, text="À propos", width=30,
                            command=lambda: controller.show_frame(PageA_Propos), font=MEDIUM_FONT)
        BOUTON_apropos.pack(padx=10, pady=10)

        BOUTON_configuration = tk.Button(self, text="Configuration", width=30,
                            command=lambda: controller.show_frame(PageConfiguration), font=MEDIUM_FONT)
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
        LABEL_description_lien = tk.Label(self, pady=10, text="Ce logiciel est open-source et libre de droit, lien du dépôt GitHub: ")
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

        global LISTE_POINTS_CRITIQUES
        LISTE_POINTS_CRITIQUES = []

        global POINT_CRITIQUE_FIG

        global LISTE_POINTS_CRITIQUES_FIGS
        LISTE_POINTS_CRITIQUES_FIGS = []

        tk.Frame.__init__(self, parent)
        LABEL_titre = tk.Label(self, text="Graphe", font=LARGE_FONT)
        LABEL_titre.pack(pady=10, padx=10)

        ###########################################
        ''' FRAMES D'INTERFACE '''

        # pack_propagate(False) permet d'éviter que la frame se redimensionne toute seule à cause des données
        # qu'elle contient

        FRAME_droite = tk.LabelFrame(self, text="Menu", padx=10, pady=10, font=MEDIUM_FONT) # Frame droite
        FRAME_droite.pack(side=tk.RIGHT)

        FRAME_options = tk.LabelFrame(FRAME_droite, text="Options", width=330, padx=10, pady=20, font=MEDIUM_FONT) # Frames des options
        FRAME_options.pack()

        FRAME_donnees = tk.LabelFrame(FRAME_droite, text="Données", padx=10, pady=20,
                                      width=330, height=230, font=MEDIUM_FONT) # Frames des données

        SUB_FRAME_donnees_curseur = tk.LabelFrame(FRAME_donnees, text="Curseur", width=110, height=80)

        SUB_FRAME_donnees_gradient_fonction = tk.LabelFrame(FRAME_donnees, text="Grdt. fonct.",
                                                           width=110, height=80, fg="blue") # Frame des coord. du gradt de la fnct

        SUB_FRAME_donnees_gradient_contrainte = tk.LabelFrame(FRAME_donnees, text="Grdt. contr.",
                                                           width=110, height=80, fg="red") # Frame des coord. du gradt. de la contr

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
        ###########################################

        f = Figure(figsize=(6, 6), dpi=100)
        a = f.add_subplot(111)

        x, y = np.meshgrid(np.linspace(-1.2, 1.2, 201), np.linspace(-1.2, 1.2, 201))
        z = fnct.fonction_rosenbrock(x, y)

        graphe = a.contour(x, y, z, 25, zorder=0)
        a.autoscale(False) # évite que le graphe se redimensionne

        # DEFINITION DES POINTS D'UNE ELLIPSE
        ellipse_data = ellipse.Ellipse(point_2d.Point_2D(0, 0), 1.0, 0.6)

        # DEFINITION DES POINTS D'UN CERCLE
        cercle_data =  cercle.Cercle(point_2d.Point_2D(0,0), 0.5)

        # DEFINITION DE LA FIGURE D'UNE ELLIPSE
        global ELLIPSE_FIGURE
        ELLIPSE_FIGURE = mpatches.Ellipse([0, 0], 1, 0.6, linewidth=1, fill=0, color="red")


        # DEFINITION DE LA FIGURE D'UN CERCLE
        global CERCLE_FIGURE
        CERCLE_FIGURE = mpatches.Circle([0, 0], 0.5, linewidth=1, fill=0, color="green")

        #####################################
        #####################################



        ListeContraintes = \
            [tk.StringVar(value="Ellipse", name="Ellipse").get(), tk.StringVar(value="Cercle", name="Cercle").get()]

        TableauContraintes = \
            [
                ELLIPSE_FIGURE,
                CERCLE_FIGURE
            ]

        global CONTRAINTE_CHOISIE
        CONTRAINTE_CHOISIE = tk.StringVar()
        CONTRAINTE_CHOISIE.set(ListeContraintes[0])

        global FIGURE_CONTRAINTE
        FIGURE_CONTRAINTE = TableauContraintes[0]

        a.add_patch(FIGURE_CONTRAINTE)

        global CONTRAINTE_PRESENTE
        CONTRAINTE_PRESENTE = True

        def RetirerContrainte():

            global ELLIPSE_FIGURE
            global CONTRAINTE_PRESENTE

            if not CONTRAINTE_PRESENTE:
                return

            FIGURE_CONTRAINTE.remove()

            CONTRAINTE_PRESENTE = False
            canvas.draw()
            return

        def AjouterContrainte():

            global FIGURE_CONTRAINTE
            global ELLIPSE_FIGURE
            global CONTRAINTE_PRESENTE

            if CONTRAINTE_PRESENTE == True:
                return

            if CONTRAINTE_PRESENTE == False:

                a.add_patch(FIGURE_CONTRAINTE)
                CONTRAINTE_PRESENTE = True
                canvas.draw()

            return


        def choix_contrainte(*args):

            global FIGURE_CONTRAINTE
            global CONTRAINTE_CHOISIE
            global CONTRAINTE_PRESENTE

            FIGURE_CONTRAINTE.remove()
            FIGURE_CONTRAINTE = TableauContraintes[ListeContraintes.index(CONTRAINTE_CHOISIE.get())]
            a.add_patch(FIGURE_CONTRAINTE)
            canvas.draw()

            CONTRAINTE_PRESENTE = True

            return

        CONTRAINTE_CHOISIE.trace("w", choix_contrainte)

        #####################################
        #####################################

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

            global LISTE_POINTS_CRITIQUES

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

            point_contrainte = POINT_ACTUEL.trouver_point_proche(ellipse_data.points_)

            fig_gradient_contrainte = mpatches.FancyArrowPatch((point_contrainte.x_, point_contrainte.y_),
                                             (ellipse_data.gradient_x(point_contrainte),
                                              ellipse_data.gradient_y(point_contrainte)),
                                             mutation_scale=8, color='r')


            if AFFICHER_GRDT_CONTRAINTE == True and POINT_ACTUEL.def_distance(point_contrainte)<0.1\
                    and CONTRAINTE_PRESENTE == True:
                a.add_patch(fig_gradient_contrainte)


            canvas.draw()

            if CONTRAINTE_CHOISIE.get() == ListeContraintes[0]:
                vecteur_gradient_contrainte = vecteur.Vecteur(point_contrainte, point_2d.Point_2D(ellipse_data.gradient_x(point_contrainte),
                                                                                              ellipse_data.gradient_y(point_contrainte)))
            if CONTRAINTE_CHOISIE.get() == ListeContraintes[1]:
                vecteur_gradient_contrainte = vecteur.Vecteur(point_contrainte, point_2d.Point_2D(cercle_data.gradient_x(point_contrainte),
                                                                                              cercle_data.gradient_y(point_contrainte)))

            vecteur_gradient_rosenbrock = vecteur.Vecteur(POINT_ACTUEL, point_2d.Point_2D(
                fnct.gradient_rosenbrock_X(POINT_ACTUEL.x_, POINT_ACTUEL.y_)
                , fnct.gradient_rosenbrock_Y(POINT_ACTUEL.x_, POINT_ACTUEL.y_)))

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

                # Si aucun point critique existant n'est proche du point critique observé
                if not point_contrainte.point_adjacent(LISTE_POINTS_CRITIQUES, 0.1):

                    # Alors on ajoute ce nouveau point critique à la liste des points critiques
                    LISTE_POINTS_CRITIQUES.append(point_contrainte)
                    # Puis on ajoute la figure représentant ce point critique à la liste des figures de points critiques
                    LISTE_POINTS_CRITIQUES_FIGS.append(a.scatter(point_contrainte.x_, point_contrainte.y_, s=20, c="cyan", zorder=3))

                canvas.draw()

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

            global LISTE_POINTS_CRITIQUES
            global LISTE_POINTS_CRITIQUES_FIGS

            if not LISTE_POINTS_CRITIQUES_FIGS:
                return
            else:
                for POINT_CRITIQUE_FIG in LISTE_POINTS_CRITIQUES_FIGS:
                    POINT_CRITIQUE_FIG.remove()

                LISTE_POINTS_CRITIQUES_FIGS.clear()
                LISTE_POINTS_CRITIQUES.clear()

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

        ''' MENUS DEROULANTS D'INTERFACE '''

        # LABEL_choix_contraintes = tk.Label(FRAME_options, text="Choix de la contrainte:")
        # MENU_DEROULANT_contraintes = tk.OptionMenu(FRAME_options, CONTRAINTE_CHOISIE, *ListeContraintes)
        # LABEL_choix_contraintes.pack()
        # MENU_DEROULANT_contraintes.pack()

        ''' ###################### '''

        ''' CHECKBOXES D'INTERFACE '''

        CHECK_aff_gradient_contrainte = tk.Checkbutton(FRAME_options, text="Afficher gradient contrainte", command=afficher_gradient_contrainte,
                                                       font=SMALL_FONT)
        CHECK_aff_gradient_contrainte.pack()

        ''' #####################  '''

        canvas.mpl_connect('motion_notify_event', Survol)

app = ModulePrincipal()
app.iconbitmap('../img/graph_icon.ico') # defining the bee icon (POLYTECHNIQUE MONTREAL)
app.wm_title("LMV")
app.mainloop()
