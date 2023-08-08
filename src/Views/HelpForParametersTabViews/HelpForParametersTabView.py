from customtkinter import (CTkLabel, CTkButton, CTkRadioButton, IntVar, CTkFrame, CTkCanvas, CTkScrollbar, CTkScrollableFrame)
from Models.Alternative import Alternative
from Views.HelpForParametersTabViews.QuestionsTabView import QuestionsTabView

class HelpForParametersTabView(QuestionsTabView.Listener):
    """
    A class to display the content of the helpForParameters tab

    Attributes
    ----------
    master : CTkFrame
        the master frame
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

        def showQuestions(self):
            pass
        def confirm(self):
            pass
        def apply(self):
            pass
        def next(self):
            pass
        def recomputeResults(self):
            pass
        def showPreferenceLearning(self):
            pass
        def showCustom(self):
            pass
        def cancel(self):
            pass

    def __init__(self, master) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        """

        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.questionsTabView = None
        startText = "Please choose a method. The preference learning button will launch the application's built-in preference learning algorithm. The custom button will load the method you've previously integrated into the source code in the Custom class."
        self.startLabel = CTkLabel(master=self.master, text=startText, text_color="#000000", wraplength=580)
        self.preferenceLearningButton = CTkButton(master=self.master, text="Preference learning", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.startPreferenceLearning)
        self.customButton = CTkButton(master=self.master, text="Custom", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.startCustom)
        explanation = "In order to help determine the 3 parameters introduced by the PROMETHEE Gamma method, it is necessary to know your opinion on a small number of pairwise comparisons between alternatives. Please answer the questions below."
        self.explanationLabel = CTkLabel(master=self.master, text=explanation, text_color="#000000", wraplength=580)
        self.generateButton = CTkButton(master=self.master, text="Generate questions", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.generateQuestions)
        self.confirmButton = CTkButton(master=self.master, text="Confirm", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.confirm)
        self.nextButton = CTkButton(master=self.master, text="Next", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.next)
        self.Ilabel = CTkLabel(master=self.master, text="I = 0 - 1", text_color="#000000")
        self.Jlabel = CTkLabel(master=self.master, text="J = 0 - 1", text_color="#000000")
        self.Plabel = CTkLabel(master=self.master, text="P = 1 - infinity", text_color="#000000")
        self.applyButton = CTkButton(master=self.master, text="Use results in result tab", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.apply)
        self.cancelButton = CTkButton(master=self.master, text="Cancel", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.cancel)
        self.row = 0
        self.endCtrl = False
        self.listener = None


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
        self.startLabel.grid(row=self.row, column=0, columnspan=2, padx=10, pady=(20, 0), sticky="n")
        self.row +=1
        self.preferenceLearningButton.grid(row=self.row, column=0, padx=10, pady=(20, 0), sticky="ne")
        self.customButton.grid(row=self.row, column=1, padx=10, pady=(20, 0), sticky="nw")


    def hideStarter(self):
        """Hide the starter
        """
        self.row -= 1
        self.startLabel.grid_forget()
        self.preferenceLearningButton.grid_forget()
        self.customButton.grid_forget()


    def showPreferenceLearning(self):
        """Show the preference learning components
        """
        self.explanationLabel.grid(row=self.row, column=0, padx=10, pady=(10, 0), sticky="n")
        self.row +=1
        self.generateButton.grid(row=self.row, column=0, padx=10, pady=(10, 0), sticky="n")
        self.row +=1
        self.Ilabel.grid(row=self.row, column=0, padx=10, pady=(10, 0), sticky="n")
        self.row +=1
        self.Jlabel.grid(row=self.row, column=0, padx=10, pady=(1, 0), sticky="n")
        self.row +=1
        self.Plabel.grid(row=self.row, column=0, padx=10, pady=(1, 0), sticky="n")
        self.row +=1
        self.cancelButton.grid(row=10, column=0, padx=10, pady=(10,0), sticky="n")


    def showCustom(self):
        """Show the custom components
        """
        # TODO
        self.cancelButton.grid(row=10, column=0, padx=10, pady=(10,0), sticky="n")


    def startPreferenceLearning(self):
        """Start the preference learning method
        """
        self.listener.showPreferenceLearning()


    def startCustom(self):
        """Start the custom method
        """
        self.listener.showCustom()


    def showNextQuestion(self, question:tuple, end:bool) -> None:
        """Show the next question of preference learning algorithm

        Parameters
        ----------
        question : Tuple(Alternative, Alternative, IntVar)
            the "question", i.e. the two alternatives that will be compared and the value of preference (in the IntVar): 
            0 for indifference ; 1 for preference ; -1 for incomparability
        end : bool
            a boolean to indicate last question (True if it is the last question, False otherwise)
        """
        self.questionsTabView.addQuestion(question)
        if end:
            self.confirmButton.grid(row=self.row, column=0, padx=10, pady=(15, 0), sticky="n")
            self.row += 1
        else :
            self.nextButton.grid(row=self.row, column=0, padx=10, pady=(15, 0), sticky="n")
            self.row += 1


    def next(self):
        """Handle click on nextButton
        """
        self.nextButton.grid_forget()
        self.row -= 1
        self.listener.next()


    def confirm(self):
        """Handle click on confirmButton
        """
        self.endCtrl = True
        self.confirmButton.grid_forget()
        self.row -= 1
        self.applyButton.grid(row=self.row, column=0, padx=10, pady=(15, 0), sticky="n")
        self.row += 1
        self.listener.confirm()


    def apply(self):
        """Handle click on applyButton
        """
        self.listener.apply()


    def resetResults(self):
        """Reset the results (reset labels)
        """
        self.Ilabel.configure(text="I = 0 - 1")
        self.Jlabel.configure(text="J = 0 - 1")
        self.Plabel.configure(text="P = 1 - infinity")
        self.Ilabel.update()
        self.Jlabel.update()
        self.Plabel.update()
        


    def generateQuestions(self):
        """Reset algorithm and (re)start it
        """
        if self.endCtrl:
            self.applyButton.grid_forget()
            self.row -= 1
            self.endCtrl = False
        if self.questionsTabView != None:
            self.questionsTabView.grid_forget()
            self.resetResults()
            self.row = 5
            self.questionsTabView.destroy()
        self.questionsTabView = QuestionsTabView(master=self.master, fg_color="#ffffff")
        self.questionsTabView.setListener(self)
        self.confirmButton.grid_forget()
        #if self.resultsLabel != None:
        #    self.resultsLabel.destroy()
        #self.applyButton.grid_forget()
        self.questionsTabView.grid(row=self.row, column=0, padx=10, pady=(10, 0), sticky="n")
        self.row +=1
        self.listener.showQuestions()


    def showResults(self, results:tuple):
        """Show the results in labels (ILabel, JLabel and PLabel)

        Parameters
        ----------
        results : tuple[DoubleVar, DoubleVar, DoubleVar, DoubleVar, DoubleVar, DoubleVar]
            results = (Imin, Imax, Jmin, Jmax, Pmin, Pmax) ; these are the resulting values of preference learning algorithm
        """
        (Imin, Imax, Jmin, Jmax, Pmin, Pmax) = results
        if Imin == Imax:
            Itext = "I = " + str(Imin)
        else:
            Itext = "I = " + str(Imin) + " - " + str(Imax)
        if Jmin == Jmax:
            Jtext = "J = " + str(Jmin)
        else:
            Jtext = "J = " + str(Jmin) + " - " + str(Jmax)
        if Pmin == Pmax:
            if Pmin > 100:
                Ptext = "P = infinity"
            else:
                Ptext = "P = " + str(Pmin)
        else:
            Ptext = "P = " + str(Pmin) + " - "
            if Pmax > 100.0:
                Ptext += "infinity"
            else:
                Ptext += str(Pmax)
        self.Ilabel.configure(text=Itext)
        self.Jlabel.configure(text=Jtext)
        self.Plabel.configure(text=Ptext)
        self.Ilabel.update()
        self.Jlabel.update()
        self.Plabel.update()


    def updateInQCM(self):
        """Handle event in questions
        """
        self.listener.recomputeResults()
        if self.endCtrl:
            self.applyButton.grid_forget()
            self.row -= 1
            self.confirmButton.grid(row=self.row, column=0, padx=10, pady=(15, 0), sticky="n")
            self.row += 1


    def cancel(self):
        """Handle click on cancelButton
        """
        self.listener.cancel()


    def resetView(self):
        """Reset the view, i.e. forget all widget displayed and restart
        """
        for w in self.master.winfo_children():
            w.grid_forget()
        self.row = 0
        self.endCtrl = False
        self.resetResults()
        self.show()
