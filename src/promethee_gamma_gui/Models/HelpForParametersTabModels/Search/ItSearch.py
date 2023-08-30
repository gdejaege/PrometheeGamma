from sys import maxsize
from math import sqrt

#from Models.HelpForParametersTabModels.Range.RangeI import RangeI
#from Models.HelpForParametersTabModels.Range.RangeJ import RangeJ
from ..Range import RangeI, RangeJ

INFINITY = maxsize
"""The infinity (in the computer meaning)"""


class ItSearch:
    """
    A class to make search and determine the value of PROMETHEE Gamma method parameters

    Attributes
    ----------
    Imin : float
        lowest possible value for I
    Imax : float
        highest possible value for I
    Jmin : float
        lowest possible value for J
    Jmax : float
        highest possible value for J
    Pmin : float
        lowest possible value for P
    Pmax : float
        highest possible value for P
    listOfRangeI : list[RangeI]
        the list of range of I computed from user answers
    listOfRangeJ : list[RangeJ]
        the list of range of J computed from user answers
    listOfPreference : list[int]
        the list of preference indicators from user answers
    """

    def __init__(self, Imin=0.0, Imax=1.0, Jmin=0.0, Jmax=1.0, Pmin=1.0, Pmax=INFINITY) -> None:
        """
        Parameters
        ----------
        Imin : float, optional
            lowest possible value for I (default is 0.0)
        Imax : float, optional
            highest possible value for I (default is 1.0)
        Jmin : float, optional
            lowest possible value for J (default is 0.0)
        Jmax : float, optional
            highest possible value for J (default is 1.0)
        Pmin : float, optional
            lowest possible value for P (default is 1.0)
        Pmax : float, optional
            highest possible value for P (default is INFINITY)
        resolveIncomparability(rJ:RangeJ)
            resolve incomparability
        increasePminJ(rJ:RangeJ)
            increase the Pmin value if possible (with J range) (if not, call resolveConflict())
        """
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
        """Return the current state of the search

        Returns
        -------
        tuple of float
            the results of the search, i.e. (Imin, Imax, Jmin, Jmax, Pmin, Pmax)
        """
        return (self.Imin, self.Imax, self.Jmin, self.Jmax, self.Pmin, self.Pmax)


    def addPair(self, rI:RangeI, rJ:RangeJ, preference:int):
        """Add a pair of I range and J range and the related preference indicator

        Parameters
        ----------
        rI : RangeI
            a range of I values
        rJ : RangeJ
            a range of J values
        preference : int
            a preference indicator (1 for preference, 0 for indifference and -1 for incomparability)
        """
        self.listOfRangeI.append(rI)
        self.listOfRangeJ.append(rJ)
        self.listOfPreference.append(preference)


    def update(self):
        """Update the search state
        """
        pref = self.listOfPreference[-1]
        rI = self.listOfRangeI[-1]
        rJ = self.listOfRangeJ[-1]
        if pref == 0:
            # I >= [Imin, Imax] ; J >= I
            self.resolveIndifference(rI)
        elif pref == -1:
            # J <= [Jmin, Jmax] ; I <= J
            self.resolveIncomparability(rJ)
        elif pref == 1:
            # I <= [Imin, Imax] ; J >= [Jmin, Jmax] ; J >= I
            self.resolvePreference(rI, rJ)
    

    def resolveIndifference(self, rI:RangeI):
        """Resolve indifference

        I >= [i_min, i_max] ; J >= I

        we have a known [Imin, Imax] from previous pair(s) or strarting value ([0,1] in this case)

        And we have rI = [i_min, i_max] from the new pair

        we have to compare the 2 range and resolve any conflict

        So, we must have [Imin, Imax] >= [i_min, i_max]

        <=> Imin >= i_min and Imax >= i_max

        - If the 2 inequalities are satisfied, there's nothing to do ;
        - If Imax < i_min, there is a conflict ;
        - If Imax >= i_max but Imin < i_min, we can set Imin to i_min: Imin = i_min ;
        - If Imin >= i_min but Imax < i_max, we must reduce i_max to Imax, so increase Pmin ; if we can no longer increase Pmin, there is a conflict.
        - If Imin < i_min and Imax < i_max, we can combine the 2 solution above.
        
        If we can no longer use these solutions, there is a conflict.

        In case of conflict, we look for the values of the 3 parameters that will minimize the mean conflict in the least squares sense.

        Parameters
        ----------
        rI : RangeI
            a range of I values
        """
        
        if self.Imin >= rI.getValMin() and self.Imax >= rI.getValMax():
            # There is nothing to do
            return
        elif self.Imax < rI.getValMin():
            self.resolveConflict()
        elif self.Imax >= rI.getValMax() and self.Imin < rI.getValMin():
            self.Imin = rI.getValMin()
        elif self.Imin >= rI.getValMin() and self.Imax < rI.getValMax():
            self.increasePminI(rI)
        elif self.Imin < rI.getValMin() and self.Imax < rI.getValMax():
            self.Imin = rI.getValMin()
            self.increasePminI(rI)
        
        self.resolveConstraints(True) # We check that all constraints are still satisfied, and if not, we solve the constraints


    def increasePminI(self, rI:RangeI):
        """Increase the Pmin value if possible (with I range) (if not, call resolveConflict())
        
        rI.max = x + y/Pmin

        <=> Pmin = y/(rI.max - x)

        rI.max must be equal to Imax 

        Parameters
        ----------
        rI : RangeI
            a range of I values
        """
        x = rI.getX()
        y = rI.getY()
        if (self.Imax - x) <= 0:
            pmin = INFINITY
        else:
            pmin = y/(self.Imax - x)
        if pmin <= self.Pmax:
            self.Pmin = pmin
        else:
            self.resolveConflict()


    def resolveIncomparability(self, rJ:RangeJ):
        """Resolve incomparability

        J <= [Jmin, Jmax] ; I <= J

        we have a known [Imin, Imax] from previous pair(s) or strarting value ([0,1] in this case)

        And we have rJ = [j_min, j_max] from the new pair

        we have to compare the 2 range and resolve any conflict

        So, we must have [Jmin, Jmax] <= [j_min, j_max]

        <=> Jmin <= j_min and Jmax <= j_max

        - If the 2 inequalities are satisfied, there's nothing to do ;
        - If Jmin > j_max, there is a conflict ;
        - If Jmin <= j_min but Jmax > j_max, we can set Jmax to j_max: Jmax = j_max ;
        - If Jmax <= j_max but Jmin > j_min, we must increase j_min to Jmin, so increase Pmin ; if we can no longer increase Pmin, there is a conflict.
        - If Jmin > j_min and Jmax > j_max, we can combine the 2 solution above.
        
        If we can no longer use these solutions, there is a conflict.

        In case of conflict, we look for the values of the 3 parameters that will minimize the mean conflict in the least squares sense.

        Parameters
        ----------
        rJ : RangeJ
            a range of J values
        """

        if self.Jmin <= rJ.getValMin() and self.Jmax <= rJ.getValMax():
            # There is nothing to do
            return
        elif self.Jmin > rJ.getValMax():
            self.resolveConflict()
        elif self.Jmin <= rJ.getValMin() and self.Jmax > rJ.getValMax():
            self.Jmax = rJ.getValMax()
        elif self.Jmax <= rJ.getValMax() and self.Jmin > rJ.getValMin():
            self.increasePminJ(rJ)
        elif self.Jmin > rJ.getValMin() and self.Jmax > rJ.getValMax():
            self.Jmax = rJ.getValMax()
            self.increasePminJ(rJ)

        self.resolveConstraints(True) # We check that all constraints are still satisfied, and if not, we solve the constraints


    def increasePminJ(self, rJ:RangeJ):
        """Increase the Pmin value if possible (with J range) (if not, call resolveConflict())
        
        rJ.min = x - y/Pmin

        <=> Pmin = y/(x - rJ.min)

        rJ.min must be equal to Jmin 

        Parameters
        ----------
        rJ : RangeJ
            a range of J values
        """
        x = rJ.getX()
        y = rJ.getY()
        if (x - self.Jmin) <= 0:
            pmin = INFINITY
        else:
            pmin = y/(self.Jmin - x)
        if pmin <= self.Pmax:
            self.Pmin = pmin
        else:
            self.resolveConflict()


    def resolvePreference(self, rI:RangeI, rJ:RangeJ):
        """Resolve preference

        I <= [i_min, i_max] ; J >= [j_min, j_max] ; J >= I

        There are 2 parts in this resolution.

        1. I <= [i_min, i_max]

        we have a known [Imin, Imax] from previous pair(s) or strarting value ([0,1] in this case)

        And we have rI = [i_min, i_max] from the new pair

        we have to compare the 2 range and resolve any conflict

        So, we must have [Imin, Imax] <= [i_min, i_max]

        <=> Imin <= i_min and Imax <= i_max

        - If the 2 inequalities are satisfied, there's nothing to do ;
        - If Imin > i_max, there is a conflict ;
        - If Imin <= i_min but Imax > i_max, we can set Imax to i_max: Imax = i_max ;
        - If Imax <= i_max but Imin > i_min, we can increase i_min to Imin, so decrease Pmax ; if we can no longer decrease Pmax, there is a conflict.
        - If Imin > i_min and Imax > i_max, we can combine the 2 solution above.
        
        If we can no longer use these solutions, there is a conflict.


        2. J >= [j_min, j_max]

        we have a known [Imin, Imax] from previous pair(s) or strarting value ([0,1] in this case)

        And we have rJ = [j_min, j_max] from the new pair

        we have to compare the 2 range and resolve any conflict

        So, we must have [Jmin, Jmax] >= [j_min, j_max]

        <=> Jmin >= j_min and Jmax >= j_max

        - If the 2 inequalities are satisfied, there's nothing to do ;
        - If Jmax < j_min, there is a conflict ;
        - If Jmax >= j_max but Jmin < j_min, we can set Jmin to j_min: Jmin = j_min ;
        - If Jmin >= j_min but Jmax < j_max, we must decrease j_max to Jmax, so decrease Pmax ; if we can no longer increase Pmin, there is a conflict.
        - If Jmin < j_min and Jmax < j_max, we can combine the 2 solution above.
        
        If we can no longer use these solutions, there is a conflict.

        In case of conflict, we look for the values of the 3 parameters that will minimize the mean conflict in the least squares sense.

        Parameters
        ----------
        rI : RangeI
            a range of I values
        rJ : RangeJ
            a range of J values
        """

        # part 1
        self.ILErI(rI)

        # part 2
        self.JGErJ(rJ)

        self.resolveConstraints(True) # We check that all constraints are still satisfied, and if not, we solve the constraints


    def ILErI(self, rI:RangeI):
        """Resolve preference, part 1 : I <= rI

        I <= [i_min, i_max]

        we have a known [Imin, Imax] from previous pair(s) or strarting value ([0,1] in this case)

        And we have rI = [i_min, i_max] from the new pair

        we have to compare the 2 range and resolve any conflict

        So, we must have [Imin, Imax] <= [i_min, i_max]

        <=> Imin <= i_min and Imax <= i_max

        - If the 2 inequalities are satisfied, there's nothing to do ;
        - If Imin > i_max, there is a conflict ;
        - If Imin <= i_min but Imax > i_max, we can set Imax to i_max: Imax = i_max ;
        - If Imax <= i_max but Imin > i_min, we can increase i_min to Imin, so decrease Pmax ; if we can no longer decrease Pmax, there is a conflict.
        - If Imin > i_min and Imax > i_max, we can combine the 2 solution above. 
        
        If we can no longer use these solutions, there is a conflict.

        Parameters
        ----------
        rI : RangeI
            a range of I values
        """
        if self.Imin <= rI.getValMin() and self.Imax <= rI.getValMax():
            # There is nothing to do
            return
        elif self.Imin > rI.getValMax():
            self.resolveConflict()
        elif self.Imin <= rI.getValMin() and self.Imax > rI.getValMax():
            self.Imax = rI.getValMax()
        elif self.Imax <= rI.getValMax() and self.Imin > rI.getValMin():
            self.decreasePmaxI(rI)
        elif self.Imin > rI.getValMin() and self.Imax > rI.getValMax():
            self.Imax = rI.getValMax()
            self.decreasePmaxI(rI)

        
    def JGErJ(self, rJ:RangeJ):
        """Resolve preference, part 2 : J >= rJ

        J >= [j_min, j_max]

        we have a known [Imin, Imax] from previous pair(s) or strarting value ([0,1] in this case)

        And we have rJ = [j_min, j_max] from the new pair

        we have to compare the 2 range and resolve any conflict

        So, we must have [Jmin, Jmax] >= [j_min, j_max]

        <=> Jmin >= j_min and Jmax >= j_max

        - If the 2 inequalities are satisfied, there's nothing to do ;
        - If Jmax < j_min, there is a conflict ;
        - If Jmax >= j_max but Jmin < j_min, we can set Jmin to j_min: Jmin = j_min ;
        - If Jmin >= j_min but Jmax < j_max, we must decrease j_max to Jmax, so decrease Pmax ; if we can no longer increase Pmin, there is a conflict.
        - If Jmin < j_min and Jmax < j_max, we can combine the 2 solution above.
        
        If we can no longer use these solutions, there is a conflict.

        Parameters
        ----------
        rJ : RangeJ
            a range of J values
        """

        if self.Jmin >= rJ.getValMin() and self.Jmax >= rJ.getValMax():
            # There is nothing to do
            return
        elif self.Jmax < rJ.getValMin():
            self.resolveConflict()
        elif self.Jmax >= rJ.getValMax() and self.Jmin < rJ.getValMin():
            self.Jmin = rJ.getValMin()
        elif self.Jmin >= rJ.getValMin() and self.Jmax < rJ.getValMax():
            self.decreasePmaxJ(rJ)
        elif self.Jmin < rJ.getValMin() and self.Jmax < rJ.getValMax():
            self.Jmin = rJ.getValMin()
            self.decreasePmaxJ(rJ)


    def decreasePmaxI(self, rI:RangeI):
        """Decrease the Pmax value if possible (with I range) (if not, call resolveConflict())
        
        rI.min = x + y/Pmax

        <=> Pmax = y/(rI.min - x)

        rI.min must be equal to Imin

        Parameters
        ----------
        rI : RangeI
            a range of I values
        """
        x = rI.getX()
        y = rI.getY()
        if (self.Imin - x) <= 0:
            pmax = INFINITY
        else:
            pmax = y/(self.Imin - x)
        if pmax >= self.Pmin:
            self.Pmax = pmax
        else:
            self.resolveConflict()


    def decreasePmaxJ(self, rJ:RangeJ):
        """Decrease the Pmax value if possible (with J range) (if not, call resolveConflict())
        
        rJ.max = x - y/Pmax

        <=> Pmax = y/(x - rJ.max)

        rJ.max must be equal to Jmax

        Parameters
        ----------
        rJ : RangeJ
            a range of J values
        """
        x = rJ.getX()
        y = rJ.getY()
        if (x - self.Jmax) <= 0:
            pmax = INFINITY
        else:
            pmax = y/(self.Jmax - x)
        if pmax >= self.Pmin:
            self.Pmax = pmax
        else:
            self.resolveConflict()


    def resolveConstraints(self, s:bool):
        """Resolve the constraints

        Constaints: J >= I ; 0 <= J <= 1 ; 0 <= I <= 1 ; 1 <= P <= INFINITY

        <=> [Jmin, Jmax] >= [Imin, Imax]

        <=> Jmin >= Imin and Jmax >= Imax

        Parameters
        ----------
        s : bool
            indicator of whether resolveConflict() has already been performed or not (True if already performed, False otherwise)
        """
        parameters = (self.Imin, self.Imax, self.Jmin, self.Jmax)
        for param in parameters:
            if param < 0:
                param = 0.0
            if param > 1:
                param = 1.0
        if self.Pmin < 1:
            self.Pmin = 1.0
        if self.Pmax < 1:
            self.Pmax = 1.0

        if self.Imin > self.Imax:
            if s:
                self.resolveConflict()
                s = False
            else:
                self.Imin = (self.Imin + self.Imax)/2
                self.Imax = self.Imin
        if self.Jmin > self.Jmax:
            if s:
                self.resolveConflict()
                s = False
            else:
                self.Jmin = (self.Jmin + self.Jmax)/2
                self.Jmax = self.Jmin
        if self.Pmin > self.Pmax:
            if s:
                self.resolveConflict()
                s = False
            else:
                self.Pmin = (self.Pmin + self.Pmax)/2
                self.Pmax = self.Pmin
        
        if self.Jmin >= self.Imin and self.Jmax >= self.Imax:
            # There is nothing to do
            return
        elif self.Jmax < self.Imin:
            if s:
                self.resolveConflict()
            else:
                # another method than the average?
                # print("Jmax < Imin")
                self.Jmax = (self.Jmax + self.Imin)/2
                self.Imin = self.Jmax
        elif self.Jmin < self.Imin and self.Jmax >= self.Imax:
            self.Jmin = self.Imin
        elif self.Jmin >= self.Imin and self.Jmax < self.Imax:
            self.Imax = self.Jmax
        elif self.Jmin < self.Imin and self.Jmax < self.Imax:
            self.Jmin = self.Imin
            self.Imax = self.Jmax


    def resolveConflict(self):
        """Resolve conflict
        
        we look for the values of the 3 parameters that will minimize the mean conflict in the least squares sense

        we use a hill climbing algorithm
        
        We are certain of finding the optimum value of P thanks to the simple aspect of the optimality function: 
        there is one and only one optimum
        """
        almostFound = False
        bestI = None
        bestJ = None
        avgFitness = INFINITY
        p = 1.0
        while p <= INFINITY:
            avgI, avgJ = self.averageIandJ(p)
            fitI, fitJ = self.fitnessIandJ(p, avgI, avgJ)
            fit = sqrt(fitI**2 + fitJ**2)
            if fit < avgFitness:
                avgFitness = fit
                bestI = avgI
                bestJ = avgJ
            elif fit > avgFitness and not almostFound:
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
            
            if p > 100.0:
                p = INFINITY
                avgI, avgJ = self.averageIandJ(p)
                fitI, fitJ = self.fitnessIandJ(p, avgI, avgJ)
                fit = sqrt(fitI**2 + fitJ**2)
                if fit < avgFitness:
                    avgFitness = fit
                    bestI = avgI
                    bestJ = avgJ
                elif fit > avgFitness:
                    p = 100.0
                break

        self.Imax = bestI
        self.Imin = bestI
        self.Jmin = bestJ
        self.Jmax = bestJ
        self.Pmin = p
        self.Pmax = p

        self.resolveConstraints(False)


    def averageIandJ(self, p:float):
        """Compute the average value of I and J for a P value p

        Parameters
        ----------
        p : float
            the value of the parameter P

        Returns
        -------
        tuple of float
            (avgI, avgJ), the average of I and the average of J
        """
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
        """Compute the fitness of avgI and avgJ for a P value p

        Parameters
        ----------
        p : float
            the value of the parameter P
        avgI : float
            the average of I
        avgJ : float
            the average of J
        
        Returns
        -------
        float
            (fitI, fitJ), the fitness of avgI and the fitness of avgJ
        """
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