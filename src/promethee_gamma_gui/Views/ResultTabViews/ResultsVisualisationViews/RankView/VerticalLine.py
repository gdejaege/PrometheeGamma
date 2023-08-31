import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np
from math import atan, degrees

from .AlternativeView import AlternativeView
from .....Resources.ThreadCommunication import Ticket, TicketPurpose


class VerticalLine:
    """
    A class to draw an vertical line between two AlternativeView in the rank graph

    a1 : alternativeView
        a representation of an alternative
    a2 : AlternativeView
        a representation of an alternative
    sections : list of tuple
        the sections of the lines. Each section can be a straight line or a circular arc. 
    """

    def __init__(self, a1:AlternativeView, a2:AlternativeView):
        """
        Parameters
        ----------
        a1 : alternativeView
            a representation of an alternative
        a2 : AlternativeView
            a representation of an alternative
        """
        try:
            self.a1 = a1
            self.a2 = a2
            self.sections = []
        except SystemExit:
            raise SystemExit()


    def createLine(self, alternatives:list):
        """Create an vertical line between alternatives a1 and a2

        Parameters
        ----------
        alternatives : list of AlternativeView
            a list of alternative representations in order to avoid them
        """
        
        try:
            xy1 = self.a1.getXY()
            xy2 = self.a2.getXY()
            radius = self.a1.getRadius()
            if xy1[1] > xy2[1]: # a1 is above a2
                x1 = xy1[0]
                y1 = xy1[1]
                x2 = xy2[0]
                y2 = xy2[1]
            else:
                x1 = xy2[0]
                y1 = xy2[1]
                x2 = xy1[0]
                y2 = xy1[1]

            # keep only useful alternatives
            als = []
            for a in alternatives:
                a : AlternativeView
                if a != self.a1 and a != self.a2:
                    axy = a.getXY()
                    if axy[1] > y2 and axy[1] < y1:
                        als.append(a)
            
            ylength = y1 - y2
            y = np.linspace(y2+radius, y1-radius, ylength)
            x = np.linspace(x2, x1, ylength)
            state = {"previous":"out", "current":"out"}
            start = 0
            end = 0
            current = None

            for i in range(ylength):
                notIncluded = True
                for a in als:
                    if a.includeXY(x[i], y[i]):
                        current = a
                        notIncluded = False
                        break
                
                # Update the state
                if notIncluded:
                    if state["current"] == "in":
                        state["previous"] = "in"
                    else :
                        state["previous"] = "out"
                    state["current"] = "out"
                else:
                    if state["current"] == "in":
                        state["previous"] = "in"
                    else :
                        state["previous"] = "out"
                    state["current"] = "in"

                # Make operation following state
                if state["current"] == "in" and state["previous"] == "out":
                    end = i
                    self.sections.append(("line", x[start:end], y[start:end]))
                    start = end
                elif state["current"] == "out" and state["previous"] == "in":
                    end = i
                    self.sections.append(self.makeArc((x[start], y[start]), (x[end], y[end]), current))
                    start = end
            self.sections.append(("line", x[start:], y[start:]))
        except SystemExit:
            raise SystemExit()
        

    def theta(self, coord:tuple, center:tuple):
        """Compute theta value for x, y coordinates thanks to the center of the cicle.

        The theta value is the angle in degrees between the horizontal axis passing through the center of the circle 
        and the straight line passing through the point with coordinates (x,y) and the center of the circle.

        Parameters
        ----------
        coord : tuple of int
            (x, y), coordinates of a point tangent to the circle
        center : tuple of int
            (xc, yc), center of the circle

        Returns
        -------
        float
            the theta value
        """
        if coord[0] != center[0]:
            rad = atan(abs(coord[1]-center[1])/abs(coord[0]-center[0])) # arctan(y/x)
            deg = degrees(rad) # radians to degrees
        else:
            deg = 90
        if coord[0] >= center[0] and coord[1] >= center[1]: # 1st quadrant
            theta = deg
        elif coord[0] < center[0] and coord[1] < center[1]: # 3rd quadrant
            theta = deg + 180
        elif coord[0] < center[0] and coord[1] >= center[1]: # 2nd quadrant
            theta = 180 - deg
        elif coord[0] >= center[0] and coord[1] < center[1]: # 4rd quadrant
            theta = 360 - deg
        return theta


    def makeArc(self, start:tuple, end:tuple, alternative:AlternativeView):
        """Compute data to draw an arc of circle between start and end coordinates. The center of the arc is the center of the AlternativeView

        Parameters
        ----------
        start : tuple
            (xs, ys), the coordinates of one end of the circular arc
        end : tuple
            (xe, ye), the coordinates of the other end of the circular arc
        alternative : AlternativeView
            the alternative to avoid
        """
        xy = alternative.getXY()
        t1 = self.theta(start, xy)
        t2 = self.theta(end, xy)

        if abs(t1 - t2) <= 180:
            theta1 = min(t1,t2)
            theta2 = max(t1,t2)
        else:
            theta1 = max(t1,t2)
            theta2 = min(t1,t2)
        arc = {"xy":alternative.getXY(), "radius":alternative.getBigRaius(), "angle":0, "theta1":theta1, "theta2":theta2}
        return ("arc", arc)
    

    def draw(self, frame, queue, color):
        """Generate event(s) to draw the line

        Parameters
        ----------
        frame : CTk
            the frame that will generate the event
        queue : Queue
            a queue to store the message
        color : Color
            the line color
        """
        try:
            for s in self.sections:
                if s[0] == "line":
                    ticket = Ticket(ticketType=TicketPurpose.MATPLOTLIB_AX_PLOT, ticketValue=(s[1], s[2], color))
                    queue.put(item=ticket)
                    frame.event_generate("<<CheckMsgRankView>>")
                elif s[0] == "arc":
                    arc = Arc(s[1]["xy"], 2*s[1]["radius"], 2*s[1]["radius"], angle=0, theta1=s[1]["theta1"], theta2=s[1]["theta2"], ls="-", lw=1, edgecolor=color)
                    ticket = Ticket(ticketType=TicketPurpose.MATPLOTLIB_AX_ADD_PATCH, ticketValue=arc)
                    queue.put(ticket)
                    frame.event_generate("<<CheckMsgRankView>>")
        except SystemExit:
            raise SystemExit()
