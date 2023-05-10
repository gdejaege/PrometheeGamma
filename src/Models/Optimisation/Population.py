from Models.Optimisation.Individu import Individu
import random

class Population:
    def __init__(self, size:int) -> None:
        self.population = []
        self.size = size
        for i in range(size):
            ind = Individu()
            ind.makeRandom()
            self.population.append(ind)


    def evolution(self, nbGenerations, ListOfI:list, ListOfJ:list, listOfPreference:list):
        for i in range(nbGenerations):
            self.computeFitness(ListOfI, ListOfJ, listOfPreference)
            selectedPop = self.selection()
            self.reproduction(selectedPop)
            self.mutations()
        self.computeFitness(ListOfI, ListOfJ, listOfPreference)
        for ind in self.population[:20]:
            print("fitness =", ind.getFitness())
        self.population.sort(key=self.fit)


    def getBest(self):
        best = self.population[0]
        i = best.getI()
        j = best.getJ()
        p = best.getP()
        print("fitness of best = ", best.getFitness())
        return (i, j, p)


    def computeFitness(self, ListOfI:list, ListOfJ:list, listOfPreference:list):
        for ind in self.population:
            ind.computeFitness(ListOfI, ListOfJ, listOfPreference)
        

    def selection(self):
        self.population.sort(key=self.fit)
        nbselected = self.size//5
        nbRandomSelected = self.size//20
        new_population = self.population[0:nbselected]
        for i in range(nbRandomSelected):
            ind = random.choice(self.population[nbselected:])
            new_population.append(ind)
            ind = Individu()
            ind.makeRandom()
            new_population.append(ind)
        return new_population
    

    def reproduction(self, new_population:list):
        nbChilderen = self.size - self.size//5 - 2*self.size//20
        childeren = []
        for i in range(nbChilderen):
            father = random.choice(new_population)
            mother = random.choice(new_population)
            child = Individu()
            child.childOf(father, mother)
            childeren.append(child)
        self.population = new_population
        self.population.extend(childeren)


    def mutations(self):
        nbMutation = random.randint(1, self.size//5)
        for i in range(nbMutation):
            mutant = random.randint(0, self.size-1)
            attrMutant = random.randint(0, 3)
            mutation = random.random()/10
            self.population[mutant].mutate(attrMutant, mutation)


    def fit(self, individu:Individu):
        return individu.getFitness()
