from City import CovidCityModel
from Virus import Covid19DataBase
from Hospital import HospitalModel
from datetime import date, timedelta
import csv

class CovidCountryModel :
    def __init__(self, name = "China", version = "alpha") :
        self.name = name
        self.cityModels = []
        self.overseaModel = CovidCityModel("Oversea", 0, 0, 0, version)
        self.othersModel = CovidCityModel("Others", 0, 0, 0, version)
        self.currentDate = date(2020, 1, 1)
        self.virusdb = Covid19DataBase(version)
        self.loadCities(name + ".csv")

    def clearCities(self) :
        self.cityModels = []

    def loadCities(self, csvFile) :
        filePath = "city/" + csvFile
        with open(filePath, encoding="utf8") as f:
            reader = csv.reader(f)
            next(reader)
            for i, line in enumerate(reader, 1) :
                name = line[0]
                population = float(line[1]) * 10000
                area = float(line[2])
                sickbeds = int(line[3])
                self.addCity(name, population, area, sickbeds)
     
    def addCity(self, name, population, area, sickbeds) :
        virusInfo = self.virusdb.getVirusInfo(name)
        cityModel = CovidCityModel(name, virusInfo, population, area, sickbeds)
        self.cityModels.append(cityModel)


    def loadHospitalInCity(self, city) :
        cityModel = self.findCityModel(city)
        if cityModel != None :
            cityModel.loadHospital()

    def startInCity(self, city, dt, n) :
        startCity = self.findCityModel(city)
        for cityModel in self.cityModels :
            if cityModel == startCity :
                cityModel.startCovid19(dt, n)
            else :
                cityModel.startCovid19(dt, 0)
        self.currentDate = dt

    def migrateByLog(self, log, useSampled = False) :
        if useSampled and log.sampled :
            self.migrateSampledFromTo(log.cityFrom, log.cityTo, log.number, log.sampledRate)
        else :
            self.migrateFromTo(log.cityFrom, log.cityTo, log.number)
    
    def migrateSampledFromTo(self, cityFrom, cityTo, number, sampledRate) :
        cityFromModel = self.findCityModel(cityFrom)
        cityToModel = self.findCityModel(cityTo)
        if cityToModel != None and cityToModel != None :
            if cityFromModel.hasCovid19() :
                # cityFromModel.migrateInfectiousOut
                cityToModel.migrateInfectiousIn(number, sampledRate)
            else :
                cityFromModel.migrateSusceptibleOut(number)
                cityToModel.migrateSusceptibleIn(number)

    def migrateFromTo(self, cityFrom, cityTo, number) :
        cityFromModel = self.findCityModel(cityFrom)
        cityToModel = self.findCityModel(cityTo)
        if cityToModel != None and cityToModel != None :
            if cityFromModel.hasCovid19() :
                incubatoryCarriers = cityFromModel.migrateIncubatoryOut(number)
                cityToModel.migrateIncubatoryIn(number, incubatoryCarriers)
            else :
                cityFromModel.migrateSusceptibleOut(number)
                cityToModel.migrateSusceptibleIn(number)
    
    def lockdown(self) :
        for cityModel in self.cityModels :
            cityModel.lockdown()

    def findCityModel(self, city) :
        for cityModel in self.cityModels :
            if cityModel.name == city :
                return cityModel
        return None

    def predict(self) :
        for cityModel in self.cityModels :
            cityModel.predict()
        self.overseaModel.predict()
        self.othersModel.predict()
        self.currentDate += timedelta(1)

    def getRecord(self, city) :
        cityModel = self.findCityModel(city)
        if cityModel != None :
            return cityModel.covid19.record
        return None