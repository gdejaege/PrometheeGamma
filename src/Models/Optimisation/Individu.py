import random
from math import (sqrt)
from Models.Range.RangeI import RangeI
from Models.Range.RangeJ import RangeJ

class Individu:
    def __init__(self, I=0.0, J=0.0, P=1.0) -> None:
        self.I = I
        self.J = J
        self.P = P
        self.fitness = 0.0


    def makeRandom(self):
        r = random.randint(0,99)
        self.I = r/100
        self.J = random.randint(r,100)/100
        self.P = float(random.randint(1, 99)) + random.random()


    def getI(self):
        return self.I
    

    def getJ(self):
        return self.J
    

    def getP(self):
        return self.P
    

    def setI(self, I):
        self.I = I


    def setI(self, J):
        self.J = J


    def setI(self, P):
        self.P = P


    def childOf(self, father, mother):
        self.I = (father.getI() + mother.getI())/2
        self.J = (father.getJ() + mother.getJ())/2
        self.P = (father.getP() + mother.getP())/2
    

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


    def getFitness(self):
        return self.fitness
    

    def mutate(self, attrMutant:int, mutation:float):
        sign = random.randint(1,2)
        if attrMutant == 0:
            if sign == 1:
                self.I += mutation
                if self.I > 1:
                    self.I = 1
                if self.I > self.J:
                    self.J = self.I
            else:
                self.I -= mutation
                if self.I < 0:
                    self.I = 0
        elif attrMutant == 1:
            if sign == 1:
                self.J += mutation
                if self.J > 1:
                    self.J = 1
            else:
                self.J -= mutation
                if self.J < 0:
                    self.J = 0
                if self.I > self.J:
                    self.I = self.J
        else:
            if sign == 1:
                self.P += mutation
                if self.P > 100.0:
                    self.P = 100.0
            else:
                self.P -= mutation
                if self.P < 1.0:
                    self.P = 1.0

