import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from Views.ResultTabViews.AlternativeView import AlternativeView

class VerticalLine:
    def __init__(self, a1:AlternativeView, a2:AlternativeView):
        self.a1 = a1
        self.a2 = a2
        self.a1.increaseLineNb()
        self.a2.increaseLineNb()
        self.y = None
        self.x = None


    def spacement(self):
        s1 = self.a1.getLineNb()
        if s1 == 1:
            vspace1 = 0
            hspace1 = 0
        elif s1%2 == 0:
            hspace1 = s1
            vspace1 = 0
        elif s1%2 == 1:
            hspace1 = -s1+1
            vspace1 = 0

        s2 = self.a2.getLineNb()
        if s2 == 1:
            vspace2 = 0
            hspace2 = 0
        elif 2%2 == 0:
            hspace2 = s2
            vspace2 = 0
        elif s2%2 == 1:
            hspace2 = -s2+1
            vspace2 = 0
        return (hspace1, vspace1, hspace2, vspace2)
    

    def createLine(self, alternatives:list):
        visited = []

        xy1 = self.a1.getXY()
        xy2 = self.a2.getXY()
        radius = self.a1.getRadius()

        (hspace1, vspace1, hspace2, vspace2) = self.spacement()

        if xy1[1] > xy2[1]: # a1 is above a2
            x1 = xy1[0] + hspace1
            y1 = xy1[1] - vspace1
            x2 = xy2[0] + hspace2
            y2 = xy2[1] + vspace2

            ylength = y1 - y2
            xlength = x1 - x2
            xspace = xlength/ylength
            self.y = np.linspace(y2+radius, y1-radius, ylength)
            self.x = [x2]
            for i in range(1,ylength-1):
                xnew = x2 + i * xspace
                for a in alternatives:
                    if a != self.a1 and a != self.a2:
                        if a.includeXY(xnew, self.y[i]):
                            if a not in visited:
                                a.newLineEncountered()
                                visited.append(a)
                            xnew = a.newXLine(xnew, self.y[i], self.x[-1])
                            break
                self.x.append(xnew)
            self.x.append(x1)

        else:
            x1 = xy1[0] + hspace1
            y1 = xy1[1] + vspace1
            x2 = xy2[0] + hspace2
            y2 = xy2[1] - vspace2

            ylength = y2 - y1
            xlength = x2 - x1
            xspace = xlength/ylength

            self.y = np.linspace(y1+radius, y2-radius, ylength)

            self.x = [x1]
            for i in range(1,ylength-1):
                xnew = x1 + i * xspace
                for a in alternatives:
                    if a != self.a1 and a != self.a2:
                        if a.includeXY(xnew, self.y[i]):
                            if a not in visited:
                                a.newLineEncountered()
                                visited.append(a)
                            xnew = a.newXLine(xnew, self.y[i], self.x[-1])
                            break
                self.x.append(xnew)
            self.x.append(x2)
        
        self.x = np.array(self.x)
        visited.clear()

    def draw(self, ax, dash=False):
        if dash:
            ax.plot(self.x, self.y, lw=1, ls="--", color="black")
        else:
            ax.plot(self.x, self.y, lw=1, ls="-", color="black")
