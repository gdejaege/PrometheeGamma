from Criterion import Criterion


class PrometheeGamma:
    """
    This class is the main class of the Promethee Gamma method. It computes different matrix needed,
    such as the gamma matrix and the matrix of results
    """
    def __init__(self) -> None:
        # self.units = []  # the list of Units
        self.criteria = []  # the list of criteria
        self.T_i = 0.0
        self.T_j = 0.0
        self.P_f = 1.0
        self.units = []

        self.gamma_matrix = []
        """
        gamma_matrix = [ [g11, g12, ... , g1j, ... , g1n]
                         [g21, g22, ... , g2j, ... , g2n]
                         [...]
                         [gi1, gi2, ... , gij , ..., gin]
                         [...]
                         [gn1, gn2, ... , gnj, ... , gnn] ]
        where g = gamma ; n = number of units ; i and j the index of the matrix
        """

        self.matrix_I = []
        self.matrix_J = []
        self.matrix_Pij = []
        self.matrix_Pji = []

        self.matrix_results =[]

        self.scores = {}


    def add_unit(self, name) -> None:
        """
        Add a unit
        """
        self.units.append(name)
        self.scores[name] = 0


    def get_alternatives(self) -> list:
        """
        Get the list of alternatives
        """
        return self.units


    def add_criterion(self, criterion:Criterion) -> None:
        """
        Add a new criterion at the end of the criteria list
        """
        self.criteria.append(criterion)
    

    def insert_criterion(self, criterion:Criterion, index:int) -> None:
        """
        Insert a new criterion at the given index
        """
        self.criteria.insert(index, criterion)
    

    def del_criterion(self, index=-1) -> None:
        """
        Delete the criterion of the given index. If no index is given, delete the last criterion of the list.
        """
        self.criteria.pop(index)


    def get_criteria(self) -> list:
        """
        Get the criteria list
        """
        return self.criteria


    def clear(self) -> None:
        """
        Clear all the data of the method
        """
        self.units.clear()
        self.criteria.clear()
        self.gamma_matrix.clear()
        self.matrix_I.clear()
        self.matrix_J.clear()
        self.matrix_Pij.clear()
        self.matrix_Pji.clear()
        self.matrix_results.clear()
        self.scores.clear()


    def set_T_i(self, t) -> None:
        """
        Set the value of the indifference threshold
        """
        self.T_i = t
    

    def set_T_j(self, t) -> None:
        """
        Set the value of the incomparability threshold
        """
        self.T_j = t
    

    def set_P_f(self, p) -> None:
        """
        Set the value of the global preference factor
        """
        self.P_f = p


    def build_gamma_matrix(self) -> None:
        """
        Build the gamma matrix
        """
        for c in self.criteria:
            c.build_pi_c_matrix_and_phi_c_list()
        n = self.criteria[0].get_number_of_units()
        #print(self.criteria[0].print_criterion())
        for i in range(n):
            self.gamma_matrix.append([])
            for j in range(n):
                gamma_ij = 0.0
                for k in range(len(self.criteria)):
                    gamma_ij += self.criteria[k].get_gamma_c_ij(i, j)
                self.gamma_matrix[i].append(gamma_ij)


    def get_gamma_matrix(self) -> list:
        """
        Get the Gamma matrix
        """
        return self.gamma_matrix


    def build_matrix_IPJ(self) -> None:
        self.matrix_I = []
        self.matrix_J = []
        self.matrix_Pij = []
        self.matrix_Pji = []
        for i in range(len(self.gamma_matrix)):
            self.matrix_I.append([])
            self.matrix_J.append([])
            self.matrix_Pij.append([])
            self.matrix_Pji.append([])
            for j in range(len(self.gamma_matrix)):
                gij = self.gamma_matrix[i][j]
                gji = self.gamma_matrix[j][i]
                self.matrix_I[i].append(self.T_i - max(gij, gji))
                self.matrix_Pij[i].append((gij - gji)/self.P_f)
                self.matrix_Pji[i].append((gji - gij)/self.P_f)
                self.matrix_J[i].append(min(gij, gji)-self.T_j)


    def build_matrix_I(self) -> None:
        self.matrix_I = []
        for i in range(len(self.gamma_matrix)):
            self.matrix_I.append([])
            for j in range(len(self.gamma_matrix)):
                gij = self.gamma_matrix[i][j]
                gji = self.gamma_matrix[j][i]
                self.matrix_I[i].append(self.T_i - max(gij, gji))


    def build_matrix_J(self) -> None:
        self.matrix_J = []
        for i in range(len(self.gamma_matrix)):
            self.matrix_J.append([])
            for j in range(len(self.gamma_matrix)):
                gij = self.gamma_matrix[i][j]
                gji = self.gamma_matrix[j][i]
                self.matrix_J[i].append(min(gij, gji)-self.T_j)


    def build_matrix_P(self) -> None:
        self.matrix_Pij = []
        self.matrix_Pji = []
        for i in range(len(self.gamma_matrix)):
            self.matrix_Pij.append([])
            self.matrix_Pji.append([])
            for j in range(len(self.gamma_matrix)):
                gij = self.gamma_matrix[i][j]
                gji = self.gamma_matrix[j][i]
                self.matrix_Pij[i].append((gij - gji)/self.P_f)
                self.matrix_Pji[i].append((gji - gij)/self.P_f)


    def get_matrix_I(self) -> list:
        return self.matrix_I


    def get_matrix_Pij(self) -> list:
        return self.matrix_Pij


    def get_matrix_Pji(self) -> list:
        return self.matrix_Pji


    def get_matrix_J(self) -> list:
        return self.matrix_J


    def final(self) -> None:
        """
        ai Iγ aj ⇔ Iij ≥ max(Pij , Pji, Iij , Jij ), \n
        ai Jγ aj ⇔ Jij ≥ max(Pij , Pji, Iij , Jij ), \n
        ai Pγ aj ⇔ Pij ≥ max(Pij , Pji, Iij , Jij ), \n
        aj Pγ ai ⇔ Pji ≥ max(Pij , Pji, Iij , Jij )
        """
        for k in self.scores.keys():
            self.scores[k] = 0
        self.matrix_results = []
        for i in range(len(self.units)):
            self.matrix_results.append([])
            for j in range(len(self.units)):
                Iij = self.matrix_I[i][j]
                Jij = self.matrix_J[i][j]
                Pij = self.matrix_Pij[i][j]
                Pji = self.matrix_Pji[i][j]
                ai = self.units[i]
                aj = self.units[j]
                if(Iij >= max(Pij , Pji, Iij , Jij )):
                    self.matrix_results[i].append(ai + " I " + aj)
                elif(Jij >= max(Pij , Pji, Iij , Jij )):
                    self.matrix_results[i].append(ai + " J " + aj)
                elif(Pij >= max(Pij , Pji, Iij , Jij )):
                    self.matrix_results[i].append(ai + " P " + aj)
                    self.scores[ai] += 1
                elif(Pji >= max(Pij , Pji, Iij , Jij )):
                    self.matrix_results[i].append(aj + " P " + ai)


    def get_matrix_results(self) -> list:
        """
        Get the matrix of results of the Promethee Gamma method
        """
        return self.matrix_results
    

    def get_scores(self) -> dict:
        """
        Get the scores of the alternatives
        """
        return self.scores


