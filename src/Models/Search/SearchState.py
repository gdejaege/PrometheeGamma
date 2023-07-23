from math import sqrt
from Models.Range.RangeI import RangeI
from Models.Range.RangeJ import RangeJ
import numpy as np
import time

INFINITY = 1000000000


class ConstraintError(Exception):
    """
    Error in a constraint. The message give information over the error.
    """
    def __init__(self, message:str, *args: object) -> None:
        self.message = message
        super().__init__(*args)
        
    def getMessage(self):
        return self.message


class SearchState:
    def __init__(self, Imin=0.0, Imax=1.0, Jmin=0.0, Jmax=1.0, Pmin=1.0, Pmax=INFINITY) -> None:
        self.Imin = Imin
        self.Imax = Imax
        self.Jmin = Jmin
        self.Jmax = Jmax
        self.Pmin = Pmin
        self.Pmax = Pmax
        self.listOfRangeI = []
        self.listOfRangeJ = []
        self.listOfPreference = []


    def getState(self) -> tuple:
        """
        Get the actual state of the search
        """
        return (self.Imin, self.Imax, self.Jmin, self.Jmax, self.Pmin, self.Pmax)


    def setImin(self, val):
        self.Imin = val


    def setImax(self, val):
        self.Imax = val


    def setJmin(self, val):
        self.Jmin = val


    def setJmax(self, val):
        self.Jmax = val


    def setPmin(self, val):
        self.Pmin = val


    def setPmax(self, val):
        self.Pmax = val


    def addPair(self, rI:RangeI, rJ:RangeJ, preference:int):
        self.listOfRangeI.append(rI)
        self.listOfRangeJ.append(rJ)
        self.listOfPreference.append(preference)


    def getAllPairs(self):
        return self.listOfRangeI, self.listOfRangeJ, self.listOfPreference
    

    def verifyConstraint(self):
        if self.Imin > self.Jmin:
            self.Jmin = self.Imin
        if self.Jmax < self.Imax:
            self.Imax = self.Jmax 
        if self.Imin > self.Imax:
            self.print()
            raise ConstraintError("Imin > Imax")
        if self.Jmin > self.Jmax:
            self.print()
            raise ConstraintError("Jmin > Jmax")
        if self.Pmin > self.Pmax:
            self.print()
            raise ConstraintError("Pmin > Pmax")


    def reduceRangeP(self, conflict, r=None):
        print("reduce range P", conflict)
        if r is not None:
            if conflict == 1 or conflict == 3:
                # conflit à la borne supérieure
                while self.Imax < r.getValForP(self.Pmin):
                    self.Pmin += 0.1
                self.Pmin -= 0.1
                while self.Imax < r.getValForP(self.Pmin):
                    self.Pmin += 0.01
                self.verifyConstraint()
            if conflict == 2 or conflict == 3:
                # conflit à la borne inférieure
                while self.Imin > r.getValForP(self.Pmax):
                    if self.Pmax == INFINITY:
                        self.Pmax = 100.1
                    self.Pmax -= 0.1
                self.Pmax += 0.1
                while self.Imin > r.getValForP(self.Pmax):
                    self.Pmax -= 0.01
                self.verifyConstraint()
            if conflict > 3:
                print(conflict)


    def averageIandJ(self, p:float):
        avgI = 0
        avgJ = 0
        for i in range(len(self.listOfRangeI)):
            valueI = self.listOfRangeI[i].getValForP(p)
            avgI += valueI
            valueJ = self.listOfRangeJ[i].getValForP(p)
            avgJ += valueJ
        avgI /= len(self.listOfRangeI)
        avgJ /= len(self.listOfRangeI)
        return avgI, avgJ
    

    def fitnessIandJ(self, p:float, avgI:float, avgJ:float):
        fitI = 0
        fitJ = 0
        for i in range(len(self.listOfRangeI)):
            valueI = self.listOfRangeI[i].getValForP(p)
            valueJ = self.listOfRangeJ[i].getValForP(p)
            if self.listOfPreference[i] == 0:
                if valueI > avgI:
                    fitI += (avgI-valueI)**2
                if valueI > avgJ:
                    fitJ += (avgJ-valueI)**2
            elif self.listOfPreference[i] == -1:
                if valueJ < avgJ:
                    fitJ += (avgJ-valueI)**2
                if valueJ < avgI:
                    fitI += (avgI-valueJ)**2
            elif self.listOfPreference[i] == 1:
                if valueI < avgI:
                    fitI += (avgI-valueI)**2
                if valueJ > avgJ:
                    fitJ += (avgJ-valueI)**2
        fitI = sqrt(fitI)
        fitJ = sqrt(fitJ)
        return fitI, fitJ



    def resolveConflict(self):
        print("resolve conflict")
        almostFound = False
        bestI = None
        bestJ = None
        avgFitness = INFINITY
        p = 1.0
        #it = 0
        while p <= INFINITY:
            avgI, avgJ = self.averageIandJ(p)
            fitI, fitJ = self.fitnessIandJ(p, avgI, avgJ)
            fit = sqrt(fitI**2 + fitJ**2)
            if fit < avgFitness:
                avgFitness = fit
                bestI = avgI
                bestJ = avgJ
            elif fit > avgFitness and not almostFound:
                print("almost found")
                almostFound = True
                p -= 0.1
            elif fit > avgFitness and almostFound:
                p -= 0.01
                break

            if almostFound:
                p += 0.01
            else:
                p += 0.1

            p = round(p, 2)
            
            if p > 100.0 or p == 100.01:
                p = INFINITY
                avgI, avgJ = self.averageIandJ(p)
                break

            #it +=1
            #if it > 1:
            #    break

        self.Imax = bestI
        self.Imin = bestI
        self.Jmin = bestJ
        self.Jmax = bestJ
        self.Pmin = p
        self.Pmax = p


    def resolveIndifference(self, rI:RangeI):
        # I >= [Imin, Imax] ; J >= I
        if self.Imax < rI.getValMin():
            # cas 5: au-dessus des bornes
            self.resolveConflict()
        elif self.Imin > rI.getValMax():
            # cas 6: en-dessous des bornes
            # cas ok, rien à faire
            pass
        elif self.Imin < rI.getValMin() and self.Imax > rI.getValMax():
            # cas 1: dans les bornes
            self.Imin = rI.getValMin()
            self.verifyConstraint()
        elif self.Imin < rI.getValMin() and self.Imax < rI.getValMax():
            # cas 2: conflit à la borne supérieure
            self.reduceRangeP(1, rI)
            self.Imin = rI.getValMin()
            self.verifyConstraint()
        elif self.Imin > rI.getValMin() and self.Imax > rI.getValMax():
            # cas 3: conflit à la borne inférieure
            self.reduceRangeP(2, rI)
            self.verifyConstraint()
        elif self.Imin > rI.getValMin() and self.Imax < rI.getValMax():
            # cas 4: conflit aux 2 bornes
            self.reduceRangeP(3, rI)
            self.verifyConstraint()


    def resolveIncomparability(self, rJ:RangeJ):
        # J <= [Jmin, Jmax] ; I <= J
        if self.Jmax < rJ.getValMin():
            # cas 5: au-dessus des bornes
            # cas ok, rien à faire
            pass
        elif self.Jmin > rJ.getValMax():
            # cas 6: en-dessous des bornes
            self.resolveConflict()
        elif self.Jmin < rJ.getValMin() and self.Jmax > rJ.getValMax():
            # cas 1: dans les bornes
            self.Jmax = rJ.getValMax()
            self.verifyConstraint()
        elif self.Jmin < rJ.getValMin() and self.Jmax < rJ.getValMax():
            # cas 2: conflit à la borne supérieure
            self.reduceRangeP(2, rJ)
            self.verifyConstraint()
        elif self.Jmin > rJ.getValMin() and self.Jmax > rJ.getValMax():
            # cas 3: conflit à la borne inférieure
            self.reduceRangeP(1, rJ)
            self.Jmax = rJ.getValMax()
            self.verifyConstraint()
        elif self.Jmin > rJ.getValMin() and self.Jmax < rJ.getValMax():
            # cas 4: conflit aux 2 bornes
            self.reduceRangeP(3, rJ)
            self.verifyConstraint()


    def resolvePreference(self, rI:RangeI, rJ:RangeJ):
        # I <= [Imin, Imax] ; I <= J
        if self.Imax < rI.getValMin():
            # cas 5: au-dessus des bornes
            # cas ok, rien à faire
            pass
        elif self.Imin > rI.getValMax():
            # cas 6: en-dessous des bornes
            self.resolveConflict()
            return
        elif self.Imin < rI.getValMin() and self.Imax > rI.getValMax():
            # cas 1: dans les bornes
            self.Imax = rI.getValMax()
            self.verifyConstraint()
        elif self.Imin < rI.getValMin() and self.Imax < rI.getValMax() and self.Imax > rI.getValMin():
            # cas 2: conflit à la borne supérieure
            self.reduceRangeP(1, rI)
            self.verifyConstraint()
        elif self.Imin > rI.getValMin() and self.Imax > rI.getValMax():
            # cas 3: conflit à la borne inférieure
            self.reduceRangeP(2, rI)
            self.Imax = rI.getValMax()
            self.verifyConstraint()
        elif self.Imin > rI.getValMin() and self.Imax < rI.getValMax():
            # cas 4: conflit aux 2 bornes
            self.reduceRangeP(3, rI)
            self.verifyConstraint()
        
        # J >= [Jmin, Jmax] ; J >= I
        if self.Jmax < rJ.getValMin():
            # cas 5: au-dessus des bornes
            self.resolveConflict()
            return
        elif self.Jmin > rJ.getValMax():
            # cas 6: en-dessous des bornes
            # cas ok, rien à faire
            pass
        elif self.Jmin < rJ.getValMin() and self.Jmax > rJ.getValMax():
            # cas 1: dans les bornes
            self.Jmin = rJ.getValMin()
            self.verifyConstraint()
        elif self.Jmin < rJ.getValMin() and self.Jmax < rJ.getValMax():
            # cas 2: conflit à la borne supérieure
            self.reduceRangeP(1, rJ)
            self.Jmin = rJ.getValMin()
            self.verifyConstraint()
        elif self.Jmin > rJ.getValMin() and self.Jmax > rJ.getValMax():
            # cas 3: conflit à la borne inférieure
            self.reduceRangeP(2, rJ)
            self.verifyConstraint()
        elif self.Jmin > rJ.getValMin() and self.Jmax < rJ.getValMax():
            # cas 4: conflit aux 2 bornes
            self.reduceRangeP(3, rJ)
            self.verifyConstraint()


    def update(self):
        pref = self.listOfPreference[-1]
        rI = self.listOfRangeI[-1]
        rJ = self.listOfRangeJ[-1]
        if pref == 0:
            self.resolveIndifference(rI)
        elif pref == -1:
            self.resolveIncomparability(rJ)
        elif pref == 1:
            # I <= [Imin, Imax] ; J >= [Jmin, Jmax] ; J >= I
            self.resolvePreference(rI, rJ)


    def print(self):
        print("SearchState")
        print("range I:", self.Imin, self.Imax, end="   ")
        print("range J:", self.Jmin, self.Jmax, end="   ")
        print("range P:", self.Pmin, self.Pmax)