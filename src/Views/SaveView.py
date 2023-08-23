from typing import Optional, Tuple, Union
from customtkinter import (CTkToplevel, CTkLabel, CTkEntry, CTkCheckBox, CTkButton, StringVar, IntVar)
import tkinter.filedialog as fd
import tkinter.messagebox as msg
import os

class SaveView(CTkToplevel):

    class Listener:
        def saveInDirectory(self, directory:str, name:str):
            pass


    def __init__(self, *args, saveDict:dict, parentDirectory:str, name:str, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)

        self.labelName = CTkLabel(self, text="Name:")
        self.name = StringVar(self, value="")
        if name is not None:
            self.name.set(name)
        self.entryName = CTkEntry(self, textvariable=self.name)
        self.labelSelection = CTkLabel(self, text="What do you want to save?")

        self.checkBoxList = []
        for k, v in saveDict.items():
            checkBox = CTkCheckBox(self, text=k, variable=v)
            self.checkBoxList.append(checkBox)

        self.labelDirectory = CTkLabel(self, text="Select a directory:")
        self.directory = StringVar(self, value="...")
        if parentDirectory is not None:
            self.directory.set(parentDirectory)
        self.buttondirectory = CTkButton(self, textvariable=self.directory, command=self.selectDirectory)
        self.saveButton = CTkButton(self, text="Save", command=self.save)
        self.cancelButton =CTkButton(self, text="Cancel", command=self.cancel)

        self.listener = None


    def setListener(self, l:Listener):
        self.listener = l


    def show(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.labelName.grid(row=0, column=0, sticky="e", padx=20, pady=(20,0))
        self.entryName.grid(row=0, column=1, sticky="w", padx=20, pady=(20,0))
        self.labelSelection.grid(row=1, column=0, columnspan=2, sticky="w", padx=20, pady=(20,0))

        r = 2
        for e in self.checkBoxList:
            e.grid(row=r, column=0, columnspan=2, sticky="w", padx=20, pady=(10,0))
            r += 1

        self.labelDirectory.grid(row=r, column=0, sticky="w", padx=20, pady=(20,0))
        self.buttondirectory.grid(row=r+1, column=0, columnspan=3, sticky="n", padx=20, pady=(5,0))
        self.saveButton.grid(row=r+2, column=0, columnspan=1, sticky="n", padx=20, pady=(30,20))
        self.cancelButton.grid(row=r+2, column=1, columnspan=1, sticky="n", padx=20, pady=(30,20))


    def selectDirectory(self):
        if not os.path.exists("./Projects"):
            os.makedirs("./Projects")
        directory = fd.askdirectory(initialdir="./Projects")
        self.directory.set(directory)


    def save(self):
        directory = self.directory.get()
        name= self.name.get()
        if directory == "...":
            msg.showerror("No directory", "Please, select a directory.")
        elif name == "":
            msg.showerror("No name", "Please, enter a name.")
        else:
            self.listener.saveInDirectory(directory, name)

    
    def cancel(self):
        self.destroy()
        msg.showwarning("Warning", "The project was not saved.")
