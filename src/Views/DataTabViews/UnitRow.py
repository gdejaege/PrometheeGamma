from customtkinter import (CTkEntry, DoubleVar)
from Models.Alternative import Alternative

class UnitRow:
    """
    A class to display the row of a unit (an alternative)

    Attributes
    ----------
    master : CTkFrame
        the master frame
    x : int
        the x coordinate of the row
    y : int
        the y coordinate of the row
    alternative : Alternative
        the alternative of which it is the row
    nameEntry : CTkEntry
        the entry to modify the altenative name
    valuesEntries : list[CTkEntry]
        a list that will contain all entries to modify evaluations of the altenative

    Methods
    -------
    show()
        show the row
    add_column(value:DoubleVar)
        add a column to the row
    destroy()
        destroy the row
    del_column()
        destroy the last column of the row
    """

    def __init__(self, master, x:int, y:int, alternative:Alternative) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        x : int
            the x coordinate of the row
        y : int
            the y coordinate of the row
        alternative : Alternative
            the alternative of which it is the row
        """
        self.master=master
        self.x = x
        self.y = y
        self.alternative = alternative
        self.nameEntry = CTkEntry(master=self.master, textvariable=alternative.getName())
        self.valueEntries = []
        for i in range(alternative.getSize()):
            self.valueEntries.append(CTkEntry(master=self.master, textvariable=alternative.getEvaluation(i)))

    
    def show(self):
        """Show the row
        """
        self.nameEntry.place(x=self.x, y=self.y)
        for i in range(self.alternative.getSize()):
            self.x += 141
            self.valueEntries[i].place(x=self.x, y=self.y)

    
    def add_column(self, value:DoubleVar):
        """Add a column to the row

        Parameters
        ----------
        value : DoubleVar
            The value to add in the last column
        """
        self.valueEntries.append(CTkEntry(master=self.master, textvariable=value))
        self.x += 141
        self.valueEntries[-1].place(x=self.x, y=self.y)


    def destroy(self) -> None:
        """Destroy the row
        """
        self.nameEntry.destroy()
        for i in self.valueEntries:
            i.destroy()


    def del_column(self) -> None:
        """Destroy the last column of the row
        """
        self.valueEntries[-1].destroy()
        self.valueEntries.pop()
        self.x -= 141