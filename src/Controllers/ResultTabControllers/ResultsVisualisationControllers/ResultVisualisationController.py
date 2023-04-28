from Views.ResultTabViews.ResultViusalisationView import ResultVisualisationView
from Controllers.ResultTabControllers.ResultsVisualisationControllers.OrthogonalGraphController import OrthogonalGraphController
from Controllers.ResultTabControllers.ResultsVisualisationControllers.TabularController import TabularController
from Controllers.ResultTabControllers.ResultsVisualisationControllers.RankController import RankController

class ResultVisualisationController(ResultVisualisationView.ViewListener):
    def __init__(self, master, models:tuple) -> None:
        self.resultVisualisationView = ResultVisualisationView(master=master)
        self.resultVisualisationView.setListener(self)

        self.prometheeGamma = models[0]
        self.resultTabModel = models[1]
        self.dataTabModel = models[2]
        
        self.orhtogonalGraphController = None
        self.tabularController = None
        self.rankController = None


    def show(self):
        self.resultVisualisationView.show()


    def showTabular(self, master):
        self.tabularController = TabularController(master=master, model=self.prometheeGamma)
        self.tabularController.showView()


    def showOrthogonalGraph(self, master):
        self.orhtogonalGraphController = OrthogonalGraphController(master=master, model=self.prometheeGamma)
        self.orhtogonalGraphController.showView()


    def showRank(self, master):
        self.rankController = RankController(master=master, prometheeGamma=self.prometheeGamma, resultTabModel=self.resultTabModel, dataTabModel=self.dataTabModel)
        self.rankController.showView()


    def refresh(self):
        self.tabularController.refreshView()
        self.orhtogonalGraphController.refreshView()
        self.rankController.refreshView()
        