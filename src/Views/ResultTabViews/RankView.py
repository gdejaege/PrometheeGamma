from customtkinter import (CTkCanvas, CTkScrollbar)
from tkinter import *
from Views.ResultTabViews.AlternativeView import AlternativeView
from aspose.pdf import (PsLoadOptions, Document)
from aspose.pdf.devices import PngDevice, Resolution
import io

#import aspose.pdf as asp

#from aspose.pdf.plugins 
#import aspose.pydrawing as aspdraw
#from aspose.pydrawing import
from PIL import Image, ImageDraw
#from wand.image import Image

class RankView:
    class ViewListener:
        pass

    def __init__(self, master) -> None:
        self.master = master
        self.size = 100
        self.canvas=CTkCanvas(master, bg='#FFFFFF', width=750, height=550, scrollregion=(0,0,100,100))
        self.hbar=CTkScrollbar(master, orientation=HORIZONTAL, command=self.canvas.xview)
        self.vbar=CTkScrollbar(master, orientation=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        #master.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        self.listener = None
        self.construction = {}
        self.graph = []
        self.xmin = 1000000
        self.ymin = 100
        self.xmax = 0
        self.ymax = 100


    def setListener(self, l:ViewListener):
        """
        Set the listener
        """
        self.listener = l
        

    def show(self):
        """
        Show the canvas area
        """
        self.hbar.pack(side=BOTTOM, fill=X)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)


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
        for i in range(len(r)):
            y = (i+1)*100
            x = lmax//2 - (len(r[i])-1)*50
            self.graph.append([])
            if x < self.xmin:
                self.xmin = x
            for j in range(len(r[i])):
                xlength = x+j*100
                a = AlternativeView(r[i][j], self.canvas, xlength, y, i, j)
                self.construction[r[i][j]] = a
                self.graph[i].append(a)
                if self.xmax < xlength:
                    self.xmax = xlength
        self.canvas.config(scrollregion=(0, 0, self.xmax+100, self.ymax+100))


    def add_lines(self, matrixResults:list) -> None:
        """
        Add plain and dash lines to the schema
        """
        for i in range(len(matrixResults)):
            for j in range(i+1, len(matrixResults)):
                x = matrixResults[i][j].split(' I ')
                y = matrixResults[i][j].split(' J ')
                if len(x) > 1:
                    #self.draw_indiff_line(a=self.construction[x[0]], b=self.construction[x[1]])
                    self.draw_line(a=self.construction[x[0]], b=self.construction[x[1]])
                elif len(y) > 1:
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


















    def draw_indiff_line(self, a:AlternativeView, b:AlternativeView):
        """
        Draw a plain line to represent indifferentiability
        """
        (x0, y0, x1, y1) = self.get_line_coords(a, b)
        self.canvas.create_line(x0, y0, x1, y1)
        #self.canvas.create_arc()


    def draw_incomp_line(self,  a:AlternativeView, b:AlternativeView):
        """
        Draw a dash line to represent incompatibility
        """
        (x0, y0, x1, y1) = self.get_line_coords(a, b)
        self.canvas.create_line(x0, y0, x1, y1, dash=(3,1))


    def get_line_coords(self, a:AlternativeView, b:AlternativeView):
        c1 = a.get_coords()
        c2 = b.get_coords()
        if(c1[0] == c2[0]):
            x0 = c1[0]
            x1 = x0
            if(c1[1] > c2[1]):
                y0 = c1[1] - 30
                y1 = c2[1] + 30
            else:
                y0 = c2[1] - 30
                y1 = c1[1] + 30
        elif(c1[1] == c2[1]):
            y0 = c1[1]
            y1 = y0
            if(c1[0] > c2[0]):
                x0 = c2[0] + 30
                x1 = c1[0] - 30
            else:
                x0 = c1[0] + 30
                x1 = c2[0] - 30
        else:
            if(c1[1] > c2[1]):
                x0 = c2[0]
                y0 = c2[1] + 30
                x1 = c1[0]
                y1 = c1[1] - 30
            else:
                x0 = c1[0]
                y0 = c1[1] + 30
                x1 = c2[0]
                y1 = c2[1] - 30
        return (x0, y0, x1, y1)
