from customtkinter import IntVar
from Models.PrometheeGamma import PrometheeGamma
from Models.HelpForParametersTabModels.Range.Range import Range
from Models.HelpForParametersTabModels.Range.RangeI import RangeI
from Models.HelpForParametersTabModels.Range.RangeJ import RangeJ
import random
from Models.HelpForParametersTabModels.Search.Search import Search

class PreferenceLearning:
    def __init__(self, master, prometheeGamma:PrometheeGamma) -> None:
        self.prometheeGamma = prometheeGamma
        self.master = master
        self.alternatives = []
        
        # Init values
        self.Irange = Range(0.0, 1.0)
        self.Jrange = Range(0.0, 1.0)
        self.Prange = Range(1.0, 100.0)
        self.questions = []
        """
        [(a1, a2, preference), (a1, a2, preference), ... ]
        """

        self.listOfPairs = []
        """
        [(a1, a2), (a1, a2), ... ]
        """
        self.listofPossibleThresholds = []
        self.search = Search()

    
    def setAlternatives(self, alternatives:list):
        self.alternatives = alternatives


    def selectFirstQuestion(self):
        self.questions.clear()
        self.listOfPairs.clear()
        while True:
            a1 = random.choice(self.alternatives)
            a2 = random.choice(self.alternatives)
            if a1 != a2:
                self.listOfPairs.append((a1, a2))
                break
        question = (a1, a2, IntVar(master=self.master, value=5))
        self.questions.append(question)
        self.itSearch(True)
        return question
    

    def selectNextQuestion(self):
        # TODO ? question choisie non aléatoirement

        while True:
            a1 = random.choice(self.alternatives)
            a2 = random.choice(self.alternatives)
            if a1 != a2 and ((a1, a2) not in self.listOfPairs) and ((a2, a1) not in self.listOfPairs):
                self.listOfPairs.append((a1, a2))
                break
        question = (a1, a2, IntVar(master=self.master, value=5))
        self.questions.append(question)
        self.itSearch(False)
        return question
    

    def itSearch(self, rst:bool) -> None:
        if rst:
            self.search = Search()
            for q in self.questions:
                (rI, rJ, p) = self.computeRangeOfThresholdsForOneQuestion(q)
                self.search.addPair(rI, rJ, p)
                self.search.update()
        else:
            (rI, rJ, p) = self.computeRangeOfThresholdsForOneQuestion(self.questions[-1])
            self.search.addPair(rI, rJ, p)
            self.search.update()
    

    def getResults(self):
        return self.search.getState()
    

    def computeRangeOfThresholdsForOneQuestion(self, question:tuple):
        (a1_t, a2_t, pref) = question
        a1 = self.alternatives.index(a1_t)
        a2 = self.alternatives.index(a2_t)
        preference = pref.get()
        if preference == 2:
            preference = 1 # Because of abs, max and min, it's all the same
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