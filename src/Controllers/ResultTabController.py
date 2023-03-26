from Views.ResultTabView import ResultTabView

class ResultTabController:
    def __init__(self, master) -> None:
        self.resultTabView = ResultTabView(master=master)

    
    def show(self) -> None:
        self.resultTabView.show()