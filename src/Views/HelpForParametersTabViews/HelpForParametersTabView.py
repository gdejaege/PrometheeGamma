from customtkinter import (CTkLabel, CTkButton, CTkRadioButton, IntVar, CTkFrame, CTkCanvas, CTkScrollbar, CTkScrollableFrame)
from Models.Alternative import Alternative
from Views.HelpForParametersTabViews.QuestionsTabView import QuestionsTabView
from Resources.ScrollableFrame import ScrollableFrame

class HelpForParametersTabView(QuestionsTabView.Listener):
    """
    A class to display the content of the helpForParameters tab

    Attributes
    ----------
    master : CTkFrame
        the parent master frame
    questionsTabView : CTkTabView
        the tabView that will contain the questions
    startLabel : CTkLabel
        a label to display the strarting Text
    preferenceLearningButton : CTkButton
        a button to select the built-in preferenceLearning algorithm
    explanationLabel : CTkLabel
        a label to display the explanation text for preference learning algorithm
    generateButton : CTkButton
        a button to generate questions for preference learning algorithm
    confirmButton : CTkButton
        a button to confirm the answers
    nextButton : CTkButton
        a button to generate the next question
    Ilabel : CTkLabel
        a label to display the value of the indifference parameter
    Jlabel : CTkLabel
        a label to display the value of the incomparability parameter
    Plabel : CTkLabel
        a label to display the value of the preference parameter
    applyButton : CTkButton
        a button to apply the results in result tab
    cancelButton : CTkButton
        a button to cancel selection of a method
    row : int
        the row for positionning elements with grid method
    endCtrl : bool
        control variable to keep in memory the state of the algorithm (ended or not ended)
    listener : ViewListener
        the listener of this view

    Methods
    -------
    setListener(l:ViewListener)
        set the listener
    show()
        show the view
    hideStarter()
        hide the starter
    showPreferenceLearning()
        show the preference learning components
    showCustom()
        show the custom components
    startPreferenceLearning()
        start the preference learning method
    startCustom()
        start the custom method
    showNextQuestion(question:tuple, end:bool)
        show the next question of preference learning algorithm
    next()
        handle click on nextButton
    confirm()
        handle click on confirmButton
    apply()
        handle click on applyButton
    resetResults()
        reset the results (reset labels)
    generateQuestions()
        reset algorithm and (re)start it
    showResults(results:tuple)
        show the results in labels (ILabel, JLabel and PLabel)
    updateInQCM()
        handle event in questions
    cancel()
        handle click on cancelButton
    resetView()
        reset the view, i.e. forget all widget displayed and restart
    """

    class ViewListener:
        """
        An interface for the listener of this view
        """

        def showPreferenceLearning(self):
            pass
        def showCustom(self):
            pass


    def __init__(self, master) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the parent master frame
        """
        self.sframe = ScrollableFrame(master)
        self.master = self.sframe.frame()
        startText = "Please choose a method. The preference learning button will launch the application's built-in preference learning algorithm. The custom button will load the Custom module."
        self.startLabel = CTkLabel(master=self.master, text=startText, text_color="#000000", wraplength=580)
        self.preferenceLearningButton = CTkButton(master=self.master, text="Preference learning", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.startPreferenceLearning)
        self.customButton = CTkButton(master=self.master, text="Custom", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.startCustom)
        self.listener = None
        self.row = 0


    def setListener(self, l:ViewListener):
        """Set the listener

        Parameters
        ----------
        l : ViewListener
            the new listener
        """
        self.listener = l


    def show(self):
        """Show the view
        """
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.startLabel.grid(row=self.row, column=0, columnspan=2, padx=10, pady=(20, 0), sticky="n")
        self.row +=1
        self.preferenceLearningButton.grid(row=self.row, column=0, padx=10, pady=(20, 0), sticky="ne")
        self.customButton.grid(row=self.row, column=1, padx=10, pady=(20, 0), sticky="nw")


    def hide(self):
        """Hide the view
        """
        self.row -= 1
        self.startLabel.grid_forget()
        self.preferenceLearningButton.grid_forget()
        self.customButton.grid_forget()
        self.master.grid_columnconfigure(1, weight=0)


    def startPreferenceLearning(self):
        """Start the preference learning method
        """
        self.listener.showPreferenceLearning()


    def startCustom(self):
        """Start the custom method
        """
        self.listener.showCustom()
