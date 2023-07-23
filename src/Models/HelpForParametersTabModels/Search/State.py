from math import sqrt
from Models.HelpForParametersTabModels.Range.RangeI import RangeI
from Models.HelpForParametersTabModels.Range.RangeJ import RangeJ

class State:
    def __init__(self) -> None:
        self.I = 0
        self.J = 0
        self.P = 1.0
        self.fitness = None


    def setI(self, val):
        self.I = val


    def setJ(self, val):
        self.J = val


    def setP(self, val):
        self.P = val


    def getParam(self):
        return self.I, self.J, self.P


    def computeFitness(self, ListOfI:list, ListOfJ:list, preference:list):
        averageI = 0.0
        averageJ = 0.0
        for k in range(len(ListOfI)):
            i = ListOfI[k]
            j = ListOfJ[k]
            if (preference[k] == 0 and self.I >= i.getValForP(self.P)) or (preference[k] == 1 and self.I <= i.getValForP(self.P)) or (preference[k] == -1 and self.I <= j.getValForP(self.P)):
                averageI += 0.0
            else: 
                averageI += (self.I - i.getValForP(self.P))**2
            if (preference[k] == 0 and self.J >= i.getValForP(self.P)) or (preference[k] == 1 and self.J >= j.getValForP(self.P)) or (preference[k] == -1 and self.J <= j.getValForP(self.P)):
                averageJ += 0.0
            else:
                averageI += (self.J - j.getValForP(self.P))**2
        averageI = sqrt(averageI)
        averageJ = sqrt(averageJ)
        self.fitness = sqrt((averageI**2) + (averageJ**2))
        return self.fitness