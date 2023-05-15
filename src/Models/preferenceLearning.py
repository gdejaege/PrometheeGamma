from customtkinter import IntVar
from Models.PrometheeGamma import PrometheeGamma
from Models.Range.Range import Range
from Models.Range.RangeI import RangeI
from Models.Range.RangeJ import RangeJ
import random
from Models.Optimisation.Population import Population

class PreferenceLearning:
    def __init__(self, master, prometheeGamma:PrometheeGamma) -> None:
        self.prometheeGamma = prometheeGamma
        self.master = master
        
        # Init values
        self.Irange = Range(0.0, 1.0)
        self.Jrange = Range(0.0, 1.0)
        self.Prange = Range(1.0, 100.0)
        """
        self.Iminimum = 0
        self.Imaximum = 1
        self.Jminimum = 0
        self.Jmaximum = 1
        self.Pminimum = 1
        self.Pmaximum = 100
        """

        self.listOfPairs = []
        """
        [(a1, a2, preference), (a1, a2, preference), ... ]
        """
        self.listofPossibleThresholds = []


    def createPairs(self, alternatives:list):
        possiblePairs = self.createAllPossiblePairs(alternatives)
        self.choosePairs(possiblePairs)


    def createAllPossiblePairs(self, alternatives:list) -> list:
        possiblePairs = []
        for i in range(len(alternatives)):
            for j in range(i+1, len(alternatives)):
                    possiblePairs.append(((alternatives[i], i), (alternatives[j], j), IntVar(master=self.master, value=0)))
        return possiblePairs
    

    def choosePairs(self, possiblePairs:list):
        self.listOfPairs.clear()
        if len(possiblePairs) > 5:
            for i in range(5):
                j = random.choice(possiblePairs)
                while j in self.listOfPairs:
                    j = random.choice(possiblePairs)
                self.listOfPairs.append(j)
        else :
            self.listOfPairs = possiblePairs


    def getPair(self, index:int):
        if index < len(self.listOfPairs):
            r = self.listOfPairs[index]
            return (r[0][0], r[1][0], r[2])
        else:
            raise Exception("index > len(listOfPairs)")
        

    def getNumberOfPairs(self):
        return len(self.listOfPairs)
    

    def computeRangeOfThresholdsForAllPairs(self):
        listOfIrange = []
        listOfJrange = []
        listOfPreference = []
        for pair in self.listOfPairs:
            (i, j, p) = self.computeRangeOfThresholdsForOnePair(pair)
            listOfIrange.append(i)
            listOfJrange.append(j)
            listOfPreference.append(p)
        return (listOfIrange, listOfJrange, listOfPreference)
    

    def findOptimum(self):
        (listOfIrange, listOfJrange, listOfPreference) = self.computeRangeOfThresholdsForAllPairs()
        population = Population(100)
        population.evolution(200, listOfIrange, listOfJrange, listOfPreference)
        (i, j, p) = population.getBest()
        print("I =", i, " J =", j, " P=", p)
        return (i, j, p)


    

    def computeRangeOfThresholdsForOnePair(self, pair:tuple):
        (a1_t, a2_t, pref) = pair
        a1 = a1_t[1]
        a2 = a2_t[1]
        preference = pref.get()
        if preference == 2:
            temp = a1
            a1 = a2
            a2 = temp
            preference = 1
        matrixGamma = self.prometheeGamma.getMatrixGamma()
        Pmin = 1
        Pmax = 100
        rI = None
        rJ = None
        y = abs(matrixGamma[a1][a2] - matrixGamma[a2][a1])
        if preference == 0: # indifference
            xI = max(matrixGamma[a1][a2], matrixGamma[a2][a1])
            rI = RangeI(xI, y, Pmax, Pmin)
            rJ = rI
            # !!! I >= [Imin, Imax] ; J >= I
        elif preference == 1: # preference
            xI = max(matrixGamma[a1][a2], matrixGamma[a2][a1])
            xJ = min(matrixGamma[a1][a2], matrixGamma[a2][a1])
            rI = RangeI(xI, y, Pmax, Pmin)
            rJ = RangeJ(xJ, y, Pmax, Pmin)
            # !!! I <= [Imin, Imax] ; J >= [Jmin, Jmax] ; J >= I
        elif preference == -1: # incomparability
            xJ = min(matrixGamma[a1][a2], matrixGamma[a2][a1])
            rJ = RangeJ(xJ, y, Pmax, Pmin)
            rI = rJ
            # !!! J <= [Jmin, Jmax] ; I <= J
        return (rI, rJ, preference)



    def computePossibleThresholdsForOnePair(self, pair:tuple):
        (a1_t, a2_t, pref) = pair
        a1 = a1_t[1]
        a2 = a2_t[1]
        preference = pref.get()
        if preference == 2:
            temp = a1
            a1 = a2
            a2 = temp
            preference = 1
        matrixGamma = self.prometheeGamma.getMatrixGamma()
        Pmin = 1
        Pmax = 100
        pair_Irange = None
        pair_Jrange = None
        y = abs(matrixGamma[a1][a2] - matrixGamma[a2][a1])
        if preference == 0: # indifference
            xI = max(matrixGamma[a1][a2], matrixGamma[a2][a1])
            rI = RangeI(xI, y, Pmax, Pmin)
            print("rI")
            rI.print()
            pair_Irange = Range(rI, 1.0)
            pair_Jrange = Range(rI, 1.0)
            # !!! I >= [Imin, Imax] ; J >= I
        elif preference == 1: # preference
            xI = max(matrixGamma[a1][a2], matrixGamma[a2][a1])
            xJ = min(matrixGamma[a1][a2], matrixGamma[a2][a1])
            rI = RangeI(xI, y, Pmax, Pmin)
            rJ = RangeJ(xJ, y, Pmax, Pmin)
            print("rI")
            rI.print()
            print("rJ")
            rJ.print()
            pair_Irange = Range(0.0, rI)
            pair_Jrange = Range(rJ, 1.0)
            # !!! I <= [Imin, Imax] ; J >= [Jmin, Jmax] ; J >= I
        elif preference == -1: # incomparability
            xJ = min(matrixGamma[a1][a2], matrixGamma[a2][a1])
            rJ = RangeJ(xJ, y, Pmax, Pmin)
            print("rJ")
            rJ.print()
            pair_Irange = Range(0.0, rJ)
            pair_Jrange = Range(0.0, rJ)
            # !!! J <= [Jmin, Jmax] ; I <= J
        print("ranges for pair: ", a1_t[0].getName_str(), " and ", a2_t[0].getName_str())
        pair_Irange.print()
        pair_Jrange.print()
        return (pair_Irange, pair_Jrange)
    

    def computePossibleThresholdsForAllPairs(self):
        for p in self.listOfPairs:
            result = self.computePossibleThresholdsForOnePair(p)
            self.listofPossibleThresholds.append(result)


    def chooseThresholds(self):
        for e in self.listofPossibleThresholds:
            if self.Irange.include(e[0]):
                self.Irange = e[0]
            elif e[0].getMin() >= self.Irange.getMin():
                self.Irange.setMin(e[0].getMin())
            elif e[0].getMax() <= self.Irange.getMax():
                self.Irange.setMax(e[0].getMax())

            if self.Jrange.include(e[1]):
                self.Jrange = e[1]
            elif e[1].getMin() >= self.Jrange.getMin():
                self.Jrange.setMin(e[1].getMin())
            elif e[1].getMax() <= self.Jrange.getMax():
                self.Jrange.setMax(e[1].getMax())

        # Tests  
        print("Irange:")
        self.Irange.print()
        print("Jrange:")
        self.Jrange.print()



"""
    def computePossibleThreshold(self, pair:tuple):
        (a1, a2, preference) = pair
        matrixGamma = self.prometheeGamma.getMatrixGamma()
        Pmin = 1
        Pmax = 100
        y = abs(matrixGamma[a1][a2] - matrixGamma[a2][a1])
        if preference == 0: # indifference
            xI = max(matrixGamma[a1][a2], matrixGamma[a2][a1])
            Imin = min(xI + y/Pmax, 1)
            Imax = min(xI + y/Pmin, 1)
            Jmin = Imin
            Jmax = Imax
            # !!! I >= [Imin, Imax] ; J >= I
        elif preference == 1: # preference
            xI = max(matrixGamma[a1][a2], matrixGamma[a2][a1])
            xJ = min(matrixGamma[a1][a2], matrixGamma[a2][a1])
            Imin = min(xI + y/Pmax, 1)
            Imax = min(xI + y/Pmin, 1)
            Jmin = xJ - y/Pmax
            Jmax = xJ - y/Pmin
            # !!! I <= [Imin, Imax] ; J >= [Jmin, Jmax] ; J >= I
            if Jmax < Imin:
                # example :
                # J = [0.2, 0.3]  and I = [0.4, 0.5]
                # TODO
                print("erreur, J < I")
            elif Jmin < Imax:
                # example :
                # J = [0.2, 0.3]  and I = [0.25, 0.35]
                # TODO
                print("J and I linked. !!! P !!!")
        elif preference == -1: # incomparability
            xJ = min(matrixGamma[a1][a2], matrixGamma[a2][a1])
            Jmin = xJ - y/Pmax
            Jmax = xJ - y/Pmin
            Imin = Jmin
            Imax = Jmax
            # !!! J <= [Jmin, Jmax] ; I <= J
        return (Imin, Imax, Jmin, Jmax, Pmin, Pmax)
    

    def evalParameters(self):
        for i in range(len(self.listOfPairs)):
            (Imin, Imax, Jmin, Jmax, Pmin, Pmax) = self.computePossibleThreshold(self.listOfPairs[i])
            self.listofPossibleValues.append((Imin, Imax, Jmin, Jmax, Pmin, Pmax))
            if self.listOfPairs[i][2] == 0: # indifference
                # I >= [Imin, Imax] ; J >= I
                if Imax < self.Jminimum and Imin < self.Imaximum and Imin > self.Iminimum:
                    self.Iminimum = Imin
                else :
                    self.resolveConflict()
            elif self.listOfPairs[i][2] == 1: # Preference
                pass
            elif self.listOfPairs[i][2] == -1: # incomparability
                # J <= [Jmin, Jmax] ; I <= J
                if Jmax < self.Jmaximum and Jmax > self.Jminimum:
                    if Jmax > Imax:
                        self.Jmaximum = Jmax
                    elif Jmax > Imin:
                        self.Jmaximum = Jmax
                        if Jmin > Imin:
                            pass



    
    def resolveConflict(self):
        print("conflit")
        # TODO
        pass

"""



"""
    def computeFIandFJ(self, a1:int, a2:int) -> tuple:
        matrixGamma = self.prometheeGamma.getMatrixGamma()
        xI = max(matrixGamma[a1][a2], matrixGamma[a2][a1])
        xJ = min(matrixGamma[a1][a2], matrixGamma[a2][a1])
        y = abs(matrixGamma[a1][a2] - matrixGamma[a2][a1])
        return (xI, xJ, y)
"""