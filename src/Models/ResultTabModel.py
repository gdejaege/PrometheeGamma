from customtkinter import (DoubleVar)

class ResultTabModel:
    def __init__(self, master) -> None:
        # Parameters
        self.indifferenceThreshold = DoubleVar(master=master, value=0.0)
        self.incomparabilityThreshold = DoubleVar(master=master, value=0.0)
        self.preferenceParameter = DoubleVar(master=master, value=1.0)

        self.scores = {}


    def getTi(self) -> DoubleVar:
        return self.indifferenceThreshold
    

    def getTj(self) -> DoubleVar:
        return self.incomparabilityThreshold
    

    def getPf(self) -> DoubleVar:
        return self.preferenceParameter
    

    def getTi_float(self) -> float:
        return self.indifferenceThreshold.get()
    

    def getTj_float(self) -> float:
        return self.incomparabilityThreshold.get()
    

    def getPf_float(self) -> float:
        return self.preferenceParameter.get()
    

    def setTi(self, val:float):
        self.indifferenceThreshold.set(val)


    def setTj(self, val:float):
        self.incomparabilityThreshold.set(val)


    def initScores(self, alternativesName:list):
        for name in alternativesName:
            self.scores[name] = 0


    def incrementScore(self, alternativeName:str):
        self.scores[alternativeName] += 1


    def getScores(self) -> dict:
        return self.scores