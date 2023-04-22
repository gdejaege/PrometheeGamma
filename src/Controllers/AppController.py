from Views.AppView import AppView
from Controllers.DataTabControllers.DataTabController import DataTabController
from Controllers.ResultTabControllers.ResultTabController import ResultTabController
from Models.PrometheeGamma import PrometheeGamma

class AppController(AppView.ViewListener, ResultTabController.Listener):
    def __init__(self) -> None:
        self.appView = AppView()
        self.appView.setListener(self)
        self.alreadyCompute = False


    def run(self) -> None:
        """
        Launch the app
        """
        self.appView.show()
        self.appView.mainloop()

        self.dataTabController = None
        self.resultTabController = None
        self.prometheeGamma = PrometheeGamma()


    def showDataTabView(self, master):
        self.dataTabController = DataTabController(master=master)
        self.dataTabController.showView()


    def showResultTabView(self, master):
        self.resultTabController = ResultTabController(master=master)
        self.resultTabController.showView()


    def computeResults(self):
        dataTabModel = self.dataTabController.getModel()
        resultTabModel = self.resultTabController.getModel()
        self.prometheeGamma.setDataTabModel(dataTabModel)
        self.prometheeGamma.setResultTabModel(resultTabModel)
        self.prometheeGamma.computeAll()
        self.alreadyCompute = True


    def changeOnTiAndTj(self):
        if self.alreadyCompute:
            self.prometheeGamma.build_matrix_I()
            self.prometheeGamma.build_matrix_J()
            self.prometheeGamma.computeResults()


    def changeOnTi(self):
        if self.alreadyCompute:
            self.prometheeGamma.build_matrix_I()
            self.prometheeGamma.computeResults()


    def changeOnTj(self):
        if self.alreadyCompute:
            self.prometheeGamma.build_matrix_J()
            self.computeResults()


    def changeOnPf(self):
        if self.alreadyCompute:
            self.prometheeGamma.build_matrix_P()
            self.computeResults()