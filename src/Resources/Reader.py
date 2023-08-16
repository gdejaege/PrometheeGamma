#from Controllers.DataTabControllers.DataTabController import DataTabController
#from Models.DataTabModel import DataTabModel
#from Models.PrometheeGamma import PrometheeGamma
#from Models.ResultTabModel import ResultTabModel

class Reader:
    def readCsv(self, file, master, dataModel, controller):
        """Read a csv file and add its content in the model

        Parameters
        ----------
        file : IO
            file descriptor of the input file
        master : CTkFrame
            the master frame for the data tab. It is needed to link DoubleVar, IntVar and StringVar used to store data
        """
        controller.clearTable()
        self.readData(file, master, dataModel)
        controller.fillDataTable()


    def readProject(self, file, dataMaster, dataModel, dataController, resultTabModel=None):
        for line in file:
            line = line.strip()
            if line == "Data":
                file.readline()
                dataController.clearTable()
                self.readData(file=file, master=dataMaster, dataModel=dataModel)
                dataController.fillDataTable()
            elif line == "Parameters" and resultTabModel is not None:
                file.readline()
                self.readParameters(file=file, model=resultTabModel)


    def readData(self, file, master, dataModel):
        criteriaP = None
        criteriaQ = None
        for line in file:
            line = line.strip()
            if line == "":
                break
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
                dataModel.createAlternative(master, temp[0], temp[1:])
        dataModel.createCriteria(master, criteriaNames, criteriaWeights, criteriaPreferenceFunctionType, criteriaP, criteriaQ)


    def readParameters(self, file, model):
        for line in file:
            line = line.strip()
            if line == "":
                break
            temp = line.split(" ")
            val = float(temp[-1])
            if temp[0] == "I":
                model.setTi(val)
            elif temp[0] == "J":
                model.setTj(val)
            elif temp[0] == "P":
                model.setPf(val)