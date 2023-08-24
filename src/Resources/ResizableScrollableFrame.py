from Resources.HVScrollableFrame import HVScrollableFrame

class ResizableScrollableFrame(HVScrollableFrame):
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
        self.minWidth = width
        self.minHeight = height