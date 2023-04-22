from customtkinter import CTkTabview

class ResultVisualisationView:
    class ViewListener:
        def showTabular(self, master):
            pass
        def showOrthogonalGraph(self, master):
            pass
        def showRank(self, master):
            pass
    
    def __init__(self, master) -> None:
        self.frame = CTkTabview(master=master, fg_color="#ffffff")

        self.tab_tabular = self.frame.add("Tabular")
        self.tab_ograph = self.frame.add("Orthogonal graph")
        self.tab_rank = self.frame.add("Ranking")

        self.listener = None


    def setListener(self, l:ViewListener):
        self.listener = l


    def show(self):
        self.frame.place(relx=0.02, y=150, relwidth=0.96, bordermode='inside')
        self.listener.showTabular(master=self.tab_tabular)
        self.listener.showOrthogonalGraph(master=self.tab_ograph)
        self.listener.showRank(master=self.tab_rank)
