from Incubation import IncubationModel
from Record import RecordModel
from Quarantine import QuarantineModel
from datetime import date

class SarsModel:
    def __init__(self, R0 = 3.5, T1 = 4, maxT1 = 16, T2 = 14, deathRate = 0.11, dt = date(2003, 2, 24)):
        self.R0 = R0
        self.incubation = IncubationModel(T1, maxT1, "symptom")
        self.record = RecordModel(dt)
        self.quarantine = QuarantineModel(T2, deathRate)

    def reset(self, n = 1) :
        self.incubation.addInfected(n)
        self.record.reset()
        self.quarantine.reset()
    
    def changeR0(self, R0) :
        self.R0 = R0

    def predict(self):
        symOnset = self.incubation.getSymOnset()     
        newInfected = symOnset * self.R0
        newCured, newDead = self.quarantine.addPatients(symOnset)
        self.record.reportEpidemics(newInfected, symOnset, symOnset, newCured, newDead)
        self.incubation.addInfected(newInfected)
        self.incubation.overnight()

    def predictDays(self, days) :
        for k in range(1, days + 1) :
            self.predict()
    
