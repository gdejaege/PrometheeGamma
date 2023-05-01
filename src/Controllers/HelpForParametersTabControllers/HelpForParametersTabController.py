from Views.HelpForParametersTabViews.HelpForParametersTabView import HelpForParametersTabView
from Models.DataTabModel import DataTabModel
from Models.preferenceLearning import PreferenceLearning

class HelpForParametersTabController(HelpForParametersTabView.ViewListener):
    def __init__(self, master, dataTabModel:DataTabModel) -> None:
        self.helpForParametersTabView = HelpForParametersTabView(master)
        self.helpForParametersTabView.setListener(self)
        self.dataTabModel = dataTabModel
        self.questions = []


    def showView(self):
        self.helpForParametersTabView.show()


    def showQuestions(self):
        # example
        # TODO Algorithme de choix d'alternative : 
        # aléatoire ou trouver celles les plus susceptibles de donner des indications satisfaisantes
        if self.dataTabModel.getNumberOfAlternatives() > 2:
            a1 = self.dataTabModel.getAlternative(0)
            a2 = self.dataTabModel.getAlternative(1)
            self.questions.append((a1, a2))
            self.helpForParametersTabView.showQuestions(self.questions)