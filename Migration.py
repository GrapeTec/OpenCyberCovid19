from datetime import datetime
import csv

class MigrationLog :
    def __init__(self, dt, cityFrom, cityTo, number, sampled = False, sampledRate = 0.0) :
        self.date = dt
        self.cityFrom = cityFrom
        self.cityTo = cityTo
        self.number = number
        self.sampled = sampled
        self.sampledRate = sampledRate

class MigrationModel :
    def __init__(self, dt) :
        self.date = dt
        self.logs = []
        csvFile = self.csvFileName(dt)
        self.loadLogs(csvFile)
    
    def csvFileName(self, dt) :
        return str(dt) + ".csv"

    def loadLogs(self, csvFile) :
        filePath = "migration/" + csvFile
        with open(filePath, encoding="utf8") as f:
            reader = csv.reader(f)
            next(reader)
            for i, line in enumerate(reader, 1):
                dt = datetime.strptime(line[0], "%Y-%m-%d").date()
                cityFrom = line[1]
                cityTo = line[2]
                number = int(float(line[3]))
                sampled = False
                sampledRate = 0.0
                if len(line) >= 5 :
                    sampled = (line[4] == "True")
                if len(line) >= 6 :
                    sampledRate = float(line[5])
                log = MigrationLog(dt, cityFrom, cityTo, number, sampled, sampledRate)
                self.logs.append(log)
            

    def getNumber(self, cityFrom, cityTo) :
        for log in self.logs :
            if log.cityFrom == cityFrom and log.cityTo == cityTo :
                return log.number
        return 0

    def setSampledInfo(self, sampled = True, sampledRate = 0.0) :
        for log in self.logs :
            log.sampled = sampled
            log.sampledRate = sampledRate

    def saveLogs(self) :
        csvFile = self.csvFileName(self.date)
        filePath = "migration/" + csvFile
        with open(filePath, 'w', encoding="utf8", newline = '') as f:
            writer = csv.writer(f)
            writer.writerow([ "date", "cityFrom", "cityTo", "number", "sampled", "sampledRate"])
            for log in self.logs :
                writer.writerow([ log.date, log.cityFrom, log.cityTo, log.number, log.sampled, log.sampledRate])