from customtkinter import (CTkLabel, CTkButton, CTkRadioButton)
from Models.Alternative import Alternative

class HelpForParametersTabView:
    class ViewListener:
        def showQuestions(self):
            pass

    def __init__(self, master) -> None:
        self.master = master
        explanation = "In order to help determine the 3 parameters introduced by the PROMETHEE Gamma method, it is necessary to know your opinion on a small number of pairwise comparisons between alternatives. Please answer the questions below."
        self.explanationLabel = CTkLabel(master=self.master, text=explanation, text_color="#000000", wraplength=580)
        self.button = CTkButton(master=self.master, text="Generate questions", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.generateQuestions)
        self.questionLabels = []
        self.yQuestions = 125
        self.listener = None


    def setListener(self, l:ViewListener):
        self.listener = l

    
    def show(self):
        self.explanationLabel.place(relx=0.5, y=25, anchor='center')
        self.button.place(relx=0.5, y=80, anchor='center')


    def showQuestions(self, questions:list) -> None:
        for q in questions:
            l0 = self.alternativeInLabel(q[0])
            l1 = self.alternativeInLabel(q[1])
            self.placeQuestionLabel(l0, l1)
            self.qcm(q[0].getName_str(), q[1].getName_str())
            

    def alternativeInLabel(self, a:Alternative) -> CTkLabel:
        textLabel = a.getName_str() + ":"
        for i in range(a.getSize()):
            textLabel += "   " + str(a.getEvaluation_float(i))
        return CTkLabel(master=self.master, text_color="#000000", text=textLabel)
    

    def placeQuestionLabel(self, l0:CTkLabel, l1:CTkLabel):
        l0.place(x = 50, y = self.yQuestions)
        self.yQuestions += 25
        l1.place(x = 50, y = self.yQuestions)
        self.yQuestions += 25


    def qcm(self, nameA1:str, nameA2:str) -> None:
        pass


    def generateQuestions(self):
        self.listener.showQuestions()
