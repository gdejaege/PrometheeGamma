from customtkinter import (CTkButton, CTkLabel, CTkFrame)

from ...Resources.ScrollableFrames.HVScrollableFrame import HVScrollableFrame


class DataTabView:
    """
    A class to display the content of the data tab

    Attributes
    ----------
    listener : ViewListener
        the listener of this view
    row : int
        row coordinate for grid method
    col : int
        column coordinate for grid method
    openFileButton : CTkButton
        a button to open data file
    dataNoteLabel : CTkLabel
        a label to display a note
    scrollableFrame : HVScrollableFrame
        a scrollable frame (vertically and horizontally) for the data table
    table : CTkFrame
        the data table frame
    criteriaLabel : CTkLabel
        a label to display "Criteria:"
    weightsLabel : CTkLabel
        a label to display "Weights:"
    typesLabel : CTkLabel
        a label to display "Preference functions:"
    pcLabel : CTkLabel
        a label to display "Pc:"
    qcLabel : CTkLabel
        a label to display "Qc:"
    buttonAddCriterion : CTkButton
        a button to add a criterion
    buttonAddUnit : CTkButton
        a button to add an alternative
    buttonDeleteCriterion : CTkButton
        a button to delete a criterion
    buttonDeleteUnit : CTkButton
        a button to delete an alternative
    """

    class ViewListener:
        """
        An interface for the listener of this view
        """
        def openFile(self, master):
            """Open a file selected by the user and load data from file to the data table

            Parameters
            ----------
            master : CTkFrame
                the master frame
            """
            pass

        def addCriterionColumn(self, master, row:int, col:int):
            """Add a criterion and its column in the data table

            Parameters
            ----------
            master : CTkFrame
                the master frame
            row : int
                the row for grid coordinate to place the new criterion column
            col : int
                the column for grid coordinate to place the new criterion column
            """
            pass

        def addUnitRow(self, master, row:int, col:int):
            """Add an alternative (a unit) and its row in the data table

            Parameters
            ----------
            master : CTkFrame
                the master frame
            row : int
                the row for grid coordinate to place the new unit row
            col : int
                the column for grid coordinate to place the new unit row
            """
            pass

        def deleteCriterion(self):
            """Delete the last criterion and its column in the data table
            """
            pass

        def deleteUnit(self):
            """Delete the last alternative (unit) and its row in the data table
            """
            pass


    def __init__(self, master) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the parent master frame
        """
        self.listener = None

        self.row = 0
        self.col = 0

        # header
        self.openFileButton = CTkButton(master=master, text="Open a file", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.openFile)
        self.dataNoteLabel = CTkLabel(master=master, text="Only csv files are accepted", fg_color="#ffffff", text_color="#000000", corner_radius=5)
        
        # Table
        self.scrollableFrame = HVScrollableFrame(master)
        self.table = self.scrollableFrame.frame()
        self.criteriaLabel = CTkLabel(master=self.table, text="Criteria:", text_color="#000000")
        self.weightsLabel = CTkLabel(master=self.table, text="Weights:", text_color="#000000")
        self.typesLabel = CTkLabel(master=self.table, text="Preference Functions:", text_color="#000000")
        self.pcLabel = CTkLabel(master=self.table, text="Pc:", text_color="#000000")
        self.qcLabel = CTkLabel(master=self.table, text="Qc:", text_color="#000000")
        self.buttonAddCriterion = CTkButton(master=self.table, text="Add a criterion", command=self.addCriterion, width=180)
        self.buttonAddUnit = CTkButton(master=self.table, text="Add an alternative", command=self.addUnit, width=180)
        self.buttonDeleteCriterion = CTkButton(master=self.table, text="Delete a criterion", command=self.deleteCriterion, width=180)
        self.buttonDeleteUnit = CTkButton(master=self.table, text="Delete an alternative", command=self.deleteUnit, width=180)


    def setListener(self, l:ViewListener):
        """Set the listener

        Parameters
        ----------
        l : ViewListener
            the new listener
        """
        self.listener = l


    def show(self) -> None:
        """Show the view   
        """
        self.openFileButton.pack(pady=10)
        self.dataNoteLabel.pack(pady=10)

        self.scrollableFrame.pack(fill="both", expand=True)

        self.criteriaLabel.grid(row=0, column=0)
        self.weightsLabel.grid(row=1, column=0)
        self.typesLabel.grid(row=2, column=0)
        self.pcLabel.grid(row=3, column=0)
        self.qcLabel.grid(row=4, column=0)

        self.row = 5
        self.col = 1

        self.buttonAddCriterion.grid(row=0, column=self.col, sticky="w")
        self.buttonAddUnit.grid(row=self.row, column=0, sticky="e")
        self.buttonDeleteCriterion.grid(row=1, column=self.col, sticky="w")
        self.buttonDeleteUnit.grid(row=self.row, column=1, columnspan=2, sticky="w")


    def getViewCData(self) ->tuple:
        """Return the needed view information to place a criterion column

        Returns
        -------
        tuple of CTkFrame and int
            (table, row, col), the master frame and the grid coordinates for criterion column
        """
        return (self.table, 0, self.col)


    def getViewUData(self) ->tuple:
        """Return the needed view information to place a unit row

        Returns
        -------
        tuple of CTkFrame and int
            (table, row, col), the master frame and the grid coordinates for unit row
        """
        return (self.table, self.row, 0)


    def openFile(self) -> None:
        """Handle click on openFileButton
        """
        self.listener.openFile(self.table)


    def addCriterion(self) -> None:
        """Handle click on buttonAddCriterion
        """
        self.listener.addCriterionColumn(master=self.table, row=0, col=self.col)

    
    def shiftRight(self):
        """Shift right buttons add and delete criterion and update col
        """
        self.col += 1
        self.buttonAddCriterion.grid_configure(column=self.col)
        self.buttonDeleteCriterion.grid_configure(column=self.col)


    def shiftLeft(self):
        """Shift left buttons add and delete criterion and update col
        """
        self.col -= 1
        self.buttonAddCriterion.grid_configure(column=self.col)
        self.buttonDeleteCriterion.grid_configure(column=self.col)


    def shiftUp(self):
        """Shift up buttons add and delete unit and update row
        """
        self.row -= 1
        self.buttonAddUnit.grid_configure(row=self.row)
        self.buttonDeleteUnit.grid_configure(row=self.row)


    def shiftDown(self):
        """Shift down buttons add and delete unit and update row
        """
        self.row += 1
        self.buttonAddUnit.grid_configure(row=self.row)
        self.buttonDeleteUnit.grid_configure(row=self.row)


    def addUnit(self) -> None:
        """Handle click on buttonAddUnit
        """
        self.listener.addUnitRow(master=self.table, row=self.row, col=0)


    def deleteCriterion(self) -> None:
        """Handle click on buttonDeleteCriterion
        """
        self.listener.deleteCriterion()


    def deleteUnit(self) -> None:
        """Handle click on buttonDeleteUnit
        """
        self.listener.deleteUnit()