from customtkinter import CTkTabview

class ResultVisualisationView:
    """
    A class to visualise the results of PROMETHEE Gamma method

    Attributes
    ----------
    frame : CTkTabView
        the frame that will contain the 3 tabs of the view
    textboxTab : CTkFrame
        the frame of textbox tab
    ographTab : CTkFrame
        the frame of orthogonal graph tab
    rankGraphTab
        the frame of rank graph tab

    Methods
    -------
    show()
        show the main frame
    getTextBoxMaster()
        return the master frame of textbox tab
    getOrthogonalGraphMaster()
        return the master frame of orthogonal graph tab
    getRankGraphMaster():
        return the master frame of rank graph tab
    """

    def __init__(self, master) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the parent master frame
        """
        
        self.frame = CTkTabview(master=master, fg_color="#ffffff")
        self.textboxTab = self.frame.add("Tabular")
        self.ographTab = self.frame.add("Orthogonal graph")
        self.rankGraphTab = self.frame.add("Ranking")


    def show(self):
        """Show the main frame
        """

        self.frame.place(relx=0.02, y=0.02, relwidth=0.96, relheight=0.96, bordermode='inside')
        #self.frame.grid(row=4, column=0, columnspan=4, sticky="n")
        #self.frame.pack(side="top", expand=True, fill='both')


    def getTextBoxMaster(self):
        """Return the master frame of textbox tab

        Return
        ------
        textboxTab : CTkFrame
            the master frame of textbox tab
        """

        return self.textboxTab
    

    def getOrthogonalGraphMaster(self):
        """Return the master frame of orthogonal graph tab

        Return
        ------
        ographTab : CTkFrame
            the master frame of orthogonal graph tab
        """

        return self.ographTab
    

    def getRankGraphMaster(self):
        """Return the master frame of rank graph tab

        Return
        ------
        rankGraphTab : CTkFrame
            the master frame of rank graph tab
        """

        return self.rankGraphTab
    

    def destroy(self):
        self.frame.destroy()