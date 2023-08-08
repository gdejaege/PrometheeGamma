
class Range:
    """
    A class to represent a range of values

    Attributes
    ----------
    min : float | Range
        the lowest value in the range or a range
    max : float | Range
        the highest value in the range or a range

    Methods
    -------
    getMin()
        return min, the lowest value in the range or a range
    getMax()
        return max, the highest value in the range or a range
    getValMin()
        return the lowest value of the range
    getValMax()
        return the highest value of the range
    setMin(val)
        set the min value
    setMax(val)
        set the max value
    include(r)
        test if r is strictly in the range
    print()
        print the extreme values of the range
    """

    def __init__(self, min=None, max=None) -> None:
        """
        Parameters
        ----------
        min : float | Range
            lowest value in the range or a range
        max : float | Range
            highest value in the range or a range
        """
        self.min = min
        self.max = max


    def getMin(self):
        """Return min, the lowest value in the range or a range
        
        Return
        ------
        min : float | Range
            lowest value in the range or a range
        """
        return self.min
    

    def getMax(self):
        """Return max, the highest value in the range or a range
        
        Return
        ------
        max : float | Range
            highest value in the range or a range
        """
        return self.max


    def getValMin(self):
        """Return the lowest value of the range

        if min is a Range, call this function recursively, up to obtain a float value

        Return
        ------
        min : float | Range
            lowest value in the range or a range
        """
        if type(self.min) is float:
            return self.min
        else:
            return self.min.getValMin()
    

    def getValMax(self):
        """Return the highest value of the range

        if max is a Range, call this function recursively, up to obtain a float value

        Return
        ------
        max : float | Range
            highest value in the range or a range
        """
        if type(self.max) is float:
            return self.max
        else:
            return self.max.getValMax()
    

    def setMin(self, val):
        """Set the min value

        Parameters
        ----------
        val : float | Range
            the new min value
        """
        self.min = val


    def setMax(self, val):
        """Set the max value
        
        Parameters
        ----------
        val : float | Range
            the new max value
        """
        self.max = val


    def include(self, r):
        """Test if r is strictly in the range

        Return
        ------
        True if r is strictly in the range, False otherwise
        """
        return self.min < r and self.max > r 
    

    def print(self):
        """Print the extreme values of the range
        """
        if type(self.min) is float:
            print("Min=", self.min)
        else:
            print("Min=", self.min.getValMin())
        if type(self.max) is float:
            print("Max=", self.max)
        else:
            print("Max=", self.max.getValMax())


    # operator <
    def __lt__(self, r):
        if type(r) is Range:
            return self.max < r.getValMin()
        else: 
            return self.max < r
        

    # operator <=
    def __le__(self, r):
        if type(r) is Range:
            return self.max <= r.getValMin() or (self.max <= r.getValMax() and self.min <= r.getValMin())
        else: 
            return self.max <= r or (self.max >= r and self.min <= r)
        

    # operator ==
    def __eq__(self, r):
        if type(r) is Range:
            return self.max == r.getValMax() and self.min == r.getValMin()
        else:
            return self.min <= r and self.max >= r
        

    # operator !=
    def __ne__(self, r):
        if type(r) is Range:
            return not(self.max == r.getValMax() and self.min == r.getValMin())
        else:
            return not(self.min <= r and self.max >= r)
        

    # operator >
    def __gt__(self, r):
        if type(r) is Range:
            return self.min > r.getValMax()
        else: 
            return self.min > r
        

    # operator >=
    def __ge__(self, r):
        if type(r) is Range:
            return self.min >= r.getValMax() or (self.min >= r.getValMin() and self.max >= r.getValMax())
        else: 
            return self.min >= r or (self.max >= r and self.min <= r)