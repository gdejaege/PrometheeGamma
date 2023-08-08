from customtkinter import (StringVar, DoubleVar)

class Alternative:
    """
    This class represents an alternative (a unit) for the Promethee Gamma application

    Attributes
    ----------
    name : StringVar
        the alternative name
    evaluations : list[DoubleVar]
        the list of alternative evaluation for each criterion

    Methods
    -------
    setName(name:StringVar)
        set the name of the alternative
    addEvaluations(evaluation:DoubleVar)
        add an evaluation for a criterion in the alternative
    deleteEvaluation(index:int=-1)
        delete an evaluation for a criterion in the alternative
    getName()
        return the name in a StringVar object
    getName_str()
        return the name in str
    getEvaluation(index=-1)
        return the evaluation at the position index in a DoubleVar object. By default, return the last evaluation
    getEvaluation_float(index=-1)
        return the evaluation at the position index in float. By default, return the last evaluation
    getSize()
        return the size of the alternative, i.e. the number of evaluations for this alternative
    """
    
    def __init__(self, name:StringVar=None, evaluations:list[DoubleVar]=[]) -> None:
        """
        Parameters
        ----------
        name : StringVar, optional
            the alternative name (default is None)
        evaluations : list, optional
            the list of alternative evaluation for each criterion (default is a void list)
        """

        self.name = name
        self.evaluations = evaluations


    def setName(self, name:StringVar) -> None:
        """Set the name of the alternative

        Parameters
        ----------
        name : StringVar
            the new alternative name
        """

        self.name = name


    def addEvaluations(self, evaluation:DoubleVar) -> None:
        """Add an evaluation for a criterion in the alternative

        Parameters
        ----------
        evaluation : DoubleVar
            the evaluation to add
        """

        self.evaluations.append(evaluation)


    def deleteEvaluation(self, index:int=-1) -> None:
        """Delete an evaluation for a criterion in the alternative

        Index corresponds to the position of the evaluation to be deleted from the list. By default, deletes the last evaluation

        Parameters
        ----------
        index : int, optional
            the index of the evaluation that must be deleted (default is -1)
        """

        self.evaluations.pop(index)

    
    def getName(self) -> StringVar:
        """Return the name in a StringVar object

        Return
        ------
        name : StringVar
            the alternative name
        """

        return self.name
    

    def getName_str(self) -> str:
        """Return the name in str

        Return
        ------
        name : str
            the alternative name (in str)
        """

        return self.name.get()
    

    def getEvaluation(self, index=-1) -> DoubleVar:
        """Return the evaluation at the position index in a DoubleVar object. By default, return the last evaluation

        Parameters
        ----------
        index : int
            the index of the evaluation that must be returned (default is -1)
        
        Return
        ------
        evaluations[index] : DoubleVar
            the evaluation at position index in the list evaluations
        """

        return self.evaluations[index]
    
    
    def getEvaluation_float(self, index=-1) -> float:
        """Return the evaluation at the position index in float. By default, return the last evaluation

        Parameters
        ----------
        index : int
            the index of the evaluation that must be returned (default is -1)
        
        Return
        ------
        evaluations[index].get() : float
            the evaluation at position index in the list evaluations (in float)
        """

        return self.evaluations[index].get()


    def getSize(self) -> int:
        """Return the size of the alternative, i.e. the number of evaluations for this alternative

        Return
        ------
        len(evaluations) : int
            the length of the evaluations list
        """
        
        return len(self.evaluations)