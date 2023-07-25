#############################################################################
### This class is designed to provide an alternative way                  ###
### of obtaining parameter values specific to the PROMETHEE Gamma method. ###
### Edit it as you wish.                                                  ###
#############################################################################

class Custom:
    def __init__(self) -> None:
        self.Imin = 0.0
        self.Imax = 1.0
        self.Jmin = 0.0
        self.Jmax = 1.0
        self.Pmin = 1.0
        self.Pmax = 1000000000.0


    def getValues(self):
        return (self.Imin, self.Imax, self.Jmin, self.Jmax, self.Pmin, self.Pmax)
    

    def compute(self):
        pass