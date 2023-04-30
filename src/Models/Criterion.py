from customtkinter import (StringVar, IntVar, DoubleVar)
from Models.PreferenceFunction import PreferenceFunction

class Criterion:
    """
    Class to represent a criterion of the PROMETHEE γ method.
    """
    def __init__(self, name:StringVar, weight:DoubleVar, pfType:IntVar=None, p:DoubleVar=None, q:DoubleVar=None) -> None:
        self.name = name
        self.weight = weight
        self.preference_function = PreferenceFunction(type=pfType, p=p, q=q)  # init the preference function
        
        self.pi_c_matrix = []
        """
        self.pi_c_matrix[i][j] = πc_ij = Fc(dc(ai, aj)): "how much ai is preferred over aj on criterion c"
        """
        self.phi_c_list = []
        """
        self.phi_c_list[i] = φc(ai) = (1/n-1) * ∑_{j=1}^{n} (πc_ij - πc_ji)
        """
        self.column = []


    ##################################
    #### Getters and Setters part ####
    ##################################

    def setName(self, n:StringVar) -> None:
        """
        Set the name of the criterion
        """
        self.name = n


    def setWeight(self, w:DoubleVar) -> None:
        """
        Set the weight of the criterion
        """
        self.weight = w


    def getName_str(self) -> str:
        """
        Get the name of the criterion
        """
        return self.name.get()


    def getWeight_float(self) -> float:
        """
        Get the weight of the criterion
        """
        return self.weight.get()


    def getName(self) -> StringVar:
        """
        Return the criterion name in a StringVar object.
        """
        return self.name
    

    def getWeight(self) -> DoubleVar:
        """
        Return the criterion weight in a DoubleVar object.
        """
        return self.weight


    def get_pf(self) -> int:
        """
        Return the type of the preference function.
        """
        return self.preference_function.getType_int()
    

    def getP(self) -> DoubleVar:
        """
        Return the preference threshold of the preference function in a DoubleVar object
        """
        return self.preference_function.getP()
    

    def getQ(self) -> DoubleVar:
        """
        Return the indifference threshold of the preference function in a DoubleVar object
        """
        return self.preference_function.getQ()
    

    def getPf(self) -> IntVar:
        """
        Return the type of the preference function in a IntVar object
        """
        return self.preference_function.getType()


############################################################################################################################

    ########################
    ### Computation part ###
    ########################

    def add_unit(self, val:float) -> None:
        """
        Add a unit value
        """
        self.column.append(val)


    def del_unit(self, index=-1) -> None:
        """
        Delete the unit at the given index. If no index is given, delete the last unit
        """
        self.column.pop(index)


    def clearColumn(self):
        """
        Clear all value in the column
        """
        self.column.clear()


    def build_pi_c_matrix(self) -> None:
        """
        Build the pi matrix and the phi list of the criterion \n
        πc_ij = Fc(dc(ai, aj)): "how much ai is preferred over aj on criterion c" \n
        Fc is the preference function 
        and dc(ai, aj) = fc(ai) - fc(aj ) is the difference between the evaluations of ai and aj on the criterion c
        """
        for i in range(len(self.column)):
            self.pi_c_matrix.append([])
            for j in range(len(self.column)):
                pi_c_ij = self.preference_function.compute_preference(self.column[i] - self.column[j])
                self.pi_c_matrix[i].append(pi_c_ij)


    def build_phi_c_list(self) -> None:
        """
        Build the phi list that corresponds to the criterion \n
        phi list: [φc(a1), φc(a2), ..., φc(ai), ..., φc(an)] where φc(ai): the mono-criterion net flow of ai on criterion c
        and n the number of alternatives
        """
        for i in range(len(self.column)):
            phi_c_i = 0.0
            for j in range(len(self.column)):
                phi_c_i += (self.pi_c_matrix[i][j] - self.pi_c_matrix[j][i])
            phi_c_i *= 1/(len(self.column)-1)
            self.phi_c_list.append(phi_c_i)


    def get_phi_c_list(self) -> list:
        """
        Get the phi list of the criterion \n
        phi list: [φc(a1), φc(a2), ..., φc(ai), ..., φc(an)] where φc(ai): the mono-criterion net flow of ai on criterion c
        and n the number of alternatives
        """
        return self.phi_c_list


    def get_gamma_c_ij(self, i:int, j:int) -> float:
        """
        Get the value of γc_ij \n
        γc_ij = wc · (φc(ai) - φc(aj))
        when fc(ai) > fc(aj) and γc_ij = 0 otherwise,
        where wc is the weight associated to the criterion
        """
        val = 0.0
        weight = self.weight.get()
        if(i < len(self.column) and j < len(self.column)):
            if(self.column[i]>self.column[j]):
                val = weight*(self.phi_c_list[i] - self.phi_c_list[j])
        return val