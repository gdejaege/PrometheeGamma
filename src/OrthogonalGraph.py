from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *

class OrthogonalGraph:
    def __init__(self, master, gamma_matrix:list, matrix_results:list) -> None:
        self.master = master
        self.fig = Figure()
        self.gamma_matrix = gamma_matrix
        self.matrix_results = matrix_results
        self.canvas_ograph = FigureCanvasTkAgg(self.fig, master=self.master)
        toolbar = NavigationToolbar2Tk(self.canvas_ograph, self.master, pack_toolbar=False)
        toolbar.update()

        self.xb = []
        self.xv = []
        self.xr = []
        self.yb = []
        self.yv = []
        self.yr = []

        self.canvas_ograph.get_tk_widget().pack(expand=True)
        toolbar.pack(side=BOTTOM)

    
    def set_gamma_matrix_and_results(self, gamma_matrix:list, matrix_results:list):
        self.gamma_matrix = gamma_matrix
        self.matrix_results = matrix_results
        

    def show_graph(self):
        self.fig.clear()
        ax = self.fig.add_subplot()
        self.clear_list()
        
        for i in range(len(self.gamma_matrix)):
            for j in range(len(self.gamma_matrix[i])):
                if(i != j and len(self.matrix_results[i][j].split('P')) > 1):
                    self.xb.append(self.gamma_matrix[i][j])
                    self.yb.append(self.gamma_matrix[j][i])
                elif(i != j and len(self.matrix_results[i][j].split('I')) > 1):
                    self.xv.append(self.gamma_matrix[i][j])
                    self.yv.append(self.gamma_matrix[j][i])
                elif(i != j and len(self.matrix_results[i][j].split('J')) > 1):
                    self.xr.append(self.gamma_matrix[i][j])
                    self.yr.append(self.gamma_matrix[j][i])

        ax.plot(self.xv, self.yv, 'go',markersize=2)
        ax.plot(self.xr, self.yr, 'ro',markersize=2)
        ax.plot(self.xb, self.yb, 'bo',markersize=2)
        ax.set_xlabel('γij')
        ax.set_ylabel('γji')
        ax.axis([0, 1.2, 0, 1.2])
        ax.set_box_aspect(1.0)

        self.canvas_ograph.draw()


    def clear_list(self) -> None:
        self.xb.clear()
        self.xv.clear()
        self.xr.clear()
        self.yb.clear()
        self.yv.clear()
        self.yr.clear()