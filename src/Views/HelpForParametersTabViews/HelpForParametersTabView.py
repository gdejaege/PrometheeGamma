from customtkinter import (CTkLabel, CTkButton, CTkRadioButton, IntVar, CTkFrame, CTkCanvas, CTkScrollbar, CTkScrollableFrame)
from Models.Alternative import Alternative

class HelpForParametersTabView:
    class ViewListener:
        def showQuestions(self):
            pass
        def changeQCM(self):
            pass
        def confirm(self):
            pass
        def apply(self):
            pass
        def next(self):
            pass

    def __init__(self, master) -> None:
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.master = CTkScrollableFrame(master=master, fg_color="#ffffff")
        self.master.grid_columnconfigure(0, weight=1)
        explanation = "In order to help determine the 3 parameters introduced by the PROMETHEE Gamma method, it is necessary to know your opinion on a small number of pairwise comparisons between alternatives. Please answer the questions below."
        self.explanationLabel = CTkLabel(master=self.master, text=explanation, text_color="#000000", wraplength=580)
        self.button = CTkButton(master=self.master, text="Generate questions", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.generateQuestions)
        self.confirmButton = CTkButton(master=self.master, text="Confirm", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.confirm)
        self.nextButton = CTkButton(master=self.master, text="Next", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.next)
        self.questionLabels = []
        self.questionsQCM = []
        self.resultsLabel = None
        self.applyButton = CTkButton(master=self.master, text="Use results in result tab", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.apply)
        self.row = 0
        self.listener = None


    def setListener(self, l:ViewListener):
        self.listener = l

    
    def show(self):
        self.master.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.explanationLabel.grid(row=self.row, column=0, padx=10, pady=(10, 0), sticky="n")
        self.row +=1
        self.button.grid(row=self.row, column=0, padx=10, pady=(10, 0), sticky="n")
        self.row +=1


    def showNextQuestion(self, question:tuple, end:bool) -> None:
        l0 = self.alternativeInLabel(question[0])
        l1 = self.alternativeInLabel(question[1])
        self.placeQuestionLabel(l0, l1)
        self.qcm(question[0].getName_str(), question[1].getName_str(), question[2])
        if end:
            self.confirmButton.grid(row=self.row, column=0, padx=10, pady=(20, 0), sticky="n")
            self.row += 1
        else :
            self.nextButton.grid(row=self.row, column=0, padx=10, pady=(20, 0), sticky="n")


    def next(self):
        self.nextButton.grid_forget()
        self.listener.next()
            

    def alternativeInLabel(self, a:Alternative) -> CTkLabel:
        textLabel = a.getName_str() + ":"
        for i in range(a.getSize()):
            textLabel += "   " + str(a.getEvaluation_float(i))
        return CTkLabel(master=self.master, text_color="#000000", text=textLabel)
    

    def placeQuestionLabel(self, l0:CTkLabel, l1:CTkLabel):
        l0.grid(row=self.row, column=0, padx=10, pady=(20, 0), sticky="n")
        self.row +=1
        l1.grid(row=self.row, column=0, padx=10, pady=(0, 0), sticky="n")
        self.row +=1
        self.questionLabels.append((l0, l1))


    def qcm(self, nameA1:str, nameA2:str, value:IntVar) -> None:
        r1 = CTkRadioButton(master=self.master, text=nameA1 + " I " + nameA2, text_color="#000000", command=self.radioButtonEvent, variable=value, value=0)
        r2 = CTkRadioButton(master=self.master, text=nameA1 + " J " + nameA2, text_color="#000000", command=self.radioButtonEvent, variable=value, value=-1)
        r3 = CTkRadioButton(master=self.master, text=nameA1 + " P " + nameA2, text_color="#000000", command=self.radioButtonEvent, variable=value, value=1)
        r4 = CTkRadioButton(master=self.master, text=nameA2 + " P " + nameA1, text_color="#000000", command=self.radioButtonEvent, variable=value, value=2)

        self.placeQCM((r1, r2, r3, r4))


    def placeQCM(self, qcm):
        for q in qcm:
            q.grid(row=self.row, column=0, padx=50, pady=(5, 0), sticky="n")
            self.row +=1
        self.questionsQCM.append(qcm)


    def radioButtonEvent(self):
        self.listener.changeQCM()


    def generateQuestions(self):
        for l in self.questionLabels:
            for ll in l:
                ll.destroy()
        self.questionLabels.clear()
        for q in self.questionsQCM:
            for qq in q:
                qq.destroy()
        self.questionsQCM.clear()
        self.row = 2
        self.confirmButton.grid_forget()
        if self.resultsLabel != None:
            self.resultsLabel.destroy()
        self.applyButton.grid_forget()
        self.listener.showQuestions()


    def confirm(self):
        self.listener.confirm()


    def showResults(self, results):
        (i, j, p) = results
        textResults = "The results are I=" + str(round(i, 2)) + " J=" + str(round(j, 2)) + " P=" + str(round(p, 2))
        self.resultsLabel = CTkLabel(master=self.master, text=textResults, text_color="#000000")
        self.resultsLabel.grid(row=self.row, column=0, padx=10, pady=(10, 0), sticky="n")
        self.row += 1
        self.applyButton.grid(row=self.row, column=0, padx=10, pady=(10, 30), sticky="n")


    def apply(self):
        self.listener.apply()
