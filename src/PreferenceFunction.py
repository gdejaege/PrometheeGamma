import numpy as np

class PreferenceFunction:
    """
    This class represent the preference funtion used by the Promethee Gamma method
    """
    def __init__(self):
        self.type = 1
        self.pc = None
        self.qc = None


    def set_type(self, new_type:int, p=0.0, q=0.0) -> None:
        """
        Set the function
        """
        self.type = new_type
        self.pc = p
        self.qc = q


    def set_qc(self, new_qc) -> None:
        """
        Set the indifference parameter
        """
        self.qc = new_qc


    def set_pc(self, new_pc) -> None:
        """
        Set the preference parameter
        """
        self.pc = new_pc


    def compute_preference(self, value) -> float:
        """
        Compute the preference value
        """
        preference = 0.0
        if self.type == 1:
            if value > 0:
                preference = 1.0
        elif self.type == 2:
            if value >= self.qc:
                preference = 1.0
        elif self.type == 3:
            if value >= self.pc :
                preference = 1.0
            elif value > 0:
                preference = value/self.pc
        elif self.type == 4:
            if value >= self.pc:
                preference = 1.0
            elif value >= self.qc:
                preference = 0.5
        elif self.type == 5:
            if value >= self.pc:
                preference = 1.0
            elif value > self.qc:
                preference = (value - self.qc)/(self.pc - self.qc)
        elif self.type == 6:
            if value > 0:
                preference = np.exp(-value**2)
        return preference


    def get_type(self) -> int:
        return self.type


    def print_p_fun(self) -> None:
        print("type =", self.type)
        print("pc =", self.pc)
        print("qc =", self.qc)