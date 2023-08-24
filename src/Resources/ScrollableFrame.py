import platform
from customtkinter import (CTkFrame, CTkCanvas, CTkScrollbar)


class ScrollableFrame(CTkFrame):
    """
    A class to make a custom scrollable frame with customtkinter
    It is inspired by the vertical scrollable frame on https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01

    Attributes
    ----------
    canvas : CTkCanvas
        a canvas that will contain the scrollable frame and the scrollbars
    innerFrame : CTkFrame
        the scrollable frame
    vsb : CTkScrollbar
        the vertical scrollbar
    hsb : CTkScrollbar
        the horizontal scrollbar
    canvas_window : int
        id of canvas window that contain the innerFrame
    
    Methods
    -------
    frame()
        return the inner frame, i.e. the scrollable frame
    onFrameConfigure(event)                             
        reset the scroll region to encompass the inner frame
    resize(region=(0,0,100,100))
        resize the canvas
    onCanvasConfigure(event)
        reset the canvas window to encompass inner frame when required
    onMouseWheel(event)
        ross platform scroll wheel event
    onEnter(event)
        cross platform binding
    onLeave(event)
        cross platform unbinding
    """
    
    def __init__(self, master, bg_color="#ffffff", fg_color="#ffffff"):
        super().__init__(master, bg_color=bg_color, fg_color=fg_color, border_color=fg_color)
        """
        Parameters
        ----------
        master : CTkFrame
            a parent master frame
        bg_color : str
            the background color
        fg_color : str
            the foreground color
        """

        self.canvas = CTkCanvas(self, borderwidth=0, background=bg_color, highlightbackground=bg_color, highlightcolor=bg_color)
        self.innerFrame = CTkFrame(self.canvas, bg_color=bg_color, fg_color=fg_color, border_color=fg_color)
        self.vsb = CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.hsb = CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((0,0), window=self.innerFrame, anchor="nw", tags="self.innerFrame")
        self.innerFrame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        self.innerFrame.bind('<Enter>', self.onEnter)
        self.innerFrame.bind('<Leave>', self.onLeave)
        self.onFrameConfigure(None)


    def frame(self) -> CTkFrame:
        """Return the inner frame, i.e. the scrollable frame

        Return
        ------
        innerFrame : CTkFrame
            the inner frame, i.e. the scrollable frame
        """
        return self.innerFrame


    def onFrameConfigure(self, event):                             
        """Reset the scroll region to encompass the inner frame

        Parameters
        ----------
        event : Event
            a configure event
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))        


    def onCanvasConfigure(self, event):
        """Reset the canvas window to encompass inner frame when required

        Parameters
        ----------
        event : Event
            a configure event
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        #canvas_width = event.width
        #canvas_height = event.height
        #self.canvas.itemconfig(self.canvas_window, width = canvas_width, height = canvas_height)

        

    def onMouseWheel(self, event):
        """cross platform scroll wheel event

        Parameters
        ----------
        event : Event
            a scroll wheel event
        """
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )


    def onEnter(self, event):
        """cross platform binding

        Parameters
        ----------
        event : Event
            an entering event
        """
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)


    def onLeave(self, event):
        """cross platform unbinding

        Parameters
        ----------
        event : Event
            a leaving event
        """
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")
