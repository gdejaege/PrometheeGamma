from Views.ResultTabViews.OrthogonalGraphView import OrthogonalGraphView
from Models.PrometheeGamma import PrometheeGamma

class OrthogonalGraphController:
    def __init__(self, master, model:PrometheeGamma) -> None:
        self.master = master
        self.model = model
        matrixGamma = self.model.getMatrixGamma()
        matrixResults = self.model.getMatrixResults()

        self.orthogonalGraphView = OrthogonalGraphView(self.master, matrixGamma, matrixResults)


    def showView(self):
        self.orthogonalGraphView.show()


    def refreshView(self):
        matrixGamma = self.model.getMatrixGamma()
        matrixResults = self.model.getMatrixResults()
        self.orthogonalGraphView.reshresh(matrixGamma, matrixResults)
