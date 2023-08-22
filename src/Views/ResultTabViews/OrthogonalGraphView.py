from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
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

    Methods
    -------
    show()
        show the view
    refresh(mGamma:list, mResults:list)
        refresh the view
    makePoints()
        make the list of points coordinates
    makeGraph()
        make the graph
    clearList()
        clear the lists xb, xg, xr, yb, yg and yr
    """

    def __init__(self, master, mGamma:list, mResults:list) -> None:
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
        self.canvasOgraph = FigureCanvasTkAgg(self.fig, master=self.master)
        self.toolbar = NavigationToolbar2Tk(self.canvasOgraph, self.master, pack_toolbar=False)
        self.toolbar.update()
        self.xb = []
        self.xg = []
        self.xr = []
        self.yb = []
        self.yg = []
        self.yr = []
        self.matrixGamma = mGamma
        self.matrixResults = mResults

    
    def show(self):
        """Show the view
        """

        self.canvasOgraph.get_tk_widget().grid(row=0,column=0, padx=10, pady=(10,0), sticky="n")
        self.toolbar.grid(row=1,column=0, padx=10, pady=(10,0), sticky="n")
        self.makePoints()
        self.makeGraph()
        self.canvasOgraph.draw()
        

    def reshresh(self, mGamma:list, mResults:list):
        """Refresh the view

        Parameters
        ----------
        mGamma : list
            the matrix gamma of PROMETHEE Gamma method
        mResults : list
            the result matrix of PROMETHEE Gamma method
        """

        self.matrixGamma = mGamma
        self.matrixResults = mResults
        self.fig.clear()
        self.makePoints()
        self.makeGraph()
        self.canvasOgraph.draw()

        
    def makePoints(self):
        """Make the list of points coordinates
        """

        self.clearList()
        for i in range(len(self.matrixGamma)):
            for j in range(len(self.matrixGamma[i])):
                if(i != j and len(self.matrixResults[i][j].split('P')) > 1):
                    self.xb.append(self.matrixGamma[i][j])
                    self.yb.append(self.matrixGamma[j][i])
                elif(i != j and len(self.matrixResults[i][j].split('I')) > 1):
                    self.xg.append(self.matrixGamma[i][j])
                    self.yg.append(self.matrixGamma[j][i])
                elif(i != j and len(self.matrixResults[i][j].split('J')) > 1):
                    self.xr.append(self.matrixGamma[i][j])
                    self.yr.append(self.matrixGamma[j][i])

    
    def makeGraph(self):
        """Make the graph
        """

        ax = self.fig.add_subplot()
        ax.plot(self.xg, self.yg, 'go',markersize=2)
        ax.plot(self.xr, self.yr, 'ro',markersize=2)
        ax.plot(self.xb, self.yb, 'bo',markersize=2)
        ax.set_xlabel('γij')
        ax.set_ylabel('γji')
        ax.axis([0, 1.2, 0, 1.2])
        ax.set_box_aspect(1.0)

        redPoints = mpatches.Circle([], 1, color="red", fill=True, label="Incomparability")
        bluePoints = mpatches.Circle([], 1, color="blue", fill=True, label="Preference")
        greenPoints = mpatches.Circle([], 1, color="green", fill=True, label="Indifference")

        ax.legend(handles=[redPoints, bluePoints, greenPoints], loc='upper right')


    def clearList(self) -> None:
        """Clear the lists xb, xg, xr, yb, yg and yr
        """
        self.xb.clear()
        self.xg.clear()
        self.xr.clear()
        self.yb.clear()
        self.yg.clear()
        self.yr.clear()


    def save(self, filename):
        self.fig.savefig(filename)