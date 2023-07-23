from Models.HelpForParametersTabModels.Range.Range import Range

class RangeJ(Range):
    def __init__(self, x: float, y: float, Pmax:float, Pmin:float) -> None:
        self.x = x
        self.y = y
        self.Pmin = Pmin
        self.Pmax = Pmax
        valMin = self.x - self.y/self.Pmin
        valMax = self.x - self.y/self.Pmax
        super().__init__(valMin, valMax)


    def getValForP(self, P:float) -> float:
        return self.x - self.y/P
    

    def setX(self, value:float):
        self.x = value
        valMin = self.x - self.y/self.Pmin
        valMax = self.x - self.y/self.Pmax
        super().setMax(valMax)
        super().setMin(valMin)


    def setY(self, value:float):
        self.y = value
        valMin = self.x - self.y/self.Pmin
        valMax = self.x - self.y/self.Pmax
        super().setMax(valMax)
        super().setMin(valMin)


    def setPmax(self, value:float):
        self.Pmax = value
        valMin = self.x - self.y/self.Pmin
        super().setMin(valMin)


    def setPmin(self, value:float):
        self.Pmin = value
        valMax = self.x - self.y/self.Pmax
        super().setMax(valMax)