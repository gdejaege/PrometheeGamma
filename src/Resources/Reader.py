
class Reader:
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
            if line == "Parameters" or line == "parameters" or line == "PARAMETERS" or line == "Parameter" or line == "parameter" or line == "PARAMETER":
                file.readline()
                for line in file:
                    line = line.strip()
                    if line == "":
                        return
                    temp = line.split(" ")
                    val = float(temp[-1])
                    if temp[0] == "I":
                        model.setTi(val)
                    elif temp[0] == "J":
                        model.setTj(val)
                    elif temp[0] == "P":
                        model.setPf(val)