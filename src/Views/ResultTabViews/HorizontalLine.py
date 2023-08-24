import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import threading
import time

from Views.ResultTabViews.AlternativeView import AlternativeView

SPACE = 100

class HorizontalLine(threading.Thread):
    def __init__(self, a1:AlternativeView, a2:AlternativeView, ax, color):
        threading.Thread.__init__(self, daemon=True)
        self.a1 = a1
        self.a2 = a2
        self.y = None
        self.x = None
        self.arc = False
        self.ax = ax
        self.color = color

    def run(self):
        self.createLine()
        self.draw()


    def createLine(self):
        xy1 = self.a1.getXY()
        xy2 = self.a2.getXY()
        radius = self.a1.getRadius()

        if abs(xy1[0] - xy2[0]) == SPACE:
            if xy1[0] < xy2[0]:
                self.x = [xy1[0]+radius, xy2[0]-radius]
                self.y = [xy1[1], xy2[1]]
            else:
                self.x = [xy2[0]+radius, xy1[0]-radius]
                self.y = [xy2[1], xy1[1]]
            self.arc = False
        else:
            self.arc = True


    def draw(self):
        if self.arc:
            self.drawArc()
        else:
            self.ax.plot(self.x, self.y, lw=1, ls="-", color=self.color)


    def drawArc(self):
        xy1 = self.a1.getXY()
        xy2 = self.a2.getXY()
        radius = self.a1.getRadius()

        width = abs(xy1[0] - xy2[0])
        height = 8 + width//SPACE
        yc = xy1[1] - radius
        xc = width//2 + min(xy1[0],xy2[0])

        arc = Arc((xc, yc), width, height, angle=0, theta1=180, theta2=360, ls="-", lw=1, edgecolor=self.color)
        self.ax.add_patch(arc)