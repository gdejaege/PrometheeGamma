import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

from .AlternativeView import AlternativeView
from .....Resources.ThreadCommunication import Ticket, TicketPurpose


SPACE = 100
"""The space between the center of 2 circles that represent alternatives"""

class HorizontalLine:
    """
    A class to draw an horizontal line between two AlternativeView in the rank graph

    a1 : alternativeView
        a representation of an alternative
    a2 : AlternativeView
        a representation of an alternative
    x : list or None
        the list of x coordinates of points between the 2 alternativeView
    y : list or None
        the list of y coordinates of points between the 2 alternativeView
    arc : Arc or None
        an arc between the 2 alternative
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
            self.arc = False
        except SystemExit:
            raise SystemExit()


    def createLine(self):
        """Create an horizontal line between alternatives a1 and a2

        Raises
        ------
        SystemExit
            if a SystemExit occurs.
        """
        try:
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
        except SystemExit:
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

        Raises
        ------
        SystemExit
            if a SystemExit occurs.
        """
        try:
            if self.arc:
                self.drawArc(frame, queue, color)
            else:
                ticket = Ticket(ticketType=TicketPurpose.MATPLOTLIB_AX_PLOT, ticketValue=(self.x, self.y, color))
                queue.put(ticket)
                frame.event_generate("<<CheckMsgRankView>>")
        except SystemExit:
            raise SystemExit()


    def drawArc(self, frame, queue, color):
        """Generate an event to draw an arc

        Parameters
        ----------
        frame : CTk
            the frame that will generate the event
        queue : Queue
            a queue to store the message
        color : Color
            the line color

        Raises
        ------
        SystemExit
            if a SystemExit occurs.
        """
        try:
            xy1 = self.a1.getXY()
            xy2 = self.a2.getXY()
            radius = self.a1.getRadius()

            width = abs(xy1[0] - xy2[0])
            height = 8 + width//SPACE
            yc = xy1[1] - radius
            xc = width//2 + min(xy1[0],xy2[0])

            arc = Arc((xc, yc), width, height, angle=0, theta1=180, theta2=360, ls="-", lw=1, edgecolor=color)
            ticket = Ticket(ticketType=TicketPurpose.MATPLOTLIB_AX_ADD_PATCH, ticketValue=arc)
            queue.put(ticket)
            frame.event_generate("<<CheckMsgRankView>>")
        except SystemExit:
            raise SystemExit()