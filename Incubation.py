import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class IncubationModel :
    def __init__(self, T, maxT = 14, infectMode = "incubation") :
        self.T = T
        self.maxT = maxT
        self.infectMode = infectMode
        self.distibutionList = [0]

        posibiltiy = 0.0
        for k in range(1, self.maxT + 1) :
            distribution = stats.poisson.pmf(k, T)
            self.distibutionList.append(distribution)
            posibiltiy += distribution        
        for k in range(1, self.maxT + 1) :
            self.distibutionList[k] /= posibiltiy

        self.incubationQueue = [0]
        for i in range(1, self.maxT + 1) :
            self.incubationQueue.append(0)

    def getSymOnset(self) :
        return self.incubationQueue[0]
    
    def getInfectious(self) :
        if self.infectMode == "incubation" :
            infectious = 0
            for k in range(0, self.maxT + 1) :
                infectious += self.incubationQueue[k]
            return infectious
        elif self.infectMode == "symptom" :
            return self.getSymOnset()

    def overnight(self) :
        self.incubationQueue = self.incubationQueue[1 : self.maxT + 1]
        self.incubationQueue.append(0)
    
    def addInfected(self, infected) :
        for k in range(1, self.maxT + 1) :
            self.incubationQueue[k] += infected * self.distibutionList[k]

    def addIncubatoryCarriers(self, incubatoryCarriers) :
        for k in range(0, self.maxT + 1) :
            self.incubationQueue[k] += incubatoryCarriers[k]
    
    def reduceInfectious(self, rate) :
        reduced = 0
        for k in range(1, self.maxT + 1) :
            self.incubationQueue[k] *= (1 - rate)
            reduced += self.incubationQueue[k] * rate
        return reduced

class IncubationViewer :
    def __init__(self, incubation) :
        self.incubation = incubation
    
    def plotIncubation(self) :
        plt.figure()
        plt.plot(self.incubation.incubationQueue, label = "Infected in Incubation", \
            linewidth = 2, linestyle=':', color = 'r')

    def plotDistribution(self) :
        plt.figure()
        plt.plot(self.incubation.distibutionList, label = "Distribution of Incubation", \
            linewidth = 2, linestyle=':', color = 'r')

    def show(self) :
        plt.show()
    
    def showIncubation(self) :
        plt.plot(self.incubation.incubationQueue, label = "Infected in Incubation", \
            linewidth = 2, linestyle=':', color = 'r')
        plt.show()

    def showDistribution(self) :
        plt.plot(self.incubation.incubationQueue, label = "Distribution of Incubation", \
            linewidth = 2, linestyle=':', color = 'r')
        plt.show()