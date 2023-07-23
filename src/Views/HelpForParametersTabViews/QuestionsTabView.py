from customtkinter import (CTkTabview, CTkLabel, CTkRadioButton, IntVar)
from Models.Alternative import Alternative

class QuestionsTabView(CTkTabview):
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
        self.listener = l


    def addTab(self):
        self.nb += 1
        name = "Question " + str(self.nb)
        self.add(name)
        self.masterList.append(self.tab(name))
        self.set(name)


    def addQuestion(self, question):
        self.addTab()
        self.row = 0
        l0 = self.alternativeInLabel(self.masterList[-1], question[0])
        l1 = self.alternativeInLabel(self.masterList[-1], question[1])
        self.placeQuestionLabel(l0, l1)
        self.qcm(self.masterList[-1], question[0].getName_str(), question[1].getName_str(), question[2])



    def alternativeInLabel(self, master, a:Alternative) -> CTkLabel:
        textLabel = a.getName_str() + ":"
        for i in range(a.getSize()):
            textLabel += "   " + str(a.getEvaluation_float(i))
        return CTkLabel(master=master, text_color="#000000", text=textLabel)
    

    def placeQuestionLabel(self, l0:CTkLabel, l1:CTkLabel):
        l0.grid(row=self.row, column=0, padx=10, pady=(20, 0), sticky="n")
        self.row +=1
        l1.grid(row=self.row, column=0, padx=10, pady=(0, 0), sticky="n")
        self.row +=1
        #self.questionLabels.append((l0, l1))


    def qcm(self, master, nameA1:str, nameA2:str, value:IntVar) -> None:
        r1 = CTkRadioButton(master=master, text=nameA1 + " I " + nameA2, text_color="#000000", command=self.radioButtonEvent, variable=value, value=0)
        r2 = CTkRadioButton(master=master, text=nameA1 + " J " + nameA2, text_color="#000000", command=self.radioButtonEvent, variable=value, value=-1)
        r3 = CTkRadioButton(master=master, text=nameA1 + " P " + nameA2, text_color="#000000", command=self.radioButtonEvent, variable=value, value=1)
        r4 = CTkRadioButton(master=master, text=nameA2 + " P " + nameA1, text_color="#000000", command=self.radioButtonEvent, variable=value, value=2)

        self.placeQCM((r1, r2, r3, r4))


    def placeQCM(self, qcm):
        for q in qcm:
            q.grid(row=self.row, column=0, padx=50, pady=(5, 0), sticky="n")
            self.row +=1
        #self.questionsQCM.append(qcm)


    def radioButtonEvent(self):
        self.listener.updateInQCM()