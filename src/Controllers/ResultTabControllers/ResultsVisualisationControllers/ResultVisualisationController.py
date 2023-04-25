from Views.ResultTabViews.ResultViusalisationView import ResultVisualisationView

class ResultVisualisationController(ResultVisualisationView.ViewListener):
    def __init__(self, master) -> None:
        self.resultVisualisationView = ResultVisualisationView(master=master)
        self.resultVisualisationView.setListener(self)


    def show(self):
        self.resultVisualisationView.show()


    def showTabular(self, master):
        pass


    def showOrthogonalGraph(self, master):
        pass


    def showRank(self, master):
        pass
        