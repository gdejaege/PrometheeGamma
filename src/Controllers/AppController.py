from Views.AppView import AppView
from Controllers.DataTabControllers.DataTabController import DataTabController
from Controllers.ResultTabControllers.ResultTabController import ResultTabController
from Controllers.HelpForParametersTabControllers.HelpForParametersTabController import HelpForParametersTabController
from Models.PrometheeGamma import PrometheeGamma
import tkinter.messagebox

class AppController(AppView.ViewListener, ResultTabController.Listener, HelpForParametersTabController.Listener):
    """
    The main controller of the application

    It allows to start and stop the application, but also to make the link between its different parts

    Attributes
    ----------
    appView : AppView()
        the tkinter master frame, the root frame of the app
    alreadyCompute : bool
        a control variable to keep in memory if the results are already computed or not
    prometheeGamma : PrometheeGamma
        the model that compute results with PROMETHEE Gamma method
    dataTabController : DataTabController
        the main controller of the data tab
    resultTabController : ResultTabController
        the main controller of the result tab
    helpForParametersTabController : HelpForParametersTabController
        the main controller of the helpForParameters tab

    Methods
    -------
    run()
        launch the app
    showDataTabView(master)
        show the data tab
    showResultTabView(master)
        show the result tab
    showHelpForParametersTabView(master)
        show the helpForParameters tab
    obtainResults(load:bool)
        obtain the results or, if there is no or not enought data, show an error message to the user
    computeResults()
        compute the result of the Promethee Gamma method
    changeOnTiAndTj()
        recompute the needed results in case of change on Ti and Tj
    changeOnTi()
        recompute the needed results in case of change on Ti
    changeOnTj()
        recompute the needed results in case of change on Tj
    changeOnPf()
        recompute the needed results in case of change on Pf
    getPrometheeGammaModel()
        return the current used model for the Promethee Gamma method
    getDataTabModel()
        return the current data tab model
    applyResultsOfHelp(results)
        apply the results obtained in the helpForParameters tab in the result tab
    """

    def __init__(self) -> None:
        self.appView = AppView()
        self.appView.setListener(self)
        self.alreadyCompute = False
        self.prometheeGamma = PrometheeGamma()
        self.dataTabController = None
        self.resultTabController = None
        self.helpForParametersTabController = None


    def run(self) -> None:
        """Launch the app
        """
        self.appView.show()
        (dataTab, resultTab, helpForParametersTab) = self.appView.getTabs()
        self.showDataTabView(dataTab)
        self.showResultTabView(resultTab)
        self.showHelpForParametersTabView(helpForParametersTab)
        self.appView.mainloop()


    def showDataTabView(self, master) -> None:
        """Show the data tab

        Parameters
        ----------
        master : CTkFrame
            the master frame for the data tab
        """
        self.dataTabController = DataTabController(master=master)
        self.dataTabController.showView()


    def showResultTabView(self, master) -> None:
        """Show the result tab

        Parameters
        ----------
        master : CTkFrame
            the master frame for the result tab
        """
        self.resultTabController = ResultTabController(master=master)
        self.resultTabController.setListener(self)
        self.resultTabController.showView()


    def showHelpForParametersTabView(self, master) -> None:
        """Show the helpForParameters tab

        Parameters
        ----------
        master : CTkFrame
            the master frame for the helpForParameters tab
        """
        dataTabModel = self.dataTabController.getModel()
        self.helpForParametersTabController = HelpForParametersTabController(master, dataTabModel, self.prometheeGamma)
        self.helpForParametersTabController.setListener(self)
        self.helpForParametersTabController.showView()


    def obtainResults(self, load:bool):
        """Obtain the results or, if there is no or not enought data, show an error message to the user

        Parameters
        ----------
        load : bool
            True if the resut visualisation must be loaded, False otherwise
        """
        if self.dataTabController.voidModel():
            tkinter.messagebox.showerror(title="No data", message="No data available. Impossible to obtain results. Please fill in the data tab")
        elif self.dataTabController.no2AlterInModel():
            tkinter.messagebox.showerror(title="Not enougth alternatives", message="At least 2 alternatives are needed to obtain results. Please, add alternatives.")
        else:
            if load:
                self.resultTabController.loadResultsVisualisation()
            self.computeResults()


    def computeResults(self) -> None:
        """Compute the result of the Promethee Gamma method
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
        """Recompute the needed results in case of change on Ti and Tj
        
        This method must be called if there is a simultaneous change of the thresholds Ti and Tj
        """
        if self.alreadyCompute:
            self.prometheeGamma.computeMatrixI()
            self.prometheeGamma.computeMatrixJ()
            self.prometheeGamma.computeMatrixResults()
            self.resultTabController.refreshResultsVisualisation()


    def changeOnTi(self) -> None:
        """Recompute the needed results in case of change on Ti

        This method must be called if there is a change of the threshold Ti and not on Tj
        """
        if self.alreadyCompute:
            self.prometheeGamma.computeMatrixI()
            self.prometheeGamma.computeMatrixResults()
            self.resultTabController.refreshResultsVisualisation()


    def changeOnTj(self) -> None:
        """Recompute the needed results in case of change on Tj

        This method must be called if there is a change of the threshold Tj and not on Ti
        """
        if self.alreadyCompute:
            self.prometheeGamma.computeMatrixJ()
            self.computeResults()
            self.resultTabController.refreshResultsVisualisation()


    def changeOnPf(self) -> None:
        """Recompute the needed results in case of change on Pf

        This method must be called if there is a change of the parameter Pf
        """
        if self.alreadyCompute:
            self.prometheeGamma.computeMatrixP()
            self.computeResults()
            self.resultTabController.refreshResultsVisualisation()


    def getPrometheeGammaModel(self) -> PrometheeGamma:
        """Return the current used model for the Promethee Gamma method

        Return
        ------
        prometheeGamma : PrometheeGamma
        """
        return self.prometheeGamma
    

    def getDataTabModel(self):
        """Return the current data tab model

        Return
        ------
        dataTabController.dataTabModel : DataTabModel
        """
        return self.dataTabController.getModel()
    

    def applyResultsOfHelp(self, results):
        """Apply the results obtained in the helpForParameters tab in the result tab

        i.e. modify the values of I, J and P in the result tab accordingly to their values in the helpForParameters tab

        Parameters
        ----------
        results : tuple[float, float, float]
            results = (I, J, P), the values of the 3 parameters of PROMETHEE Gamma method
        """
        self.resultTabController.applyResults(results)
        self.appView.setTab("Results")


    def menuChoice(self, choice:str):
        "new project", "save project", "load project", "quit"
        if choice == "new project":
            if tkinter.messagebox.askokcancel("Create a new project", message="Do you really want to create a new project? All unsaved data will be lost."):
                self.reset()
        elif choice == "save project":
            self.save()
        elif choice == "load project":
            if tkinter.messagebox.askokcancel("Load a project", message="Do you really want to load a project? All unsaved data will be lost."):
                self.load()
        elif choice == "quit":
            if tkinter.messagebox.askokcancel("Quit", message="Do you really want to quit? All unsaved data will be lost."):
                self.appView.quit()


    def reset(self):
        print("reset")
        
        
    def save(self):
        print("save")
        tkinter.messagebox.showinfo("Save", message="The project has been successfully saved")


    def load(self):
        print("load")