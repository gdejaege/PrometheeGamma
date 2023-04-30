from Views.ResultTabViews.DisplayMatrixResultsView import DisplayMatrixResultsView
from Models.PrometheeGamma import PrometheeGamma

class TabularController:
    """
    Controller of the tabular tab
    """
    def __init__(self, master, model:PrometheeGamma) -> None:
        self.displayMatrixResultsView = DisplayMatrixResultsView(master=master)
        self.model = model

    
    def showView(self):
        """
        Show the tabular tab
        """
        matrixResults = self.model.getMatrixResults()
        self.displayMatrixResultsView.show(matrixResults)

    
    def refreshView(self):
        """
        Refresh the tabl-ular tab
        """
        matrixResults = self.model.getMatrixResults()
        self.displayMatrixResultsView.refresh(matrixResults)