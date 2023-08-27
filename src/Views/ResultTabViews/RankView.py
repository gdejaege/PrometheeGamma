from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.lines as mlines
from tkinter import *
from customtkinter import (CTkFrame, CTkCheckBox, IntVar, CTk)
from math import floor
import threading
#import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time

from Resources.ThreadCommunication import (Ticket, TicketPurpose)
from Resources.ResizableScrollableFrame import ResizableScrollableFrame
from Resources.VScrollableFrame import VScrollableFrame
from Views.ResultTabViews.AlternativeView import AlternativeView
from Views.ResultTabViews.VerticalLine import VerticalLine
from Views.ResultTabViews.HorizontalLine import HorizontalLine

SPACE = 100 # The space between the center of 2 circles that represent alternatives
RADIUS = 35 # The radius of the circle that represents an alternative


class RankView:
    """
    A class to display the rank graph of alternatives

    """

    class ViewListener:
        """
        An interface for the listener

        Methods
        -------
        checkBoxEvent()
            Handle checkBox events
        """
        def checkBoxEvent(self):
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
        self.xmin = 1000000
        self.ymin = 50
        self.xmax = 0
        self.ymax = 100

        self.queueMessage = Queue()
        self.root.bind("<<CheckMsgRankView>>", self.checkQueue)

        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future = None


    def checkQueue(self, event):
        """Read the queue
        """
        msg: Ticket
        msg = self.queueMessage.get()

        if msg.ticketType == TicketPurpose.MAKE_MATPLOTLIB_LEGEND:
            self.ax.legend(handles=msg.ticketValue, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        elif msg.ticketType == TicketPurpose.MATPLOTLIB_AX_ADD_PATCH:
            #print("line")
            self.ax.add_patch(msg.ticketValue)
        elif msg.ticketType == TicketPurpose.MATPLOTLIB_AX_PLOT:
            #print("line")
            (x, y, color) = msg.ticketValue
            self.ax.plot(x, y, lw=1, ls="-", color=color)
        elif msg.ticketType == TicketPurpose.CANVAS_DRAW:
            self.canvas.draw()
            #print("DRAW ______________________________________________\n")


    def buildAlternativesDict(self, aList:list):
        """Build the dictionary for alternatives selection

        Parameters
        ----------
        aList : list
            the list of alternative names
        """

        self.alternatives = {}
        for a in aList:
            self.alternatives[a] = IntVar(master=self.rightFrame, value=1)


    def BuildCheckBoxes(self):
        """Build the checkBoxes for alternatives selection
        """

        self.checkBoxList.clear()
        row=0
        for key in self.alternatives.keys():
            box = CTkCheckBox(master=self.rightFrame, text=key, text_color="#000000", variable=self.alternatives[key], command=self.listener.checkBoxEvent)
            box.grid(row=row, column=0, sticky="w", padx=5, pady=(5,0))
            row+=1
            self.checkBoxList.append(box)


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

        if self.future is not None:
            self.future.cancel() # Cancels the pending thread to allow a new thread to take its place
            # The previous thread can be cancelled, as it corresponds to an obsolete request.

        self.fig.clear()
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
        self.ax = self.fig.add_subplot()
        self.ax.set_aspect(1)
        self.ax.axis('off')

        self.build(r)

        # Create a thread. If a thread is already running, puts the new thread on hold.
        self.future = self.executor.submit(self.makeGraph, matrixResults)
        


    def makeGraph(self, matrixResults:list) -> None:
        #print("GRAPH _____________________________________________")
        self.makeLegend()
        self.add_lines(matrixResults)
        ticket = Ticket(ticketType=TicketPurpose.CANVAS_DRAW, ticketValue=None)
        self.queueMessage.put(ticket)
        self.root.event_generate("<<CheckMsgRankView>>")
        return


    def computeSize(self, r:list):
        width = 100
        height = 100
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
        
        self.leftScrollFrame.resize(1.3 * width + 5 * SPACE, 1.3 * height + SPACE)
        self.ax.axis([0, width, 0, height])
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
        """

        for i in range(len(matrixResults)):
            for j in range(i+1, len(matrixResults)):
                x = matrixResults[i][j].split(' I ')
                y = matrixResults[i][j].split(' J ')
                if len(x) > 1 and self.alternatives[x[0]].get() and self.alternatives[x[1]].get():
                    self.draw_line(a=self.construction[x[0]], b=self.construction[x[1]], color="green")
                elif len(y) > 1 and self.alternatives[y[0]].get() and self.alternatives[y[1]].get():
                    self.draw_line(a=self.construction[y[0]], b=self.construction[y[1]], color="red")


    def draw_line(self, a:AlternativeView, b:AlternativeView, color):
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


    def makeLegend(self):
        redLine = mlines.Line2D([], [], color='red', label='Incomparability lines')
        greenLine = mlines.Line2D([], [], color='green', label='Indifference lines')
        ticket = Ticket(ticketType=TicketPurpose.MAKE_MATPLOTLIB_LEGEND, ticketValue=[redLine, greenLine])
        self.queueMessage.put(ticket)
        self.root.event_generate("<<CheckMsgRankView>>")
        

    def save(self, filename):
        self.fig.savefig(filename)