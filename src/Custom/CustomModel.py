#############################################################################
### This class is a skeleton designed to provide an alternative way       ###
### of obtaining parameter values specific to the PROMETHEE Gamma method. ###
### Edit it as you wish.                                                  ###
#############################################################################

from Models.PrometheeGamma import PrometheeGamma
from Models.DataTabModels.DataTabModel import DataTabModel

class CustomModel:
    """
    A class to create a custom model

    Attributes
    ----------
    prometheeGamma : PrometheeGamma
        the model for PROMETHEE Gamma method
    dataTabModel : DataTabModel
        the model that keep input data in memory
    Imin :float
        the minimum value for the parameter I
    Imax :float
        the maximum value for the parameter I
    Jmin :float
        the minimum value for the parameter J
    Jmax :float
        the maximum value for the parameter J
    Pmin :float
        the minimum value for the parameter P
    Pmax :float
        the maximum value for the parameter P

    Methods
    -------
    """

    def __init__(self, prometheeGamma:PrometheeGamma, dataTabModel:DataTabModel) -> None:
        """
        Parameters
        ----------
        prometheeGamma : PrometheeGamma
            the model for PROMETHEE Gamma method
        dataTabModel : DataTabModel
            the model that keep input data in memory
        """
        self.prometheeGamma = prometheeGamma # with PrometheeGamma model, you can get all results of the promethee gamma method
        self.dataTabModel = dataTabModel # with the DataTabModel, you can get all input data

        self.Imin = 0.0
        self.Imax = 1.0
        self.Jmin = 0.0
        self.Jmax = 1.0
        self.Pmin = 1.0
        self.Pmax = 1000000000.0

        # You can add here the attributes that you need

    
    def run(self):
        """Example of funtion to start the model
        """

        # You can write code here to start the model

        # example:
        self.compute()

    
    def compute(self):
        """Example of function to compute parameters values
        """
        matrixGamma = self.prometheeGamma.getMatrixGamma()
        
        # Make some computation
        
        # Save results in self.Imin, self.Imax, self.Jmin, self.Jmax, self.Pmin, self.Pmax


    def getValues(self):
        """Example of funtion to get results

        Return
        ------
        (self.Imin, self.Imax, self.Jmin, self.Jmax, self.Pmin, self.Pmax) : tuple
            the results obtained with the model
        """
        return (self.Imin, self.Imax, self.Jmin, self.Jmax, self.Pmin, self.Pmax)
    

    # Add your methods if needed