import matplotlib
import matplotlib.pyplot as plt
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from math import sqrt


class AlternativeView:
    """
    A class to represent an Alternative in the rank graph

    The alternative is represented by a circle and the alternative name in the center of the circle.

    Attributes
    -----------
    xy : tuple of 2 int
        the coordinate of the center of the circle that represents the alternative
    radius : int
        the radius of the circle that represents the alternative
    name : str
        the alternative name
    lineSpace : int
        the space between the circle and any line
    """

    def __init__(self, xy=(100,100), radius=40, name="Unknown"):
        """
        Parameters
        ----------
        xy : tuple of 2 int
            the coordinate of the center of the circle that represents the alternative
        radius : int
            the radius of the circle that represents the alternative
        name : str
            the alternative name
        """
        self.xy = xy
        self.radius = radius
        self.name = name
        self.lineSpace = 7


    def draw(self, ax):
        """Draw the alternative representation

        Parameters
        ----------
        ax : Matplotlib.axes
            a matplotlib axe
        """
        circle = plt.Circle(self.xy, self.radius, color="black", fill=False)
        ax.add_artist(circle)
        ax.text(self.xy[0], self.xy[1], self.name, ha="center", va="center", size="x-small")


    def getRadius(self):
        """Return the radius of the circle that represents the alternative

        Returns
        -------
        int
            the radius of the circle that represents the alternative
        """
        return self.radius
    

    def getBigRaius(self):
        return self.radius + self.lineSpace


    def getXY(self):
        """Return the coordinate of the center of the circle that represents the alternative

        Returns
        -------
        tuple of 2 int
            the coordinate of the center of the circle that represents the alternative
        """
        return self.xy


    def includeXY(self, x, y):
        """test if the point at x, y coordinate is include or not in the disk

        Parameters
        ----------
        x : int
            x coordinate of the point
        y : int
            y coordinate of the point

        Returns
        -------
        bool
            True if the point is in the disk, False otherwise
        """
        # circle equation : (x - xc)^2 + (y-yc)^2 = R^2
        # x, y in circle if (x - xc)^2 + (y-yc)^2 <= R^2
        ineq = (x - self.xy[0])**2 + (y - self.xy[1])**2 < (self.radius+self.lineSpace)**2
        if ineq:
            return True
        return False


    def newXLine(self, x, y, px):
        """Select a new x from x, y and px where x and y are current coordinate and px is the prevoius x coordinate

        the new x must be as close as possible of x and px but the point (new x, y) must be outside the circle that represents the alternative

        Parameters
        ----------
        x : int
            current x coordinate of point
        y : int
            current y coordinate of point
        px : int
            previous x coordinate of point
        """
        # Aim : Find newx closest x and px such that newx is outside the circle
        # circle equation : (x - xc)^2 + (y-yc)^2 = R^2
        # Outside the circle if (x - xc)^2 + (y-yc)^2 >= R^2
        # <=> x >= xc + sqrt(R - (y-yc)^2 or x <= xc - sqrt(R^2 - (y-yc)^2)
        cst = sqrt(abs((self.radius+self.lineSpace)**2 - (y - self.xy[1])**2))
        if x >= self.xy[0] and px >= self.xy[0]:
            newx = self.xy[0] + cst
        elif x <= self.xy[0] and px <= self.xy[0]:
            newx = self.xy[0] - cst
        elif px >= self.xy[0]:
            newx = self.xy[0] + cst
        elif px <= self.xy[0]:
            newx = self.xy[0] - cst
        return newx