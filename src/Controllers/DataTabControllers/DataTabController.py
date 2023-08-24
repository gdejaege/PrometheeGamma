from tkinter import filedialog as fd
import os
from Models.DataTabModel import DataTabModel
from Views.DataTabViews.DataTabView import DataTabView
from Views.DataTabViews.CriterionColumn import CriterionColumn
from Views.DataTabViews.UnitRow import UnitRow
from Resources.Reader import Reader

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
    no2AlterInModel(self):
        test if there is less than 2 alternatives in the model
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
        if not os.path.exists("../Data"):
            if not os.path.exists("../Projects"):
                os.makedirs("../Projects")
            directory = "../Projects"
        else:
            directory = "../Data"
        filename = fd.askopenfilename(filetypes=(("csv file", "*.csv"), ("csv file", "*.csv")), initialdir=directory)
        self.loadData(filename, master)

    
    def loadData(self, filename, master):
        self.clearTable()
        file = open(filename, "r")
        r = Reader()
        r.readData(file, master, self.dataTabModel)
        file.close()
        self.fillDataTable()


    def fillDataTable(self) -> None:
        """Fill in the data table with the content of the models
        """
        nbCrit = self.dataTabModel.getNumberOfCriteria()
        for i in range(len(self.criteriaColums), nbCrit):
            (master, row, col) = self.dataTabView.getViewCData()
            self.dataTabView.shiftRight()
            c = self.dataTabModel.getCriterion(i)
            cc = CriterionColumn(master=master, criterion=c)
            cc.show(row,col)
            self.criteriaColums.append(cc)
        nbAlt = self.dataTabModel.getNumberOfAlternatives()
        for j in range(len(self.unitsRows), nbAlt):
            (master, row, col) = self.dataTabView.getViewUData()
            self.dataTabView.shiftDown()
            a = self.dataTabModel.getAlternative(j)
            ur = UnitRow(master=master, row=row, col=col, alternative=a)
            ur.show()
            self.unitsRows.append(ur)


    def addCriterionColumn(self, master, row:int, col:int) -> None:
        """Add a criterion and its column in the data table

        Parameters
        ----------
        master : CTkFrame
            the master frame for the data tab
        row : int
            the row for grid coordinate to place the new criterion column
        col : int
            the column for grid coordinate to place the new criterion column
        """
        self.dataTabView.shiftRight()
        self.dataTabModel.addCriterion(master=master)
        c = self.dataTabModel.getCriterion()
        cc = CriterionColumn(master=master, criterion=c)
        cc.show(row, col)
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
        
    
    def addUnitRow(self, master, row: int, col: int) -> None:
        """Add an alternative (a unit) and its row in the data table

        Parameters
        ----------
        master : CTkFrame
            the master frame for the data tab
        row : int
            the row for grid coordinate to place the new unit row
        col : int
            the column for grid coordinate to place the new unit row
        """
        self.dataTabView.shiftDown()
        self.dataTabModel.addAlternative(master)
        a = self.dataTabModel.getAlternative()
        ur = UnitRow(master=master, row=row, col=col, alternative=a)
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
        self.dataTabModel.clearAll()


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
    

    def no2AlterInModel(self):
        """Test if there is less than 2 alternatives in the model

        Return
        ------
        True if there is less than 2 alternatives in the model, False otherwise
        """
        return self.dataTabModel.twoAlter()
    

    def save(self, folder):
        filename = folder + '/' + "Data.csv"
        file = open(filename, mode="w", encoding="UTF-8")

        nbCriteria = self.dataTabModel.getNumberOfCriteria()
        nbAlternatives = self.dataTabModel.getNumberOfAlternatives()

        line = "c"
        for i in range(nbCriteria):
            line += "," + self.dataTabModel.getCriterion(i).getName_str()
        file.write(line+"\n")

        for j in range(nbAlternatives):
            alternative = self.dataTabModel.getAlternative(j)
            line = alternative.getName_str()
            for k in range(nbCriteria):
                line += "," + str(alternative.getEvaluation_float(k))
            file.write(line+"\n")

        line = "w"
        for l in range(nbCriteria):
            line += "," + str(self.dataTabModel.getCriterion(l).getWeight_float())
        file.write(line+"\n")

        line = "f"
        for m in range(nbCriteria):
            line += "," + str(self.dataTabModel.getCriterion(m).getPf_int())
        file.write(line+"\n")

        line = "p"
        for n in range(nbCriteria):
            line += "," + str(self.dataTabModel.getCriterion(n).getP_float())
        file.write(line+"\n")

        line = "q"
        for o in range(nbCriteria):
            line += "," + str(self.dataTabModel.getCriterion(o).getQ_float())
        file.write(line+"\n")

        file.close()


    def reset(self):
        self.clearTable()