from customtkinter import IntVar
import random

from Models.PrometheeGamma import PrometheeGamma
from Models.HelpForParametersTabModels.Range.Range import Range
from Models.HelpForParametersTabModels.Range.RangeI import RangeI
from Models.HelpForParametersTabModels.Range.RangeJ import RangeJ
from Models.HelpForParametersTabModels.Search.Search import Search


class PreferenceLearning:
    """
    A class to implement a preference learning algorithm

    This algorithm is based on a small number of pairwise comparisons submitted to the user. 
    Based on the user's responses, an iterative search determines the possible values for the 3 parameters specific to the PROMETHEE Gamma method.
    
    Attributes
    ----------
    prometheeGamma : PrometheeGamma
        the PROMETHEE Gamma model
    master : CTkFrame
        the master frame
    alternatives : list of Alternative
        the list of all laternatives
    Irange : Range
        a range of value for parameter I
    Jrange : Range
        a range of value for parameter J
    Prange : Range
        a range of value for parameter P
    questions : list
        a list of peer comparisons
    listOfPairs : list of tuple of Aternative
        a list of pair of alternatives
    search : Search
        the instance of class for search method
    """


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
        self.search = Search()

    
    def setAlternatives(self, alternatives:list):
        """Set the alternatives list

        Parameters
        ----------
        alternatives : list of Alternative
            a list of alternatives
        """
        self.alternatives = alternatives


    def selectFirstQuestion(self):
        """Select the first peer comparison at random

        Returns
        -------
        tuple of Alternative and IntVar
            a peer comparison (the 2 alternatives, and the value for relation between the 2 alternatives)
        """
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
        """Select a non already selected peer comparison at random

        Returns
        -------
        tuple of Alternative and IntVar
            a peer comparison (the 2 alternatives, and the value for relation between the 2 alternatives)
        """
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
        """Make an iteration of iterative search or or restart the whole search if rst is True

        Parameters
        ----------
        rst : bool
            if True, restart the search, otherwise make an iteration of iterative search
        """
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
        """Return the results of the search

        Returns
        -------
        tuple of float
            the results of the search, i.e. (Imin, Imax, Jmin, Jmax, Pmin, Pmax)
        """
        return self.search.getState()
    

    def computeRangeOfThresholdsForOneQuestion(self, question:tuple):
        """Compute a range of possible thresholds for one peer comparison

        Parameters
        ----------
        question : tuple
            a peer comparison
        """
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