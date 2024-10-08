from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.patches as mpatches
from tkinter import *


class OrthogonalGraphView:
    """
    A class to display the orthogonal graph of results of PROMETHEE Gamma method

    Attributes
    ----------
    master : CTKFrame
        the master frame
    fig : Figure
        the matplotlib figure that will contain the orthogonal graph
    canvasOgraph : FigureCanvasTkAgg
        the canvas container that will contain the figure
    toolbar : NavigationToolbar2Tk
        the matplotlib navigation toolbar
    xb : list
        the list of x coordinates of blue points
    xg : list
        the list of x coordinates of green points
    xr : list
        the list of x coordinates of red points
    yb : list
        the list of y coordinates of blue points
    yg : list
        the list of y coordinates of green points
    yr : list
        the list of y coordinates of red points
    matrixGamma : list
        the matrix gamma of PROMETHEE Gamma method
    matrixResults : list
        the result matrix of PROMETHEE Gamma method
    """

    def __init__(self, master, mGamma: list, mResults: list, parameters: dict) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        mGamma : list
            the matrix gamma of PROMETHEE Gamma method
        mResults : list
            the result matrix of PROMETHEE Gamma method
        """
        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.fig = Figure()
        self.fig.subplots_adjust(left=0, right=1, bottom=0.1, top=0.95)
        self.canvasOgraph = FigureCanvasTkAgg(self.fig, master=self.master)
        self.toolbar = NavigationToolbar2Tk(
            self.canvasOgraph, self.master, pack_toolbar=False
        )
        self.toolbar.update()
        self.xb = []
        self.xg = []
        self.xr = []
        self.yb = []
        self.yg = []
        self.yr = []
        self.matrixGamma = mGamma
        # print(mGamma)
        self.matrixResults = mResults
        self.lines = {}
        self.parameters = parameters

    def show(self):
        """Show the view"""
        self.toolbar.pack(side="bottom")
        self.canvasOgraph.get_tk_widget().pack(expand=True, fill="both", side="bottom")
        self.makePoints()
        self.makeGraph()
        self.canvasOgraph.draw()

    def reshresh(self, mGamma: list, mResults: list, parameters: dict):
        """Refresh the view

        Parameters
        ----------
        mGamma : list
            the matrix gamma of PROMETHEE Gamma method
        mResults : list
            the result matrix of PROMETHEE Gamma method
        """
        self.matrixGamma = mGamma
        self.parameters = parameters
        self.matrixResults = mResults
        self.fig.clear()
        self.makePoints()
        self.makeLines()
        self.makeGraph()
        self.canvasOgraph.draw()

    def makeLines(self) -> None:
        if len(self.parameters) > 0:
            # Ti
            self.Ti = self.parameters["Ti"]
            self.Tj = self.parameters["Tj"]
            p = self.parameters["Pf"]
            self.Tii = self.Ti*(1-p) 
            self.Tjf = self.Tj + (1.2 - self.Tj)*p 

        return 

    def makePoints(self):
        """Make the list of points coordinates"""
        self.clearList()
        for i in range(len(self.matrixGamma)):
            for j in range(len(self.matrixGamma[i])):
                if i != j and len(self.matrixResults[i][j].split("P")) > 1:
                    self.xb.append(self.matrixGamma[i][j])
                    self.yb.append(self.matrixGamma[j][i])
                elif i != j and len(self.matrixResults[i][j].split("I")) > 1:
                    self.xg.append(self.matrixGamma[i][j])
                    self.yg.append(self.matrixGamma[j][i])
                elif i != j and len(self.matrixResults[i][j].split("J")) > 1:
                    self.xr.append(self.matrixGamma[i][j])
                    self.yr.append(self.matrixGamma[j][i])

    def makeGraph(self):
        """Make the graph"""
        ax = self.fig.add_subplot()
        ax.plot(self.xg, self.yg, "go", markersize=2)
        ax.plot(self.xr, self.yr, "ro", markersize=2)
        ax.plot(self.xb, self.yb, "bo", markersize=2)
        # Plot lines
        if len(self.parameters) > 0:
            ax.plot([0, self.Ti], [self.Tii, self.Ti], "g", )
            ax.plot([self.Tii, self.Ti], [0, self.Ti], "g", )
            ax.plot([self.Ti, self.Tj], [self.Ti, self.Tj], "black", )
            ax.plot([self.Tj, self.Tjf], [self.Tj, 1.2], "r", )
            ax.plot([self.Tj, 1.2], [self.Tj, self.Tjf], "r", )
        ax.set_xlabel("γij")
        ax.set_ylabel("γji")
        ax.set_xlabel("γij")
        ax.set_ylabel("γji")
        ax.axis([0, 1.2, 0, 1.2])
        ax.set_box_aspect(1.0)


        redPoints = mpatches.Circle(
            [], 1, color="red", fill=True, label="Incomparability"
        )
        bluePoints = mpatches.Circle([], 1, color="blue", fill=True, label="Preference")
        greenPoints = mpatches.Circle(
            [], 1, color="green", fill=True, label="Indifference"
        )

        ax.legend(handles=[redPoints, bluePoints, greenPoints], loc="upper right")

    def clearList(self) -> None:
        """Clear the lists xb, xg, xr, yb, yg and yr"""
        self.xb.clear()
        self.xg.clear()
        self.xr.clear()
        self.yb.clear()
        self.yg.clear()
        self.yr.clear()
        self.lines = {}


    def save(self, filename: str):
        """Save the graph

        Parameters
        ----------
        filename : str
            the name of the save file
        """
        self.fig.savefig(filename)
