import numpy as np
from customtkinter import (IntVar, DoubleVar)

class PreferenceFunction:
    """
    This class represent the preference funtion used by the Promethee Gamma method.
    """
    def __init__(self, type:IntVar=None, p:DoubleVar=None, q:DoubleVar=None):
        self.type = type
        self.pc = p
        self.qc = q


    def getP(self) -> DoubleVar:
        """
        Return the preference threshold in a DoubleVar object.
        """
        return self.pc
    

    def getQ(self):
        """
        Return the indifference threshold in a DoubleVar object.
        """
        return self.qc
    

    def getType(self):
        """
        Return the type of the preference function in an IntVar object.
        """
        return self.type


    def getType_int(self) -> int:
        """
        Return the type of the preference function.
        """
        return self.type.get()


    def set_type(self, new_type:IntVar, p:DoubleVar, q:DoubleVar) -> None:
        """
        Set the function
        """
        self.type = new_type
        self.pc = p
        self.qc = q


    def set_qc(self, new_qc:DoubleVar) -> None:
        """
        Set the indifference parameter
        """
        self.qc = new_qc


    def set_pc(self, new_pc:DoubleVar) -> None:
        """
        Set the preference parameter
        """
        self.pc = new_pc


    def compute_preference(self, value) -> float:
        """
        Compute the preference value
        """
        preference = 0.0
        type = self.type.get()
        pc = self.pc.get()
        qc = self.qc.get()

        if type == 1:
            if value > 0:
                preference = 1.0
        elif type == 2:
            if value >= qc:
                preference = 1.0
        elif type == 3:
            if value >= pc :
                preference = 1.0
            elif value > 0:
                preference = value/pc
        elif type == 4:
            if value >= pc:
                preference = 1.0
            elif value >= qc:
                preference = 0.5
        elif type == 5:
            if value >= pc:
                preference = 1.0
            elif value > qc:
                preference = (value - qc)/(pc - qc)
        elif type == 6:
            if value > 0:
                preference = np.exp(-value**2)
        return preference