from Models.HelpForParametersTabModels.Range.Range import Range


class RangeI(Range):
    """
    A class to represent a range of indifference threshold of PROMETHEE Gamma method

    Attributes
    ----------
    x : float
        max(gamma_ij, gamma_ji)
    y : float
        |gamma_ij - gamma_ji|
    Pmax : float
        maximum value of P, the preference parameter of PROMETHEE Gamma method
    Pmin : float
        minimum value of P, the preference parameter of PROMETHEE Gamma method

    Methods
    -------
    """

    def __init__(self, x:float, y:float, Pmax:float, Pmin:float) -> None:
        """
        Parameters
        ----------
        x : float
            max(gamma_ij, gamma_ji)
        y : float
            |gamma_ij - gamma_ji|
        Pmax : float
            maximum value of P, the preference parameter of PROMETHEE Gamma method
        Pmin : float
            minimum value of P, the preference parameter of PROMETHEE Gamma method
        """

        self.x = x
        self.y = y
        self.Pmax = Pmax
        self.Pmin = Pmin
        valMin = max(0.0,min(self.x + self.y/self.Pmax, 1.0))
        valMax = max(0.0,min(self.x + self.y/self.Pmin, 1.0))
        super().__init__(valMin, valMax)


    def getX(self) -> float:
        """Return x, x = max(gamma_ij, gamma_ji)

        Returns
        -------
        float
            x = max(gamma_ij, gamma_ji)
        """
        return self.x
    
    def getY(self) -> float:
        """Return y, y = |gamma_ij - gamma_ji|

        Returns
        -------
        float
            y = |gamma_ij - gamma_ji|
        """
        return self.y


    def getValForP(self, P:float) -> float:
        """Return the indifference threshold value for the value P of preference parameter
        
        Returns
        -------
        float
            max(gamma_ij, gamma_ji) + |gamma_ij - gamma_ji|/P or 1.0 if max(gamma_ij, gamma_ji) + |gamma_ij - gamma_ji|/P > 1.0
        """
        return min(self.x + self.y/P, 1.0)
    

    def setX(self, value:float):
        """Set the value of x
        
        Parameters
        ----------
        value : float
            the new value of x
        """
        self.x = value
        valMin = min(self.x + self.y/self.Pmax, 1.0)
        valMax = min(self.x + self.y/self.Pmin, 1.0)
        super().setMax(valMax)
        super().setMin(valMin)


    def setY(self, value:float):
        """Set the value of y
        
        Parameters
        ----------
        value : float
            the new value of y
        """
        self.y = value
        valMin = min(self.x + self.y/self.Pmax, 1.0)
        valMax = min(self.x + self.y/self.Pmin, 1.0)
        super().setMax(valMax)
        super().setMin(valMin)


    def setPmax(self, value:float):
        """Set the value of Pmax
        
        Parameters
        ----------
        value : float
            the new value of Pmax
        """
        self.Pmax = value
        valMin = min(self.x + self.y/self.Pmax, 1.0)
        super().setMin(valMin)


    def setPmin(self, value:float):
        """Set the value of Pmin
        
        Parameters
        ----------
        value : float
            the new value of Pmin
        """
        self.Pmin = value
        valMax = min(self.x + self.y/self.Pmin, 1.0)
        super().setMax(valMax)