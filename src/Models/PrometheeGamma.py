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
        self.scores = {}

        self.dataTabModel = None
        self.resultTabModel = None


    def setDataTabModel(self, model:DataTabModel):
        self.dataTabModel = model


    def setResultTabModel(self, model:ResultTabModel):
        self.resultTabModel = model

    
    def clear(self) -> None:
        """
        Clear all data
        """
        self.matrixGamma.clear()
        self.matrixI.clear()
        self.matrixJ.clear()
        self.matrixP.clear()
        self.matrixResults.clear()
        self.scores.clear()


    def build_matrixGamma(self) -> None:
        """
        Build the gamma matrix
        """
        nbAlternatives = self.dataTabModel.getNumberOfAlternatives()
        nbCriteria = self.dataTabModel.getNumberOfCriteria()
        for i in range(nbAlternatives):
            self.matrixGamma.append([])
            for j in range(nbAlternatives):
                gamma_ij = 0.0
                for k in range(nbCriteria):
                    gamma_ij += self.dataTabModel.getGamma_ij_Criteria_k(i=i, j=j, criteria=k)
                self.matrixGamma[i].append(gamma_ij)


    def build_matrix_IPJ(self) -> None:
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


    def build_matrix_I(self) -> None:
        Ti = self.resultTabModel.getTi_float()
        for i in range(len(self.matrixGamma)):
            self.matrixI.append([])
            for j in range(len(self.matrixGamma)):
                gij = self.matrixGamma[i][j]
                gji = self.matrixGamma[j][i]
                self.matrixI[i].append(Ti - max(gij, gji))


    def build_matrix_J(self) -> None:
        Tj = self.resultTabModel.getTj_float()
        for i in range(len(self.matrixGamma)):
            self.matrixJ.append([])
            for j in range(len(self.matrixGamma)):
                gij = self.matrixGamma[i][j]
                gji = self.matrixGamma[j][i]
                self.matrixJ[i].append(min(gij, gji) - Tj)


    def build_matrix_P(self) -> None:
        Pf = self.resultTabModel.getPf_float()
        for i in range(len(self.matrixGamma)):
            self.matrixP.append([])
            for j in range(len(self.matrixGamma)):
                gij = self.matrixGamma[i][j]
                gji = self.matrixGamma[j][i]
                self.matrixP[i].append((gij - gji)/Pf)


    def computeResults(self) -> None:
        """
        ai Iγ aj ⇔ Iij ≥ max(Pij , Pji, Iij , Jij ), \n
        ai Jγ aj ⇔ Jij ≥ max(Pij , Pji, Iij , Jij ), \n
        ai Pγ aj ⇔ Pij ≥ max(Pij , Pji, Iij , Jij ), \n
        aj Pγ ai ⇔ Pji ≥ max(Pij , Pji, Iij , Jij )
        """
        alternativesName = self.dataTabModel.getAlternativesName()
        self.resultTabModel.initScores(alternativesName)
        nbAlternatives = self.dataTabModel.getNumberOfAlternatives()
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


    def computeAll(self):
        self.build_matrixGamma()
        self.build_matrix_IPJ()
        self.computeResults()