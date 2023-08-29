import tkinter.messagebox as msg
from math import comb

from Views.HelpForParametersTabViews.PreferenceLearningView import PreferenceLearningView
from Models.HelpForParametersTabModels.preferenceLearning import PreferenceLearning
from Models.DataTabModels.DataTabModel import DataTabModel
from Models.PrometheeGamma import PrometheeGamma

# Constants
MAX_NUMBER_OF_QUESTIONS = 10
"""The maximum number of questions that can be asked of the user
"""


class PreferenceLearningController(PreferenceLearningView.ViewListener):
    """
    A class to control the preference learning algorithm

    Attributes
    ----------
    dataTabModel : DataTabModel
        the model that keep input data in memory
    prometheeGamma : PrometheeGamma
        the model for PROMETHEE Gamma method
    preferenceLearningView : PreferenceLearningView
        the preference learning view
    questions : list
        the list of questions asked of the user
    listener : PreferenceLearningController.Listener
        the listener of this class

    Methods
    -------
    """

    class Listener:
        """
        An interface for the listener of this class

        Methods
        -------
        """
        def apply(self, results):
            """use the results obtained from preference learning in the result tab

            Parameters
            ----------
            results : tuple of float
                (I, J, P), the values of the 3 parameters of PROMETHEE Gamma method
            """
            pass

        def reset(self):
            """reset the tab
            """
            pass


    def __init__(self, master, dataTabModel:DataTabModel, prometheeGamma:PrometheeGamma) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        dataTabModel : DataTabModel
            the model that keep input data in memory
        prometheeGamma : PrometheeGamma
            the model for PROMETHEE Gamma method
        """
        self.dataTabModel = dataTabModel
        self.prometheeGamma = prometheeGamma
        self.preferenceLearningView = PreferenceLearningView(master)
        self.preferenceLearningView.setListener(self)
        self.preferenceLearning = PreferenceLearning(master, self.prometheeGamma)
        self.questions = []
        self.listener = None
        self.numberOfQuestions = MAX_NUMBER_OF_QUESTIONS


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
        """Confirm the answers to questions if all questions have an answer. Otherwise, show an error message to the user
        """
        if self.questions[-1][2].get() == 5:
            msg.showerror(title="No answer", message="Please select an answer")
        else:
            self.preferenceLearningView.showApplyCancel()
            results = self.preferenceLearning.getResults()
            self.preferenceLearningView.showResults(results)


    def apply(self):
        """Format the results, i.e. reduce range to a single value and transmit them for use in the results tab
        """
        (Imin, Imax, Jmin, Jmax, Pmin, Pmax) = self.preferenceLearning.getResults()
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
                i = Imin
        if Jmin == Jmax:
            j = Jmin
        else:
            if Jmin >= i:
                j = Jmin
            elif Jmax >= i:
                j = i
            else:
                j = Jmax
        if Pmin == Pmax:
            p = Pmin
        else:
            p = (Pmin + Pmax)/2
        self.listener.apply((i, j, p))


    def next(self):
        """Show the next question if the current question has an answer. Otherwise show an error message to the user
        """
        if self.questions[-1][2].get() == 5:
            msg.showerror(title="No answer", message="Please select an answer")
        else:
            results = self.preferenceLearning.getResults()
            self.preferenceLearningView.showResults(results)
            question = self.preferenceLearning.selectNextQuestion()
            self.questions.append(question)
            self.preferenceLearningView.showNextQuestion(question, self.dataTabModel.getCriteriaNames())
            self.preferenceLearningView.showNextConfirm(len(self.questions) >= self.numberOfQuestions)


    def selectFirstQuestion(self):
        """Select the first question. If no question can be created, show an error message to the user
        """
        self.numberOfQuestions = MAX_NUMBER_OF_QUESTIONS
        nbAlter = self.dataTabModel.getNumberOfAlternatives()
        maxQuestions = comb(nbAlter, 2)
        if self.numberOfQuestions > maxQuestions:
            self.numberOfQuestions = maxQuestions
        if nbAlter < 2:
            msg.showerror(title="Not enought alternatives", message="There are not enough alternatives in the model to generate a question")
        else:
            alter = []
            for i in range(nbAlter):
                a = self.dataTabModel.getAlternative(i)
                alter.append(a)
            self.preferenceLearning.setAlternatives(alter)
            question = self.preferenceLearning.selectFirstQuestion()
            self.questions.append(question)
            self.preferenceLearningView.showNextQuestion(question, self.dataTabModel.getCriteriaNames())
            self.preferenceLearningView.showNextConfirm(len(self.questions) >= self.numberOfQuestions)


    def generate(self):
        """Generate the questions. If it is not possible, show an error message to the user
        """
        if self.prometheeGamma.isComputed():
            self.preferenceLearningView.resetResults()
            self.preferenceLearningView.createQuestionsTab()
            self.questions.clear()
            self.selectFirstQuestion()
        else:
            msg.showerror(title="No results", message='The results of the promethee gamma method are required for the algorithm. Please click on the "Obtain results" button in the "result tab".')


    def updateInmcq(self):
        """Update restults if a change occurs in answer
        """
        self.recomputeResults()
        self.preferenceLearningView.showNextConfirm(len(self.questions) >= self.numberOfQuestions)


    def recomputeResults(self):
        """Recompute the results and show them
        """
        self.preferenceLearning.itSearch(True)
        results = self.preferenceLearning.getResults()
        self.preferenceLearningView.showResults(results)


    def cancel(self):
        """Cancel confirmation
        """
        self.preferenceLearningView.showNextConfirm(len(self.questions) >= self.numberOfQuestions)


    def quit(self):
        """Quit the preference learning view
        """
        self.preferenceLearningView.resetView()
        self.listener.reset()