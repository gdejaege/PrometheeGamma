from customtkinter import CTkTabview

class ResultVisualisationView:
    def __init__(self, master) -> None:
        self.frame = CTkTabview(master=master, fg_color="#ffffff")

        self.tab_tabular = self.frame.add("Tabular")
        self.tab_ograph = self.frame.add("Orthogonal graph")
        self.tab_rank = self.frame.add("Ranking")


    def show(self):
        """
        Show the main frame
        """
        self.frame.place(relx=0.02, y=150, relwidth=0.96, bordermode='inside')


    def getTabularMaster(self):
        """
        Return the frame of the tabular tab
        """
        return self.tab_tabular
    

    def getOrthogonalGraphMaster(self):
        """
        Return the frame of the orthogonal graph tab
        """
        return self.tab_ograph
    

    def getRankMaster(self):
        """
        Retunr the frame of the rank tab
        """
        return self.tab_rank