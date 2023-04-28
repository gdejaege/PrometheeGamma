from tkinter import filedialog as fd
from Models.DataTabModel import DataTabModel
from Views.DataTabViews.DataTabView import DataTabView
from Views.DataTabViews.CriterionColumn import CriterionColumn
from Views.DataTabViews.UnitRow import UnitRow

class DataTabController(DataTabView.ViewListener):
    def __init__(self, master) -> None:
        self.dataTabModel = DataTabModel()
        self.dataTabView = DataTabView(master=master, listener=self)
        self.criteriaColums = []
        self.unitsRows = []

    def showView(self):
        """
        show the dataTabView
        """
        self.dataTabView.show()
        

    def openFile(self, master):
        file = fd.askopenfile(mode="r", filetypes=(("csv file", "*.csv"), ("all files","*.*")))
        self.clearTab()
        self.dataTabModel.readFile(file, master)
        file.close()
        self.fillDataTab()


    def fillDataTab(self):
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


    def addCriterionColumn(self, master, x, y):
        self.dataTabView.shiftRight()
        self.dataTabModel.addVoidCriterion(master)
        c = self.dataTabModel.getCriterion()
        cc = CriterionColumn(master=master, x=x, y=y, criterion=c)
        self.criteriaColums.append(cc)
        self.addOneColumnToAllUnits(master=master)

    
    def deleteCriterion(self):
        if(len(self.criteriaColums) >= 1):
            self.criteriaColums[-1].destroy()
            self.criteriaColums.pop()
            self.dataTabModel.deleteCriterion()
            self.dataTabView.shiftLeft()
            self.deleteOneColumnInAllUnits()
        
    
    def addUnitRow(self, master, x: int, y: int):
        self.dataTabView.shiftDown()
        self.dataTabModel.addVoidAlternative(master)
        a = self.dataTabModel.getAlternative()
        ur = UnitRow(master=master, x=x, y=y, alternative=a)
        self.unitsRows.append(ur)


    def deleteUnit(self):
        if(len(self.unitsRows) >= 1):
            self.unitsRows[-1].destroy()
            self.unitsRows.pop()
            self.dataTabModel.deleteAlternative()
            self.dataTabView.shiftUp()


    def addOneColumnToAllUnits(self, master):
        self.dataTabModel.addOneEvaluationInAllAlternatives(master=master)
        for i in range(len(self.unitsRows)):
            value = self.dataTabModel.getEvaluationOfAlternative(indexAlt=i, indexEval=-1)
            self.unitsRows[i].add_column(value=value)


    def deleteOneColumnInAllUnits(self):
        for i in range(len(self.unitsRows)):
            self.unitsRows[i].del_column()
            self.dataTabModel.deleteEvaluationOfAlternative(indexAlt=i, indexEval=-1)


    def clearTab(self):
        while(len(self.criteriaColums)>0):
            self.deleteCriterion()
        while(len(self.unitsRows)>0):
            self.deleteUnit()


    def getModel(self):
        return self.dataTabModel