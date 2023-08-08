import numpy as np
from customtkinter import (IntVar, DoubleVar)

class PreferenceFunction:
    """
    This class represent the preference funtion used by the Promethee Gamma method

    Attributes
    ----------
    type : IntVar
        the type of the preference function
    pc : DoubleVar
        the preference threshold in the preference function
    qc : DoubleVar
        the indifference threshold in the preference function

    Methods
    -------
    getP()
        return the preference threshold in a DoubleVar object
    getQ()
        return the indifference threshold in a DoubleVar object
    getType():
        return the type of the preference function in an IntVar object
    getType_int()
        return the type of the preference function
    set_type(new_type:IntVar, p:DoubleVar=None, q:DoubleVar=None)
        set the function
    set_qc(new_qc:DoubleVar)
        set the indifference parameter
    set_pc(new_pc:DoubleVar)
        set the preference parameter
    compute_preference(value:float)
        compute the preference value
    """

    def __init__(self, type:IntVar=None, p:DoubleVar=None, q:DoubleVar=None):
        """
        Parameters
        ----------
        type : IntVar, optional
            the type of the preference function (default is None)
        p : DoubleVar, optional
            the preference threshold in the preference function (default is None)
        q : DoubleVar, optional
            the indifference threshold in the preference function (default is None)
        """

        self.type = type
        self.pc = p
        self.qc = q


    def getP(self) -> DoubleVar:
        """Return the preference threshold in a DoubleVar object

        Return
        ------
        pc : DoubleVar
            the preference threshold in the preference function (in a DoubleVar)
        """
        return self.pc
    

    def getQ(self):
        """Return the indifference threshold in a DoubleVar object

        Return
        ------
        q : DoubleVar
            the indifference threshold in the preference function (in a DoubleVar)
        """
        return self.qc
    

    def getType(self):
        """Return the type of the preference function in an IntVar object

        Return
        ------
        type : IntVar
            the type of the preference function (in a IntVar)
        """
        return self.type


    def getType_int(self) -> int:
        """Return the type of the preference function

        Return
        ------
        type : int
            the type of the preference function
        """
        return self.type.get()


    def set_type(self, new_type:IntVar, p:DoubleVar=None, q:DoubleVar=None) -> None:
        """Set the function

        Parameters
        ----------
        new_type : IntVar
            the new type of the preference function
        p : DoubleVar, optional
            the new preference threshold in the preference function (default is None)
        q : DoubleVar, optional
            the new indifference threshold in the preference function (default is None)
        """
        self.type = new_type
        self.pc = p
        self.qc = q


    def set_qc(self, new_qc:DoubleVar) -> None:
        """Set the indifference parameter

        Parameters
        ----------
        new_qc : DoubleVar
            the new indifference threshold in the preference function
        """
        self.qc = new_qc


    def set_pc(self, new_pc:DoubleVar) -> None:
        """Set the preference parameter

        Parameters
        ----------
        new_pc : DoubleVar
            the new preference threshold in the preference function
        """
        self.pc = new_pc


    def compute_preference(self, value:float) -> float:
        """Compute the preference value

        Parameters
        ----------
        value : float
            the difference between the evaluations of the alternatives i and j for the criterion that use this preference function

        Return
        ------
        preference : float
            the value of preference between alternatives i and j
        """
        preference = 0.0
        type = self.type.get()
        pc = self.pc.get()
        qc = self.qc.get()

        if type == 1: # Usual
            if value > 0:
                preference = 1.0
        elif type == 2: # U-shape
            if value >= qc:
                preference = 1.0
        elif type == 3: # V-shape
            if value >= pc :
                preference = 1.0
            elif value > 0:
                preference = value/pc
        elif type == 4: # Level
            if value >= pc:
                preference = 1.0
            elif value >= qc:
                preference = 0.5
        elif type == 5: # Linear
            if value >= pc:
                preference = 1.0
            elif value > qc:
                preference = (value - qc)/(pc - qc)
        elif type == 6: # Gaussian
            if value > 0:
                preference = np.exp(-value**2)
        return preference