from Models.PrometheeGamma import PrometheeGamma
from Models.Range.Range import Range
from Models.Range.RangeI import RangeI
from Models.Range.RangeJ import RangeJ

class PreferenceLearning:
    def __init__(self, prometheeGamma:PrometheeGamma) -> None:
        self.prometheeGamma = prometheeGamma
        
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


    def computePossibleThresholdsForOnePair(self, pair:tuple):
        (a1, a2, preference) = pair
        matrixGamma = self.prometheeGamma.getMatrixGamma()
        Pmin = 1
        Pmax = 100
        pair_Irange = None
        pair_Jrange = None
        y = abs(matrixGamma[a1][a2] - matrixGamma[a2][a1])
        if preference == 0: # indifference
            xI = max(matrixGamma[a1][a2], matrixGamma[a2][a1])
            rI = RangeI(xI, y, Pmax, Pmin)
            pair_Irange = Range(rI, 1.0)
            pair_Jrange = Range(rI, 1.0)
            # !!! I >= [Imin, Imax] ; J >= I
        elif preference == 1: # preference
            xI = max(matrixGamma[a1][a2], matrixGamma[a2][a1])
            xJ = min(matrixGamma[a1][a2], matrixGamma[a2][a1])
            rI = RangeI(xI, y, Pmax, Pmin)
            rJ = RangeJ(xJ, y, Pmax, Pmin)
            pair_Irange = Range(0.0, rI)
            pair_Jrange = Range(rJ, 1.0)
            # !!! I <= [Imin, Imax] ; J >= [Jmin, Jmax] ; J >= I
        elif preference == -1: # incomparability
            xJ = min(matrixGamma[a1][a2], matrixGamma[a2][a1])
            rJ = RangeJ(xJ, y, Pmax, Pmin)
            pair_Irange = Range(0.0, rJ)
            pair_Jrange = Range(0.0, rJ)
            # !!! J <= [Jmin, Jmax] ; I <= J
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