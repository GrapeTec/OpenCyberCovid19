import csv

# class SarsData :
#     def __init__(self) :
#         self.name = "SARS"
#         self.R0 = 3.5
#         self.T1 = 4.0
#         self.maxT1 = 16
#         self.T2 = 14
#         self.deathRate1 = 0.06
#         self.deathRate2 = 0.11

# class Covid19Data :
#     def __init__(self, version) :
#         self.name = "COVID-19"
#         self.version = version
#         if version == "alpha" :
#             self.initAlpha()
#         elif version == "delta" :
#             self.initDelta()
#         elif version == "omicron" :
#             self.initOmicron()

#     def initAlpha(self) :
#         self.R0 = 2.41
#         self.T1 = 5.5
#         self.maxT1 = 14
#         self.T2 = 14
#         self.deathRate1 = 0.01
#         self.deathRate2 = 0.05
    
#     def initDelta(self) :
#         self.R0 = 4.0
#         self.T1 = 5.5
#         self.maxT1 = 14
#         self.T2 = 14
#         self.deathRate1 = 0.03
#         self.deathRate2 = 0.06

#     def initOmicron(self) :
#         self.R0 = 4.0
#         self.T1 = 5.5
#         self.maxT1 = 14
#         self.T2 = 14
#         self.deathRate1 = 0.03
#         self.deathRate2 = 0.06

class Covid19Info :
    def __init__(self, name, city, R0, ldR0, T1, maxT1, T2, 
                 deathRate1 = 0.0, deathRate2 = 0.0, infectMode = "incubation", asymRate = 0.0) :
        self.name = name
        self.city = city
        self.R0 = R0
        self.ldR0 = ldR0
        self.T1 = T1
        self.maxT1 = maxT1
        self.T2 = T2
        self.deathRate1 = deathRate1
        self.deathRate2 = deathRate2
        self.infectMode = infectMode
        self.asymRate = asymRate

class Covid19DataBase :
    def __init__(self, version) :
        self.virusInfos = []
        self.loadVirusData(version)

    def loadVirusData(self, version) :
        csvFile = "COVID19-" + version.capitalize() + ".csv"
        filePath = "virus/" + csvFile
        with open(filePath, encoding="utf8") as f:
            reader = csv.reader(f)
            next(reader)
            for i, line in enumerate(reader, 1):
                name = line[0]
                city = line[1]
                R0 = float(line[2])
                ldR0 = float(line[3])
                T1 = float(line[4])
                maxT1 = int(line[5])
                T2 = int(line[6])
                deathRate1 = float(line[7])
                deathRate2 = float(line[8])
                infectMode = line[9]
                asymRate = float(line[10])
                info = Covid19Info(name, city, R0, ldR0, T1, maxT1, T2, deathRate1, deathRate2, infectMode, asymRate)
                self.virusInfos.append(info)

    def getVirusInfo(self, city) :
        for info in self.virusInfos :
            if city == info.city :
                return info
        return self.virusInfos[0]
