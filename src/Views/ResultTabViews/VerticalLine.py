import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from Views.ResultTabViews.AlternativeView import AlternativeView
from Resources.ThreadCommunication import (Ticket, TicketPurpose)

class VerticalLine:
    def __init__(self, a1:AlternativeView, a2:AlternativeView):
        self.a1 = a1
        self.a2 = a2
        self.y = None
        self.x = None


    def createLine(self, alternatives):
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
    

    def draw(self, frame, queue, color):
        ticket = Ticket(ticketType=TicketPurpose.MATPLOTLIB_AX_PLOT, ticketValue=(self.x, self.y, color))
        queue.put(item=ticket)
        frame.event_generate("<<CheckMsgRankView>>")
