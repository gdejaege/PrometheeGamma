from PrometheeGamma import PrometheeGamma

class DataTabModel:
    def __init__(self) -> None:
        self.units = []
        """
        Matrix of units
        """
        self.criteria = []
        """
        List of criteria. The index correspond to the column number
        """
        self.preferenceFunctionsTypes = []
        """
        List of preference function's types
        """
        self.p = []
        """
        List of preference parameters
        """
        self.q = []
        """
        List of indiferrence parameters
        """
        self.weights = []
        """
        List of criteria's weight
        """
        self.method = PrometheeGamma()
        """
        The used method
        """
        self.pf_types = {1:"Usual", 2:"U-shape", 3:"V-shape", 4:"Level", 5:"Linear", 6:"Gaussian"}


    def setUnits(self, new_units:list) -> None:
        self.units = new_units


    def setCiteria(self, new_criteria:list) -> None:
        self.criteria = new_criteria

    
    def setPreferenceFunctionsTypes(self, new_f:list) -> None:
        self.preferenceFunctionsTypes = new_f


    def setPreferenceParameters(self, new_p:list) -> None:
        self.p = new_p


    def setIndifferenceParameters(self, new_q:list) -> None:
        self.q = new_q


    def setWeights(self, new_weights:list) -> None:
        self.weights = new_weights