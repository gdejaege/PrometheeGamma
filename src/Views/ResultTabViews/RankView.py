from customtkinter import (CTkCanvas, CTkScrollbar, CTkFrame, CTkCheckBox, IntVar)
from Resources.ScrollableFrame import ScrollableFrame
from Views.ResultTabViews.AlternativeView import AlternativeView
from aspose.pdf import (PsLoadOptions, Document)
from aspose.pdf.devices import PngDevice, Resolution
import io
from PIL import Image, ImageDraw

SPACE = 100 # The space between the center of 2 circles that represent alternatives
RADIUS = 30 # The radius of the circle that represents an alternative

class RankView:
    class ViewListener:
        def checkBoxEvent(self):
            pass

    def __init__(self, master) -> None:
        self.leftFrame = CTkFrame(master, bg_color="#ffffff", fg_color="#ffffff")
        self.scrollFrame = ScrollableFrame(master)
        self.rightFrame = self.scrollFrame.frame()
        
        self.canvas=CTkCanvas(self.leftFrame, bg="#ffffff", highlightcolor="#ffffff", scrollregion=(0,0,100,100))
        self.hbar=CTkScrollbar(self.leftFrame, orientation="horizontal", command=self.canvas.xview)
        self.vbar=CTkScrollbar(self.leftFrame, orientation="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        self.checkBoxList = []
        self.alternatives = {}

        self.listener = None
        self.construction = {}
        self.graph = []
        self.xmin = 1000000
        self.ymin = 100
        self.xmax = 0
        self.ymax = SPACE


    def buildAlternativesDict(self, aList:list):
        """
        Build the dictionary for alternatives selection
        """
        self.alternatives = {}
        for a in aList:
            self.alternatives[a] = IntVar(master=self.rightFrame, value=1)


    def BuildCheckBoxes(self):
        """
        Build the checkBoxes for alternatives selection
        """
        self.checkBoxList.clear()
        row=0
        for key in self.alternatives.keys():
            box = CTkCheckBox(master=self.rightFrame, text=key, text_color="#000000", variable=self.alternatives[key], command=self.listener.checkBoxEvent)
            box.grid(row=row, column=0, sticky="w", padx=5, pady=(5,0))
            row+=1
            self.checkBoxList.append(box)


    def setListener(self, l:ViewListener):
        """
        Set the listener
        """
        self.listener = l
        

    def show(self):
        """
        Show the canvas area
        """
        self.leftFrame.place(x=1, y=1, relheight=1.0, relwidth=0.75)
        self.hbar.pack(side="bottom", fill="x")
        self.vbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", expand=True, fill="both")

        self.scrollFrame.place(relx=0.75, y=1, relheight=1.0, relwidth=0.25)


    def resizeCanvas(self, width:int, height:int):
        """
        Resize the canvas
        """
        self.canvas.config(scrollregion=(0, 0, width+SPACE, height+SPACE))


    def drawCanvas(self, r:list, lmax:int, matrixResults:list) -> None:
        """
        Display result in a schematic ranking
        """
        self.canvas.delete('all')
        #self.pilImage = Image.new()
        self.build(r, lmax)
        self.add_lines(matrixResults)
        self.canvas.update()


    def _on_mousewheel(self, event):
        """
        Link mouse scroll to vertical canvas scrolling
        """
        self.canvas.yview_scroll(-1*(event.delta//120), "units")


    def build(self, r:list, lmax:int) -> None:
        """
        Build the schema
        """
        self.ymin = SPACE
        self.ymax = len(r)*SPACE
        self.xmin = 1000000
        self.xmax = 0
        self.graph = []
        columnLength = 0
        for i in range(len(r)):
            y = (columnLength+1)*SPACE
            x = lmax//2 + SPACE//2
            for k in range(len(r[i])):
                if self.alternatives[r[i][k]].get():
                    x -= SPACE//2
            if x < self.xmin:
                self.xmin = x
            rowLength = 0
            row = []
            for j in range(len(r[i])):
                xlength = x+rowLength*SPACE
                if self.alternatives[r[i][j]].get():
                    a = AlternativeView(name=r[i][j], canvas=self.canvas, x=xlength, y=y, radius=RADIUS, row=columnLength, column=rowLength)
                    self.construction[r[i][j]] = a
                    row.append(a)
                    rowLength += 1
                    if self.xmax < xlength:
                        self.xmax = xlength
            if rowLength > 0:
                columnLength += 1
                self.graph.append(row)
        self.canvas.config(scrollregion=(self.xmin-SPACE, self.ymin-SPACE, self.xmax+SPACE, self.ymax+SPACE))


    def add_lines(self, matrixResults:list) -> None:
        """
        Add plain and dash lines to the schema
        """
        for i in range(len(matrixResults)):
            for j in range(i+1, len(matrixResults)):
                x = matrixResults[i][j].split(' I ')
                y = matrixResults[i][j].split(' J ')
                if len(x) > 1 and self.alternatives[x[0]].get() and self.alternatives[x[1]].get():
                    self.draw_line(a=self.construction[x[0]], b=self.construction[x[1]])
                elif len(y) > 1 and self.alternatives[y[0]].get() and self.alternatives[y[1]].get():
                    self.draw_line(a=self.construction[y[0]], b=self.construction[y[1]], dash=True)


    def draw_line(self, a:AlternativeView, b:AlternativeView, dash=False):
        """
        Draw the lines
        """
        (xa, ya) = a.get_coords()
        (xb, yb) = b.get_coords()
        if ya == yb:
            if xa > xb:
                h = round((xa - xb)/(self.xmax-self.xmin) * 20) + RADIUS + 5
                points = (xb, yb+RADIUS), (xb + (xa-xb)/2, ya+h), (xa, ya+RADIUS)
            else:
                h = round((xb - xa)/(self.xmax-self.xmin) * 20) + RADIUS + 5
                points = (xa, ya+RADIUS), (xa + (xb-xa)/2, ya+h), (xb, yb+RADIUS)
        else:
            points = self.computePoints(a, b)
        if dash:
            self.canvas.create_line(points, smooth=True, dash=(3,1))
        else:
            self.canvas.create_line(points, smooth=True)


    def computePoints(self, a:AlternativeView, b:AlternativeView):
        """
        Compute the points sequence for lines
        """
        (xa, ya) = a.get_coords()
        (xb, yb) = b.get_coords()
        ra = a.getRow()
        rb = b.getRow()
        points = []
        bSpace = 1.5*SPACE-5
        space = SPACE-5
        lSpace = 0.5*SPACE-5
        if ya > yb:
            pair = len(self.graph[rb])%2 == 0
            if ya == yb + SPACE:
                points = (xa, ya-RADIUS), (xb, yb+RADIUS)
            elif xa >= xb:
                points.append((xb, yb+RADIUS))
                for r in range(ra-rb-1):
                    if len(self.graph[r+rb+1])%2 == 0:
                        if pair:
                            points.append((xb+lSpace, yb+lSpace+r*SPACE))
                            points.append((xb+lSpace, yb+bSpace+r*SPACE))
                        else:
                            points.append((xb+space, yb+lSpace+r*SPACE))
                            points.append((xb+space, yb+bSpace+r*SPACE))
                    else:
                        if pair:
                            points.append((xb+space, yb+lSpace+r*SPACE))
                            points.append((xb+space, yb+bSpace+r*SPACE))
                        else:
                            points.append((xb+lSpace, yb+space+r*SPACE))
                            points.append((xb+lSpace, yb+bSpace+r*SPACE))
                points.append((xb+lSpace, ya-lSpace))
                points.append((xa, ya-RADIUS))
            elif xa < xb:
                points.append((xb, yb+RADIUS))
                for r in range(ra-rb-1):
                    if len(self.graph[r+rb+1])%2 == 0:
                        if pair:
                            points.append((xb-lSpace, yb+lSpace+r*SPACE))
                            points.append((xb-lSpace, yb+bSpace+r*SPACE))
                        else:
                            points.append((xb-space, yb+lSpace+r*SPACE))
                            points.append((xb-space, yb+bSpace+r*SPACE))
                    else:
                        if pair:
                            points.append((xb-space, yb+lSpace+r*SPACE))
                            points.append((xb-space, yb+bSpace+r*SPACE))
                        else:
                            points.append((xb-lSpace, yb+lSpace+r*SPACE))
                            points.append((xb-lSpace, yb+bSpace+r*SPACE))
                points.append((xb-lSpace, ya-lSpace))
                points.append((xa, ya-RADIUS))
        else:
            pair = len(self.graph[ra])%2 == 0
            if yb == ya + SPACE:
                points = (xb, yb-RADIUS), (xa, ya+RADIUS)
            elif xb >= xa:
                points.append((xa, ya+RADIUS))
                for r in range(rb-ra-1):
                    if len(self.graph[r+ra+1])%2 == 0:
                        if pair:
                            points.append((xa+lSpace, ya+lSpace+r*SPACE))
                            points.append((xa+lSpace, ya+bSpace+r*SPACE))
                        else:
                            points.append((xa+space, ya+lSpace+r*SPACE))
                            points.append((xa+space, ya+bSpace+r*SPACE))
                    else:
                        if pair:
                            points.append((xa+space, ya+lSpace+r*SPACE))
                            points.append((xa+space, ya+bSpace+r*SPACE))
                        else:
                            points.append((xa+lSpace, ya+lSpace+r*SPACE))
                            points.append((xa+lSpace, ya+bSpace+r*SPACE))
                points.append((xa+lSpace, yb-lSpace))
                points.append((xb, yb-RADIUS))
            elif xb < xa:
                points.append((xa, ya+RADIUS))
                for r in range(rb-ra-1):
                    if len(self.graph[r+ra+1])%2 == 0:
                        if pair:
                            points.append((xa-lSpace, ya+lSpace+r*SPACE))
                            points.append((xa-lSpace, ya+bSpace+r*SPACE))
                        else:
                            points.append((xa-space, ya+lSpace+r*SPACE))
                            points.append((xa-space, ya+bSpace+r*SPACE))
                    else:
                        if pair:
                            points.append((xa-space, ya+lSpace+r*SPACE))
                            points.append((xa-space, ya+bSpace+r*SPACE))
                        else:
                            points.append((xa-lSpace, ya+lSpace+r*SPACE))
                            points.append((xa-lSpace, ya+bSpace+r*SPACE))
                points.append((xa-lSpace, yb-lSpace))
                points.append((xb, yb-RADIUS))
        return tuple(points)






    def register(self) -> None:
        """
        Register the canvas image in a file
        """
        self.canvas.update()
        self.canvas.postscript(file="./processing_files/rank.ps", colormode="color", width=self.xmax+100, height=self.ymax+100)
        #self.convert_PS_to_PNG("./processing_files/rank.ps", "./rank.png")
        #aspdraw.
        #img_src = Image(filename="./processing_files/rank.ps")
        #img_dest = img_src.convert('png')
        #img_dest.save("./rank.png")
        #img = Image.open("./processing_files/rank.ps")
        #img.show()
        #img.save("./rank.png")


    def convert_PS_to_PNG(self, srcPath, destPath):
            """
            https://products.aspose.com/pdf/fr/python-net/conversion/ps-to-png/
            """
            
            #path_infile = self.dataDir + infile       
            options = PsLoadOptions()
            #options.SupressErrors = True
            # Open .ps document with created load options
            document = Document(srcPath, options)
            # Create Resolution object
            resolution = Resolution(300)
            device = PngDevice(resolution)
            #pageCount = 1
            #while pageCount <= document.Pages.Count:
            stream = io.FileIO(file=destPath, mode="w")
            #img = open(destPath, "w")
                #imageStream = FileStream(self.dataDir + outfile + str(pageCount) + "_out.png" , FileMode.Create)
                # Convert a particular page and save the image to stream
            device.process(document.pages[1],stream)
            #device.Process(document.Pages[pageCount], img)
                # Close stream
            #img.close()
            stream.close()
                #pageCount = pageCount + 1
            print(srcPath + " converted into " + destPath)