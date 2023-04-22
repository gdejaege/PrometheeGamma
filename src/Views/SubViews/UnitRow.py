from customtkinter import (CTkEntry, DoubleVar)
from Models.Alternative import Alternative

class UnitRow:
    def __init__(self, master, x:int, y:int, alternative:Alternative) -> None:
        self.master=master
        self.x = x
        self.y = y
        self.entry_name = CTkEntry(master=self.master, textvariable=alternative.getName())
        self.entry_name.place(x=self.x, y=self.y)
        self.valueEntries = []
        for i in range(alternative.getSize()-1):
            self.valueEntries.append(CTkEntry(master=self.master, textvariable=alternative.getEvaluation(i+1)))
            self.x = x+(i+1)*141
            self.valueEntries[i].place(x=self.x, y=self.y)

    
    def add_column(self, value:DoubleVar):
        self.valueEntries.append(CTkEntry(master=self.master, textvariable=value))
        self.x += 141
        self.valueEntries[-1].place(x=self.x, y=self.y)


    def destroy(self) -> None:
        self.entry_name.destroy()
        for i in self.valueEntries:
            i.destroy()


    def del_column(self) -> None:
        self.valueEntries[-1].destroy()
        self.valueEntries.pop()
        self.x -= 141