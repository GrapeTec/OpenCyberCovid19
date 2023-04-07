import csv

class TraceLog :
    def __init__(self, city, virus, version, traceRate, detectRate) :
        self.city = city
        self.virus = virus
        self.version = version
        self.traceRate = traceRate
        self.detectRate = detectRate

class TraceModel :
    def __init__(self) :
        self.logs = []
        self.loadData("Trace.csv")

    def loadData(self, csvFile) :
        filePath = "trace/" + csvFile
        with open(filePath, encoding="utf8") as f:
            reader = csv.reader(f)
            next(reader)
            for i, line in enumerate(reader, 1):
                city = line[0]
                virus = line[1]
                version = line[2]
                traceRate = float(line[3])
                detectRate = float(line[4])
                log = TraceLog(city, virus, version, traceRate, detectRate)
                self.logs.append(log)

    def getRates(self, city, virus, version) :
        for log in self.logs :
            if log.city == city and \
               log.virus == virus and \
               log.version == version :
                return log.traceRate, log.detectRate
        return 0.0, 0.0