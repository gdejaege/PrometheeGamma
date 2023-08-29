from customtkinter import (StringVar, IntVar, DoubleVar)
from Models.DataTabModels.Alternative import Alternative
from Models.DataTabModels.Criterion import Criterion


class DataTabModel:
    """
    A class to create alternatives and criteria, and keep them in memory

    Attributes
    ----------
    alternatives : list of Alternative
        the list of alternatives
    criteria : list of Criterion
        the list of criteria

    Methods
    -------
    """
    
    def __init__(self) -> None:
        self.alternatives = []
        """List of alternatives. The index correspond to the row number"""
        self.criteria = []
        """List of criteria. The index correspond to the column number"""


    def getCriterion(self, index=-1) -> Criterion:
        """Return the criterion object at position index. By default, return the last criterion

        Parameters
        ----------
        index : int, optional
            the index of criterion that must be returned (default is -1)

        Return
        ------
        criteria[index] : Criterion
            the criterion at position index in the criteria list
        """
        return self.criteria[index]
    

    def getAlternative(self, index=-1) -> Alternative:
        """Return the alternative object at position index. By default, return the last alternative

        Parameters
        ----------
        index : int, optional
            the index of alternative that must be returned (default is -1)

        Return
        ------
        alternatives[index] : Alternative
            the alternative at position index in the alternatives list
        """
        return self.alternatives[index]


    def addCriterion(self, master):
        """Add a new criterion

        Create a new criterion with default values: 
        "New Criterion" as name,
        0.0 as weight,
        1 as preference function type,
        1.0 as preference threshold in preference function,
        0.0 as indifference threshold in preference function.

        Parameters
        ----------
        master : CTkFrame, optional
            the tkinter master frame to link StringVar, IntVar and DoubleVar
        """

        name = StringVar(master=master, value="Criterion"+ str(len(self.criteria)+1))
        weight = DoubleVar(master=master, value=0.0)
        f = IntVar(master=master, value=1)
        p = DoubleVar(master=master, value=1.0)
        q = DoubleVar(master=master, value=0.0)
        c = Criterion(name=name, weight=weight, pfType=f, p=p, q=q)
        self.criteria.append(c)


    def addAlternative(self, master) -> None:
        """Add a new alternative

        Create a new criterion with default values:
        "New Alternative" as name,
        0.0 as evaluation for all criteria

        Parameters
        ----------
        master : CTkFrame
            the tkinter master frame to link StringVar and DoubleVar
        """
        name = StringVar(master=master, value="Alternative" + str(len(self.alternatives)+1))
        data = []
        for i in range(len(self.criteria)):
            val = DoubleVar(master=master, value=0.0)
            data.append(val)
        a = Alternative(name=name, evaluations=data)
        self.alternatives.append(a)


    def deleteCriterion(self, index:int=-1) -> None:
        """Delete the criterion at position index. By default, delete the last criterion

        Parameters
        ----------
        index : int, optional
            the index of the criterion that must be deleted (default is -1)
        """
        self.criteria.pop(index)


    def deleteAlternative(self, index:int=-1) -> None:
        """Delete the alternative at position index. By default, delete the last alternative

        Parameters
        ----------
        index : int, optional
            the index of the alternative that must be deleted (default is -1)
        """
        self.alternatives.pop(index)


    def getNumberOfCriteria(self) -> int:
        """Return the number of criteria in the model

        Returns
        -------
        int
            the length of the criteria list
        """
        return len(self.criteria)
    

    def getNumberOfAlternatives(self) -> int:
        """Return the number of alternatives in the model

        Returns
        -------
        int
            the length of the alternatives list
        """
        return len(self.alternatives)


    def clearAll(self) -> None:
        """Clear the model, i.e. delete all criteria and alternatives
        """
        self.alternatives.clear()
        self.criteria.clear()

    
    def isVoid(self) -> bool:
        """Test if model contains no alternative or no criterion

        Returns
        -------
        bool
            True if no alternative or no criterion, False otherwise
        """
        return len(self.alternatives) == 0 or len(self.criteria) == 0
    

    def twoAlter(self) -> bool:
        """test if model contains less than two alternatives

        Returns
        -------
        bool
            True if there is less than 2 alternatives in the model, False otherwise
        """
        return len(self.alternatives) < 2


    def createAlternative(self, master, name:str, data:list) -> None:
        """Create a new alternative from a name in str and a list of evaluation in float

        Parameters
        ----------
        master : CTkFrame
            the tkinter master frame to link StringVar and DoubleVar
        name : str
            the name of the new alternative
        data : list[float]
            the list of alternative evaluation for each criterion
        """
        n = StringVar(master=master, value=name)
        l = []
        for d in data:
            val = float(d)
            e = DoubleVar(master=master, value=val)
            l.append(e)
        a = Alternative(name=n, evaluations=l)
        self.alternatives.append(a)


    def createCriteria(self, master, criteriaNames:list, criteriaWeights:list, criteriaPreferenceFunctionType:list, criteriaP:list, criteriaQ:list) -> None:
        """Create a new list of criteria from list of caracteristics of criteria

        Parameters
        ----------
        master : CTkFrame
            the tkinter master frame to link StringVar, IntVar and DoubleVar
        criteriaNames : list[str]
            list of names of criteria
        criteriaWeights : list[str]
            list of weights of criteria
        criteriaPreferenceFunctionType : list[str]
            list of type of preference function of criteria
        criteriaP : list[str]
            list of preference threshold in preference function
        criteriaQ : list[str]
            list of indifference threshold in preference function
        """
        p = None
        q = None
        for i in range(len(criteriaNames)):
            name = StringVar(master=master, value=criteriaNames[i])
            weight = DoubleVar(master=master, value=float(criteriaWeights[i]))
            pfType = IntVar(master=master, value=int(criteriaPreferenceFunctionType[i]))
            if(criteriaP != None):
                p = DoubleVar(master=master, value=float(criteriaP[i]))
            if(criteriaQ != None):
                q = DoubleVar(master=master, value=float(criteriaQ[i]))
            c = Criterion(name=name, weight=weight, pfType=pfType, p=p, q=q)
            self.criteria.append(c)


    def addOneEvaluationInAllAlternatives(self, master) -> None:
        """Add an evaluation in all alternatives

        This method must be called when creating a new criterion

        Parameters
        ----------
        master : CTkFrame
            the tkinter master frame to link DoubleVar
        """
        for i in range(len(self.alternatives)):
            val = DoubleVar(master=master, value=0.0)
            self.alternatives[i].addEvaluations(evaluation=val)

    
    def getEvaluationOfAlternative(self, indexAlt:int, indexEval:int) -> DoubleVar:
        """Return the evaluation at position indexEval from the alternative at position indexAlt in the model

        Parameters
        ----------
        indexAlt : int
            the index of the selected alternative in alternatives list
        indexEval : int
            the index of the selected evaluation in evaluation list (in the selected alternative)

        Returns
        -------
        DoubleVar
            the selected evaluation of the selected alternative
        """
        return self.alternatives[indexAlt].getEvaluation(indexEval)
    

    def deleteEvaluationOfAlternative(self, indexAlt:int, indexEval:int) -> None:
        """Delete the evaluation at position indexEval from the alternative at position indexAlt in the model

        Parameters
        ----------
        indexAlt : int
            the index of the selected alternative in alternatives list
        indexEval : int
            the index of the selected evaluation in evaluation list (in the selected alternative)

        """
        self.alternatives[indexAlt].deleteEvaluation(indexEval)


    def getAlternativesName(self) -> list:
        """Return the list of alternative names

        Returns
        -------
        list
            the list of alternative names
        """
        names = []
        for a in self.alternatives:
            names.append(a.getName_str())
        return names
    

    def getCriteriaNames(self) -> list:
        """Return the list of criteria names

        Returns
        -------
        list
            the list of criteria names
        """
        names = []
        for a in self.criteria:
            names.append(a.getName_str())
        return names


    ###################
    ### Computation ###
    ###################

    def computeCriterionDependentValues(self) -> None:
        """Add evaluation of units in the column of each criterion and compute the pi_c_matrix and the phi_c_list for each criterion

        It is needed for the computation of the gamma matrix for Promethee Gamma method
        """
        for c in range(len(self.criteria)):
            self.criteria[c].clearColumn()
            for a in self.alternatives:
                val = a.getEvaluation_float(c)
                self.criteria[c].addEvaluation(val)
            self.criteria[c].build_pi_c_matrix()
            self.criteria[c].build_phi_c_list()


    def getGamma_ij_Criteria_k(self, i:int, j:int, criterion:int) -> float:
        """Return the gamma_ij value for criterion k

        Parameters
        ----------
        i : int
            the index of alternative i in column of criterion k
        j : int
            the index of alternative j in column of criterion k
        criterion : int
            the index of selected criterion k in criteria list

        Returns
        -------
        float
            γ_k_ij, the value of γ for criterion k and alternatives i and j
        """
        c = self.criteria[criterion]
        return c.get_gamma_c_ij(i=i, j=j)