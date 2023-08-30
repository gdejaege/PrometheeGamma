#############################################################################
### This class is a skeleton designed to provide an alternative way       ###
### of obtaining parameter values specific to the PROMETHEE Gamma method. ###
### Edit it as you wish.                                                  ###
###                                                                       ###
###                         !!!WARNING!!!                                 ###
### The name of this class cannot be changed,                             ###  
### otherwise the link with the rest of the application will be broken.   ###
#############################################################################

"""
from Models.PrometheeGamma import PrometheeGamma
from Models.DataTabModels.DataTabModel import DataTabModel

from Custom.CustomView import CustomView
from Custom.CustomModel import CustomModel
"""

from ..Models.PrometheeGamma import PrometheeGamma
from ..Models.DataTabModels.DataTabModel import DataTabModel
from .CustomView import CustomView
from .CustomModel import CustomModel


class CustomController(CustomView.ViewListener):
    """
    A class to control the custom module

    Attributes
    ----------
    master : CTkFrame
        the master frame
    prometheeGamma : PrometheeGamma
        the model for PROMETHEE Gamma method
    dataTabModel : DataTabModel
        the model that keep input data in memory
    listener : Listener
        the listener of this class i.e. the parent controller
    customView : CustomView
        the view of the custom module
    customModel : CustomModel
        the model of the custom module

    Methods
    -------
    """

    class Listener:
        """
        An interface for the listener

        Methods
        -------
        """

        def apply(self, results): # !!! Warning !!! The name (and arguments) of this method cannot be modified
            """apply the results in the result tab

            Parameters
            ----------
            results : tuple of float
                (I,J,P) where I, J and P are the values of the 3 parameters of PROMETHEE Gamma method
            """
            pass
        
        def reset(self): # !!! Warning !!! The name of this method cannot be modified
            """quit the custom module and resart the tab
            """
            pass


    def __init__(self, master, prometheeGamma:PrometheeGamma, dataTabModel:DataTabModel) -> None:
        """
        !!! Warning !!! The arguments of this constructor cannot be modified

        Parameters
        ----------
        master : CTkFrame
            the master frame
        prometheeGamma : PrometheeGamma
            the model for PROMETHEE Gamma method
        dataTabModel : DataTabModel
            the model that keep input data in memory
        """
        self.master = master
        self.prometheeGamma = prometheeGamma # with PrometheeGamma model, you can get all results of the promethee gamma method
        self.dataTabModel = dataTabModel # with the DataTabModel, you can get all input data
        self.listener = None

        # Initialize all variable that you need

        self.customView = None
        self.customModel = None


    def setListener(self, l:Listener):
        """Set the listener

        !!! Warning !!! This method cannot be modified

        Parameters
        ----------
        l : Listener
            the new listener
        """
        self.listener = l


    def run(self):
        """Example of method to launch the module

        !!! Warning !!! The name of this method cannot be modified, and it must effectively launch the module
        """
        # You can write core here to start module

        # Example: launch a view
        self.customView = CustomView(self.master)
        self.customView.setListener(self)
        self.customView.show()

        # Example: launch a model
        self.customModel = CustomModel(self.prometheeGamma, self.dataTabModel)
        self.customModel.run()


    def apply(self):
        """Apply results
        """

        # Get the results
        # example:
        (Imin, Imax, Jmin, Jmax, Pmin, Pmax) = self.customModel.getValues()

        # You can write code here to format results correctly
        # results must be in the form : (I,J,P) where I, J and P are the values of the 3 parameters of PROMETHEE Gamma method, in float
        # example:
        results = (Imin, Jmin, Pmin)

        # Call the parent controller to apply the results
        self.listener.apply(results)


    def reset(self):
        """Reset the tab and quit Custom module

        This method should not be modified
        """
        # Destroy all children of the master frame to clear the view
        for w in self.master.winfo_children():
            w.destroy()

        # Call the parent controller to restart the helpForParameters tab
        self.listener.reset()

    
    # Add your methods if needed