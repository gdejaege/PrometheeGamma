from Views.ResultTabViews.RankView import RankView
from Models.ResultTabModel import ResultTabModel
from Models.DataTabModel import DataTabModel
from Models.PrometheeGamma import PrometheeGamma

class RankController(RankView.ViewListener):
    def __init__(self, master, prometheeGamma:PrometheeGamma, resultTabModel:ResultTabModel, dataTabModel:DataTabModel) -> None:
        self.dataTabModel = dataTabModel
        self.resultTabModel = resultTabModel
        self.prometheeGamma = prometheeGamma
        
        self.rankView = RankView(master)
        self.rankView.setListener(self)


    def showView(self):
        self.rankView.show()


    def refreshView(self):
        nb = self.dataTabModel.getNumberOfAlternatives()
        size = nb*80
        self.rankView.resizeCanvas(size)
        self.rankView.refresh()


    def getRankedAlternatives(self) -> list:
        """
        Rank alternatives from scores \n
        Return a sort list of alternatives
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
    

    def getMatrixResults(self):
        return self.prometheeGamma.getMatrixResults()