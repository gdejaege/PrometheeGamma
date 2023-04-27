from Views.ResultTabViews.DisplayMatrixResultsView import DisplayMatrixResultsView
from Models.PrometheeGamma import PrometheeGamma

class TabularController:
    def __init__(self, master, model:PrometheeGamma) -> None:
        self.displayMatrixResultsView = DisplayMatrixResultsView(master=master)
        self.model = model

    
    def showView(self):
        matrixResults = self.model.getMatrixResults()
        self.displayMatrixResultsView.show(matrixResults)

    
    def refreshView(self):
        matrixResults = self.model.getMatrixResults()
        self.displayMatrixResultsView.refresh(matrixResults)