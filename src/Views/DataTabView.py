from customtkinter import (CTkButton, CTkLabel)
#from Controllers.DataTabController import DataTabController
from Views.SubViews.CriterionColumn import CriterionColumn
from Views.SubViews.UnitRow import UnitRow

class DataTabView:
    def __init__(self, master, listener) -> None:
        self.master = master
        self.listener = listener

        self.xc = 191
        self.yc = 125
        self.xu = 50
        self.yu = 275
        self.criteria = []
        self.units = []

        self.openFileButton = CTkButton(master=self.master, text="Open a file", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.openFile)
        self.dataNoteLabel = CTkLabel(self.master, text="Only csv files are accepted", fg_color="#ffffff", text_color="#000000", corner_radius=5)

        self.criteriaLabel = CTkLabel(master=self.master, text="Criteria:", text_color="#000000")
        self.weightsLabel = CTkLabel(master=self.master, text="Weights:", text_color="#000000")
        self.typesLabel = CTkLabel(master=self.master, text="Preference Function:", text_color="#000000")
        self.pcLabel = CTkLabel(master=self.master, text="Pc:", text_color="#000000")
        self.qcLabel = CTkLabel(master=self.master, text="Qc:", text_color="#000000")
        self.buttonAddCriterion = CTkButton(master=self.master, text="Add a criterion", command=self.addCriterion)
        self.buttonAddUnit = CTkButton(master=self.master, text="Add an alternative", command=self.addUnit)
        self.buttonDeleteCriterion = CTkButton(master=self.master, text="Delete a criterion", command=self.deleteCriterion)
        self.buttonDeleteUnit = CTkButton(master=self.master, text="Delete an alternative", command=self.deleteUnit)


    def show(self) -> None:
        self.openFileButton.place(relx=0.5, y=25, anchor='center')
        self.dataNoteLabel.place(relx=0.5, y=75, anchor='center')

        self.criteriaLabel.place(x=self.xu, y=self.yc)
        self.weightsLabel.place(x=self.xu, y=self.yc+25)
        self.typesLabel.place(x=self.xu, y=self.yc+50)
        self.pcLabel.place(x=self.xu, y=self.yc+75)
        self.qcLabel.place(x=self.xu, y=self.yc+100)
        self.buttonAddCriterion.place(x=self.xc, y=self.yc)
        self.buttonAddUnit.place(x=self.xu, y=self.yu)
        self.buttonDeleteCriterion.place(x=self.xc, y=self.yc+25)
        self.buttonDeleteUnit.place(x=self.xu+141, y=self.yu)


    def openFile(self) -> None:
            self.listener.openFile()

    
    def addCriterion(self) -> None:
        self.xc += 141
        self.listener.addCriterionColumn()
        self.buttonAddCriterion.place(x=self.xc+150, y=self.yc)
        self.buttonDeleteCriterion.place(x=self.xc+150, y=self.yc+25)


    def addUnit(self) -> None:
        self.yu += 25
        self.listener.addUnitRow()
        self.buttonAddUnit.place(x=self.xu, y=self.yu+30)
        self.buttonDeleteUnit.place(x=self.xu+141, y=self.yu+30)


    def deleteCriterion(self) -> None:
        self.criteria[-1].destroy()
        self.criteria.pop()
        self.xc -= 141
        for i in range(len(self.units)):
            self.units[i].deleteColumn()
        self.buttonAddCriterion.place(x=self.xc+150, y=self.yc)
        self.buttonDeleteCriterion.place(x=self.xc+150, y=self.yc+25)


    def deleteUnit(self) -> None:
        self.units[-1].destroy()
        self.units.pop()
        self.yu -= 25
        self.buttonAddUnit.place(x=self.xu, y=self.yu+30)
        self.buttonDeleteUnit.place(x=self.xu+141, y=self.yu+30)


    class ViewListener:
        def openFile(self):
            pass
        def addCriterionColumn(self):
            pass
        def addUnitRow(self):
            pass