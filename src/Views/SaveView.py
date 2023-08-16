from typing import Optional, Tuple, Union
from customtkinter import (CTkToplevel, CTkLabel, CTkEntry, CTkCheckBox, CTkButton, StringVar, IntVar)
import tkinter.filedialog as fd
import tkinter.messagebox as msg

class SaveView(CTkToplevel):

    class Listener:
        def saveInFolder(self, folder:str, name:str):
            pass


    def __init__(self, *args, saveDict:dict, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)

        self.labelName = CTkLabel(self, text="Name:")
        self.name = StringVar(self, value="")
        self.entryName = CTkEntry(self, textvariable=self.name)
        self.labelSelection = CTkLabel(self, text="What do you want to save?")

        self.checkBoxList = []
        for k, v in saveDict.items():
            checkBox = CTkCheckBox(self, text=k, variable=v)
            self.checkBoxList.append(checkBox)

        """
        self.checkBoxData = CTkCheckBox(self, text="Data")
        self.checkBoxData.select()
        self.checkBoxParameters = CTkCheckBox(self, text="Parameters")
        self.checkBoxParameters.select()
        self.checkBoxResults = CTkCheckBox(self, text="Result matrix")
        self.checkBoxResults.select()
        self.checkBoxGamma = CTkCheckBox(self, text="Gamma matrix")
        self.checkBoxGamma.select()
        self.checkBoxOrtho = CTkCheckBox(self, text="Orthogonal graph")
        self.checkBoxOrtho.select()
        self.checkBoxRank = CTkCheckBox(self, text="Rank graph")
        self.checkBoxRank.select()
        """

        self.labelFolder = CTkLabel(self, text="Select a folder:")
        self.folder = StringVar(self, value="...")
        self.buttonFolder = CTkButton(self, textvariable=self.folder, command=self.selectFolder)
        self.saveButton = CTkButton(self, text="Save", command=self.save)

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

        """
        self.checkBoxData.grid(row=2, column=0, columnspan=2, sticky="w", padx=20, pady=(10,0))
        self.checkBoxParameters.grid(row=3, column=0, columnspan=2, sticky="w", padx=20, pady=(10,0))
        self.checkBoxResults.grid(row=4, column=0, columnspan=2, sticky="w", padx=20, pady=(10,0))
        self.checkBoxGamma.grid(row=5, column=0, columnspan=2, sticky="w", padx=20, pady=(10,0))
        self.checkBoxOrtho.grid(row=6, column=0, columnspan=2, sticky="w", padx=20, pady=(10,0))
        self.checkBoxRank.grid(row=7, column=0, columnspan=2, sticky="w", padx=20, pady=(10,0))
        """

        self.labelFolder.grid(row=r, column=0, sticky="w", padx=20, pady=(20,0))
        self.buttonFolder.grid(row=r+1, column=0, columnspan=3, sticky="n", padx=20, pady=(5,0))
        self.saveButton.grid(row=r+2, column=0, columnspan=2, sticky="n", padx=20, pady=(30,20))


    def selectFolder(self):
        directory = fd.askdirectory(initialdir="./Projects")
        self.folder.set(directory)


    def save(self):
        folder = self.folder.get()
        name= self.name.get()
        if folder == "...":
            msg.showerror("No folder", "Please, select a folder.")
        elif name == "":
            msg.showerror("No name", "Please, enter a name.")
        else:
            self.listener.saveInFolder(folder, name)
