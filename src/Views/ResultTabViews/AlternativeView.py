import matplotlib
import matplotlib.pyplot as plt
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from math import sqrt


class AlternativeView:
    def __init__(self, xy=(100,100), radius=40, name="Unknown"):
        self.xy = xy
        self.radius = radius
        self.name = name
        self.lineSpace = 4
        self.lineNb = 0


    def draw(self, ax):
        circle = plt.Circle(self.xy, self.radius, color="black", fill=False)
        ax.add_artist(circle)
        #text = TextPath(self.xy, self.name, size=self.radius//3)
        #ax.add_patch(PathPatch(text, color="black", lw=1))
        ax.text(self.xy[0], self.xy[1], self.name, ha="center", va="center", size="x-small")


    def getRadius(self):
        return self.radius


    def getXY(self):
        return self.xy


    def getLineNb(self):
        return self.lineNb


    def increaseLineNb(self):
        self.lineNb += 1


    def includeXY(self, x, y):
        # circle equation : (x - xc)^2 + (y-yc)^2 = R^2
        # x, y in circle if (x - xc)^2 + (y-yc)^2 <= R^2
        #print((x - self.xy[0])**2)
        #print((y - self.xy[1])**2)
        #print((self.radius+5)**2)
        eq = (x - self.xy[0])**2 + (y - self.xy[1])**2 < (self.radius+self.lineSpace)**2
        if eq:
            return True
        return False


    def newXLine(self, x, y, px):
        """

        px = previous x
        """
        # Aim : Find newx closest x and px such that newx is outside the circle
        # circle equation : (x - xc)^2 + (y-yc)^2 = R^2
        # Outside the circle if (x - xc)^2 + (y-yc)^2 >= R^2
        # <=> x >= xc + sqrt(R - (y-yc)^2 or x <= xc - sqrt(R^2 - (y-yc)^2)
        cst = sqrt(abs((self.radius+self.lineSpace)**2 - (y - self.xy[1])**2))
        if x >= self.xy[0] and px >= self.xy[0]-5:
            newx = self.xy[0] + cst
        elif x <= self.xy[0] and px <= self.xy[0]+5:
            newx = self.xy[0] - cst
        elif px >= self.xy[0]:
            newx = self.xy[0] + cst
        elif px <= self.xy[0]:
            newx = self.xy[0] - cst
        return newx


    def newLineEncountered(self):
        self.lineSpace += 2