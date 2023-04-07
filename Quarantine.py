
class QuarantineModel :
    def __init__(self, T, deathRate) :
        self.T = T
        self.deathRate = deathRate
        self.reset()

    def addPatients(self, n) :
        cured = self.getCured()
        dead = self.getDead()
        self.patientQueue = self.patientQueue[1 : self.T + 1]
        self.patientQueue.append(n)
        return cured, dead

    def reset(self) :
        self.patientQueue = [0]
        for k in range(1, self.T + 1) :
            self.patientQueue.append(0)
    
    def getCured(self) :
        return self.patientQueue[0] * (1.0 - self.deathRate)

    def getDead(self) :
        return self.patientQueue[0] * self.deathRate

class SaturedQuarantineModel : 
    def __init__(self, T, deathRate1, deathRate2, maxSickbeds) :
        self.T = T
        self.deathRate1 = deathRate1
        self.deathRate2 = deathRate2
        self.maxSickbeds = maxSickbeds
        self.reset()

    def reset(self) :
        self.quarantinedPatientQueue = [0]
        self.exposedPatientQueue = [0]
        for k in range(1, self.T + 1) :
            self.quarantinedPatientQueue.append(0)
            self.exposedPatientQueue.append(0)

    def setMaxSickbeds(self, maxSickbeds) :
        self.maxSickbeds = maxSickbeds
    
    def getFreeSickbeds(self) :
        free = self.maxSickbeds
        for k in range(1, self.T + 1) :
            free -= self.quarantinedPatientQueue[k]
        return free
    
    def addPatients(self, n) :
        newCured = self.getCured()
        newDead = self.getDead()

        freeSickbeds = self.getFreeSickbeds()
        newQuarantine = 0
        self.quarantinedPatientQueue = self.quarantinedPatientQueue[1 : self.T + 1]
        self.exposedPatientQueue = self.exposedPatientQueue[1 : self.T + 1]
        if(n <= freeSickbeds) :
            self.quarantinedPatientQueue.append(n)
            self.exposedPatientQueue.append(0)
            newQuarantine = n
        else :
            self.quarantinedPatientQueue.append(freeSickbeds)
            self.exposedPatientQueue.append(n - freeSickbeds)
            newQuarantine = freeSickbeds

        return newQuarantine, newCured, newDead

    def getQuarantineCured(self) :
        return self.quarantinedPatientQueue[0] * (1.0 - self.deathRate1)

    def getExposedCured(self) :
        return self.exposedPatientQueue[0] * (1.0 - self.deathRate2)

    def getCured(self) :
        return self.getQuarantineCured() + self.getExposedCured()
    
    def getQuarantinedDead(self) :
        return self.quarantinedPatientQueue[0] * self.deathRate1

    def getExposedDead(self) :
        return self.exposedPatientQueue[0] * self.deathRate2
    
    def getDead(self) :
        return self.getQuarantinedDead() + self.getExposedDead()

    def getInfectious(self) :
        infectious = 0
        for k in range(0, self.T + 1) :
            infectious += self.exposedPatientQueue[k]
        return infectious