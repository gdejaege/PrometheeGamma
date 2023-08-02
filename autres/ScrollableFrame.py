import platform
from customtkinter import (CTkFrame, CTkCanvas, CTkScrollbar, CTkLabel, CTk)


class ScrollableFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.canvas = CTkCanvas(self, borderwidth=0, background="#ffffff")
        self.innerFrame = CTkFrame(self.canvas, bg_color="#ffffff", fg_color="#ffffff")
        self.vsb = CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.hsb = CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4,4), window=self.innerFrame, anchor="nw", tags="self.innerFrame")

        self.innerFrame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        self.innerFrame.bind('<Enter>', self.onEnter)
        self.innerFrame.bind('<Leave>', self.onLeave)

        self.onFrameConfigure(None)


    def frame(self) -> CTkFrame:
        """
        The inner frame
        """
        return self.innerFrame


    def onFrameConfigure(self, event):                             
        """
        Reset the scroll region to encompass the inner frame
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def onCanvasConfigure(self, event):
        """
        Reset the canvas window to encompass inner frame when required
        """
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)


    def onMouseWheel(self, event):
        """
        cross platform scroll wheel event
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
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)


    def onLeave(self, event):
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")



class Test:
    def __init__(self, master) -> None:
        self.frame = ScrollableFrame(master=master)

        label = CTkLabel(master=self.frame.frame(), text="testLabel")
        label.place(x=20, y=20)

        self.frame.pack()


if __name__ == "__main__":
    root = CTk()
    t = Test(root)
    root.mainloop()
