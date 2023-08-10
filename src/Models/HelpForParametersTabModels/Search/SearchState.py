from math import sqrt
from Models.HelpForParametersTabModels.Range.RangeI import RangeI
from Models.HelpForParametersTabModels.Range.RangeJ import RangeJ

INFINITY = 1000000000


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


    def addPair(self, rI:RangeI, rJ:RangeJ, preference:int):
        self.listOfRangeI.append(rI)
        self.listOfRangeJ.append(rJ)
        self.listOfPreference.append(preference)


    def update(self):
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
        - If Imin >= i_min but Imax < i_max, we must reduce i_max to Imax, so increase Pmin.
        If we can no longer increase Pmin, there is a conflict.
        - If Imin < i_min and Imax < i_max, we can combine the 2 solution above.
        If we can no longer use these solutions, there is a conflict.

        In case of conflict, we look for the values of the 3 parameters that will minimize the mean conflict in the least squares sense.
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
        """
        
        rI.max = x + y/Pmin

        <=> Pmin = y/(rI.max - x)

        rI.max must be equal to Imax 
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
        - If Jmax <= j_max but Jmin > j_min, we must increase j_min to Jmin, so increase Pmin.
        If we can no longer increase Pmin, there is a conflict.
        - If Jmin > j_min and Jmax > j_max, we can combine the 2 solution above.
        If we can no longer use these solutions, there is a conflict.

        In case of conflict, we look for the values of the 3 parameters that will minimize the mean conflict in the least squares sense.
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
        """
        
        rJ.min = x - y/Pmin

        <=> Pmin = y/(x - rJ.min)

        rJ.min must be equal to Jmin 
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
        """
        I <= [Imin, Imax] ; J >= [Jmin, Jmax] ; J >= I

        There are 2 parts in this resolution.

        1. I <= [Imin, Imax]

        we have a known [Imin, Imax] from previous pair(s) or strarting value ([0,1] in this case)

        And we have rI = [i_min, i_max] from the new pair

        we have to compare the 2 range and resolve any conflict

        So, we must have [Imin, Imax] <= [i_min, i_max]

        <=> Imin <= i_min and Imax <= i_max

        - If the 2 inequalities are satisfied, there's nothing to do ;
        - If Imin > i_max, there is a conflict ;
        - If Imin <= i_min but Imax > i_max, we can set Imax to i_max: Imax = i_max ;
        - If Imax <= i_max but Imin > i_min, we can increase i_min to Imin, so decrease Pmax  ;
        If we can no longer decrease Pmax, there is a conflict.
        - If Imin > i_min and Imax > i_max, we can combine the 2 solution above.
        If we can no longer use these solutions, there is a conflict.


        2. J >= [Jmin, Jmax]

        we have a known [Imin, Imax] from previous pair(s) or strarting value ([0,1] in this case)

        And we have rJ = [j_min, j_max] from the new pair

        we have to compare the 2 range and resolve any conflict

        So, we must have [Jmin, Jmax] >= [j_min, j_max]

        <=> Jmin >= j_min and Jmax >= j_max

        - If the 2 inequalities are satisfied, there's nothing to do ;
        - If Jmax < j_min, there is a conflict ;
        - If Jmax >= j_max but Jmin < j_min, we can set Jmin to j_min: Jmin = j_min ;
        - If Jmin >= j_min but Jmax < j_max, we must decrease j_max to Jmax, so decrease Pmax.
        If we can no longer increase Pmin, there is a conflict.
        - If Jmin < j_min and Jmax < j_max, we can combine the 2 solution above.
        If we can no longer use these solutions, there is a conflict.

        In case of conflict, we look for the values of the 3 parameters that will minimize the mean conflict in the least squares sense.
        """

        # part 1
        self.ILErI(rI)

        # part 2
        self.JGErJ(rJ)

        self.resolveConstraints(True) # We check that all constraints are still satisfied, and if not, we solve the constraints


    def ILErI(self, rI:RangeI):
        """
        I <= [Imin, Imax]

        we have a known [Imin, Imax] from previous pair(s) or strarting value ([0,1] in this case)

        And we have rI = [i_min, i_max] from the new pair

        we have to compare the 2 range and resolve any conflict

        So, we must have [Imin, Imax] <= [i_min, i_max]

        <=> Imin <= i_min and Imax <= i_max

        - If the 2 inequalities are satisfied, there's nothing to do ;
        - If Imin > i_max, there is a conflict ;
        - If Imin <= i_min but Imax > i_max, we can set Imax to i_max: Imax = i_max ;
        - If Imax <= i_max but Imin > i_min, we can increase i_min to Imin, so decrease Pmax  ;
        If we can no longer decrease Pmax, there is a conflict.
        - If Imin > i_min and Imax > i_max, we can combine the 2 solution above.
        If we can no longer use these solutions, there is a conflict.
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
        """
        J >= [Jmin, Jmax]

        we have a known [Imin, Imax] from previous pair(s) or strarting value ([0,1] in this case)

        And we have rJ = [j_min, j_max] from the new pair

        we have to compare the 2 range and resolve any conflict

        So, we must have [Jmin, Jmax] >= [j_min, j_max]

        <=> Jmin >= j_min and Jmax >= j_max

        - If the 2 inequalities are satisfied, there's nothing to do ;
        - If Jmax < j_min, there is a conflict ;
        - If Jmax >= j_max but Jmin < j_min, we can set Jmin to j_min: Jmin = j_min ;
        - If Jmin >= j_min but Jmax < j_max, we must decrease j_max to Jmax, so decrease Pmax.
        If we can no longer increase Pmin, there is a conflict.
        - If Jmin < j_min and Jmax < j_max, we can combine the 2 solution above.
        If we can no longer use these solutions, there is a conflict.
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
        """
        
        rI.min = x + y/Pmax

        <=> Pmax = y/(rI.min - x)

        rI.min must be equal to Imin
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
        """
        
        rJ.max = x - y/Pmax

        <=> Pmax = y/(x - rJ.max)

        rJ.max must be equal to Jmax
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
        """
        Constaints: J >= I ; 0 <= J <= 1 ; 0 <= I <= 1 ; 1 <= P <= INFINITY

        <=> [Jmin, Jmax] >= [Imin, Imax]

        <=> Jmin >= Imin and Jmax >= Imax
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