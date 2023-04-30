from customtkinter import (StringVar, DoubleVar)

class Alternative:
    """
    This class represents an alternative (a unit) for the Promethee Gamma application
    """
    def __init__(self, name:DoubleVar=None, evaluations:list[DoubleVar]=[]) -> None:
        self.name = name
        self.evaluations = evaluations


    def setName(self, name:StringVar) -> None:
        """
        Change the name of the alternative
        """
        self.name = name


    def addEvaluations(self, evaluation:DoubleVar) -> None:
        """
        Add an evaluation for a criterion in the alternative
        """
        self.evaluations.append(evaluation)


    def deleteEvaluation(self, index:int=-1) -> None:
        """
        Delete an evaluation for a criterion in the alternative.
        Index corresponds to the position of the evaluation to be deleted from the list. By default, deletes the last evaluation.
        """
        self.evaluations.pop(index)

    
    def getName(self) -> StringVar:
        """
        Return the name in a StringVar object.
        """
        return self.name
    

    def getName_str(self) -> str:
        """
        Return the name in str.
        """
        return self.name.get()
    

    def getEvaluation(self, index=-1) -> DoubleVar:
        """
        Return the evaluation at the position index in a DoubleVar object. By default, return the last evaluation.
        """
        return self.evaluations[index]
    
    
    def getEvaluation_float(self, index=-1) -> float:
        """
        Return the evaluation at the position index in float. By default, return the last evaluation.
        """
        return self.evaluations[index].get()


    def getSize(self) -> int:
        """
        Return the size of the alternative, i.e. the number of evaluations for this alternative.
        """
        return len(self.evaluations)