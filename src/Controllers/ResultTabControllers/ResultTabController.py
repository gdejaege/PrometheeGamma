from Models.ResultTabModel import ResultTabModel
from Views.ResultTabViews.ResultTabView import ResultTabView
from Controllers.ResultTabControllers.ResultsVisualisationControllers.ResultVisualisationController import ResultVisualisationController

class ResultTabController(ResultTabView.ViewListener):
    """
    Controller of the result tab
    """
    class Listener:
        """
        Interface. Listener of the ResultTabController
        """
        def changeOnTi(self):
            pass
        def changeOnTj(self):
            pass
        def changeOnTiAndTj(self):
            pass
        def changeOnPf(self):
            pass
        def computeResults(self):
            pass
        def getPrometheeGammaModel(self):
            pass
        def getDataTabModel(self):
            pass
    

    def __init__(self, master) -> None:
        """
        Constructor
        Init the ResultTabModel and the ResultTabView
        """
        self.resultTabModel = ResultTabModel(master=master)
        Ti = self.resultTabModel.getTi()
        Tj = self.resultTabModel.getTj()
        Pf = self.resultTabModel.getPf()
        self.resultTabView = ResultTabView(master=master, Ti=Ti, Tj=Tj, Pf=Pf)
        self.resultTabView.setListener(self)
        self.listener = None
        self.resultsVisualisationController = None


    def setListener(self, l:Listener) -> None:
        """
        Set the listener of this controller
        """
        self.listener = l

    
    def showView(self) -> None:
        """
        show the resultTabView
        """
        self.resultTabView.show()


    def changeOnTi(self, newValue:float) -> None:
        """"
        This method controls the reaction of the application following a modification of the value of parameter Ti by the user.
        newValue is the new value of the parameter Ti.
        """
        Tj = self.resultTabModel.getTj_float()
        if newValue > Tj:
            self.resultTabModel.setTj(newValue)
            self.resultTabView.setSliderTjValue(newValue)
            self.listener.changeOnTiAndTj()
        else:
            self.listener.changeOnTi()


    def changeOnTj(self, newValue:float) -> None:
        """"
        This method controls the reaction of the application following a modification of the value of parameter Tj by the user.
        newValue is the new value of the parameter Tj.
        """
        Ti = self.resultTabModel.getTi_float()
        if newValue < Ti:
            self.resultTabModel.setTi(newValue)
            self.resultTabView.setSliderTiValue(newValue)
            self.listener.changeOnTiAndTj()
        else:
            self.listener.changeOnTj()
    
    
    def changeOnPf(self) -> None:
        """"
        This method controls the reaction of the application following a modification of the value of parameter Pf by the user.
        newValue is the new value of the parameter Pf.
        """
        self.listener.changeOnPf()


    def obtainResults(self) -> None:
        """"
        This method controls the reaction of the application following a click on the button Obtain Results.
        """
        self.listener.computeResults()

    
    def getModel(self) -> ResultTabModel:
        """
        Return the current ResultTabModel
        """
        return self.resultTabModel
    

    def loadResultsVisualisation(self, master):
        """
        Loads the three types of results visualizations and show them.
        """
        models = (self.listener.getPrometheeGammaModel(), self.resultTabModel, self.listener.getDataTabModel())
        self.resultsVisualisationController = ResultVisualisationController(master, models)
        self.resultsVisualisationController.show()


    def refreshResultsVisualisation(self):
        """
        Refresh the visualisation of the results
        """
        self.resultsVisualisationController.refresh()