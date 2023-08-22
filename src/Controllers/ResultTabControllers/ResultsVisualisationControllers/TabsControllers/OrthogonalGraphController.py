from Views.ResultTabViews.OrthogonalGraphView import OrthogonalGraphView
from Models.PrometheeGamma import PrometheeGamma

class OrthogonalGraphController:
    """
    A class to control the orthogonal graph tab

    Attributes
    ----------
    model : PrometheeGamma
        the model for Promethee Gamma method. It contains the results of the method
    orthogonalGraphView : OrthogonalGraphView
        the view to display the orthogonal graph

    Methods
    -------
    showView()
        show the orthogonal graph tab
    refreshView()
        refresh the orthogonal graph tab
    """

    def __init__(self, master, model:PrometheeGamma) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        model : PrometheeGamma
            the model for Promethee Gamma method. It contains the results of the method
        """

        self.model = model
        matrixGamma = self.model.getMatrixGamma()
        matrixResults = self.model.getMatrixResults()
        self.orthogonalGraphView = OrthogonalGraphView(master, matrixGamma, matrixResults)


    def showView(self) -> None:
        """Show the orthogonal graph tab
        """
        self.orthogonalGraphView.show()


    def refreshView(self) -> None:
        """Refresh the orthogonal graph tab
        """
        matrixGamma = self.model.getMatrixGamma()
        matrixResults = self.model.getMatrixResults()
        self.orthogonalGraphView.reshresh(matrixGamma, matrixResults)


    def saveOgraph(self, folder):
        filename = folder + "/OrthogonalGraph.png"
        self.orthogonalGraphView.save(filename)
