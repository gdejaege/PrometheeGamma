import os


class Reader:
    """
    A class to handle reading operation in PROMETHEE Gamma GUI app
    """

    def readData(self, file, master, dataModel):
        """Read a data file and store readed data in data tab model

        Parameters
        ----------
        file : io
            the data file
        master : CTkFrame
            the data tab master frame
        dataModel : DataTabModel
            the data tab model

        Raises
        ------
        ValueError
            if a ValueError occurs in converting str to float or int
        """
        error = False
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
                try:
                    dataModel.createAlternative(master, temp[0], temp[1:])
                except ValueError:
                    error = True
        try:
            dataModel.createCriteria(master, criteriaNames, criteriaWeights, criteriaPreferenceFunctionType, criteriaP, criteriaQ)
        except ValueError:
            error = True
        finally:
            if error:
                raise ValueError()


    def readParameters(self, file, model):
        """Read a file with parameters of PROMETHEE Gamma method and store parameters in the result tab model

        Parameters
        ----------
        file : io
            the results file
        model : ResultTabModel
            the result tab model
        """
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


    def readTxt(self, filename:str):
        """Open a .txt file, read and return its content

        Parameters
        ----------
        filename : str
            the .txt file name

        Returns
        -------
        str
            the content of the .txt file
        """
        if os.path.exists(filename):
            file = open(filename, encoding="UTF-8")
            text = ""
            for line in file:
                text += line.strip() + "\n"
        else:
            raise FileNotFoundError()
        return text
        