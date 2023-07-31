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
        self.graph = []
        self.xmin = 1000000
        self.ymin = 1000000
        self.xmax = 0
        self.ymax = 0


    def setListener(self, l:ViewListener):
        """
        Set the listener
        """
        self.listener = l
        

    def show(self):
        """
        Show the canvas area
        """
        self.hbar.pack(side=BOTTOM, fill=X)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.drawCanvas()


    def refresh(self):
        """
        Refresh the canvas
        """
        self.drawCanvas()


    def resizeCanvas(self, size:int):
        """
        Resize the canvas
        """
        self.size = size+120
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
        self.graph = []
        for i in range(len(r)):
            y = (i+1)*100
            x = self.size//2 - (len(r[i])-1)*50
            self.graph.append([])
            for j in range(len(r[i])):
                a = AlternativeView(r[i][j], self.canvas, x+j*100, y, i, j)
                self.construction[r[i][j]] = a
                self.graph[i].append(a)
        self.findExtremums()


    def findExtremums(self):
        self.xmin = 1000000
        self.ymin = 1000000
        self.xmax = 0
        self.ymax = 0
        for i in range(len(self.graph)):
            for a in self.graph[i]:
                (x, y) = a.get_coords()
                if x < self.xmin:
                    self.xmin = x
                if y < self.ymin:
                    self.ymin=y
                if x > self.xmax:
                    self.xmax = x
                if y > self.ymax:
                    self.ymax = y


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
                    #self.draw_indiff_line(a=self.construction[x[0]], b=self.construction[x[1]])
                    self.draw_line(a=self.construction[x[0]], b=self.construction[x[1]])
                elif len(y) > 1:
                    #self.draw_incomp_line(a=self.construction[y[0]], b=self.construction[y[1]])
                    self.draw_line(a=self.construction[y[0]], b=self.construction[y[1]], dash=True)


    def draw_line(self, a:AlternativeView, b:AlternativeView, dash=False):
        (xa, ya) = a.get_coords()
        (xb, yb) = b.get_coords()
        if ya == yb:
            if xa > xb:
                h = round((xa - xb)/(self.xmax-self.xmin) * 20) + 35
                points = (xb, yb+30), (xb + (xa-xb)/2, ya+h), (xa, ya+30)
            else:
                h = round((xb - xa)/(self.xmax-self.xmin) * 20) + 35
                points = (xa, ya+30), (xa + (xb-xa)/2, ya+h), (xb, yb+30)
            #print(h)
        else:
            points = self.computePoints(a, b)
        if dash:
            self.canvas.create_line(points, smooth=True, dash=(3,1))
        else:
            self.canvas.create_line(points, smooth=True)


    def computePoints(self, a:AlternativeView, b:AlternativeView):
        (xa, ya) = a.get_coords()
        (xb, yb) = b.get_coords()
        ra = a.getRow()
        rb = b.getRow()
        points = []
        if ya > yb:
            pair = len(self.graph[rb])%2 == 0
            if ya == yb + 100:
                points = (xa, ya-30), (xb, yb+30)
            elif xa >= xb:
                points.append((xb, yb+30))
                for r in range(ra-rb-1):
                    if len(self.graph[r+rb+1])%2 == 0:
                        if pair:
                            points.append((xb+45, yb+45+r*100))
                            points.append((xb+45, yb+145+r*100))
                        else:
                            points.append((xb+95, yb+45+r*100))
                            points.append((xb+95, yb+145+r*100))
                    else:
                        if pair:
                            points.append((xb+95, yb+45+r*100))
                            points.append((xb+95, yb+145+r*100))
                        else:
                            points.append((xb+45, yb+45+r*100))
                            points.append((xb+45, yb+145+r*100))
                points.append((xb+45, ya-45))
                points.append((xa, ya-30))
            elif xa < xb:
                points.append((xb, yb+30))
                for r in range(ra-rb-1):
                    if len(self.graph[r+rb+1])%2 == 0:
                        if pair:
                            points.append((xb-45, yb+45+r*100))
                            points.append((xb-45, yb+145+r*100))
                        else:
                            points.append((xb-95, yb+45+r*100))
                            points.append((xb-95, yb+145+r*100))
                    else:
                        if pair:
                            points.append((xb-95, yb+45+r*100))
                            points.append((xb-95, yb+145+r*100))
                        else:
                            points.append((xb-45, yb+45+r*100))
                            points.append((xb-45, yb+145+r*100))
                points.append((xb-45, ya-45))
                points.append((xa, ya-30))
        else:
            pair = len(self.graph[ra])%2 == 0
            if yb == ya + 100:
                points = (xb, yb-30), (xa, ya+30)
            elif xb >= xa:
                points.append((xa, ya+30))
                for r in range(rb-ra-1):
                    if len(self.graph[r+ra+1])%2 == 0:
                        if pair:
                            points.append((xa+45, ya+45+r*100))
                            points.append((xa+45, ya+145+r*100))
                        else:
                            points.append((xa+95, ya+45+r*100))
                            points.append((xa+95, ya+145+r*100))
                    else:
                        if pair:
                            points.append((xa+95, ya+45+r*100))
                            points.append((xa+95, ya+145+r*100))
                        else:
                            points.append((xa+45, ya+45+r*100))
                            points.append((xa+45, ya+145+r*100))
                points.append((xa+45, yb-45))
                points.append((xb, yb-30))
            elif xb < xa:
                #points = (xa, ya+30), (xa-45, ya+45), (xa-45, yb-45), (xb, yb-30)
                points.append((xa, ya+30))
                for r in range(rb-ra-1):
                    if len(self.graph[r+ra+1])%2 == 0:
                        if pair:
                            points.append((xa-45, ya+45+r*100))
                            points.append((xa-45, ya+145+r*100))
                        else:
                            points.append((xa-95, ya+45+r*100))
                            points.append((xa-95, ya+145+r*100))
                    else:
                        if pair:
                            points.append((xa-95, ya+45+r*100))
                            points.append((xa-95, ya+145+r*100))
                        else:
                            points.append((xa-45, ya+45+r*100))
                            points.append((xa-45, ya+145+r*100))
                points.append((xa-45, yb-45))
                points.append((xb, yb-30))
        return tuple(points)


    def draw_indiff_line(self, a:AlternativeView, b:AlternativeView):
        """
        Draw a plain line to represent indifferentiability
        """
        (x0, y0, x1, y1) = self.get_line_coords(a, b)
        self.canvas.create_line(x0, y0, x1, y1)
        #self.canvas.create_arc()


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
