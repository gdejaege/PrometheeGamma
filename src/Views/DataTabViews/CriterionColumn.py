from tkinter import *
from customtkinter import (CTkEntry, CTkButton, CTkToplevel)
from Views.DataTabViews.PreferenceFunctionWindow import PreferenceFunctionWindow
from Models.Criterion import Criterion

class CriterionColumn:
    def __init__(self, master, x, y, criterion:Criterion) -> None:
        self.master = master
        self.dico_types = {1:"Usual", 2:"U-shape", 3:"V-shape", 4:"Level", 5:"Linear", 6:"Gaussian"}

        self.pfType = criterion.getPf()

        self.entry_name = CTkEntry(master=master, textvariable=criterion.getName())
        self.entry_weight = CTkEntry(master=master, textvariable=criterion.getWeight())
        self.text_button_type = StringVar(master=master, value=self.dico_types[self.pfType.get()])
        self.button_type = CTkButton(master=master, textvariable=self.text_button_type, command=self.buttonTypeEvent)
        self.entry_pc = CTkEntry(master=master, textvariable=criterion.getP())
        self.entry_qc = CTkEntry(master=master, textvariable=criterion.getQ())

        self.entry_name.place(x=x, y=y)
        self.entry_weight.place(x=x, y=y+25)
        self.button_type.place(x=x, y=y+50)
        self.entry_pc.place(x=x, y=y+75)
        self.entry_qc.place(x=x, y=y+100)

        self.pfw = None


    def buttonTypeEvent(self):
        w = CTkToplevel(self.master)
        w.title("Preference functions")
        self.pfw = PreferenceFunctionWindow(master=w, textvar=self.text_button_type, intvar=self.pfType)

    
    def destroy(self) -> None:
        self.entry_name.destroy()
        self.entry_weight.destroy()
        self.button_type.destroy()
        self.entry_pc.destroy()
        self.entry_qc.destroy()