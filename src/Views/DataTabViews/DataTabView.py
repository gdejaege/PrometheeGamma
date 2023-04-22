from customtkinter import (CTkButton, CTkLabel, CTkEntry, StringVar, IntVar, DoubleVar)

class DataTabView:

    class ViewListener:
        def openFile(self):
            pass
        def addCriterionColumn(self, master, x:int, y:int):
            pass
        def addUnitRow(self, master, x:int, y:int):
            pass
        def deleteCriterion(self):
            pass
        def deleteUnit(self):
            pass


    def __init__(self, master, listener:ViewListener) -> None:
        self.master = master
        self.listener = listener

        self.dico_pfTypes = {1:"Usual", 2:"U-shape", 3:"V-shape", 4:"Level", 5:"Linear", 6:"Gaussian"}
        """
        Dictionary of preference function types
        """

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


    def getViewCData(self) ->tuple:
        return (self.master, self.xc, self.yc)


    def getViewUData(self) ->tuple:
        return (self.master, self.xu, self.yu)


    def openFile(self) -> None:
        self.listener.openFile(self.master)


    def addCriterion(self) -> None:
        self.listener.addCriterionColumn(master=self.master, x=self.xc, y=self.yc)

    
    def shiftRight(self):
        self.buttonAddCriterion.place(x=self.xc+150, y=self.yc)
        self.buttonDeleteCriterion.place(x=self.xc+150, y=self.yc+25)
        self.xc += 141


    def shiftLeft(self):
        self.xc -= 141
        self.buttonAddCriterion.place(x=self.xc+9, y=self.yc)
        self.buttonDeleteCriterion.place(x=self.xc+9, y=self.yc+25)


    def shiftUp(self):
        self.yu -= 25
        self.buttonAddUnit.place(x=self.xu, y=self.yu+5)
        self.buttonDeleteUnit.place(x=self.xu+141, y=self.yu+5)


    def shiftDown(self):
        self.yu += 25
        self.buttonAddUnit.place(x=self.xu, y=self.yu+5)
        self.buttonDeleteUnit.place(x=self.xu+141, y=self.yu+5)


    def addUnit(self) -> None:
        self.listener.addUnitRow(master=self.master, x=self.xu, y=self.yu)


    def deleteCriterion(self) -> None:
        self.listener.deleteCriterion()


    def deleteUnit(self) -> None:
        self.listener.deleteUnit()