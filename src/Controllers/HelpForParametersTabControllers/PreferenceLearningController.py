from Models.HelpForParametersTabModels.preferenceLearning import PreferenceLearning
from Views.HelpForParametersTabViews.PreferenceLearningView import PreferenceLearningView

from Models.DataTabModel import DataTabModel
from Models.PrometheeGamma import PrometheeGamma

import tkinter.messagebox
from math import comb

MAX_NUMBER_OF_QUESTIONS = 10

class PreferenceLearningController(PreferenceLearningView.ViewListener):

    class Listener:
        def apply(self, results):
            pass
        def reset(self):
            pass


    def __init__(self, master, dataTabModel:DataTabModel, prometheeGamma:PrometheeGamma) -> None:
        self.master = master
        self.preferenceLearningView = PreferenceLearningView(self.master)
        self.preferenceLearningView.setListener(self)
        self.dataTabModel = dataTabModel
        self.prometheeGamma = prometheeGamma
        self.preferenceLearning = PreferenceLearning(master, self.prometheeGamma)
        self.questions = []
        self.results = None
        self.listener = None
        self.maxNumberOfQuestions = MAX_NUMBER_OF_QUESTIONS



    def setListener(self, l:Listener):
        """Set the listener

        Parameters
        ----------
        l : Listener
            the new listener
        """
        self.listener = l


    def showView(self):
        """Show the view
        """
        self.preferenceLearningView.show()


    def confirm(self):
        self.results = self.preferenceLearning.getResults()
        self.preferenceLearningView.showResults(self.results)


    def apply(self):
        (Imin, Imax, Jmin, Jmax, Pmin, Pmax) = self.results
        i = None
        j = None
        p = None
        if Imin == Imax:
            i = Imin
        else:
            if Imax <= Jmax:
                i = Imax
            elif Imin <= Jmax:
                i = Jmax
            else:
                # error ?
                i = Imin
        if Jmin == Jmax:
            j = Jmin
        else:
            if Jmin >= i:
                j = Jmin
            elif Jmax >= i:
                j = i
            else:
                # error ?
                j = Jmax
        if Pmin == Pmax:
            p = Pmin
        else:
            p = (Pmin + Pmax)/2
        self.listener.apply((i, j, p))


    def next(self):
        self.results = self.preferenceLearning.getResults()
        self.preferenceLearningView.showResults(self.results)
        question = self.preferenceLearning.selectNextQuestion()
        self.questions.append(question)
        self.preferenceLearningView.showNextQuestion(question, len(self.questions) >= self.maxNumberOfQuestions)


    def selectFirstQuestion(self):
        self.maxNumberOfQuestions = MAX_NUMBER_OF_QUESTIONS
        nbAlter = self.dataTabModel.getNumberOfAlternatives()
        maxQuestions = comb(nbAlter, 2)
        if self.maxNumberOfQuestions > maxQuestions:
            self.maxNumberOfQuestions = maxQuestions
        if nbAlter < 2:
            tkinter.messagebox.showerror(title="Not enought alternatives", message="There are not enough alternatives in the model to generate a question")
        else:
            alter = []
            for i in range(nbAlter):
                a = self.dataTabModel.getAlternative(i)
                alter.append(a)
            self.preferenceLearning.setAlternatives(alter)
            question = self.preferenceLearning.selectFirstQuestion()
            self.questions.append(question)
            self.preferenceLearningView.showNextQuestion(question, len(self.questions) >= self.maxNumberOfQuestions)


    def showQuestions(self):
        if self.prometheeGamma.isComputed():
            self.questions.clear()
            self.selectFirstQuestion()
        else:
            tkinter.messagebox.showerror(title="No results", message='The results of the promethee gamma method are required for the algorithm. Please click on the "Obtain results" button in the "result tab".')


    def recomputeResults(self):
        self.preferenceLearning.itSearch(True)


    def cancel(self):
        self.preferenceLearningView.resetView()
        self.listener.reset()