from Views.AppView import AppView
from Views.SaveView import SaveView
from Controllers.DataTabControllers.DataTabController import DataTabController
from Controllers.ResultTabControllers.ResultTabController import ResultTabController
from Controllers.HelpForParametersTabControllers.HelpForParametersTabController import HelpForParametersTabController
from Models.PrometheeGamma import PrometheeGamma
import tkinter.messagebox as msg
from tkinter import filedialog as fd
from tkinter import IntVar
import os


class AppController(AppView.ViewListener, SaveView.Listener, ResultTabController.Listener, HelpForParametersTabController.Listener):
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
        self.saveView = None
        self.saveDict = {"Data":IntVar(self.appView, 1), 
                         "Parameters":IntVar(self.appView, 1), 
                         "Result matrix":IntVar(self.appView, 1), 
                         "Gamma matrix":IntVar(self.appView, 1), 
                         "Orthogonal graph":IntVar(self.appView, 1), 
                         "Rank graph":IntVar(self.appView, 1)}
        self.saveFolder = None


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
            msg.showerror(title="No data", message="No data available. Impossible to obtain results. Please fill in the data tab")
        elif self.dataTabController.no2AlterInModel():
            msg.showerror(title="Not enougth alternatives", message="At least 2 alternatives are needed to obtain results. Please, add alternatives.")
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
        if choice == "new project":
            if msg.askokcancel("Create a new project", message="Do you really want to create a new project? All unsaved data will be lost."):
                self.reset()
        elif choice == "save project as":
            self.saveAs()
        elif choice == "save project":
            self.save()
        elif choice == "load project":
            if msg.askokcancel("Load a project", message="Do you really want to load a project? All unsaved data will be lost."):
                self.load()
        elif choice == "quit":
            if msg.askokcancel("Quit", message="Do you really want to quit? All unsaved data will be lost."):
                self.appView.quit()


    def reset(self):
        print("reset")
        

    def save(self):
        # Si un dossier est déjà lié (par load ou par save as) -> save dans ce dossier
        if self.saveFolder is None or not os.path.exists(self.saveFolder):
            self.saveAs()
        else:
            if msg.askokcancel("Folder selection", "The content of the folder will be overwrite. Use this folder?\n" + self.saveFolder):
                self.saveProject()
            else:
                msg.showwarning("Warning", "The project was not saved.")

        
    def saveAs(self):
        self.saveView = SaveView(master=self.appView, saveDict=self.saveDict)
        self.saveView.grab_set()
        self.saveView.focus_set()
        self.saveView.title("Save")
        self.saveView.setListener(self)
        self.saveView.show()


    def saveInFolder(self, folder, name):
        # TODO 
        # Créer un dossier de nom name dans le dossier folder. 
        # Si un dossier de ce nom existe déjà, demander si écraser
        # Si pas écraser, relancer self.save()
        # 
        self.saveView.destroy()

        newFolder = folder + '/' + name
        if not os.path.exists(newFolder):
            os.makedirs(newFolder)
            self.saveFolder = newFolder
        else:
            if msg.askokcancel("The folder already exists", "Do you want to overwrite the contents of the folder?"):
                self.saveFolder = newFolder
            else:
                msg.showwarning("Warning", "The project was not saved.")
                return

        self.saveProject()


    def saveProject(self):
        if self.saveDict["Data"].get() == 1:
            self.dataTabController.save(self.saveFolder)
        if self.saveDict["Parameters"].get() == 1 or self.saveDict["Result matrix"].get() == 1 or self.saveDict["GammaMatrix"].get() == 1:
            self.saveResults(self.saveFolder)
        if self.saveDict["Orthogonal graph"].get() == 1:
            self.resultTabController.saveOgraph(self.saveFolder)
        if self.saveDict["Rank graph"].get() == 1:
            self.resultTabController.saveRgraph(self.saveFolder)


    def saveResults(self, folder):
        filename = folder + "/Results.txt"
        Params = []
        Rmatrix = []
        Gmatrix = []
        if os.path.exists(filename):
            pass
        else:
            pass

        print("Résultats sauvegardés")


    def fileWriteMatrix(self, file, m):
        for i in range(len(m)):
            line = ""
            for k in range(len(m[i])):
                line += str(m[i][k]) + "  "
            file.write(line + "\n")




    def load(self):
        file = fd.askopenfile(filetypes=(("PROMETHEE Gamma GUI project file", "*.prometheeGammaProject"), ("PROMETHEE Gamma GUI project file", "*.prometheeGammaProject")), 
                              initialdir="./Projects")
        if file is not None:
            try:
                tabs = self.appView.getTabs()
                self.dataTabController.openFile(master=tabs[0], file=file)
                self.resultTabController.readFile(master=tabs[1], file=file)
                self.readFile(file=file)
                file.close()
            except:
                msg.showerror("Error", "An error has occurred: unable to load correclty the project")
                return
            msg.showinfo("Load", message="The project has been successfully laoded")

            print("load")
