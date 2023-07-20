from Models.Search.Search import Search
from Models.Range.RangeI import RangeI
from Models.Range.RangeJ import RangeJ

if __name__=='__main__':
    s = Search()
    rI = RangeI(0.4, 0.1, 100.0, 1.0)
    rJ = rI
    s.iterativeSearch(rI, rJ, 0)
    
    rJ = RangeJ(0.7, 0.1, 100.0, 1.0)
    rI = rJ
    s.iterativeSearch(rI, rJ, -1)

    rI = RangeI(0.68, 0.15, 100.0, 1.0)
    rJ = rI
    print(rI.getValMin(), rI.getValMax())
    s.iterativeSearch(rI, rJ, 0)

    """
    rJ = RangeJ(0.5, 0.1, 100.0, 1.0)
    rI = rJ
    print(rJ.getValMin(), rJ.getValMax())
    s.iterativeSearch(rI, rJ, -1)
    """
    
    rI = RangeI(0.5, 0.1, 100.0, 1.0)
    rJ = RangeJ(0.6, 0.1, 100.0, 1.0)
    s.iterativeSearch(rI, rJ, 1)
