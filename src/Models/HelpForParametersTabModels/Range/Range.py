
class Range:
    def __init__(self, min=None, max=None) -> None:
        self.min = min
        self.max = max


    def getMin(self):
        return self.min
    

    def getMax(self):
        return self.max


    def getValMin(self):
        if type(self.min) is float:
            return self.min
        else:
            return self.min.getValMin()
    

    def getValMax(self):
        if type(self.max) is float:
            return self.max
        else:
            return self.max.getValMax()
    

    def setMin(self, val):
        self.min = val


    def setMax(self, val):
        self.max = val


    def include(self, r):
        return self.min < r and self.max > r 
    

    def print(self):
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