from customtkinter import (StringVar, IntVar, DoubleVar)
from Models.Alternative import Alternative
from Models.Criterion import Criterion

class DataTabModel:
    def __init__(self) -> None:
        self.alternatives = []
        """
        List of alternatives. The index correspond to the row number.
        """
        self.criteria = []
        """
        List of criteria. The index correspond to the column number.
        """


    def getCriterion(self, index=-1) -> Criterion:
        """
        Return the criterion object at position index. By default, return the last criterion.
        """
        return self.criteria[index]
    

    def getAlternative(self, index=-1) -> Alternative:
        """
        Return the alternative object at position index. By default, return the last alternative.
        """
        return self.alternatives[index]


    def addVoidCriterion(self, master) -> None:
        """
        Add a new void criterion
        """
        name = StringVar(master=master, value="New Criterion")
        weight = DoubleVar(master=master, value=0.0)
        f = IntVar(master=master, value=1)
        p = DoubleVar(master=master, value=1.0)
        q = DoubleVar(master=master, value=0.0)
        self.addCriterion(name, weight, f, p, q)


    def addCriterion(self, name:StringVar, weight:DoubleVar, f:IntVar, p:DoubleVar=None, q:DoubleVar=None):
        """
        Add a new criterion.
        Parameters are the characteristics of the new criterion.
        """
        c = Criterion(name=name, weight=weight, pfType=f, p=p, q=q)
        self.criteria.append(c)


    def addVoidAlternative(self, master) -> None:
        """
        Add a new void alternative
        """
        name = StringVar(master=master, value="New Alternative")
        data = []
        for i in range(len(self.criteria)):
            val = DoubleVar(master=master, value=0.0)
            data.append(val)
        self.addAlternative(name=name, data=data)


    def addAlternative(self, name:StringVar, data:list):
        """
        Add a new alternative.
        Parameters are the characteristics of the new alternative.
        """
        a = Alternative(name=name, evaluations=data)
        self.alternatives.append(a)


    def deleteCriterion(self, index:int=-1) -> None:
        """
        Delete the criterion at position index. By default, delete the last criterion.
        """
        self.criteria.pop(index)


    def deleteAlternative(self, index:int=-1) -> None:
        """
        Delete the alternative at position index. By default, delete the last alternative.
        """
        self.alternatives.pop(index)


    def getNumberOfCriteria(self) -> int:
        """
        Return the number of criteria in the model.
        """
        return len(self.criteria)
    

    def getNumberOfAlternatives(self) -> int:
        """
        Return the number of alternatives in the model.
        """
        return len(self.alternatives)


    def clearAll(self) -> None:
        """
        Clear the model, i.e. delete all criteria and alternatives.
        """
        self.alternatives.clear()
        self.criteria.clear()


    def createAlternative(self, master, name:str, data:list) -> None:
        """
        Create a new alternative from a name in str and a list of evaluation in float
        """
        n = StringVar(master=master, value=name)
        l = []
        for d in data:
            val = float(d)
            e = DoubleVar(master=master, value=val)
            l.append(e)
        self.addAlternative(n,l)


    def createCriteria(self, master, criteriaNames:list, criteriaWeights:list, criteriaPreferenceFunctionType:list, criteriaP:list, criteriaQ:list) -> None:
        """
        Create a new list of criteria from list of caracteristics of criteria
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
            self.addCriterion(name=name, weight=weight, f=pfType, p=p, q=q)
    

    def readFile(self, file, master) -> None:
        """
        Read a csv file and add its content in the model
        """
        criteriaP = None
        criteriaQ = None
        for line in file:
            line = line.strip()
            temp = line.split(',')
            if(temp[0] == 'c'):
                criteriaNames = temp[1:]
            elif(temp[0] == 'w'):
                criteriaWeights = temp[1:]
            elif(temp[0] == 'f'):
                criteriaPreferenceFunctionType = temp[1:]
            elif(temp[0] == 'p'):
                criteriaP = temp[1:]
            elif(temp[0] == 'q'):
                criteriaQ = temp[1:]
            else:
                self.createAlternative(master, temp[0], temp[1:])
        self.createCriteria(master, criteriaNames, criteriaWeights, criteriaPreferenceFunctionType, criteriaP, criteriaQ)


    def addOneEvaluationInAllAlternatives(self, master) -> None:
        """
        Add an evaluation in all alternatives.
        This method must be called when creating a new criterion.
        """
        for i in range(1, len(self.alternatives)):
            val = DoubleVar(master=master, value=0.0)
            self.alternatives[i].addEvaluations(evaluation=val)

    
    def getEvaluationOfAlternative(self, indexAlt:int, indexEval:int) -> DoubleVar:
        """
        Return the evaluation at position indexEval from the alternative at position indexAlt in the model
        """
        return self.alternatives[indexAlt].getEvaluation(indexEval)
    

    def deleteEvaluationOfAlternative(self, indexAlt:int, indexEval:int) -> None:
        """
        Delete the evaluation at position indexEval from the alternative at position indexAlt in the model
        """
        self.alternatives[indexAlt].deleteEvaluation(indexEval)


    def getAlternativesName(self) -> list:
        """
        Return the list of alternative names.
        """
        names = []
        for a in self.alternatives:
            names.append(a.getName_str())
        return names


    ###################
    ### Computation ###
    ###################

    def computeCriterionDependentValues(self) -> None:
        """
        Add evaluation of units in the column of each criterion and compute the pi_c_matrix and the phi_c_list for each criterion.
        It is needed for the computation of the gamma matrix for Promethee Gamma method.
        """
        for c in range(len(self.criteria)):
            self.criteria[c].clearColumn()
            for a in self.alternatives:
                val = a.getEvaluation_float(c)
                self.criteria[c].add_unit(val)
            self.criteria[c].build_pi_c_matrix()
            self.criteria[c].build_phi_c_list()


    def getGamma_ij_Criteria_k(self, i:int, j:int, criterion:int) -> float:
        """
        Return the gamma_ij value for criterion k.
        """
        c = self.criteria[criterion]
        return c.get_gamma_c_ij(i=i, j=j)