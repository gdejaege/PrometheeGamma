#from Resources.ScrollableFrames.HVScrollableFrame import HVScrollableFrame
from .HVScrollableFrame import HVScrollableFrame


class ResizableScrollableFrame(HVScrollableFrame):
    """
    A class to make a resizable scrollable frame

    Attributes
    ----------
    minWidth : int
        the minimal width (in pixel) of the inner frame
    minHeight : int
        the minimal height (in pixel) of the inner frame

    """

    def __init__(self, master, bg_color="#ffffff", fg_color="#ffffff"):
        super().__init__(master, bg_color=bg_color, fg_color=fg_color)

        self.minWidth = 0
        self.minHeight = 0


    def onCanvasConfigure(self, event):
        """Reset the canvas window to encompass inner frame when required

        Parameters
        ----------
        event : Event
            a configure event
        """
        canvas_width = event.width
        canvas_height = event.height
        self.canvas.itemconfig(self.canvas_window, width = max(canvas_width, self.minWidth), height = max(canvas_height, self.minHeight))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def resize(self, width:int, height:int):
        """Resize the inner frame

        In fact, this function does not really resize the inner frame, but set the values of minimal size of inner frame
        Followed by a configure event, the inner frame size will be effectively modified

        Parameters
        ----------
        width : int
            the new minimal width (in pixel) of the inner frame
        height : int
            the new minimal height (in pixel) of the inner frame
        """
        self.minWidth = width
        self.minHeight = height