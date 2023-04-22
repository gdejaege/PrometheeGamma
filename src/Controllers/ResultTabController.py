from Views.ResultTabView import ResultTabView

class ResultTabController:
    def __init__(self, master) -> None:
        self.resultTabView = ResultTabView(master=master)

    
    def showView(self) -> None:
        """
        show the resultTabView
        """
        #self.resultTabView.show()