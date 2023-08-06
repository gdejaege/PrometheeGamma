from Views.ResultTabViews.RankView import RankView
from Models.ResultTabModel import ResultTabModel
from Models.DataTabModel import DataTabModel
from Models.PrometheeGamma import PrometheeGamma

class RankController(RankView.ViewListener):
    """
    Controller of the Rank tab
    """
    def __init__(self, master, prometheeGamma:PrometheeGamma, resultTabModel:ResultTabModel, dataTabModel:DataTabModel) -> None:
        self.dataTabModel = dataTabModel
        self.resultTabModel = resultTabModel
        self.prometheeGamma = prometheeGamma
        
        self.rankView = RankView(master)
        self.rankView.setListener(self)


    def showView(self) -> None:
        """
        Show the Rank tab
        """
        self.rankView.show()
        self.draw()


    def draw(self):
        """
        Draw the canvas
        """
        r = self.getRankedAlternatives()
        lmax = 0
        for k in range(len(r)):
            if len(r[k]) > lmax:
                lmax = len(r[k])
        self.rankView.resizeCanvas(width=lmax*100, height=len(r)*100)
        matrixResults = self.prometheeGamma.getMatrixResults()
        self.rankView.drawCanvas(r, lmax, matrixResults)


    def refreshView(self) -> None:
        """
        Refresh the rank tab
        """
        self.draw()


    def getRankedAlternatives(self) -> list:
        """
        Rank alternatives from scores.
        Return a sorted list of alternatives.
        """
        scores = self.resultTabModel.getScores()
        sortedDict = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        if(sortedDict == []):
            return []
        ranked = []
        ranked.append([])
        ranked[0].append(sortedDict[0][0])
        for i in range(1,len(sortedDict)):
            if(sortedDict[i][1] == sortedDict[i-1][1]):
                ranked[-1].append(sortedDict[i][0])
            else:
                ranked.append([])
                ranked[-1].append(sortedDict[i][0])
        return ranked