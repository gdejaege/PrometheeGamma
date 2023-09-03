from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.lines as mlines
from tkinter import *
from customtkinter import (CTkFrame, CTkCheckBox, IntVar, CTk)
from math import floor
import threading
from queue import Queue
import ctypes

from .AlternativeView import AlternativeView
from .VerticalLine import VerticalLine
from .HorizontalLine import HorizontalLine
from .....Resources.ThreadCommunication import Ticket, TicketPurpose
from .....Resources.ScrollableFrames import ResizableScrollableFrame, VScrollableFrame


SPACE = 100
"""The space between the center of 2 circles that represent alternatives"""
RADIUS = 35
"""The radius of the circle that represents an alternative"""


class RankView:
    """
    A class to display the rank graph of alternatives

    Attributes
    ----------
    root : CTk
        the root window of the app
    leftScrollFrame : ResizableScrollableFrame
        a resisable vertically and horizontally scrollable frame for the canvas that contains the graph
    leftFrame : CTkFrame
        the master frame for the canvas that contains the graph
    rightScrollFrame : VScrollableFrame
        a vertical scrollable frame for the selection view
    rightFrame : CTkFrame
        the master frame for the selection view
    fig : Figure
        the matplotlib figure for the graph
    ax : Axes
        the matplotlib axes to draw the graph
    canvas : FigureCanvasTkAgg
        the canvas that contains the figure
    toolbar : NavigationToolbar2Tk
        the matplotlib navigation toolbar
    checkBoxList : list of CTkCheckBox
        the list of checkboxes for selection
    alternatives : dict of str:Intvar
        a dictionnary that contains alternatives names as key and an Intvar as item. 
        It is used for selection : if the IntVar value is set to 1, the alternative is showed, otherwise the alternative is hided.
    listener : ViewListener
        the listener of this view
    construction : dict of str:AlternativeView
        a dictionnary to link alternatives to their representation
    graphName : list of list of str
        a representation of the graph in list with alternatives names as items
    als : list of AlternativeView
        a list that contains all AlternativeViews
    queueMessage : Queue
        A queue to transmit messages from secondary thread to main thread
    thread : Thread
        a secondary thread to computes graph lines
    """

    class ViewListener:
        """
        An interface for the listener
        """
        def checkBoxEvent(self):
            """Handle checkBox events
            """
            pass

        def checkBoxEventAll(self, alternativesDict):
            """Handle "All" checkBox event

            Parameters
            ----------
            alternativeDict : dict
                the dictionnary of alternatives names for selection
            """
            pass


    def __init__(self, master:CTkFrame, root:CTk) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        root : CTk
            the root window
        """
        self.root = root
        self.leftScrollFrame = ResizableScrollableFrame(master)
        self.leftFrame = self.leftScrollFrame.frame()

        self.rightScrollFrame = VScrollableFrame(master)
        self.rightFrame = self.rightScrollFrame.frame()
        self.fig = Figure()
        self.ax = None

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.leftFrame)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.leftFrame, pack_toolbar=False)
        self.toolbar.update()

        self.checkBoxList = []
        self.alternatives = {}
        self.listener = None
        self.construction = {}
        self.graphName = []
        self.als = []

        self.queueMessage = Queue()
        self.root.bind("<<CheckMsgRankView>>", self.checkQueue)

        self.thread = None


    def checkQueue(self, event):
        """Read the queue
        """
        msg: Ticket
        msg = self.queueMessage.get()

        if msg.ticketType == TicketPurpose.MATPLOTLIB_AX_ADD_PATCH:
            self.ax.add_patch(msg.ticketValue)
        elif msg.ticketType == TicketPurpose.MATPLOTLIB_AX_PLOT:
            (x, y, color) = msg.ticketValue
            self.ax.plot(x, y, lw=1, ls="-", color=color)
        elif msg.ticketType == TicketPurpose.CANVAS_DRAW:
            self.canvas.draw()


    def buildAlternativesDict(self, aList:list):
        """Build the dictionary for alternatives selection

        Parameters
        ----------
        aList : list
            the list of alternative names
        """
        self.alternatives = {}
        self.alternatives["ALL ALTERNATIVES"] = IntVar(master=self.rightFrame, value=1)
        for a in aList:
            self.alternatives[a] = IntVar(master=self.rightFrame, value=1)


    def BuildCheckBoxes(self):
        """Build the checkBoxes for alternatives selection
        """
        self.checkBoxList.clear()
        row=1
        for key in self.alternatives.keys():
            if key == "ALL ALTERNATIVES":
                box = CTkCheckBox(master=self.rightFrame, text="ALL", text_color="#000000", variable=self.alternatives[key], command=self.checkBoxEventAll)
                box.grid(row=0, column=0, sticky="w", padx=5, pady=(5,0))
            else:
                box = CTkCheckBox(master=self.rightFrame, text=key, text_color="#000000", variable=self.alternatives[key], command=self.listener.checkBoxEvent)
                box.grid(row=row, column=0, sticky="w", padx=5, pady=(5,0))
                row+=1
            self.checkBoxList.append(box)


    def checkBoxEventAll(self):
        """Handle "All" checkBox event
        """
        self.listener.checkBoxEventAll(self.alternatives)


    def setListener(self, l:ViewListener):
        """Set the listener

        Parameters
        ----------
        l : RankView.ViewListener
            the new listener
        """

        self.listener = l


    def show(self):
        """Show the view
        """
        self.rightScrollFrame.place(relx=0.75, y=1, relheight=1.0, relwidth=0.25)
        self.leftScrollFrame.place(x=1, y=1, relheight=1.0, relwidth=0.75)
        self.toolbar.pack(side='bottom')
        self.canvas.get_tk_widget().pack(expand=True, fill='both', side='bottom')
        

    def drawCanvas(self, r:list, matrixResults:list) -> None:
        """Display result in a schematic ranking

        Parameters
        ----------
        r : list
            ranked list of alternatives
        matrixResults : list
            the result matrix of PROMETHEE Gamma method
        """
        
        # The previous thread can be cancelled, as it corresponds to an obsolete request.
        if self.thread is not None and self.thread.is_alive():
            resu = ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread.ident, ctypes.py_object(SystemExit)) # Kill the thread
            if resu > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread.ident, 0)
                
        self.fig.clear()
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
        self.ax = self.fig.add_subplot()
        self.ax.set_aspect(1)
        self.ax.axis('off')

        self.build(r)
        self.makeLegend()

        # Create a thread. If a thread is already running, puts the new thread on hold.
        self.thread = threading.Thread(target=self.makeGraph, args=(matrixResults, ), daemon=True)
        self.thread.start()


    def makeGraph(self, matrixResults:list) -> None:
        """Add lines to the graph and draw it

        Parameters
        ----------
        matrixResults : list
            the result matrix of PROMETHEE Gamma method
        """
        try:
            self.add_lines(matrixResults)
            ticket = Ticket(ticketType=TicketPurpose.CANVAS_DRAW, ticketValue=None)
            self.queueMessage.put(ticket)
            self.root.event_generate("<<CheckMsgRankView>>")
        except SystemExit:
            pass


    def computeSize(self, r:list):
        """Compute the size of the canvas

        Parameters
        ----------
        r : list
            ranked list of alternatives
        """
        width = 2*SPACE
        height = 2*SPACE
        self.graphName.clear()

        h = 0
        for i in range(len(r)):
            w = 0
            row = []
            for k in range(len(r[i])):
                if self.alternatives[r[i][k]].get():
                    w += SPACE
                    row.append(r[i][k])
            if w > 0:
                h += SPACE
                self.graphName.append(row)
            if w > width:
                width = w
        if h > height:
            height = h

        if width > 2*height:
            wspace = SPACE
            hspace = 2*SPACE + 0.1*height
        elif height > 2*width:
            wspace = 2*SPACE + 0.1*width
            hspace = SPACE
        else : 
            wspace = SPACE + 0.1*width
            hspace = SPACE + 0.1*height
        
        self.leftScrollFrame.resize(1.4 *(width + wspace) + SPACE, 1.4 * (height + hspace) + SPACE)
        self.ax.axis([0, width+wspace, 0, height+hspace])
        return width, height
                    

    def build(self, r:list) -> None:
        """Build the schema

        Parameters
        ----------
        r : list
            the ranked list of alternatives
        """
        self.construction.clear()
        self.als.clear()

        (width, height) = self.computeSize(r)
        h = height - SPACE//2

        for row in self.graphName:
            length = len(row)
            if length%2 == 0:
                x = width//2 + SPACE//2 - SPACE * length//2
            else:
                x = width//2 - SPACE * floor(length/2)
            y = h
            for n in row:
                a = AlternativeView(xy=(x, y), radius=RADIUS, name=n)
                a.draw(self.ax)
                self.construction[n] = a
                self.als.append(a)
                x += SPACE
            h -= SPACE


    def add_lines(self, matrixResults:list) -> None:
        """Add plain and dash lines to the schema

        Parameters
        ----------
        matrixResults : list
            the result matrix of PROMETHEE Gamma method

        Raises
        ------
        SystemExit
            if a SystemExit occurs.
        """
        try:
            for i in range(len(matrixResults)):
                for j in range(i+1, len(matrixResults)):
                    x = matrixResults[i][j].split(' I ')
                    y = matrixResults[i][j].split(' J ')
                    if len(x) > 1 and self.alternatives[x[0]].get() and self.alternatives[x[1]].get():
                        self.draw_line(a=self.construction[x[0]], b=self.construction[x[1]], color="green")
                    elif len(y) > 1 and self.alternatives[y[0]].get() and self.alternatives[y[1]].get():
                        self.draw_line(a=self.construction[y[0]], b=self.construction[y[1]], color="red")
        except SystemExit:
            raise SystemExit()


    def draw_line(self, a:AlternativeView, b:AlternativeView, color):
        """Draw a line between alternatives a and b

        Parameters
        ----------
        a : AlternativeView
            a representation of an alternative on the graph
        b : AlternativeView
            a representation of an alternative on the graph
        color : Color
            the line color
        
        Raises
        ------
        SystemExit
            if a SystemExit occurs.
        """
        try:
            xya = a.getXY()
            xyb = b.getXY()
            if xya[1] == xyb[1]:
                # Horizontal line
                line = HorizontalLine(a, b)
                line.createLine()
                line.draw(color=color, frame=self.root, queue=self.queueMessage)
            else:
                line = VerticalLine(a, b)
                line.createLine(self.als)
                line.draw(color=color, frame=self.root, queue=self.queueMessage)
        except SystemExit:
            raise SystemExit()


    def makeLegend(self):
        """Add legend to the graph
        """
        redLine = mlines.Line2D([], [], color='red', label='Incomparability lines')
        greenLine = mlines.Line2D([], [], color='green', label='Indifference lines')
        self.ax.legend(handles=[redLine, greenLine], loc='upper right')


    def save(self, filename):
        """Save the graph in filename
        """
        self.fig.savefig(filename)