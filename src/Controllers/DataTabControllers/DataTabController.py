from tkinter import filedialog as fd
from Models.DataTabModel import DataTabModel
from Views.DataTabViews.DataTabView import DataTabView
from Views.DataTabViews.CriterionColumn import CriterionColumn
from Views.DataTabViews.UnitRow import UnitRow

class DataTabController(DataTabView.ViewListener):
    """
    A class to control the data tab

    Attributes
    ----------
    dataTabModel : DataTabModel
        the model for the data tab
    dataTabView : DataTabView
        the view of the data tab
    criteriaColumns : list[CriterionColumn]
        the list that will contain all criterion column
    unitsRows : list[UnitRow]
        the list that will contain all unit row

    Methods
    -------
    showView()
        show the dataTabView
    openFile(master)
        open a file selected by the user, read its content and close it
    readFile(file, master)
        read a csv file and add its content in the model
    fillDataTable()
        fill in the data table with the content of the models
    addCriterionColumn(master, x:int, y:int)
        add a criterion and its column in the data table
    deleteCriterion()
        delete the last criterion and its column in the data table
    addUnitRow(master, x: int, y: int)
        add an alternative (a unit) and its row in the data table
    deleteUnit()
        delete an alternative (a unit) and its row in the data table
    addOneColumnToAllUnits(master)
        add a column to the row of all alternatives
    deleteOneColumnInAllUnits()
        delete a column in the row of all alternatives
    clearTable()
        clear the data table
    getModel()
        return the current dataTabModel
    voidModel()
        test if model has no alternative or no criterion
    """

    def __init__(self, master) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame for the data tab
        """
        self.dataTabModel = DataTabModel()
        self.dataTabView = DataTabView(master=master)
        self.dataTabView.setListener(self)
        self.criteriaColums = []
        self.unitsRows = []


    def showView(self) -> None:
        """Show the dataTabView
        """
        self.dataTabView.show()
        

    def openFile(self, master) -> None:
        """Open a file selected by the user, read its content and close it

        Parameters
        ----------
        master : CTkFrame
            the master frame for the data tab. It is needed to link DoubleVar, IntVar and StringVar used to store data
        """
        file = fd.askopenfile(mode="r", filetypes=(("csv file", "*.csv"), ("all files","*.*")))
        self.clearTable()
        self.readFile(file, master)
        file.close()
        self.fillDataTable()


    def readFile(self, file, master) -> None:
        """Read a csv file and add its content in the model

        Parameters
        ----------
        file : IO
            file descriptor of the input file
        master : CTkFrame
            the master frame for the data tab. It is needed to link DoubleVar, IntVar and StringVar used to store data
        """
        criteriaP = None
        criteriaQ = None
        for line in file:
            line = line.strip()
            temp = line.split(',')
            if(temp[0] == 'c'):
                criteriaNames = temp[1:]
            elif(temp[0] == 'w'):
                criteriaWeights = temp[1:]
            elif(temp[0] == 'f'):
                criteriaPreferenceFunctionType = temp[1:]
            elif(temp[0] == 'p'):
                criteriaP = temp[1:]
            elif(temp[0] == 'q'):
                criteriaQ = temp[1:]
            else:
                self.dataTabModel.createAlternative(master, temp[0], temp[1:])
        self.dataTabModel.createCriteria(master, criteriaNames, criteriaWeights, criteriaPreferenceFunctionType, criteriaP, criteriaQ)


    def fillDataTable(self) -> None:
        """Fill in the data table with the content of the models
        """
        nbCrit = self.dataTabModel.getNumberOfCriteria()
        for i in range(len(self.criteriaColums), nbCrit):
            (master, x, y) = self.dataTabView.getViewCData()
            self.dataTabView.shiftRight()
            c = self.dataTabModel.getCriterion(i)
            cc = CriterionColumn(master=master, criterion=c)
            cc.show(x,y)
            self.criteriaColums.append(cc)
        nbAlt = self.dataTabModel.getNumberOfAlternatives()
        for j in range(len(self.unitsRows), nbAlt):
            (master, x, y) = self.dataTabView.getViewUData()
            self.dataTabView.shiftDown()
            a = self.dataTabModel.getAlternative(j)
            ur = UnitRow(master=master, x=x, y=y, alternative=a)
            ur.show()
            self.unitsRows.append(ur)


    def addCriterionColumn(self, master, x:int, y:int) -> None:
        """Add a criterion and its column in the data table

        Parameters
        ----------
        master : CTkFrame
            the master frame for the data tab
        x : int
            the x coordinate to place the new criterion column
        y : int
            the y coordinate to place the new criterion column
        """
        self.dataTabView.shiftRight()
        self.dataTabModel.addCriterion(master=master)
        c = self.dataTabModel.getCriterion()
        cc = CriterionColumn(master=master, criterion=c)
        cc.show(x, y)
        self.criteriaColums.append(cc)
        self.addOneColumnToAllUnits(master=master)

    
    def deleteCriterion(self) -> None:
        """Delete the last criterion and its column in the data table
        """
        if(len(self.criteriaColums) >= 1):
            self.criteriaColums[-1].destroy()
            self.criteriaColums.pop()
            self.dataTabModel.deleteCriterion()
            self.dataTabView.shiftLeft()
            self.deleteOneColumnInAllUnits()
        
    
    def addUnitRow(self, master, x: int, y: int) -> None:
        """Add an alternative (a unit) and its row in the data table

        Parameters
        ----------
        master : CTkFrame
            the master frame for the data tab
        x : int
            the x coordinate to place the new unit row
        y : int
            the y coordinate to place the new unit row
        """
        self.dataTabView.shiftDown()
        self.dataTabModel.addAlternative(master)
        a = self.dataTabModel.getAlternative()
        ur = UnitRow(master=master, x=x, y=y, alternative=a)
        ur.show()
        self.unitsRows.append(ur)


    def deleteUnit(self) -> None:
        """Delete an alternative (a unit) and its row in the data table
        """
        if(len(self.unitsRows) >= 1):
            self.unitsRows[-1].destroy()
            self.unitsRows.pop()
            self.dataTabModel.deleteAlternative()
            self.dataTabView.shiftUp()


    def addOneColumnToAllUnits(self, master) -> None:
        """Add a column to the row of all alternatives

        This method must be called after adding a criterion if there is at least one alternative in the data table

        Parameters
        ----------
        master : CTkFrame
            the master frame for the data tab
        """
        self.dataTabModel.addOneEvaluationInAllAlternatives(master=master)
        for i in range(len(self.unitsRows)):
            value = self.dataTabModel.getEvaluationOfAlternative(indexAlt=i, indexEval=-1)
            self.unitsRows[i].add_column(value=value)


    def deleteOneColumnInAllUnits(self) -> None:
        """Delete a column in the row of all alternatives

        This method must be called after deleting a criterion if there is at least one alternative in the data table
        """
        for i in range(len(self.unitsRows)):
            self.unitsRows[i].del_column()
            self.dataTabModel.deleteEvaluationOfAlternative(indexAlt=i, indexEval=-1)


    def clearTable(self) -> None:
        """Clear the data table
        """
        while(len(self.criteriaColums)>0):
            self.deleteCriterion()
        while(len(self.unitsRows)>0):
            self.deleteUnit()


    def getModel(self) -> DataTabModel:
        """Return the current dataTabModel

        Return
        ------
        dataTabModel : DataTabModel
        """
        return self.dataTabModel
    
    def voidModel(self) -> bool:
        """Test if model has no alternative or no criterion

        Return
        ------
        True if no alternative or no criterion, False otherwise
        """
        return self.dataTabModel.isVoid()
    

    def twoAlterInModel(self):
        return self.dataTabModel.twoAlter()
