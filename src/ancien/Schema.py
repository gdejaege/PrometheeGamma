from tkinter import *
from Alternative import Alternative

class Schema():
    """
    Draw a schema that represents results of Promethee Gamma method
    """
    def __init__(self, als:list, r:list, m:Canvas, size:int):
        self.alternatives = als
        self.nb_als = len(als)
        self.matrix = r
        self.construction = {}
        self.master = m
        self.x = size//2


    def show(self):
        pass


    def build(self, scores:dict) -> None:
        """
        Build the schema
        """
        r = self.rank(scores=scores)
        for i in range(len(r)):
            y = (i+1)*80
            x = self.x - (len(r[i])-1)*40
            for j in range(len(r[i])):
                self.construction[r[i][j]] = Alternative(r[i][j], self.master, x+j*80, y)


    def rank(self, scores:dict) -> list:
        """
        Rank alternatives from scores \n
        Return a sort list of alternatives
        """
        sortedDict = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        ranked = []
        ranked.append([])
        ranked[0].append(sortedDict[0][0])
        for i in range(1,len(sortedDict)):
            if(sortedDict[i][1] == sortedDict[i-1][1]):
                ranked[-1].append(sortedDict[i][0])
            else:
                ranked.append([])
                ranked[-1].append(sortedDict[i][0])
        return ranked
    

    def add_lines(self) -> None:
        """
        Add plain and dash lines to the schema
        """
        for i in range(len(self.matrix)):
            for j in range(i+1, len(self.matrix)):
                if len(self.matrix[i][j].split('I')) > 1:
                    self.draw_indiff_line(a=self.construction[self.alternatives[i]], b=self.construction[self.alternatives[j]])
                elif len(self.matrix[i][j].split('J')) > 1:
                    self.draw_incomp_line(a=self.construction[self.alternatives[i]], b=self.construction[self.alternatives[j]])
    

    def get_line_coords(self, a:Alternative, b:Alternative):
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
    

    def draw_indiff_line(self, a:Alternative, b:Alternative):
        """
        Draw a plain line to represent indifferentiability
        """
        (x0, y0, x1, y1) = self.get_line_coords(a, b)
        self.master.create_line(x0, y0, x1, y1)


    def draw_incomp_line(self,  a:Alternative, b:Alternative):
        """
        Draw a dash line to represent incompatibility
        """
        (x0, y0, x1, y1) = self.get_line_coords(a, b)
        self.master.create_line(x0, y0, x1, y1, dash=(3,1))