from customtkinter import (DoubleVar)

class ResultTabModel:
    """
    Model of the result tab.
    It contains the three new parameters of Promethee Gamma
    """
    def __init__(self, master) -> None:
        # Parameters
        self.indifferenceThreshold = DoubleVar(master=master, value=0.0)
        self.incomparabilityThreshold = DoubleVar(master=master, value=0.0)
        self.preferenceParameter = DoubleVar(master=master, value=1.0)
        # Scores for rank
        self.scores = {}


    def getTi(self) -> DoubleVar:
        """
        Return the indifference threshold in a DoubleVar object.
        """
        return self.indifferenceThreshold
    

    def getTj(self) -> DoubleVar:
        """
        Return the incomparability threshold in a DoubleVar object.
        """
        return self.incomparabilityThreshold
    

    def getPf(self) -> DoubleVar:
        """
        Return the preference parameter in a DoubleVar object.
        """
        return self.preferenceParameter
    

    def getTi_float(self) -> float:
        """
        Return the indifference threshold.
        """
        return self.indifferenceThreshold.get()
    

    def getTj_float(self) -> float:
        """
        Return the incomparability threshold.
        """
        return self.incomparabilityThreshold.get()
    

    def getPf_float(self) -> float:
        """
        Return the preference parameter
        """
        return self.preferenceParameter.get()
    

    def setTi(self, val:float) -> None:
        """
        Change the value of the indifference threshold.
        """
        self.indifferenceThreshold.set(val)


    def setTj(self, val:float) -> None:
        """
        Change the value of the indifference threshold.
        """
        self.incomparabilityThreshold.set(val)


    def initScores(self, alternativesName:list):
        """
        Init the scores at zero
        """
        for name in alternativesName:
            self.scores[name] = 0


    def incrementScore(self, alternativeName:str):
        """
        Increment the score of the alternative given in parameter
        """
        self.scores[alternativeName] += 1


    def getScores(self) -> dict:
        """
        Return the Scores
        """
        return self.scores