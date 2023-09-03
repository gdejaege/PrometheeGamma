from .TabsControllers import OrthogonalGraphController, TextboxController, RankController
from ....Views.ResultTabViews.ResultsVisualisationViews.ResultVisualisationView import ResultVisualisationView


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
    """

    def __init__(self, master, models:tuple, root) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        models : tuple[PrometheeGamma, ResultTabModel, DataTabModel]
            models = (prometheeGamma, resultTabModel, dataTabModel), the 3 needed models for result visualisation
        root : CTk
            the root window
        """
        self.root = root
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
        self.rankController = RankController(master=master, prometheeGamma=self.prometheeGamma, resultTabModel=self.resultTabModel, 
                                             dataTabModel=self.dataTabModel, root=self.root)
        self.rankController.showView()


    def refresh(self) -> None:
        """Refresh the 3 tabs
        """
        self.textboxController.refreshView()
        self.orhtogonalGraphController.refreshView()
        self.rankController.refreshView()


    def saveOgraph(self, directory):
        """Save the orthogonal graph in directory

        Parameters
        ----------
        directory : str
            the directory in which to save the graph
        """
        self.orhtogonalGraphController.saveOgraph(directory)


    def saveRgraph(self, directory):
        """Save the rank graph in directory

        Parameters
        ----------
        directory : str
            the directory in which to save the graph
        """
        self.rankController.saveRgraph(directory)


    def destroy(self):
        """Destroy the resultVisualisationView
        """
        self.resultVisualisationView.destroy()