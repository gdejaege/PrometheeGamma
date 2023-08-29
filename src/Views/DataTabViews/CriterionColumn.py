from tkinter import *
from customtkinter import (CTkEntry, CTkButton, CTkToplevel)
import platform

from Models.DataTabModels.Criterion import Criterion
from Views.DataTabViews.PreferenceFunctionWindow import PreferenceFunctionWindow


TYPEDICT = {1:"Usual", 2:"U-shape", 3:"V-shape", 4:"Level", 5:"Linear", 6:"Gaussian"}
"""a dictionnary to link each type of preference function with a number"""

class CriterionColumn:
    """
    A class to display a criterion column in PROMETHEE Gamma GUI application

    master : CTkFrame
        the master frame
    pfType : IntVar
        the type of the preference function used for this criterion
    nameEntry : CTkEntry
        the entry to modify the criterion name
    weightEntry : CTkEntry
        the entry to modify the criterion weight
    typePfTextButton : StringVar
        the variable text associated with the typePfButton
    typePfButton : CTkButton
        button that opens a PrefenceFunctionWindow to select a preference function
    pcEntry : CTkEntry
        the entry to modify the preference threshold associated to the preference function
    qcEntry : CTkEntry
        the entry to modify the indifference threshold associated to the preference function
    
    Methods
    -------
    """

    def __init__(self, master, criterion:Criterion) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        criterion : Criterion
            the criterion of wich this class represents the column
        """
        self.master = master
        self.pfType = criterion.getPf()
        self.nameEntry = CTkEntry(master=master, textvariable=criterion.getName(), width=120)
        self.weightEntry = CTkEntry(master=master, textvariable=criterion.getWeight(), width=120)
        self.typePfTextButton = StringVar(master=master, value=TYPEDICT[self.pfType.get()])
        self.typePfButton = CTkButton(master=master, textvariable=self.typePfTextButton, width=120, command=self.buttonTypeEvent)
        self.pcEntry = CTkEntry(master=master, textvariable=criterion.getP(), width=120)
        self.qcEntry = CTkEntry(master=master, textvariable=criterion.getQ(), width=120)


    def show(self, row:int, col:int):
        """Show the column

        Parameters
        ----------
        row : int
            the current row to place the CriterionColumn in the frame
        col : int
            the current column to place the CriterionColumn in the frame
        """
        self.nameEntry.grid(row=row, column=col)
        self.weightEntry.grid(row=row+1, column=col)
        self.typePfButton.grid(row=row+2, column=col)
        self.pcEntry.grid(row=row+3, column=col)
        self.qcEntry.grid(row=row+4, column=col)


    def buttonTypeEvent(self):
        """Handle click event on the typePfButton
        """
        w = CTkToplevel(self.master)
        if platform.system() == 'Windows':
            w.grab_set()
            w.focus_set()
        w.title("Preference functions")
        pfw = PreferenceFunctionWindow(master=w, textvar=self.typePfTextButton, intvar=self.pfType, typesDict=TYPEDICT)
        pfw.show()

    
    def destroy(self) -> None:
        """Destroy (erase and forget) the column
        """
        self.nameEntry.destroy()
        self.weightEntry.destroy()
        self.typePfButton.destroy()
        self.pcEntry.destroy()
        self.qcEntry.destroy()