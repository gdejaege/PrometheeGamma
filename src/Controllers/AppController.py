from Views.AppView import AppView
from Controllers.DataTabController import DataTabController
from Controllers.ResultTabController import ResultTabController

class AppController(AppView.ViewListener):
    def __init__(self) -> None:
        self.appView = AppView()
        self.appView.setListener(self)

    def run(self) -> None:
        """
        Launch the app
        """
        self.appView.show()
        self.appView.mainloop()


    def showDataTabView(self, master):
        dataTabController = DataTabController(master=master)
        dataTabController.show()


    def showResultTabView(self, master):
        resultTabController = ResultTabController(master=master)
        resultTabController.show()
