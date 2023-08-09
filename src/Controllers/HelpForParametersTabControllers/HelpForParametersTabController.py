from Controllers.HelpForParametersTabControllers.PreferenceLearningController import PreferenceLearningController
from Views.HelpForParametersTabViews.HelpForParametersTabView import HelpForParametersTabView
from Models.DataTabModel import DataTabModel
from Models.PrometheeGamma import PrometheeGamma

from Custom.CustomController import CustomController

class HelpForParametersTabController(HelpForParametersTabView.ViewListener, PreferenceLearningController.Listener, CustomController.Listener):
    
    class Listener:
        def applyResultsOfHelp(self, results):
            pass

    def __init__(self, master, dataTabModel:DataTabModel, prometheeGamma:PrometheeGamma) -> None:
        self.helpForParametersTabView = HelpForParametersTabView(master)
        self.helpForParametersTabView.setListener(self)
        self.dataTabModel = dataTabModel
        self.prometheeGamma = prometheeGamma
        self.preferenceLearningController = None
        self.customController = None
        self.listener = None


    def setListener(self, l:Listener):
        """Set the listener

        Parameters
        ----------
        l : Listener
            the new listener
        """
        self.listener = l


    def showView(self):
        """
        Show theView
        """
        self.helpForParametersTabView.show()


    def showPreferenceLearning(self):
        self.helpForParametersTabView.hide()
        master = self.helpForParametersTabView.getMaster()
        self.preferenceLearningController = PreferenceLearningController(master, self.dataTabModel, self.prometheeGamma)
        self.preferenceLearningController.setListener(self)
        self.preferenceLearningController.showView()


    def showCustom(self):
        self.helpForParametersTabView.hide()
        master = self.helpForParametersTabView.getMaster()
        self.customController = CustomController(master, self.prometheeGamma, self.dataTabModel)
        self.customController.setListener(self)
        self.customController.run()


    def apply(self, results:tuple):
        """Apply results
        
        Parameters
        ----------
        results : tuple[float, float, float]
            results = (I, J, P), the values of the 3 parameters of PROMETHEE Gamma method
        """
        self.listener.applyResultsOfHelp(results)


    def reset(self):
        self.helpForParametersTabView.restart()
        self.helpForParametersTabView.show()