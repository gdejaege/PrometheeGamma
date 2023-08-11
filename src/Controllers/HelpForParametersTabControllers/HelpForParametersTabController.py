from Views.HelpForParametersTabViews.HelpForParametersTabView import HelpForParametersTabView
from Models.DataTabModel import DataTabModel
from Models.PrometheeGamma import PrometheeGamma
from Controllers.HelpForParametersTabControllers.PreferenceLearningController import PreferenceLearningController
from Custom.CustomController import CustomController


class HelpForParametersTabController(HelpForParametersTabView.ViewListener, PreferenceLearningController.Listener, CustomController.Listener):
    """
    A calss to control the helpForParameters tab

    Attributes
    ----------
    helpForParametersTabView : HelpForParametersTabView
        the tab view
    dataTabModel : DataTabModel
        the data tab model
    prometheeGamma : PrometheeGamma
        the model for PROMETHEE Gamma method
    preferenceLearningController : PreferenceLearningController
        the controller that controls the preference learning. This is a sub controller of this class
    customController : CustomController
        the controller that controls the custom module. This is a sub controller of this class
    listerer : HelpForParametersTabController.Listener
        the listener of this class

    Methods
    -------
    setListener(l:Listener)
        set the listener
    showView()
        show the View
    showPreferenceLearning()
        show graphical components for preference learning method
    showCustom()
        show graphical components for custom module
    apply(results:tuple)
        Use the results obtained from parameters determination methods (such as preference learning) in the result tab
    reset()
        reset the view
    """
    
    class Listener:
        """
        An interface for the listener of this class

        Methods
        -------
        applyResultsOfHelp(results)
            Use the results obtained from parameters determination methods (such as preference learning) in the result tab
        """

        def applyResultsOfHelp(self, results):
            pass


    def __init__(self, master, dataTabModel:DataTabModel, prometheeGamma:PrometheeGamma) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
            dataTabModel : DataTabModel
            the model that keep input data in memory
        prometheeGamma : PrometheeGamma
            the model for PROMETHEE Gamma method
        """
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
        """Show the View
        """
        self.helpForParametersTabView.show()


    def showPreferenceLearning(self):
        """Show graphical components for preference learning method
        """
        self.helpForParametersTabView.hide()
        master = self.helpForParametersTabView.getMaster()
        self.preferenceLearningController = PreferenceLearningController(master, self.dataTabModel, self.prometheeGamma)
        self.preferenceLearningController.setListener(self)
        self.preferenceLearningController.showView()


    def showCustom(self):
        """Show graphical components for custom module
        """
        self.helpForParametersTabView.hide()
        master = self.helpForParametersTabView.getMaster()
        self.customController = CustomController(master, self.prometheeGamma, self.dataTabModel)
        self.customController.setListener(self)
        self.customController.run()


    def apply(self, results:tuple):
        """Use the results obtained from parameters determination methods (such as preference learning) in the result tab
        
        Parameters
        ----------
        results : tuple[float, float, float]
            results = (I, J, P), the values of the 3 parameters of PROMETHEE Gamma method
        """
        self.listener.applyResultsOfHelp(results)


    def reset(self):
        """Reset the view
        """
        self.helpForParametersTabView.restart()
        self.helpForParametersTabView.show()