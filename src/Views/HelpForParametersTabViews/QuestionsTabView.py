from customtkinter import (CTkTabview, CTkLabel, CTkRadioButton, IntVar)
from Models.Alternative import Alternative

class QuestionsTabView(CTkTabview):
    """
    A class to display a tabView with question for preference learning algorithm

    Attributes
    ----------
    nb : int
        the number of questions (and of tabs too)
    masterList : list[CTkFrame]
        the list of tabs
    row : int
        the row of components, used by grid method
    listener : Listener
        the listener of the view
    
    Methods
    -------
    setListener(l:Listener)
        set the listener
    addTab()
        add a tab and set the focus on it
    addQuestion(question)
        add a question
    alternativeInLabel(master, a:Alternative)
        create a label for the alternative
    placeQuestionLabel(l0:CTkLabel, l1:CTkLabel)
        place questions labels in the tab (with grid)
    qcm(master, nameA1:str, nameA2:str, value:IntVar)
        create a qcm with radioButton
    placeQCM(qcm)
        place qcm in the tab (with grid)
    radioButtonEvent()
        handle radioButton event (answer change)
    """

    class Listener:
        def updateInQCM(self):
            pass


    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.nb = 0
        self.masterList = []
        self.row = 0
        self.listener = None


    def setListener(self, l:Listener):
        """Set the listener

        Parameters
        ----------
        l : Listener
            the new listener
        """
        self.listener = l


    def addTab(self):
        """Add a tab and set the focus on it
        """
        self.nb += 1
        name = "Question " + str(self.nb)
        self.add(name)
        self.tab(name).grid_columnconfigure(0, weight=1)
        self.masterList.append(self.tab(name))
        self.set(name)


    def addQuestion(self, question):
        """Add a question

        Parameters
        ----------
        question : tuple[Alternative, Alternative, IntVar]
            the "question" to add, i.e. the two alternatives that will be compared and the value of preference (in the IntVar): 
            0 for indifference ; 1 for preference ; -1 for incomparability
        """
        self.addTab()
        self.row = 0
        l0 = self.alternativeInLabel(self.masterList[-1], question[0])
        l1 = self.alternativeInLabel(self.masterList[-1], question[1])
        self.placeQuestionLabel(l0, l1)
        self.qcm(self.masterList[-1], question[0].getName_str(), question[1].getName_str(), question[2])


    def alternativeInLabel(self, master, a:Alternative) -> CTkLabel:
        """Create a label for the alternative

        master : CTkFrame
            the tab where place the new label
        a : Alternative
            the alternative
        """
        textLabel = a.getName_str() + ":"
        for i in range(a.getSize()):
            textLabel += "   " + str(a.getEvaluation_float(i))
        return CTkLabel(master=master, text_color="#000000", text=textLabel)
    

    def placeQuestionLabel(self, l0:CTkLabel, l1:CTkLabel):
        """Place questions labels in the tab (with grid)

        Parameters
        ----------
        l0 : CTkLabel
            the first label to place
        l1 : CTkLabel
            the second label to place
        """
        l0.grid(row=self.row, column=0, padx=10, pady=(20, 0), sticky="n")
        self.row +=1
        l1.grid(row=self.row, column=0, padx=10, pady=(0, 0), sticky="n")
        self.row +=1
        #self.questionLabels.append((l0, l1))


    def qcm(self, master, nameA1:str, nameA2:str, value:IntVar) -> None:
        """Create a qcm with radioButton

        Parameters
        ----------
        master : CTkFrame
            the tab where place qcm
        nameA1 : str
            the name of the first alternative of the question
        nameA2 : str
            the name of the second alternative of the question
        value : IntVar
            the radioButton variable thath will contain the answer
        """
        r1 = CTkRadioButton(master=master, text=nameA1 + " I " + nameA2, text_color="#000000", command=self.radioButtonEvent, variable=value, value=0)
        r2 = CTkRadioButton(master=master, text=nameA1 + " J " + nameA2, text_color="#000000", command=self.radioButtonEvent, variable=value, value=-1)
        r3 = CTkRadioButton(master=master, text=nameA1 + " P " + nameA2, text_color="#000000", command=self.radioButtonEvent, variable=value, value=1)
        r4 = CTkRadioButton(master=master, text=nameA2 + " P " + nameA1, text_color="#000000", command=self.radioButtonEvent, variable=value, value=2)

        self.placeQCM((r1, r2, r3, r4))


    def placeQCM(self, qcm):
        """Place qcm in the tab (with grid)
        """
        for q in qcm:
            q.grid(row=self.row, column=0, padx=50, pady=(5, 0), sticky="n")
            self.row +=1
        #self.questionsQCM.append(qcm)


    def radioButtonEvent(self):
        """Handle radioButton event (answer change)
        """
        self.listener.updateInQCM()