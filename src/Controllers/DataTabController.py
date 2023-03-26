from tkinter import filedialog as fd
from Models.DataModels.DataTabModel import DataTabModel
from Views.DataTabView import DataTabView
from customtkinter import (StringVar, IntVar, DoubleVar)

class DataTabController(DataTabView.ViewListener):
    def __init__(self, master) -> None:
        self.dataTabModel = DataTabModel()
        self.dataTabView = DataTabView(master=master, listener=self)


    def show(self):
        self.dataTabView.show()
        

    def openFile(self):
        unames = []
        uval = []
        units = []
        file = fd.askopenfile(mode="r", filetypes=(("csv file", "*.csv"), ("all files","*.*")))
        for line in file:
            line = line.strip()
            temp = line.split(',')
            if(temp[0] == 'c'):
                self.dataTabModel.setCiteria(temp[1:])
            elif(temp[0] == 'w'):
                self.dataTabModel.setWeights(temp[1:])
            elif(temp[0] == 'q'):
                self.dataTabModel.setIndifferenceParameters(temp[1:])
            elif(temp[0] == 'p'):
                self.dataTabModel.setPreferenceParameters(temp[1:])
            elif(temp[0] == 'f'):
                self.dataTabModel.setPreferenceFunctionsTypes(temp[1:])
            else:
                unames.append(temp[0])
                uval.append(temp[1:])
                units.append(temp)
        self.dataTabModel.setUnits(units)
        file.close()


    def addCriterionColumn(self):
        pass


    def addUnitRow(self):
        pass