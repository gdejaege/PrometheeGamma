from customtkinter import (CTkTabview, CTkLabel, CTkRadioButton, IntVar)
import tkinter as tk
import platform

#from Models.DataTabModels.Alternative import Alternative
from ...Models.DataTabModels.Alternative import Alternative


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
    """

    class Listener:
        """
        An interface for the listener of this view
        """

        def updateInmcq(self):
            """Handle an update in mcq
            """
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


    def addQuestion(self, question:tuple, criteriaNames:list):
        """Add a question

        Parameters
        ----------
        question : tuple[Alternative, Alternative, IntVar]
            the "question" to add, i.e. the two alternatives that will be compared and the value of preference (in the IntVar): 
            0 for indifference ; 1 for preference ; -1 for incomparability
        """
        self.addTab()
        nbcolumns = len(criteriaNames) + 1
        for i in range(nbcolumns):
            self.masterList[-1].grid_columnconfigure(i, weight=1)
        self.questionName(self.masterList[-1], question[0], question[1], criteriaNames)
        self.row = 3
        self.mcq(self.masterList[-1], question[0].getName_str(), question[1].getName_str(), question[2], columnspan=nbcolumns)
    

    def questionName(self, master, a1:Alternative, a2:Alternative, criteriaNames:list):
        """Put alternatives and criteria in labels and display them

        Parameters
        ----------
        master : CTkFrame
            the master frame
        a1 : Alternative
            an alternative
        a2 : Alternative
            an other alternative
        criteriaNames : list of str
            the list of criteria names
        """
        la1 = CTkLabel(master=master, text_color="#000000", text=a1.getName_str())
        la1.grid(row=1, column=0, sticky="n", pady=(0,0), padx=20)
        la2 = CTkLabel(master=master, text_color="#000000", text=a2.getName_str())
        la2.grid(row=2, column=0, sticky="n", pady=(0,0), padx=20)
        
        column = 1
        for i in range(len(criteriaNames)):
            l0 = CTkLabel(master=master, text_color="#000000", text=criteriaNames[i])
            l0.grid(row=0, column=column, sticky="n", pady=(20,0), padx=10)

            l1 = CTkLabel(master=master, text_color="#000000", text=str(a1.getEvaluation_float(i)))
            l1.grid(row=1, column=column, sticky="n", pady=(0,0), padx=10)
            
            l2 = CTkLabel(master=master, text_color="#000000", text=str(a2.getEvaluation_float(i)))
            l2.grid(row=2, column=column, sticky="n", pady=(0,0), padx=10)

            column += 1


    def mcq(self, master, nameA1:str, nameA2:str, value:IntVar, columnspan:int) -> None:
        """Create a mcq with radioButton

        Parameters
        ----------
        master : CTkFrame
            the tab where place mcq
        nameA1 : str
            the name of the first alternative of the question
        nameA2 : str
            the name of the second alternative of the question
        value : IntVar
            the radioButton variable thath will contain the answer
        """

        if platform.system() == "windows":
            r1 = CTkRadioButton(master=master, text=nameA1 + " I " + nameA2, text_color="#000000", command=self.radioButtonEvent, variable=value, value=0)
            r2 = CTkRadioButton(master=master, text=nameA1 + " J " + nameA2, text_color="#000000", command=self.radioButtonEvent, variable=value, value=-1)
            r3 = CTkRadioButton(master=master, text=nameA1 + " P " + nameA2, text_color="#000000", command=self.radioButtonEvent, variable=value, value=1)
            r4 = CTkRadioButton(master=master, text=nameA2 + " P " + nameA1, text_color="#000000", command=self.radioButtonEvent, variable=value, value=2)
        else:
            r1 = tk.Radiobutton(master=master, text=nameA1 + " I " + nameA2, fg="black", bg="white", command=self.radioButtonEvent, variable=value, value=0, 
            activebackground="#6cffff", highlightbackground="white")
            r2 = tk.Radiobutton(master=master, text=nameA1 + " J " + nameA2, fg="black", bg="white", command=self.radioButtonEvent, variable=value, value=-1, 
            activebackground="#6cffff", highlightbackground="white")
            r3 = tk.Radiobutton(master=master, text=nameA1 + " P " + nameA2, fg="black", bg="white", command=self.radioButtonEvent, variable=value, value=1,
            activebackground="#6cffff", highlightbackground="white")
            r4 = tk.Radiobutton(master=master, text=nameA2 + " P " + nameA1, fg="black", bg="white", command=self.radioButtonEvent, variable=value, value=2,
            activebackground="#6cffff", highlightbackground="white")

        self.placemcq((r1, r2, r3, r4), columnspan)


    def placemcq(self, mcq, columnspan):
        """Place mcq in the tab (with grid)
        """
        for q in mcq:
            q.grid(row=self.row, column=0, columnspan=columnspan, padx=50, pady=(5, 0), sticky="n")
            self.row +=1


    def radioButtonEvent(self):
        """Handle radioButton event (answer change)
        """
        self.listener.updateInmcq()