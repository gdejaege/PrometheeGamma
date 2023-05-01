from Models.Range.Range import Range

class RangeI(Range):
    def __init__(self, x: float, y: float, Pmax:float, Pmin:float) -> None:
        self.x = x
        self.y = y
        self.Pmax = Pmax
        self.Pmin = Pmin
        valMin = min(self.x + self.y/self.Pmax, 1.0)
        valMax = min(self.x + self.y/self.Pmin, 1.0)
        super().__init__(valMin, valMax)


    def getValForP(self, P:float) -> float:
        return min(self.x + self.y/P, 1.0)
    

    def setX(self, value:float):
        self.x = value
        valMin = min(self.x + self.y/self.Pmax, 1.0)
        valMax = min(self.x + self.y/self.Pmin, 1.0)
        super().setMax(valMax)
        super().setMin(valMin)


    def setY(self, value:float):
        self.y = value
        valMin = min(self.x + self.y/self.Pmax, 1.0)
        valMax = min(self.x + self.y/self.Pmin, 1.0)
        super().setMax(valMax)
        super().setMin(valMin)


    def setPmax(self, value:float):
        self.Pmax = value
        valMin = min(self.x + self.y/self.Pmax, 1.0)
        super().setMin(valMin)


    def setPmin(self, value:float):
        self.Pmin = value
        valMax = min(self.x + self.y/self.Pmin, 1.0)
        super().setMax(valMax)