from tkinter import *
from customtkinter import CTkEntry

class UnitRow:
    def __init__(self, master, nb_criteria:int, x, y) -> None:
        self.master=master
        self.name = StringVar(master=self.master, value="New unit")
        self.entry_name = CTkEntry(master=self.master, textvariable=self.name)
        self.entry_name.place(x=x, y=y)
        self.values = []
        self.entries = []
        self.x = x
        self.y = y
        for i in range(nb_criteria):
            self.values.append(StringVar(master=self.master, value="0.0"))
            self.entries.append(CTkEntry(master=self.master, textvariable=self.values[i]))
            self.x = x+(i+1)*141
            self.entries[i].place(x=self.x, y=self.y)

    
    def add_column(self):
        self.values.append(StringVar(master=self.master, value="0.0"))
        self.entries.append(CTkEntry(master=self.master, textvariable=self.values[-1]))
        self.x += 141
        self.entries[-1].place(x=self.x, y=self.y)

    
    def get_row(self) -> list:
        result = []
        result.append(self.name.get())
        for i in range(len(self.values)):
            result.append(float(self.values[i].get()))
        return result
    

    def set_name(self, new_name:str) -> None:
        self.name.set(new_name)


    def set_values(self, new_values:list) -> None:
        for i in range(len(new_values)):
            self.values[i].set(str(new_values[i]))


    def destroy(self) -> None:
        self.entry_name.destroy()
        for i in self.entries:
            i.destroy()


    def del_column(self) -> None:
        self.entries[-1].destroy()
        self.entries.pop()
        self.values.pop()
        self.x -= 141