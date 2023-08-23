from Models.ResultTabModel import ResultTabModel
from Views.ResultTabViews.ResultTabView import ResultTabView
from Controllers.ResultTabControllers.ResultsVisualisationControllers.ResultVisualisationController import ResultVisualisationController

class ResultTabController(ResultTabView.ViewListener):
    """
    A class to control the result tab

    Attributes
    ----------
    resultTabModel : ResultTabModel
        the model of the result tab
    resultTabView : ResultTabView
        the view of the result tab
    listener : ResultTabController.Listener
        the listener of this class
    resultsVisualisationController : ResultVisualisationController
        the controller that control visualisation of results. It is a sub controller of this class

    Methods
    -------
    setListener(l:Listener)
        set the listener
    showView()
        show the resultTabView
    refresh()
        refresh the resultTabView
    changeOnTi(newValue:float)
        this method controls the reaction of the application following a modification of the value of parameter Ti by the user
    changeOnTj(newValue:float)
        this method controls the reaction of the application following a modification of the value of parameter Tj by the user
    changeOnPf()
        this method controls the reaction of the application following a modification of the value of parameter Pf by the user
    obtainResults()
        handle click on button Obtain Results
    applyResults(results)
        apply the results provided by a method to help determine the parameters (from helpForParametersTab)
    getModel()
        return the current ResultTabModel
    loadResultsVisualisation(master)
        load the 3 types of results visualizations and show them
    refreshResultsVisualisation()
        refresh the results visualisation
    """

    class Listener:
        """
        Interface for the listener of the ResultTabController

        Methods
        -------
        changeOnTi()
            inform the listener of a change on Ti
        changeOnTj()
            inform the listener of a change on Tj
        changeOnTiAndTj()
            inform the listener of a change on Ti and Tj
        obtainResults()
            demand to the listener to obtain the results
        getPrometheeGammaModel()
            demand to the listener to obtain the PrometheeGamma model
        getDataTabModel()
            demand to the listener to obtain the dataTab model
        """

        def changeOnTi(self):
            pass
        def changeOnTj(self):
            pass
        def changeOnTiAndTj(self):
            pass
        def changeOnPf(self):
            pass
        def obtainResults(self):
            pass
        def getPrometheeGammaModel(self):
            pass
        def getDataTabModel(self):
            pass
    

    def __init__(self, master) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame for the result tab
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
        """Set the listener
        """
        self.listener = l

    
    def showView(self) -> None:
        """Show the resultTabView
        """
        self.resultTabView.show()


    def refresh(self) -> None:
        """Refresh the resultTabView
        """
        self.resultTabView.refresh()


    def changeOnTi(self, newValue:float) -> None:
        """"This method controls the reaction of the application following a modification of the value of parameter Ti by the user

        Parameters
        ----------
        newValue : float
            the new value of Ti parameter
        """
        Tj = self.resultTabModel.getTj_float()
        if newValue > Tj:
            self.resultTabModel.setTj(newValue)
            self.resultTabView.setTjSliderValue(newValue)
            self.listener.changeOnTiAndTj()
        else:
            self.listener.changeOnTi()


    def changeOnTj(self, newValue:float) -> None:
        """"This method controls the reaction of the application following a modification of the value of parameter Tj by the user

        Parameters
        ----------
        newValue : float
            the new value of Tj parameter
        """
        Ti = self.resultTabModel.getTi_float()
        if newValue < Ti:
            self.resultTabModel.setTi(newValue)
            self.resultTabView.setTiSliderValue(newValue)
            self.listener.changeOnTiAndTj()
        else:
            self.listener.changeOnTj()
    
    
    def changeOnPf(self) -> None:
        """"This method controls the reaction of the application following a modification of the value of parameter Pf by the user

        Parameters
        ----------
        newValue : float
            the new value of Pf parameter
        """
        self.listener.changeOnPf()


    def obtainResults(self, load) -> None:
        """"Handle click on button Obtain Results
        """
        self.listener.obtainResults(load)


    def applyResults(self, results):
        """Apply the results provided by a method to help determine the parameters (from helpForParametersTab)

        Parameters
        ----------
        results : tuple[float, float, float]
            results = (I, J, P), the values of the 3 parameters of PROMETHEE Gamma method
        """
        (i, j, p) = results
        self.resultTabModel.setTi(i)
        self.resultTabModel.setTj(j)
        self.resultTabModel.setPf(p)
        self.refresh()

    
    def getModel(self) -> ResultTabModel:
        """Return the current ResultTabModel

        Return
        ------
        resultTabModel : ResultTabModel
        """
        return self.resultTabModel
    

    def loadResultsVisualisation(self) -> None:
        """Loads the 3 types of results visualizations and show them
        """
        self.resultTabView.ObtainResultsChange()
        master = self.resultTabView.getMaster()
        models = (self.listener.getPrometheeGammaModel(), self.resultTabModel, self.listener.getDataTabModel())
        self.resultsVisualisationController = ResultVisualisationController(master, models)
        self.resultsVisualisationController.show()


    def refreshResultsVisualisation(self) -> None:
        """Refresh the results visualisation
        """
        self.resultsVisualisationController.refresh()


    def saveOgraph(self, folder):
        self.resultsVisualisationController.saveOgraph(folder)


    def saveRgraph(self, folder):
        self.resultsVisualisationController.saveRgraph(folder)


    def saveParameters(self, file):

        file.write("Parameters\n\n")

        i = self.resultTabModel.getTi_float()
        j = self.resultTabModel.getTj_float()
        p = self.resultTabModel.getPf_float()

        file.write("I = " + str(i) + "\n")
        file.write("J = " + str(j) + "\n")
        file.write("P = " + str(p) + "\n")

        

