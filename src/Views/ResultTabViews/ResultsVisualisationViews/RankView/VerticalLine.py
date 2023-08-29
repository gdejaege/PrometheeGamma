import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from Views.ResultTabViews.ResultsVisualisationViews.RankView.AlternativeView import AlternativeView
from Resources.ThreadCommunication import (Ticket, TicketPurpose)


class VerticalLine:
    """
    A class to draw an vertical line between two AlternativeView in the rank graph

    a1 : alternativeView
        a representation of an alternative
    a2 : AlternativeView
        a representation of an alternative
    x : list or None
        the list of x coordinates of points between the 2 alternativeView
    y : list or None
        the list of y coordinates of points between the 2 alternativeView
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
            self.y = None
            self.x = None
        except:
            raise SystemExit()


    def createLine(self, alternatives:list):
        """Create an vertical line between alternatives a1 and a2

        Parameters
        ----------
        alternatives : list of AlternativeView
            a list of alternative representations in order to get around them
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
                                xnew = a.newXLine(xnew, self.y[i], self.x[-1])
                                break
                    self.x.append(xnew)
                self.x.append(x1)

            else:
                x1 = xy1[0]
                y1 = xy1[1]
                x2 = xy2[0]
                y2 = xy2[1]

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
                                xnew = a.newXLine(xnew, self.y[i], self.x[-1])
                                break
                    self.x.append(xnew)
                self.x.append(x2)
            self.x = np.array(self.x)
        except:
            raise SystemExit()
    

    def draw(self, frame, queue, color):
        """Generate an event to draw the line

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
            ticket = Ticket(ticketType=TicketPurpose.MATPLOTLIB_AX_PLOT, ticketValue=(self.x, self.y, color))
            queue.put(item=ticket)
            frame.event_generate("<<CheckMsgRankView>>")
        except:
            raise SystemExit()
