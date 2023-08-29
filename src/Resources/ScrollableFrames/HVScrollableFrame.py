from customtkinter import (CTkFrame, CTkCanvas, CTkScrollbar)

from Resources.ScrollableFrames.VScrollableFrame import VScrollableFrame


class HVScrollableFrame(VScrollableFrame):
    """
    A class to make a scrollable frame with vertical and horizontal scrollbars

    Attributes
    ----------
    hsb : CTkScrollbar
        the horizontal scrollbar

    Methods
    -------
    """

    def __init__(self, master, bg_color="#ffffff", fg_color="#ffffff"):
        super().__init__(master, bg_color=bg_color, fg_color=fg_color)

        self.hsb = CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hsb.set)
        self.canvas.pack_forget()
        self.vsb.pack_forget()

        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)


    def onCanvasConfigure(self, event):
        """Reset the canvas window to encompass inner frame when required

        Parameters
        ----------
        event : Event
            a configure event
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))