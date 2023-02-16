from PreferenceFunction import PreferenceFunction

class Criterion:
    """
    Class to represent a criterion of the Promethee Gamma method.
    """
    def __init__(self, name=None, weight=0.0) -> None:
        self.name = name
        self.weight = weight
        self.preference_function = PreferenceFunction()  # init the preference function
        self.pi_c_matrix = []
        """
        pi_c_ij = F_c(d_c(unit_i - unit_j))
        """
        self.phi_c_list = []
        """
        phi_c_i = (1/n-1) * S_{j=1}^{n} (pi_c_ij - pi_c_ji)
        """
        self.column = []


    def set_pf(self, type=None, pc=None, qc=None) -> None:
        """
        Set the preference function
        """
        if(type != None):
            self.preference_function.set_type(type)
            self.preference_function.set_pc(pc)
            self.preference_function.set_qc(qc)


    def set_name(self, n:str) -> None:
        """
        Set the name of the criterion
        """
        self.name = n


    def set_weight(self, w:float) -> None:
        """
        Set the weight of the criterion
        """
        self.weight = w


    def get_name(self) -> str:
        """
        Get the name of the criterion
        """
        return self.name


    def get_weight(self) -> float:
        """
        Get the weight of the criterion
        """
        return self.weight


    def get_pf(self) -> PreferenceFunction:
        """
        Get the preference function
        """
        return self.preference_function
    

    def add_unit(self, val) -> None:
        """
        Add a unit
        """
        self.column.append(val)


    def insert_unit(self, val, index) -> None:
        """
        Insert a unit at the given index
        """
        self.column.insert(index, val)


    def del_unit(self, index=-1) -> None:
        """
        Delete the unit at the given index. If no index is given, delete the last unit
        """
        self.column.pop(index)


    def get_number_of_units(self) -> int:
        """
        Get the number of units
        """
        return len(self.column)


    def build_pi_c_matrix_and_phi_c_list(self) -> None:
        """
        Build the pi matrix and the phi list of the criterion, 
        """
        for i in range(len(self.column)):
            self.pi_c_matrix.append([])
            for j in range(len(self.column)):
                pi_c_ij = self.preference_function.compute_preference(self.column[i] - self.column[j])
                self.pi_c_matrix[i].append(pi_c_ij)
        self.build_phi_c_list()


    def build_phi_c_list(self) -> None:
        """
        Build the phi list that corresponds to the criterion
        """
        for i in range(len(self.column)):
            phi_c_i = 0.0
            for j in range(len(self.column)):
                phi_c_i += (self.pi_c_matrix[i][j] - self.pi_c_matrix[j][i])
            phi_c_i *= 1/(len(self.column)-1)
            self.phi_c_list.append(phi_c_i)


    def get_phi_c_list(self) -> list:
        """
        Get the phi list of the criterion
        """
        return self.phi_c_list


    def get_gamma_c_ij(self, i:int, j:int) -> float:
        """
        Get the value of Gamma c ij
        """
        val = 0.0
        if(self.column[i]>self.column[j]):
            val = self.weight*(self.phi_c_list[i] - self.phi_c_list[j])
        return val


    def print_criterion(self) -> None:
        """
        Print all information about the criterion
        """
        print("\nCRITERION:")
        print("name =", self.name, "weigt=", self.weight)
        print("column =", self.column)
        print("pi_c_matrix =", self.pi_c_matrix)
        print("phi_c_list =", self.phi_c_list)
        print("\nPREFERENCE FUNCTION:")
        self.preference_function.print_p_fun()