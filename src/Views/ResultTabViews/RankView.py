from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
from customtkinter import (CTkFrame, CTkCheckBox, IntVar)
from Resources.ScrollableFrame import ScrollableFrame
from Views.ResultTabViews.AlternativeView import AlternativeView
from Views.ResultTabViews.VerticalLine import VerticalLine
from Views.ResultTabViews.HorizontalLine import HorizontalLine
from math import floor

SPACE = 100 # The space between the center of 2 circles that represent alternatives
RADIUS = 35 # The radius of the circle that represents an alternative


class RankView:
    """
    A class to display the rank graph of alternatives

    """

    class ViewListener:
        """
        An interface for the listener

        Methods
        -------
        checkBoxEvent()
            Handle checkBox events
        """
        def checkBoxEvent(self):
            pass

    def __init__(self, master) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        """
        self.leftFrame = CTkFrame(master, bg_color="#ffffff", fg_color="#ffffff")
        self.scrollFrame = ScrollableFrame(master)
        self.rightFrame = self.scrollFrame.frame()
        self.leftFrame.grid_columnconfigure(0, weight=1)
        self.fig = Figure()
        self.ax = None

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.leftFrame)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.leftFrame, pack_toolbar=False)
        self.toolbar.update()

        self.checkBoxList = []
        self.alternatives = {}
        self.listener = None
        self.construction = {}
        self.graph = []
        self.als = []
        self.xmin = 1000000
        self.ymin = 50
        self.xmax = 0
        self.ymax = 100


    def buildAlternativesDict(self, aList:list):
        """Build the dictionary for alternatives selection

        Parameters
        ----------
        aList : list
            the list of alternative names
        """

        self.alternatives = {}
        for a in aList:
            self.alternatives[a] = IntVar(master=self.rightFrame, value=1)


    def BuildCheckBoxes(self):
        """Build the checkBoxes for alternatives selection
        """

        self.checkBoxList.clear()
        row=0
        for key in self.alternatives.keys():
            box = CTkCheckBox(master=self.rightFrame, text=key, text_color="#000000", variable=self.alternatives[key], command=self.listener.checkBoxEvent)
            box.grid(row=row, column=0, sticky="w", padx=5, pady=(5,0))
            row+=1
            self.checkBoxList.append(box)


    def setListener(self, l:ViewListener):
        """Set the listener

        Parameters
        ----------
        l : RankView.ViewListener
            the new listener
        """

        self.listener = l


    def show(self):
        """Show the view
        """
        self.scrollFrame.place(relx=0.75, y=1, relheight=1.0, relwidth=0.25)

        self.leftFrame.place(x=1, y=1, relheight=1.0, relwidth=0.75)
        self.canvas.get_tk_widget().grid(row=0,column=0, padx=10, pady=(10,0), sticky="n")
        self.toolbar.grid(row=1,column=0, padx=10, pady=(10,0), sticky="n")


    def drawCanvas(self, r:list, matrixResults:list) -> None:
        """Display result in a schematic ranking

        Parameters
        ----------
        r : list
            ranked list of alternatives
        matrixResults : list
            the result matrix of PROMETHEE Gamma method
        """
        self.fig.clear()
        self.fig.suptitle('Rank graph', fontsize=12, fontweight='bold')
        self.ax = self.fig.add_subplot()
        self.ax.set_aspect(1)
        self.ax.axis('off')

        self.build(r)
        self.add_lines(matrixResults)
        self.canvas.draw()


    def computeSize(self, r:list):
        width = 100
        height = 100
        self.graphName = []

        h = 0
        for i in range(len(r)):
            w = 0
            row = []
            for k in range(len(r[i])):
                if self.alternatives[r[i][k]].get():
                    w += SPACE
                    row.append(r[i][k])
            if w > 0:
                h += SPACE
                self.graphName.append(row)
            if w > width:
                width = w
        if h > height:
            height = h
        
        self.ax.axis([0, width, 0, height])
        return width, height
                    

    def build(self, r:list) -> None:
        """Build the schema

        Parameters
        ----------
        r : list
            the ranked list of alternatives
        """
        (width, height) = self.computeSize(r)
        h = height - SPACE//2

        for row in self.graphName:
            length = len(row)
            if length%2 == 0:
                x = width//2 + SPACE//2 - SPACE * length//2
            else:
                x = width//2 - SPACE * floor(length/2)
            y = h
            for n in row:
                a = AlternativeView(xy=(x, y), radius=RADIUS, name=n)
                a.draw(self.ax)
                self.construction[n] = a
                self.als.append(a)
                x += SPACE
            y -= SPACE


    def add_lines(self, matrixResults:list) -> None:
        """Add plain and dash lines to the schema

        Parameters
        ----------
        matrixResults : list
            the result matrix of PROMETHEE Gamma method
        """

        for i in range(len(matrixResults)):
            for j in range(i+1, len(matrixResults)):
                x = matrixResults[i][j].split(' I ')
                y = matrixResults[i][j].split(' J ')
                if len(x) > 1 and self.alternatives[x[0]].get() and self.alternatives[x[1]].get():
                    self.draw_line(a=self.construction[x[0]], b=self.construction[x[1]])
                elif len(y) > 1 and self.alternatives[y[0]].get() and self.alternatives[y[1]].get():
                    self.draw_line(a=self.construction[y[0]], b=self.construction[y[1]], dash=True)


    def draw_line(self, a:AlternativeView, b:AlternativeView, dash=False):
        xya = a.getXY()
        xyb = b.getXY()
        if xya[1] == xyb[1]:
            # Horizontal line
            line = HorizontalLine(a, b)
            line.createLine()
            line.draw(self.ax, dash)
        else:
            line = VerticalLine(a, b)
            line.createLine(self.als)
            line.draw(self.ax, dash)