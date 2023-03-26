from customtkinter import (StringVar, IntVar, DoubleVar)
from Models.DataModels.Alternative import Alternative
from Models.DataModels.Criterion import Criterion

class DataTabModel:
    def __init__(self) -> None:
        self.alternatives = [Alternative]
        """
        List of alternatives. The index correspond to the row number.
        """
        self.criteria = []
        """
        List of criteria. The index correspond to the column number.
        """
        self.dico_pfTypes = {1:"Usual", 2:"U-shape", 3:"V-shape", 4:"Level", 5:"Linear", 6:"Gaussian"}
        """
        Dictionary of preference function types
        """


    def setUnits(self, new_units:list[Alternative]) -> None:
        self.units = new_units


    def setCiteria(self, new_criteria:list[Criterion]) -> None:
        self.criteria = new_criteria


    def addCriterion(self, name:StringVar, weight:DoubleVar, f:IntVar, p:DoubleVar=None, q:DoubleVar=None):
        c = Criterion(name=name, weight=weight, pfType=f, p=p, q=q)
        self.criteria.append(c)


    def addAlternative(self, name:StringVar, data:list[DoubleVar]):
        a = Alternative(name=name, evaluations=data)
        self.alternatives.append(a)


    def deleteCriterion(self, index:int=-1):
        self.criteria.pop(index)


    def deleteAlternative(self, index:int=-1):
        self.alternatives.pop(index)


    def clearAll(self):
        self.alternatives.clear()
        self.criteria.clear()