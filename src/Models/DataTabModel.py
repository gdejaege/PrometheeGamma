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


    def setUnits(self, new_units:list) -> None:
        self.units = new_units


    def setCiteria(self, new_criteria:list) -> None:
        self.criteria = new_criteria


    def getCriterion(self, index=-1) -> Criterion:
        return self.criteria[index]
    

    def getAlternative(self, index=-1) -> Alternative:
        return self.alternatives[index]


    def addVoidCriterion(self, master):
        """
        Add a void criterion
        """
        name = StringVar(master=master, value="New Criterion")
        weight = DoubleVar(master=master, value=0.0)
        f = IntVar(master=master, value=1)
        p = DoubleVar(master=master, value=1.0)
        q = DoubleVar(master=master, value=0.0)
        self.addCriterion(name, weight, f, p, q)


    def addCriterion(self, name:StringVar, weight:DoubleVar, f:IntVar, p:DoubleVar=None, q:DoubleVar=None):
        c = Criterion(name=name, weight=weight, pfType=f, p=p, q=q)
        self.criteria.append(c)


    def addVoidAlternative(self, master):
        """
        Add a void alternative
        """
        name = StringVar(master=master, value="New Alternative")
        data = []
        for i in range(len(self.criteria)):
            val = DoubleVar(master=master, value=0.0)
            data.append(val)
        self.addAlternative(name=name, data=data)


    def addAlternative(self, name:StringVar, data:list):
        a = Alternative(name=name, evaluations=data)
        self.alternatives.append(a)


    def deleteCriterion(self, index:int=-1):
        self.criteria.pop(index)


    def deleteAlternative(self, index:int=-1):
        self.alternatives.pop(index)


    def getNumberOfCriteria(self) -> int:
        return len(self.criteria)
    

    def getNumberOfAlternatives(self) -> int:
        return len(self.alternatives)


    def clearAll(self):
        self.alternatives.clear()
        self.criteria.clear()


    def createAlternative(self, master, name:str, data:list):
        n = StringVar(master=master, value=name)
        l = []
        for d in data:
            val = float(d)
            e = DoubleVar(master=master, value=val)
            l.append(e)
        self.addAlternative(n,l)


    def createCriteria(self, master, criteriaNames, criteriaWeights, criteriaPreferenceFunctionType, criteriaP, criteriaQ):
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
    

    def readFile(self, file, master):
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


    def addOneEvaluationInAllAlternatives(self, master):
        for i in range(1, len(self.alternatives)):
            val = DoubleVar(master=master, value=0.0)
            self.alternatives[i].addEvaluations(evaluation=val)

    
    def getEvaluationOfAlternative(self, indexAlt:int, indexEval:int):
        return self.alternatives[indexAlt].getEvaluation(indexEval)
    

    def deleteEvaluationOfAlternative(self, indexAlt:int, indexEval:int):
        self.alternatives[indexAlt].deleteEvaluation(indexEval)


    def getAlternativesName(self):
        names = []
        for a in self.alternatives:
            names.append(a.getName_str())
        return names


    ###################
    ### Computation ###
    ###################

    def computeCriterionDependentValues(self):
        for c in range(len(self.criteria)):
            self.criteria[c].clearColumn()
            for a in self.alternatives:
                val = a.getEvaluation_float(c)
                self.criteria[c].add_unit(val)
            self.criteria[c].build_pi_c_matrix()
            self.criteria[c].build_phi_c_list()


    def getGamma_ij_Criteria_k(self, i:int, j:int, criterion:int) -> float:
        c = self.criteria[criterion]
        #print(c.getName_str())
        return c.get_gamma_c_ij(i=i, j=j)