from Views.HelpForParametersTabViews.HelpForParametersTabView import HelpForParametersTabView
from Models.DataTabModel import DataTabModel
from Models.PrometheeGamma import PrometheeGamma
from Models.preferenceLearning import PreferenceLearning

class HelpForParametersTabController(HelpForParametersTabView.ViewListener):
    class Listener:
        def applyResultsOfHelp(self, results):
            pass

    def __init__(self, master, listener:Listener, dataTabModel:DataTabModel, prometheeGamma:PrometheeGamma) -> None:
        self.helpForParametersTabView = HelpForParametersTabView(master)
        self.helpForParametersTabView.setListener(self)
        self.dataTabModel = dataTabModel
        self.prometheeGamma = prometheeGamma
        self.preferenceLearning = PreferenceLearning(master, self.prometheeGamma)
        self.questions = []
        self.results = None
        self.listener = listener


    def showView(self):
        self.helpForParametersTabView.show()

    def changeQCM(self):
        pass


    def confirm(self):
        self.results = self.preferenceLearning.findOptimum()
        self.helpForParametersTabView.showResults(results=self.results)


    def apply(self):
        self.listener.applyResultsOfHelp(self.results)


    def showQuestions(self):
        self.questions.clear()
        nbAlter = self.dataTabModel.getNumberOfAlternatives()
        alter = []
        for i in range(nbAlter):
            a = self.dataTabModel.getAlternative(i)
            alter.append(a)
        self.preferenceLearning.createPairs(alter)
        nbPairs = self.preferenceLearning.getNumberOfPairs()
        for j in range(nbPairs):
            p = self.preferenceLearning.getPair(j)
            self.questions.append(p)
        self.helpForParametersTabView.showQuestions(self.questions)



        # example
        # TODO Algorithme de choix d'alternative : 
        # aléatoire ou trouver celles les plus susceptibles de donner des indications satisfaisantes
        """
        if self.dataTabModel.getNumberOfAlternatives() > 2:
            a1 = self.dataTabModel.getAlternative(0)
            a2 = self.dataTabModel.getAlternative(1)
            self.questions.append((a1, a2))
            self.helpForParametersTabView.showQuestions(self.questions)
        """