from tkinter import filedialog as fd
from Models.DataTabModel import DataTabModel
from Views.DataTabViews.DataTabView import DataTabView
from Views.DataTabViews.CriterionColumn import CriterionColumn
from Views.DataTabViews.UnitRow import UnitRow

class DataTabController(DataTabView.ViewListener):
    """
    Controller of the data tab
    """
    def __init__(self, master) -> None:
        """
        Constructor
        """
        self.dataTabModel = DataTabModel()
        self.dataTabView = DataTabView(master=master, listener=self)
        self.criteriaColums = []
        self.unitsRows = []

    def showView(self) -> None:
        """
        show the dataTabView
        """
        self.dataTabView.show()
        

    def openFile(self, master) -> None:
        """
        Open a file selected by the user, read its content and close it
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
            tkinter master frame
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
        """
        fill in the data table with the content of the models
        """
        nbCrit = self.dataTabModel.getNumberOfCriteria()
        for i in range(len(self.criteriaColums), nbCrit):
            (master, x, y) = self.dataTabView.getViewCData()
            self.dataTabView.shiftRight()
            c = self.dataTabModel.getCriterion(i)
            cc = CriterionColumn(master=master, x=x, y=y, criterion=c)
            self.criteriaColums.append(cc)
        nbAlt = self.dataTabModel.getNumberOfAlternatives()
        for j in range(len(self.unitsRows), nbAlt):
            (master, x, y) = self.dataTabView.getViewUData()
            self.dataTabView.shiftDown()
            a = self.dataTabModel.getAlternative(j)
            ur = UnitRow(master=master, x=x, y=y, alternative=a)
            self.unitsRows.append(ur)


    def addCriterionColumn(self, master, x:int, y:int) -> None:
        """
        Add a criterion and its column in the data table.
        x and y are the coordinates of the new column.
        """
        self.dataTabView.shiftRight()
        self.dataTabModel.addCriterion(master=master)
        c = self.dataTabModel.getCriterion()
        cc = CriterionColumn(master=master, criterion=c)
        cc.show(x, y)
        self.criteriaColums.append(cc)
        self.addOneColumnToAllUnits(master=master)

    
    def deleteCriterion(self) -> None:
        """
        delete the last criterion and its column in the data table.
        """
        if(len(self.criteriaColums) >= 1):
            self.criteriaColums[-1].destroy()
            self.criteriaColums.pop()
            self.dataTabModel.deleteCriterion()
            self.dataTabView.shiftLeft()
            self.deleteOneColumnInAllUnits()
        
    
    def addUnitRow(self, master, x: int, y: int) -> None:
        """
        Add an alternative (a unit) and its row in the data table.
        x and y are the coordinates of the new row.
        """
        self.dataTabView.shiftDown()
        self.dataTabModel.addAlternative(master)
        a = self.dataTabModel.getAlternative()
        ur = UnitRow(master=master, x=x, y=y, alternative=a)
        self.unitsRows.append(ur)


    def deleteUnit(self) -> None:
        """
        Delete an alternative (a unit) and its row in the data table
        """
        if(len(self.unitsRows) >= 1):
            self.unitsRows[-1].destroy()
            self.unitsRows.pop()
            self.dataTabModel.deleteAlternative()
            self.dataTabView.shiftUp()


    def addOneColumnToAllUnits(self, master) -> None:
        """
        Add a column to the row of all alternatives.
        This method must be called after adding a criterion if there is at least one alternative in the data table.
        """
        self.dataTabModel.addOneEvaluationInAllAlternatives(master=master)
        for i in range(len(self.unitsRows)):
            value = self.dataTabModel.getEvaluationOfAlternative(indexAlt=i, indexEval=-1)
            self.unitsRows[i].add_column(value=value)


    def deleteOneColumnInAllUnits(self) -> None:
        """
        Delete a column in the row of all alternatives.
        This method must be called after deleting a criterion if there is at least one alternative in the data table.
        """
        for i in range(len(self.unitsRows)):
            self.unitsRows[i].del_column()
            self.dataTabModel.deleteEvaluationOfAlternative(indexAlt=i, indexEval=-1)


    def clearTable(self) -> None:
        """
        Clear the data table
        """
        while(len(self.criteriaColums)>0):
            self.deleteCriterion()
        while(len(self.unitsRows)>0):
            self.deleteUnit()


    def getModel(self) -> DataTabModel:
        """
        Return the current dataTabModel
        """
        return self.dataTabModel