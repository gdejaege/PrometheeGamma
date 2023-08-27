from Views.ResultTabViews.RankView import RankView
from Models.ResultTabModel import ResultTabModel
from Models.DataTabModel import DataTabModel
from Models.PrometheeGamma import PrometheeGamma

class RankController(RankView.ViewListener):
    """
    A class to control the Rank tab

    Attributes
    ----------
    dataTabModel : DataTabModel
        the model of the data tab. It contain the input data of the method
    resultTabModel : ResultTabModel
        the model of the result tab. It contains the parameters of the method
    prometheeGamma : PrometheeGamma
        the model for Promethee Gamma method. It contains the results of the method
    rankView : RankView
        the view of the rank tab
    ranked : list[Alternative]
        a sorted list of ranked alternatives
    lmax : int
        the maximum length (width) of the scrollable region for the rank graph

    Methods
    -------
    showView()
        show the Rank tab
    showSelectionView()
        show the selection view
    draw()
        draw the canvas, i.e. the rank graph
    refreshView()
        refresh the rank tab
    checkBoxEvent()
        handle of checkBoxEvent in the selection view
    buildRankedAlternatives()
        rank alternatives from scores
    """

    def __init__(self, master, prometheeGamma:PrometheeGamma, resultTabModel:ResultTabModel, dataTabModel:DataTabModel, root) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame of rank tab
        prometheeGamma : PrometheeGamma
            the model for Promethee Gamma method. It contains the results of the method
        resultTabModel : ResultTabModel
            the model of the result tab. It contains the parameters of the method
        dataTabModel : DataTabModel
            the model of the data tab. It contain the input data of the method
        root : CTk
            the root window
        """
        self.dataTabModel = dataTabModel
        self.resultTabModel = resultTabModel
        self.prometheeGamma = prometheeGamma
        
        self.rankView = RankView(master, root)
        self.rankView.setListener(self)

        self.ranked = []


    def showView(self) -> None:
        """Show the Rank tab
        """
        self.rankView.show()


    def showSelectionView(self):
        """Show the selection view
        """
        aNames = self.dataTabModel.getAlternativesName()
        self.rankView.buildAlternativesDict(aNames)
        self.rankView.BuildCheckBoxes()


    def draw(self):
        """Draw the canvas, i.e. the rank graph
        """
        self.buildRankedAlternatives()
        matrixResults = self.prometheeGamma.getMatrixResults()
        self.rankView.drawCanvas(self.ranked, matrixResults)


    def refreshView(self) -> None:
        """Refresh the rank tab
        """
        self.showSelectionView()
        self.draw()


    def checkBoxEvent(self):
        """Handle of checkBoxEvent in the selection view
        """
        matrixResults = self.prometheeGamma.getMatrixResults()
        self.rankView.drawCanvas(self.ranked, matrixResults)


    def buildRankedAlternatives(self) -> None:
        """Rank alternatives from scores
        """
        scores = self.resultTabModel.getScores()
        sortedDict = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        if(sortedDict == []):
            return []
        self.ranked = []
        self.ranked.append([])
        self.ranked[0].append(sortedDict[0][0])
        for i in range(1,len(sortedDict)):
            if(sortedDict[i][1] == sortedDict[i-1][1]):
                self.ranked[-1].append(sortedDict[i][0])
            else:
                self.ranked.append([])
                self.ranked[-1].append(sortedDict[i][0])


    def saveRgraph(self, folder):
        filename = folder + "/RankGraph.png"
        self.rankView.save(filename)