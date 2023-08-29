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
    """

    def __init__(self, master) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the parent master frame
        """
        
        self.frame = CTkTabview(master=master, fg_color="#ffffff")
        self.textboxTab = self.frame.add("Matrix")
        self.ographTab = self.frame.add("Orthogonal graph")
        self.rankGraphTab = self.frame.add("Ranking")


    def show(self):
        """Show the main frame
        """
        self.frame.place(relx=0.02, y=0.02, relwidth=0.96, relheight=0.96, bordermode='inside')


    def getTextBoxMaster(self):
        """Return the master frame of textbox tab

        Returns
        -------
        CTkFrame
            the master frame of textbox tab
        """
        return self.textboxTab
    

    def getOrthogonalGraphMaster(self):
        """Return the master frame of orthogonal graph tab

        Returns
        -------
        CTkFrame
            the master frame of orthogonal graph tab
        """
        return self.ographTab
    

    def getRankGraphMaster(self):
        """Return the master frame of rank graph tab

        Returns
        -------
        CTkFrame
            the master frame of rank graph tab
        """
        return self.rankGraphTab
    

    def destroy(self):
        """Destroy the result visualisation
        """
        self.frame.destroy()