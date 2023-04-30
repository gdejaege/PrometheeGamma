from Models.DataTabModel import DataTabModel
from Models.ResultTabModel import ResultTabModel

class PrometheeGamma:
    """
    This class is the main class of the Promethee Gamma method. It computes different matrix needed,
    such as the gamma matrix and the matrix of results
    """
    def __init__(self) -> None:
        self.matrixGamma = []
        """
        matrixGamma = [ [γ11, γ12, ... , γ1j, ... , γ1n]
                         [γ21, γ22, ... , γ2j, ... , γ2n]
                         [...]
                         [γi1, γi2, ... , γij , ..., γin]
                         [...]
                         [γn1, γn2, ... , γnj, ... , γnn] ]
        where n = number of alternatives ; i and j the index of the matrix
        """
        self.matrixI = []
        self.matrixJ = []
        self.matrixP = []
        self.matrixResults = []

        self.dataTabModel = None
        self.resultTabModel = None


    def setDataTabModel(self, model:DataTabModel) -> None:
        """
        Change the dataTabModel
        """
        self.dataTabModel = model


    def setResultTabModel(self, model:ResultTabModel) -> None:
        """
        Change the ResultTabModel
        """
        self.resultTabModel = model


    def getMatrixGamma(self) -> list:
        """
        Return the Gamma Matrix
        """
        return self.matrixGamma
    

    def getMatrixResults(self) -> list:
        """
        Return the matrix of results
        """
        return self.matrixResults

    
    def clearMatrixIJP(self) -> None:
        """
        Clear matrixI, matrixJ and matrixP
        """
        self.matrixI.clear()
        self.matrixJ.clear()
        self.matrixP.clear()


    def computeGammaMatrix(self) -> None:
        """
        Compute the gamma matrix
        """
        self.dataTabModel.computeCriterionDependentValues()
        self.matrixGamma.clear()
        nbAlternatives = self.dataTabModel.getNumberOfAlternatives()
        nbCriteria = self.dataTabModel.getNumberOfCriteria()
        for i in range(nbAlternatives):
            self.matrixGamma.append([])
            for j in range(nbAlternatives):
                gamma_ij = 0.0
                for k in range(nbCriteria):
                    gamma_ij += self.dataTabModel.getGamma_ij_Criteria_k(i=i, j=j, criterion=k)
                self.matrixGamma[i].append(gamma_ij)


    def ComputeMatrixIJP(self) -> None:
        """
        Compute matrixI, matrixJ and matrixP
        """
        self.clearMatrixIJP()
        Ti = self.resultTabModel.getTi_float()
        Tj = self.resultTabModel.getTj_float()
        Pf = self.resultTabModel.getPf_float()
        for i in range(len(self.matrixGamma)):
            self.matrixI.append([])
            self.matrixJ.append([])
            self.matrixP.append([])
            for j in range(len(self.matrixGamma)):
                gij = self.matrixGamma[i][j]
                gji = self.matrixGamma[j][i]
                self.matrixI[i].append(Ti - max(gij, gji))
                self.matrixP[i].append((gij - gji)/Pf)
                self.matrixJ[i].append(min(gij, gji) - Tj)


    def computeMatrixI(self) -> None:
        """
        Compute the matrixI only
        """
        self.matrixI.clear()
        Ti = self.resultTabModel.getTi_float()
        for i in range(len(self.matrixGamma)):
            self.matrixI.append([])
            for j in range(len(self.matrixGamma)):
                gij = self.matrixGamma[i][j]
                gji = self.matrixGamma[j][i]
                self.matrixI[i].append(Ti - max(gij, gji))


    def computeMatrixJ(self) -> None:
        """
        Compute the matrixJ only
        """
        self.matrixI.clear()
        Tj = self.resultTabModel.getTj_float()
        for i in range(len(self.matrixGamma)):
            self.matrixJ.append([])
            for j in range(len(self.matrixGamma)):
                gij = self.matrixGamma[i][j]
                gji = self.matrixGamma[j][i]
                self.matrixJ[i].append(min(gij, gji) - Tj)


    def computeMatrixP(self) -> None:
        """
        Compute the matrixP only
        """
        self.matrixP.clear()
        Pf = self.resultTabModel.getPf_float()
        for i in range(len(self.matrixGamma)):
            self.matrixP.append([])
            for j in range(len(self.matrixGamma)):
                gij = self.matrixGamma[i][j]
                gji = self.matrixGamma[j][i]
                self.matrixP[i].append((gij - gji)/Pf)


    def computeMatrixResults(self) -> None:
        """
        Compute the matrix of results \n
        ai Iγ aj ⇔ Iij ≥ max(Pij , Pji, Iij , Jij ), \n
        ai Jγ aj ⇔ Jij ≥ max(Pij , Pji, Iij , Jij ), \n
        ai Pγ aj ⇔ Pij ≥ max(Pij , Pji, Iij , Jij ), \n
        aj Pγ ai ⇔ Pji ≥ max(Pij , Pji, Iij , Jij )
        """
        self.matrixResults.clear()
        alternativesName = self.dataTabModel.getAlternativesName()
        self.resultTabModel.initScores(alternativesName)
        nbAlternatives = len(alternativesName)
        for i in range(nbAlternatives):
            self.matrixResults.append([])
            for j in range(nbAlternatives):
                Iij = self.matrixI[i][j]
                Jij = self.matrixJ[i][j]
                Pij = self.matrixP[i][j]
                Pji = self.matrixP[j][i]
                ai = alternativesName[i]
                aj = alternativesName[j]
                if(Iij >= max(Pij , Pji, Iij , Jij )):
                    self.matrixResults[i].append(ai + " I " + aj)
                elif(Jij >= max(Pij , Pji, Iij , Jij )):
                    self.matrixResults[i].append(ai + " J " + aj)
                elif(Pij >= max(Pij , Pji, Iij , Jij )):
                    self.matrixResults[i].append(ai + " P " + aj)
                    self.resultTabModel.incrementScore(ai)
                elif(Pji >= max(Pij , Pji, Iij , Jij )):
                    self.matrixResults[i].append(aj + " P " + ai)


    def computeAll(self) -> None:
        """
        Compute all matrix
        """
        self.computeGammaMatrix()
        self.ComputeMatrixIJP()
        self.computeMatrixResults()