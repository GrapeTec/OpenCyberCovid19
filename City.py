from COVID19 import SaturedCovid19Model
from Hospital import HospitalModel
from Trace import TraceModel

class CovidCityModel:
    def __init__(self,
                 name,
                 virusInfo,
                 population = 0,
                 area = 0,
                 sickbeds = 0):
        self.name = name
        self.virusInfo = virusInfo
        self.population = population
        self.area = area
        self.currentPopulation = population  # 总人数
        self.currentSusceptible = population  # 易感人数
        self.sickbeds = sickbeds
        self.covid19 = None
        self.R0 = 0.0
        self.hospital = None

    def startCovid19(self, dt, n = 0):
        info = self.virusInfo
        self.covid19 = SaturedCovid19Model(info.R0, info.T1, info.maxT1, info.T2, \
            info.deathRate1, info.deathRate2, self.sickbeds, dt)
        self.R0 = info.R0
        self.covid19.reset(n)
        return self.covid19

    def loadHospital(self) :
        self.hospital = HospitalModel(self.name)

    def hasCovid19(self):
        return self.covid19 != None

    def startTrace(self) :
        pass

    def migrateInfectiousIn(self, number, infectiousRate):
        self.population += number
        self.covid19.addInfected(number * infectiousRate)

    # 输入人口 = 输入健康人口 + 输入感染人口（处于潜伏期）
    # 已经确诊的感染者不允许迁入
    def migrateIncubatoryIn(self, number, incubatoryCarriers):
        self.population += number
        self.covid19.addIncubatoryCarriers(incubatoryCarriers)

    # 输出人口 = 输出健康人口 + 输出感染人口（处于潜伏期）
    # 已经确诊的感染者不允许迁出！！！
    # 被隔离的感染者不允许迁出！！！
    # 死亡的感染者不允许迁出！！！
    # 能够迁出的人口 = 易感人口 + 潜伏期感染者 + 治愈人口
    def migrateIncubatoryOut(self, number):
        self.population -= number
        migratable = self.getMigratable()
        rate = number / migratable  # 迁出率 = 迁出人口 / 可迁移人口
        incubation = self.covid19.incubation
        # 可迁出人口的各组成部分，均应按rate比例出一定人数
        # 所以，从潜伏期中取rate比例的感染者返回
        incubatoryCarriers = []
        for incubation in incubation.incubationQueue:
            incubatoryCarriers.append(incubation * rate)
        incubatoryCarriers[0] = 0
        return incubatoryCarriers

    def migrateSusceptibleIn(self, number):
        self.population += number
        self.currentSusceptible += number

    def migrateSusceptibleOut(self, number):
        self.population -= number
        self.currentSusceptible -= number

    def escapeConfirmedIn(self, confirmed):
        pass

    def escapeConfirmedOut(self, confirmed):
        pass

    def lockdown(self):
        self.R0 = self.virusInfo.ldR0

    def startMixedDetection(self, days) :
        self.covid19.startMixedDetection(days)

    def stopMixedDetection(self) :
        self.covid19.stopMixDetection()

    def addHospital(self, beds):
        self.sickbeds += beds
        self.covid19.setMaxSickbeds(self.sickbeds)

    def getInfectiousRate(self):
        record = self.covid19.record
        return record.currentInfectious / (self.currentPopulation -
                                           record.currentQuarantine)

    def getMigratable(self):
        record = self.covid19.record
        migratable = self.currentSusceptible  # 易感人口（健康人口）
        migratable += record.currentIncubatoryCarriers  # 潜伏期感染者
        migratable += record.currentRecovered  # 治愈人口
        return migratable

    def getMigratableInfectiousRate(self):
        record = self.covid19.record
        migratable = self.getMigratable()
        infectious = record.currentIncubatoryCarriers
        return infectious / migratable

    def startTraceDetection(self, traceRate, detectRate) :
        self.covid19.startTraceDetection(traceRate, detectRate)

    def predict(self):
        if self.hasCovid19() == False:
            return
        covid19 = self.covid19
        covid19.predict()
        record = self.covid19.record
        # 总人数 = 城市人口 - 死亡人数
        self.currentPopulation = self.population - record.currentDead
        # 易感人数 = 总人数 - 社会面感染人数 - 被隔离人数 - 治愈人数
        self.currentSusceptible = self.currentPopulation - record.currentInfectious \
            - record.currentQuarantined - record.currentRecovered
        rate = self.currentSusceptible / (self.currentPopulation -
                                          record.currentQuarantined)
        covid19.changeR0(rate * self.R0)
        if self.hospital != None :
            sickbeds = self.hospital.getSickbeds(record.currentDate)
            self.covid19.setMaxSickbeds(sickbeds)