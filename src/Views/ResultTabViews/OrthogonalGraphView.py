from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *

class OrthogonalGraphView:
    def __init__(self, master, mGamma:list, mResults:list) -> None:
        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.fig = Figure()
        self.canvas_ograph = FigureCanvasTkAgg(self.fig, master=self.master)
        self.toolbar = NavigationToolbar2Tk(self.canvas_ograph, self.master, pack_toolbar=False)
        self.toolbar.update()

        self.xb = []
        self.xv = []
        self.xr = []
        self.yb = []
        self.yv = []
        self.yr = []

        self.matrixGamma = mGamma
        self.matrixResults = mResults

    
    def show(self):
        self.canvas_ograph.get_tk_widget().grid(row=0,column=0, padx=10, pady=(10,0), sticky="n")
        self.toolbar.grid(row=1,column=0, padx=10, pady=(10,0), sticky="n")
        self.makePoints()
        self.makeGraph()
        self.canvas_ograph.draw()
        

    def reshresh(self, mGamma:list, mResults:list):
        self.matrixGamma = mGamma
        self.matrixResults = mResults
        self.fig.clear()
        self.makePoints()
        self.makeGraph()
        self.canvas_ograph.draw()

        
    def makePoints(self):
        self.clear_list()
        for i in range(len(self.matrixGamma)):
            for j in range(len(self.matrixGamma[i])):
                if(i != j and len(self.matrixResults[i][j].split('P')) > 1):
                    self.xb.append(self.matrixGamma[i][j])
                    self.yb.append(self.matrixGamma[j][i])
                elif(i != j and len(self.matrixResults[i][j].split('I')) > 1):
                    self.xv.append(self.matrixGamma[i][j])
                    self.yv.append(self.matrixGamma[j][i])
                elif(i != j and len(self.matrixResults[i][j].split('J')) > 1):
                    self.xr.append(self.matrixGamma[i][j])
                    self.yr.append(self.matrixGamma[j][i])

    
    def makeGraph(self):
        ax = self.fig.add_subplot()
        ax.plot(self.xv, self.yv, 'go',markersize=2)
        ax.plot(self.xr, self.yr, 'ro',markersize=2)
        ax.plot(self.xb, self.yb, 'bo',markersize=2)
        ax.set_xlabel('γij')
        ax.set_ylabel('γji')
        ax.axis([0, 1.2, 0, 1.2])
        ax.set_box_aspect(1.0)


    def clear_list(self) -> None:
        self.xb.clear()
        self.xv.clear()
        self.xr.clear()
        self.yb.clear()
        self.yv.clear()
        self.yr.clear()