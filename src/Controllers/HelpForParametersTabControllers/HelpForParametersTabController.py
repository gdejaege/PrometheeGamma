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
        self.maxNumberOfQuestions = 5


    def showView(self):
        """
        Show the View
        """
        self.helpForParametersTabView.show()


    def changeQCM(self):
        pass


    def confirm(self):
        #self.results = self.preferenceLearning.findOptimum()
        #self.helpForParametersTabView.showResults(results=self.results)
        results = self.preferenceLearning.getResults()
        self.helpForParametersTabView.showResults(results)


    def apply(self):
        self.listener.applyResultsOfHelp(self.results)


    def next(self):
        results = self.preferenceLearning.getResults()
        self.helpForParametersTabView.showResults(results)
        question = self.preferenceLearning.selectNextQuestion()
        self.questions.append(question)
        self.helpForParametersTabView.showNextQuestion(question, len(self.questions) >= self.maxNumberOfQuestions)


    def selectFirstQuestion(self):
        nbAlter = self.dataTabModel.getNumberOfAlternatives()
        alter = []
        for i in range(nbAlter):
            a = self.dataTabModel.getAlternative(i)
            alter.append(a)
        self.preferenceLearning.setAlternatives(alter)
        question = self.preferenceLearning.selectFirstQuestion()
        self.questions.append(question)
        self.helpForParametersTabView.showNextQuestion(question, len(self.questions) >= self.maxNumberOfQuestions)


    def showQuestions(self):
        self.questions.clear()
        self.selectFirstQuestion()


    def recomputeResults(self):
        self.preferenceLearning.itSearch(True)