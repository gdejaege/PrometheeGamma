class PreferenceFunction:
    """
    This class represent the preference funtion used by the Promethee Gamma method
    """
    def __init__(self):
        self.name = 'usual'
        self.pc = None
        self.qc = None


    def set_type(self, new_type):
        """
        Set the function
        """
        if new_type == 'usual':
            self.name = new_type
        elif new_type == 'linear':
            self.name = new_type
            self.qc = 0
            self.pc = 0


    def set_qc(self, new_qc):
        """
        Set the indifference parameter
        """
        self.qc = new_qc


    def set_pc(self, new_pc):
        """
        Set the preference parameter
        """
        self.pc = new_pc


    def compute_preference(self, value) -> float:
        """
        Compute the preference value
        """
        preference = 0.0
        if self.name == 'usual':
            if value > 0:
                preference = 1.0
        if self.name == 'linear':
            if value >= self.pc:
                preference = 1.0
            elif value > self.qc:
                #print("val=", round(value,1))
                preference = (value - self.qc)/(self.pc - self.qc)
                #print("pref=", round(preference,2))
        return preference


    def print_p_fun(self) -> None:
        print("name =", self.name)
        print("pc =", self.pc)
        print("qc =", self.qc)