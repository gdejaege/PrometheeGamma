from customtkinter import (CTkCanvas, CTkScrollbar)
from tkinter import *
from Views.ResultTabViews.AlternativeView import AlternativeView

class RankView:
    class ViewListener:
        def getRankedAlternatives(self):
            pass
        def getMatrixResults(self):
            pass

    def __init__(self, master) -> None:
        self.master = master
        self.size = 100
        self.canvas=CTkCanvas(master, bg='#FFFFFF', width=750, height=550, scrollregion=(0,0,100,100))
        self.hbar=CTkScrollbar(master, orientation=HORIZONTAL, command=self.canvas.xview)
        self.vbar=CTkScrollbar(master, orientation=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        #master.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        self.listener = None
        self.construction = {}


    def setListener(self, l:ViewListener):
        self.listener = l
        

    def show(self):
        self.hbar.pack(side=BOTTOM, fill=X)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.drawCanvas()


    def refresh(self):
        self.drawCanvas()


    def resizeCanvas(self, size:int):
        self.size = size+100
        self.canvas.config(scrollregion=(0, 0, self.size, self.size))


    def drawCanvas(self) -> None:
        """
        Display result in a schematic ranking
        """
        self.canvas.delete('all')
        #size : self.tab_rank.winfo_screenwidth()
        self.build()
        self.add_lines()


    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")


    def build(self) -> None:
        """
        Build the schema
        """
        r = self.listener.getRankedAlternatives()
        for i in range(len(r)):
            y = (i+1)*80
            x = self.size//2 - (len(r[i])-1)*40
            for j in range(len(r[i])):
                self.construction[r[i][j]] = AlternativeView(r[i][j], self.canvas, x+j*80, y)


    def add_lines(self) -> None:
        """
        Add plain and dash lines to the schema
        """
        matrixResults = self.listener.getMatrixResults()
        for i in range(len(matrixResults)):
            for j in range(i+1, len(matrixResults)):
                x = matrixResults[i][j].split(' I ')
                y = matrixResults[i][j].split(' J ')
                if len(x) > 1:
                    self.draw_indiff_line(a=self.construction[x[0]], b=self.construction[x[1]])
                elif len(y) > 1:
                    self.draw_incomp_line(a=self.construction[y[0]], b=self.construction[y[1]])
    

    def draw_indiff_line(self, a:AlternativeView, b:AlternativeView):
        """
        Draw a plain line to represent indifferentiability
        """
        (x0, y0, x1, y1) = self.get_line_coords(a, b)
        self.canvas.create_line(x0, y0, x1, y1)


    def draw_incomp_line(self,  a:AlternativeView, b:AlternativeView):
        """
        Draw a dash line to represent incompatibility
        """
        (x0, y0, x1, y1) = self.get_line_coords(a, b)
        self.canvas.create_line(x0, y0, x1, y1, dash=(3,1))


    def get_line_coords(self, a:AlternativeView, b:AlternativeView):
        c1 = a.get_coords()
        c2 = b.get_coords()
        if(c1[0] == c2[0]):
            x0 = c1[0]
            x1 = x0
            if(c1[1] > c2[1]):
                y0 = c1[1] - 30
                y1 = c2[1] + 30
            else:
                y0 = c2[1] - 30
                y1 = c1[1] + 30
        elif(c1[1] == c2[1]):
            y0 = c1[1]
            y1 = y0
            if(c1[0] > c2[0]):
                x0 = c2[0] + 30
                x1 = c1[0] - 30
            else:
                x0 = c1[0] + 30
                x1 = c2[0] - 30
        else:
            if(c1[1] > c2[1]):
                x0 = c2[0]
                y0 = c2[1] + 30
                x1 = c1[0]
                y1 = c1[1] - 30
            else:
                x0 = c1[0]
                y0 = c1[1] + 30
                x1 = c2[0]
                y1 = c2[1] - 30
        return (x0, y0, x1, y1)
