
class AlternativeFace:
    def __init__(self, alternative, resultsRow, gammaRow, score) -> None:
        self.enable = True
        self.alternative = alternative
        self.resultsRow = resultsRow
        self.gammaRow = gammaRow
        self.score = score


class ResultsFace:
    def __init__(self, alternatives:list, resultsMatrix:list, gammaMatrix:list, scores:dict) -> None:
        self.alternatives = []
        for i in range(len(alternatives)):
            alter = AlternativeFace(alternatives[i], resultsMatrix[i], gammaMatrix[i], scores[alternatives[i].getName()])
            self.alternatives.append(alter)