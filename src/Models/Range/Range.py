
class Range:
    def __init__(self, min=None, max=None) -> None:
        self.min = min
        self.max = max


    def getMin(self):
        return self.min
    

    def getMax(self):
        return self.max


    def getValMin(self):
        if type(self.min) is Range:
            return self.min.getValMin()
        else:
            return self.min
    

    def getValMax(self):
        if type(self.max) is Range:
            return self.max.getValMax()
        else:
            return self.max
    

    def setMin(self, val):
        self.min = val


    def setMax(self, val):
        self.max = val


    def include(self, r):
        return self.min < r and self.max > r 
    

    def print(self):
        if type(self.min) is Range:
            print("Min=", self.min.getValMin())
        else:
            print("Min=", self.min)
        if type(self.max) is Range:
            print("Max=", self.max.getValMax())
        else:
            print("Max=", self.max)


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