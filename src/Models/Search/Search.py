from Models.Search.State import State
from Models.Search.SearchState import SearchState
from Models.Range.RangeI import RangeI
from Models.Range.RangeJ import RangeJ
import copy
import numpy as np


class Search:
    def __init__(self) -> None:
        self.infinity = 1000000000
        self.rval0_1 = np.arange(0.01, 1.01, 0.01)
        self.rval1_100 = np.arange(1.0, 100.01, 0.01)
        self.searchState = SearchState()


    def iterativeSearch(self, rI:RangeI, rJ:RangeJ, preference:int):
        self.searchState.addPair(rI, rJ, preference)
        self.searchState.update()
        self.searchState.print()


    def searchPerInterval(self, ListOfI:list, ListOfJ:list, preference:list):
        s = State()
        best = None
        valMin = 10000
        stateCeil = None
        stateFloor = None


    def dicho(self, range, state):
        pass


    def gradientSearch(self):
        pass


    def exhaustiveSearch(self, ListOfI:list, ListOfJ:list, preference:list):
        s = State()
        best = None
        valMin = 10000
        for num, i in enumerate(self.rval0_1):
            print(i)
            s.setI(i)
            for j in self.rval0_1[num:]:
                s.setJ(j)
                for p in self.rval1_100:
                    s.setP(p)
                    val = s.computeFitness(ListOfI, ListOfJ, preference)
                    if val < valMin:
                        valMin = val
                        best = copy.deepcopy(s)
                        if valMin == 0.0:
                            break
                s.setP(self.infinity)
                val = s.computeFitness(ListOfI, ListOfJ, preference)
                if val < valMin:
                    valMin = val
                    best = copy.deepcopy(s)
                    if valMin == 0.0:
                        break
        return best.getParam()
                    