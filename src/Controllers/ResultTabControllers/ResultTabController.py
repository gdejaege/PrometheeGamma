from Models.ResultTabModel import ResultTabModel
from Views.ResultTabViews.ResultTabView import ResultTabView
from Controllers.ResultTabControllers.ResultVisualisationController import ResultVisualisationController

class ResultTabController(ResultTabView.ViewListener):
    class Listener:
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
    
    def __init__(self, master) -> None:
        self.resultTabModel = ResultTabModel(master=master)
        Ti = self.resultTabModel.getTi()
        Tj = self.resultTabModel.getTj()
        Pf = self.resultTabModel.getPf()
        self.resultTabView = ResultTabView(master=master, Ti=Ti, Tj=Tj, Pf=Pf)
        self.resultTabView.setListener(self)
        self.listener = None
        self.resultsVisualisationController = None


    def setListener(self, l:Listener):
        self.listener = l

    
    def showView(self) -> None:
        """
        show the resultTabView
        """
        self.resultTabView.show()


    def changeOnTi(self, newValue: float):
        Tj = self.resultTabModel.getTj_float()
        if newValue > Tj:
            self.resultTabModel.setTj(newValue)
            self.resultTabView.setSliderTjValue(newValue)
            self.listener.changeOnTiAndTj()
        else:
            self.listener.changeOnTi()


    def changeOnTj(self, newValue: float):
        Ti = self.resultTabModel.getTi_float()
        if newValue < Ti:
            self.resultTabModel.setTi(newValue)
            self.resultTabView.setSliderTiValue(newValue)
            self.listener.changeOnTiAndTj()
        else:
            self.listener.changeOnTj()
    
    
    def changeOnPf(self):
        self.listener.changeOnPf()


    def obtainResults(self):
        self.listener.computeResults()

    
    def getModel(self):
        return self.resultTabModel
    

    def loadResultsVisualisation(self, master):
        self.resultsVisualisationController = ResultVisualisationController(master)