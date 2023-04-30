from Views.ResultTabViews.ResultViusalisationView import ResultVisualisationView
from Controllers.ResultTabControllers.ResultsVisualisationControllers.TabsControllers.OrthogonalGraphController import OrthogonalGraphController
from Controllers.ResultTabControllers.ResultsVisualisationControllers.TabsControllers.TabularController import TabularController
from Controllers.ResultTabControllers.ResultsVisualisationControllers.TabsControllers.RankController import RankController

class ResultVisualisationController:
    """
    Controller of the three tabs for visualization of the results.
    """
    def __init__(self, master, models:tuple) -> None:
        self.resultVisualisationView = ResultVisualisationView(master=master)

        self.prometheeGamma = models[0]
        self.resultTabModel = models[1]
        self.dataTabModel = models[2]
        
        self.orhtogonalGraphController = None
        self.tabularController = None
        self.rankController = None


    def show(self) -> None:
        """
        Show the three tabs
        """
        self.resultVisualisationView.show()
        master = self.resultVisualisationView.getTabularMaster()
        self.tabularController = TabularController(master=master, model=self.prometheeGamma)
        self.tabularController.showView()
        master = self.resultVisualisationView.getOrthogonalGraphMaster()
        self.orhtogonalGraphController = OrthogonalGraphController(master=master, model=self.prometheeGamma)
        self.orhtogonalGraphController.showView()
        master = self.resultVisualisationView.getRankMaster()
        self.rankController = RankController(master=master, prometheeGamma=self.prometheeGamma, resultTabModel=self.resultTabModel, dataTabModel=self.dataTabModel)
        self.rankController.showView()


    def refresh(self):
        """
        Refresh the three tabs
        """
        self.tabularController.refreshView()
        self.orhtogonalGraphController.refreshView()
        self.rankController.refreshView()
        