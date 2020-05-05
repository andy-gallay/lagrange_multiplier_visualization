import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")

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
        label = tk.Label(self, text="Configuration", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Menu principal",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

class PageGraphe(tk.Frame):

    def __init__(self, parent, controller):

        def fonction(x, y):
            return (1 - x) ** 2 + (y - x ** 2) ** 2

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graphe", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Menu principal",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(6,6), dpi = 100)
        a = f.add_subplot(111)

        x, y = np.meshgrid(np.linspace(-1, 1, 201), np.linspace(-1, 2, 201))
        z = fonction(x, y)

        graphe = a.contour(x, y, z, 20)

        # a.plot([1, 2, 3, 4, 5], [1, 7, 8, 9, 10])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack()

        def Survol(event):

            if not event.inaxes: # if the mouse cursor is not on the graph, do nothing
                return

            arrow = mpatches.FancyArrowPatch((event.xdata, event.ydata), (event.xdata+0.5, event.ydata+0.5),
                                             mutation_scale=15)

            a.add_patch(arrow)

            canvas.draw()

            print("Valeur en x", event.xdata)
            print("Valeur en y", event.ydata)

            arrow.set_visible(False)


        cid = canvas.mpl_connect('motion_notify_event', Survol)



app = ModulePrincipal()
app.iconbitmap('../img/abeille_icon.ico') # defining the bee icon (POLYTECHNIQUE MONTREAL)
app.wm_title("Lagrange Multiplier Visualizer")
app.mainloop()
