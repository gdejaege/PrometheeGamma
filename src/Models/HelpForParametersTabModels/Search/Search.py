from Models.HelpForParametersTabModels.Search.SearchState import SearchState
from Models.HelpForParametersTabModels.Range.RangeI import RangeI
from Models.HelpForParametersTabModels.Range.RangeJ import RangeJ
import numpy as np


class Search:
    def __init__(self) -> None:
        self.infinity = 1000000000
        self.rval0_1 = np.arange(0.01, 1.01, 0.01)
        self.rval1_100 = np.arange(1.0, 100.01, 0.01)
        self.searchState = SearchState()


    def iterativeSearch(self, rI:RangeI, rJ:RangeJ, preference:int) -> None:
        self.searchState.addPair(rI, rJ, preference)
        self.searchState.update()
        #self.searchState.print()
        
        
    def getResults(self) -> tuple:
        return self.searchState.getState()
    

    def reset(self):
        self.searchState = SearchState()