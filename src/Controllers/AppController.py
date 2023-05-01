from Views.AppView import AppView
from Controllers.DataTabControllers.DataTabController import DataTabController
from Controllers.ResultTabControllers.ResultTabController import ResultTabController
from Controllers.HelpForParametersTabControllers.HelpForParametersTabController import HelpForParametersTabController
from Models.PrometheeGamma import PrometheeGamma

class AppController(AppView.ViewListener, ResultTabController.Listener):
    """
    The main controller of the application.
    It allows to start and stop the application, but also to make the link between its different parts.
    """
    def __init__(self) -> None:
        """
        Constructor
        """
        self.appView = AppView()
        self.appView.setListener(self)
        self.alreadyCompute = False
        self.prometheeGamma = PrometheeGamma()
        self.dataTabController = None
        self.resultTabController = None
        self.helpForParametersTabController = None


    def run(self) -> None:
        """
        Launch the app
        """
        self.appView.show()
        self.appView.mainloop()


    def showDataTabView(self, master) -> None:
        """
        Show the data tab
        """
        self.dataTabController = DataTabController(master=master)
        self.dataTabController.showView()


    def showResultTabView(self, master) -> None:
        """
        Show the result tab
        """
        self.resultTabController = ResultTabController(master=master)
        self.resultTabController.setListener(self)
        self.resultTabController.showView()


    def showHelpForParametersTabView(self, master) -> None:
        """
        Show the HelpForParameters tab
        """
        dataTabModel = self.dataTabController.getModel()
        self.helpForParametersTabController = HelpForParametersTabController(master, dataTabModel)
        self.helpForParametersTabController.showView()


    def computeResults(self) -> None:
        """
        Compute the result of the Promethee Gamma method
        """
        if not self.alreadyCompute:
            dataTabModel = self.dataTabController.getModel()
            resultTabModel = self.resultTabController.getModel()
            self.prometheeGamma.setDataTabModel(dataTabModel)
            self.prometheeGamma.setResultTabModel(resultTabModel)
            self.alreadyCompute = True
        self.prometheeGamma.computeAll()
        self.resultTabController.refreshResultsVisualisation()


    def changeOnTiAndTj(self) -> None:
        """
        Recompute the needed results in case of change on Ti and Tj.
        This method must be called if there is a simultaneous change of the thresholds Ti and Tj.
        """
        if self.alreadyCompute:
            self.prometheeGamma.computeMatrixI()
            self.prometheeGamma.computeMatrixJ()
            self.prometheeGamma.computeMatrixResults()
            self.resultTabController.refreshResultsVisualisation()


    def changeOnTi(self) -> None:
        """
        Recompute the needed results in case of change on Ti.
        This method must be called if there is a change of the threshold Ti and not on Tj.
        """
        if self.alreadyCompute:
            self.prometheeGamma.computeMatrixI()
            self.prometheeGamma.computeMatrixResults()
            self.resultTabController.refreshResultsVisualisation()


    def changeOnTj(self) -> None:
        """
        Recompute the needed results in case of change on Tj.
        This method must be called if there is a change of the threshold Tj and not on Ti.
        """
        if self.alreadyCompute:
            self.prometheeGamma.computeMatrixJ()
            self.computeResults()
            self.resultTabController.refreshResultsVisualisation()


    def changeOnPf(self) -> None:
        """
        Recompute the needed results in case of change on Pf.
        This method must be called if there is a change of the parameter Pf.
        """
        if self.alreadyCompute:
            self.prometheeGamma.computeMatrixP()
            self.computeResults()
            self.resultTabController.refreshResultsVisualisation()


    def getPrometheeGammaModel(self) -> PrometheeGamma:
        """
        Return the current used model for the Promethee Gamma method
        """
        return self.prometheeGamma
    

    def getDataTabModel(self):
        """
        Return the current data tab model
        """
        return self.dataTabController.getModel()