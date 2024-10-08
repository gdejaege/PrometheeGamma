from .....Models.PrometheeGamma import PrometheeGamma
from .....Views.ResultTabViews.ResultsVisualisationViews.OrthogonalGraphView import OrthogonalGraphView

class OrthogonalGraphController:
    """
    A class to control the orthogonal graph tab

    Attributes
    ----------
    model : PrometheeGamma
        the model for Promethee Gamma method. It contains the results of the method
    orthogonalGraphView : OrthogonalGraphView
        the view to display the orthogonal graph
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
        parameters = self.model.getPrometheeGammaParameters()
        self.orthogonalGraphView = OrthogonalGraphView(master, matrixGamma, matrixResults, parameters)


    def showView(self) -> None:
        """Show the orthogonal graph tab
        """
        self.orthogonalGraphView.show()


    def refreshView(self) -> None:
        """Refresh the orthogonal graph tab
        """
        matrixGamma = self.model.getMatrixGamma()
        matrixResults = self.model.getMatrixResults()
        parameters = self.model.getPrometheeGammaParameters()
        self.orthogonalGraphView.reshresh(matrixGamma, matrixResults, parameters)


    def saveOgraph(self, directory:str):
        """Save the orthogonal graph in directory

        Parameters
        ----------
        directory : str
            the directory in which to save the graph
        """
        filename = directory + "/OrthogonalGraph.png"
        self.orthogonalGraphView.save(filename)
