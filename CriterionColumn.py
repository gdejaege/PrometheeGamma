from tkinter import *
from customtkinter import (CTkEntry, CTkOptionMenu)

class CriterionColumn:
    def __init__(self, master, x, y) -> None:
        self.name = StringVar(master=master, value="New criterion")
        self.weight = StringVar(master=master, value="0.0")
        self.typePF = StringVar(master=master, value="0")
        self.types = ["0", "1"]
        self.pc = StringVar(master=master, value="0")
        self.qc = StringVar(master=master, value="0")

        self.entry_name = CTkEntry(master=master, textvariable=self.name)
        self.entry_weight = CTkEntry(master=master, textvariable=self.weight)
        self.option_type = CTkOptionMenu(master=master, values=self.types, variable=self.typePF, command=self.choose_type)
        self.entry_pc = CTkEntry(master=master, textvariable=self.pc)
        self.entry_qc = CTkEntry(master=master, textvariable=self.qc)

        self.entry_name.place(x=x, y=y)
        self.entry_weight.place(x=x, y=y+25)
        self.option_type.place(x=x, y=y+50)
        self.entry_pc.place(x=x, y=y+75)
        self.entry_qc.place(x=x, y=y+100)

    
    def choose_type(self, val:str) -> None:
        self.typePF.set(val)


    def get_name(self) -> str:
        return self.name.get()
    

    def get_weight(self) -> float:
        return float(self.weight.get())
    

    def get_typePF(self) -> int:
        return int(self.typePF.get())
    

    def get_pc(self) -> float:
        return float(self.pc.get())
    

    def get_qc(self) -> float:
        return float(self.qc.get())
    

    def set_name(self, new_name:str) -> None:
        self.name.set(new_name)


    def set_weight(self, new_weight:float) -> None:
        self.weight.set(str(new_weight))


    def set_typePF(self, new_type:int) -> None:
        self.typePF.set(str(new_type))


    def set_pc(self, new_pc:float) -> None:
        self.pc.set(str(new_pc))


    def set_qc(self, new_qc:float) -> None:
        self.qc.set(str(new_qc))

    
    def destroy(self) -> None:
        self.entry_name.destroy()
        self.entry_weight.destroy()
        self.option_type.destroy()
        self.entry_pc.destroy()
        self.entry_qc.destroy()