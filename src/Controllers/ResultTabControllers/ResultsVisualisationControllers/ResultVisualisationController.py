from Views.ResultTabViews.ResultVisualisationView import ResultVisualisationView
from Controllers.ResultTabControllers.ResultsVisualisationControllers.TabsControllers.OrthogonalGraphController import OrthogonalGraphController
from Controllers.ResultTabControllers.ResultsVisualisationControllers.TabsControllers.TextboxController import TextboxController
from Controllers.ResultTabControllers.ResultsVisualisationControllers.TabsControllers.RankController import RankController

class ResultVisualisationController:
    """
    A class to control the three tabs for result visualization

    Attributes
    ----------
    resultVisualisationView : ResultVisualisationView
        the result visualisation view
    prometheeGamma : PrometheeGamma
        the model for Promethee Gamma method. It contains the results of the method
    resultTabModel : ResultTabModel
        the model of the result tab. It contains the parameters of the method
    dataTabModel : DataTabModel
        the model of the data tab. It contain the input data of the method
    orhtogonalGraphController : OrhtogonalGraphController
        the controller for the orthogonal graph part
    textboxController : TextboxController
        the controller for the textbox part
    rankController : RankController
        the controller for the rank graph part

    Methods
    -------
    show()
        show the 3 tabs
    refresh()
        refresh the 3 tabs
    """

    def __init__(self, master, models:tuple) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        models : tuple[PrometheeGamma, ResultTabModel, DataTabModel]
            models = (prometheeGamma, resultTabModel, dataTabModel), the 3 needed models for result visualisation
        """
        self.resultVisualisationView = ResultVisualisationView(master=master)
        (self.prometheeGamma, self.resultTabModel, self.dataTabModel) = models
        self.orhtogonalGraphController = None
        self.textboxController = None
        self.rankController = None


    def show(self) -> None:
        """Show the 3 tabs
        """
        self.resultVisualisationView.show()
        master = self.resultVisualisationView.getTextBoxMaster()
        self.textboxController = TextboxController(master=master, model=self.prometheeGamma)
        self.textboxController.showView()
        master = self.resultVisualisationView.getOrthogonalGraphMaster()
        self.orhtogonalGraphController = OrthogonalGraphController(master=master, model=self.prometheeGamma)
        self.orhtogonalGraphController.showView()
        master = self.resultVisualisationView.getRankGraphMaster()
        self.rankController = RankController(master=master, prometheeGamma=self.prometheeGamma, resultTabModel=self.resultTabModel, dataTabModel=self.dataTabModel)
        self.rankController.showView()


    def refresh(self) -> None:
        """Refresh the 3 tabs
        """
        self.textboxController.refreshView()
        self.orhtogonalGraphController.refreshView()
        self.rankController.refreshView()


    def saveOgraph(self, folder):
        self.orhtogonalGraphController.saveOgraph(folder)


    def saveRgraph(self, folder):
        self.rankController.saveRgraph(folder)


    def destroy(self):
        self.resultVisualisationView.destroy()