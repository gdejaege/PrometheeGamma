from customtkinter import (CTkCanvas, CTkScrollbar, CTkFrame, CTkCheckBox, IntVar)
from Resources.ScrollableFrame import ScrollableFrame
from Views.ResultTabViews.AlternativeView import AlternativeView
from aspose.pdf import (PsLoadOptions, Document)
from aspose.pdf.devices import PngDevice, Resolution
import io
from PIL import Image, ImageDraw

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
        self.ymax = 100


    def buildAlternativesDict(self, aList:list):
        self.alternatives = {}
        for a in aList:
            self.alternatives[a] = IntVar(master=self.rightFrame, value=1)


    def BuildCheckBoxs(self):
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
        self.leftFrame.place(x=1, y=1, relheight=1.0, relwidth=0.7)
        self.hbar.pack(side="bottom", fill="x")
        self.vbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", expand=True, fill="both")

        self.scrollFrame.place(relx=0.7, y=1, relheight=1.0, relwidth=0.3)


    def resizeCanvas(self, width:int, height:int):
        """
        Resize the canvas
        """
        self.canvas.config(scrollregion=(0, 0, width+50, height+50))


    def drawCanvas(self, r:list, lmax:int, matrixResults:list) -> None:
        """
        Display result in a schematic ranking
        """
        self.canvas.delete('all')
        #size : self.tab_rank.winfo_screenwidth()
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
        self.ymin = 100
        self.ymax = len(r)*100
        self.xmin = 1000000
        self.xmax = 0
        self.graph = []
        columnLength = 0
        for i in range(len(r)):
            y = (columnLength+1)*100
            x = lmax//2 + 50
            for k in range(len(r[i])):
                if self.alternatives[r[i][k]].get():
                    x -= 50
            if x < self.xmin:
                self.xmin = x
            rowLength = 0
            row = []
            for j in range(len(r[i])):
                xlength = x+rowLength*100
                if self.alternatives[r[i][j]].get():
                    a = AlternativeView(name=r[i][j], canvas=self.canvas, x=xlength, y=y, row=columnLength, column=rowLength)
                    self.construction[r[i][j]] = a
                    row.append(a)
                    rowLength += 1
                    if self.xmax < xlength:
                        self.xmax = xlength
            if rowLength > 0:
                columnLength += 1
                self.graph.append(row)
        self.canvas.config(scrollregion=(0, 0, self.xmax+100, self.ymax+100))


    def add_lines(self, matrixResults:list) -> None:
        """
        Add plain and dash lines to the schema
        """
        for i in range(len(matrixResults)):
            for j in range(i+1, len(matrixResults)):
                x = matrixResults[i][j].split(' I ')
                y = matrixResults[i][j].split(' J ')
                if len(x) > 1 and self.alternatives[x[0]].get() and self.alternatives[x[1]].get():
                    #self.draw_indiff_line(a=self.construction[x[0]], b=self.construction[x[1]])
                    self.draw_line(a=self.construction[x[0]], b=self.construction[x[1]])
                elif len(y) > 1 and self.alternatives[y[0]].get() and self.alternatives[y[1]].get():
                    #self.draw_incomp_line(a=self.construction[y[0]], b=self.construction[y[1]])
                    self.draw_line(a=self.construction[y[0]], b=self.construction[y[1]], dash=True)


    def draw_line(self, a:AlternativeView, b:AlternativeView, dash=False):
        """
        Draw the lines
        """
        (xa, ya) = a.get_coords()
        (xb, yb) = b.get_coords()
        if ya == yb:
            if xa > xb:
                h = round((xa - xb)/(self.xmax-self.xmin) * 20) + 35
                points = (xb, yb+30), (xb + (xa-xb)/2, ya+h), (xa, ya+30)
            else:
                h = round((xb - xa)/(self.xmax-self.xmin) * 20) + 35
                points = (xa, ya+30), (xa + (xb-xa)/2, ya+h), (xb, yb+30)
        else:
            points = self.computePoints(a, b)
        if dash:
            self.canvas.create_line(points, smooth=True, dash=(3,1))
        else:
            self.canvas.create_line(points, smooth=True)


    def computePoints(self, a:AlternativeView, b:AlternativeView):
        """
        Compute the points sequence
        """
        (xa, ya) = a.get_coords()
        (xb, yb) = b.get_coords()
        ra = a.getRow()
        rb = b.getRow()
        points = []
        if ya > yb:
            pair = len(self.graph[rb])%2 == 0
            if ya == yb + 100:
                points = (xa, ya-30), (xb, yb+30)
            elif xa >= xb:
                points.append((xb, yb+30))
                for r in range(ra-rb-1):
                    if len(self.graph[r+rb+1])%2 == 0:
                        if pair:
                            points.append((xb+45, yb+45+r*100))
                            points.append((xb+45, yb+145+r*100))
                        else:
                            points.append((xb+95, yb+45+r*100))
                            points.append((xb+95, yb+145+r*100))
                    else:
                        if pair:
                            points.append((xb+95, yb+45+r*100))
                            points.append((xb+95, yb+145+r*100))
                        else:
                            points.append((xb+45, yb+45+r*100))
                            points.append((xb+45, yb+145+r*100))
                points.append((xb+45, ya-45))
                points.append((xa, ya-30))
            elif xa < xb:
                points.append((xb, yb+30))
                for r in range(ra-rb-1):
                    if len(self.graph[r+rb+1])%2 == 0:
                        if pair:
                            points.append((xb-45, yb+45+r*100))
                            points.append((xb-45, yb+145+r*100))
                        else:
                            points.append((xb-95, yb+45+r*100))
                            points.append((xb-95, yb+145+r*100))
                    else:
                        if pair:
                            points.append((xb-95, yb+45+r*100))
                            points.append((xb-95, yb+145+r*100))
                        else:
                            points.append((xb-45, yb+45+r*100))
                            points.append((xb-45, yb+145+r*100))
                points.append((xb-45, ya-45))
                points.append((xa, ya-30))
        else:
            pair = len(self.graph[ra])%2 == 0
            if yb == ya + 100:
                points = (xb, yb-30), (xa, ya+30)
            elif xb >= xa:
                points.append((xa, ya+30))
                for r in range(rb-ra-1):
                    if len(self.graph[r+ra+1])%2 == 0:
                        if pair:
                            points.append((xa+45, ya+45+r*100))
                            points.append((xa+45, ya+145+r*100))
                        else:
                            points.append((xa+95, ya+45+r*100))
                            points.append((xa+95, ya+145+r*100))
                    else:
                        if pair:
                            points.append((xa+95, ya+45+r*100))
                            points.append((xa+95, ya+145+r*100))
                        else:
                            points.append((xa+45, ya+45+r*100))
                            points.append((xa+45, ya+145+r*100))
                points.append((xa+45, yb-45))
                points.append((xb, yb-30))
            elif xb < xa:
                #points = (xa, ya+30), (xa-45, ya+45), (xa-45, yb-45), (xb, yb-30)
                points.append((xa, ya+30))
                for r in range(rb-ra-1):
                    if len(self.graph[r+ra+1])%2 == 0:
                        if pair:
                            points.append((xa-45, ya+45+r*100))
                            points.append((xa-45, ya+145+r*100))
                        else:
                            points.append((xa-95, ya+45+r*100))
                            points.append((xa-95, ya+145+r*100))
                    else:
                        if pair:
                            points.append((xa-95, ya+45+r*100))
                            points.append((xa-95, ya+145+r*100))
                        else:
                            points.append((xa-45, ya+45+r*100))
                            points.append((xa-45, ya+145+r*100))
                points.append((xa-45, yb-45))
                points.append((xb, yb-30))
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