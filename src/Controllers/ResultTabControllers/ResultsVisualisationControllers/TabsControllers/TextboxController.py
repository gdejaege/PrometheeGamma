from Models.PrometheeGamma import PrometheeGamma
from Views.ResultTabViews.ResultsVisualisationViews.DisplayMatrixResultsView import DisplayMatrixResultsView


class TextboxController:
    """
    A class to Control the textbox tab

    Attributes
    ----------
    displayMatrixResultsView : DisplayMatrixResultsView
        the view to display the result matrix
    model : PrometheeGamma
        the Promethee Gamma model, needed to obtain the content to display (the result matrix)
    
    Methods
    -------
    """

    def __init__(self, master, model:PrometheeGamma) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame of the tab
        model : PrometheeGamma
            the Promethee Gamma model, needed to obtain the content to display
        """
        self.displayMatrixResultsView = DisplayMatrixResultsView(master=master)
        self.model = model

    
    def showView(self):
        """Show the textbox tab
        """
        matrixResults = self.model.getMatrixResults()
        self.displayMatrixResultsView.show(matrixResults)

    
    def refreshView(self):
        """Refresh the textbox tab
        """
        matrixResults = self.model.getMatrixResults()
        self.displayMatrixResultsView.refresh(matrixResults)