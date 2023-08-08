from customtkinter import (StringVar, IntVar, DoubleVar)
from Models.PreferenceFunction import PreferenceFunction

class Criterion:
    """
    Class to represent a criterion of the PROMETHEE γ method and compute values relatives to its column

    Attributes
    ----------
    name : StringVar
        the criterion name
    weight : DoubleVar
        the criterion weight
    preferenceFunction : PreferenceFunction
        the preference function used for this criterion
    pi_c_matrix : list[list[float]]
        the matrix of pi_c_ij (pi_c_matrix[i][j] = πc_ij = Fc(dc(ai, aj)): "how much ai is preferred over aj on criterion c")
    phi_c_list : list[float]
        the list of phi_c_i (phi_c_list[i] = φc(ai) = (1/n-1) * ∑_{j=1}^{n} (πc_ij - πc_ji))
    column : list[float]
        list of alternatives evaluation for this criterion

    Methods
    -------
    setName(newName:StringVar)
        set the name of the criterion
    setWeight(w:DoubleVar)
        set the weight of the criterion
    getName_str()
        return the name of the criterion
    getWeight_float()
        return the weight of the criterion
    getName()
        return the criterion name in a StringVar object
    getWeight()
        return the criterion weight in a DoubleVar object
    getPf_int()
        return the type of the preference function
    getPf()
        return the type of the preference function in a IntVar object
    getP()
        return the preference threshold of the preference function in a DoubleVar object
    getQ()
        return the indifference threshold of the preference function in a DoubleVar object
    addEvaluation(val:float)
        add an evaluation
    clearColumn()
        clear all value in the column
    build_pi_c_matrix()
        build the pi matrix and the phi list of the criterion
    build_phi_c_list()
        build the phi list that corresponds to the criterion
    get_phi_c_list()
        return the phi list of the criterion
    get_gamma_c_ij(i:int, j:int)
        return the value of γc_ij
    """

    def __init__(self, name:StringVar, weight:DoubleVar, pfType:IntVar=None, p:DoubleVar=None, q:DoubleVar=None) -> None:
        """
        Parameters
        ----------
        name : StringVar
            the criterion name
        weight : DoubleVar
            the criterion weight
        pftype : IntVar, optional
            the type of preference function for this criterion (default is None)
        p : DoubleVar, optional
            the preference threshold in preference function for this criterion (default is None)
        q : DoubleVar, optional
            the indifference threshold in preference function for this criterion (default is None)
        """

        self.name = name
        self.weight = weight
        self.preferenceFunction = PreferenceFunction(type=pfType, p=p, q=q)  # init the preference function
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

    def setName(self, newName:StringVar) -> None:
        """Set the name of the criterion

        Parameters
        ----------
        newName : StringVar
            the new criterion name
        """
        self.name = newName


    def setWeight(self, w:DoubleVar) -> None:
        """Set the weight of the criterion

        w : DoubleVar
            the new criterion weight
        """
        self.weight = w


    def getName_str(self) -> str:
        """Return the name of the criterion

        Return
        ------
        name.get() : str
            the criterion name (in str)
        """
        return self.name.get()


    def getWeight_float(self) -> float:
        """Return the weight of the criterion

        Return
        ------
        weight.get() : float
            the criterion weight (in float)
        """
        return self.weight.get()


    def getName(self) -> StringVar:
        """Return the criterion name in a StringVar object

        Return
        ------
        name : StringVar
            the criterion name (in a StringVar)
        """
        return self.name
    

    def getWeight(self) -> DoubleVar:
        """Return the criterion weight in a DoubleVar object

        Return
        ------
        weight : DoubleVar
            the criterion weight (in a DoubleVar)
        """
        return self.weight


    def getPf_int(self) -> int:
        """Return the type of the preference function

        Return
        ------
        preferenceFunction.type.get() : int
            the type of the preference function used for this criterion (in int)
        """
        return self.preferenceFunction.getType_int()
    
    
    def getPf(self) -> IntVar:
        """Return the type of the preference function in a IntVar object

        Return
        ------
        preferenceFunction.type : Intvar
            the type of the preference function used for this criterion (in a IntVar)
        """
        return self.preferenceFunction.getType()
    

    def getP(self) -> DoubleVar:
        """Return the preference threshold of the preference function in a DoubleVar object

        Return
        ------
        preferenceFunction.pc : DoubleVar
            the preference threshold of the preference function used for this criterion (in a DoubleVar)
        """
        return self.preferenceFunction.getP()
    

    def getQ(self) -> DoubleVar:
        """Return the indifference threshold of the preference function in a DoubleVar object

        Return
        ------
        preferenceFunction.qc : DoubleVar
            the indifference threshold of the preference function used for this criterion (in a DoubleVar)

        """
        return self.preferenceFunction.getQ()


############################################################################################################################

    ########################
    ### Computation part ###
    ########################

    def addEvaluation(self, val:float) -> None:
        """Add an evaluation

        Parameters
        ----------
        val : float
            the new evaluation
        """
        self.column.append(val)


    def clearColumn(self):
        """Clear all value in the column
        """
        self.column.clear()


    def build_pi_c_matrix(self) -> None:
        """Build the pi matrix and the phi list of the criterion

        πc_ij = Fc(dc(ai, aj)): "how much ai is preferred over aj on criterion c" \n
        Fc is the preference function 
        and dc(ai, aj) = fc(ai) - fc(aj ) is the difference between the evaluations of ai and aj on the criterion c
        """
        for i in range(len(self.column)):
            self.pi_c_matrix.append([])
            for j in range(len(self.column)):
                pi_c_ij = self.preferenceFunction.compute_preference(self.column[i] - self.column[j])
                self.pi_c_matrix[i].append(pi_c_ij)


    def build_phi_c_list(self) -> None:
        """Build the phi list that corresponds to the criterion

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
        """Return the phi list of the criterion

        phi list: [φc(a1), φc(a2), ..., φc(ai), ..., φc(an)] where φc(ai): the mono-criterion net flow of ai on criterion c
        and n the number of alternatives

        Return
        ------
        phi_c_list : list
            the list of phi_c_i (phi_c_list[i] = φc(ai) = (1/n-1) * ∑_{j=1}^{n} (πc_ij - πc_ji))
        """
        return self.phi_c_list


    def get_gamma_c_ij(self, i:int, j:int) -> float:
        """Return the value of γc_ij

        γc_ij = wc · (φc(ai) - φc(aj))
        when fc(ai) > fc(aj) and γc_ij = 0 otherwise,
        where wc is the weight associated to the criterion

        Parameters
        ----------
        i : int
            the index of the alternative i in the column
        j : int
            the index of the alternative j in the column

        Return
        ------
        val : float
            the value of γc_ij
        """
        val = 0.0
        weight = self.weight.get()
        if(i < len(self.column) and j < len(self.column)):
            if(self.column[i]>self.column[j]):
                val = weight*(self.phi_c_list[i] - self.phi_c_list[j])
        return val