from Views.ResultTabViews.DisplayMatrixResultsView import DisplayMatrixResultsView
from Models.PrometheeGamma import PrometheeGamma

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
    showView()
        show the textbox tab
    refreshView()
        refresh the textbox tab
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